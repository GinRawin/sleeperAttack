from __future__ import annotations

import argparse
import importlib
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import config as project_config
from defense import config as defense_config
from defense.guard import SUPPORTED_DEFENSE_MODES, normalize_defense_mode
from defense.table_registry import list_tables, resolve_tables


MODEL_ALIASES: Dict[str, Tuple[str, str]] = {
    "deepseek-r1": ("deepseek-r1", "config"),
    "qwen3.5-plus": ("qwen3.5-plus", "config"),
    "qwen3.5-flash": ("qwen3.5-flash", "config"),
    "gpt-5.4": ("openai/gpt-5.4", "openrouter"),
    "gemini-3-flash-preview": ("gemini-3-flash-preview", "google"),
    "gemini-3-pro-preview": ("gemini-3-pro-preview", "google"),
    "llama-3.3-70b-instruct": ("meta-llama/llama-3.3-70b-instruct", "openrouter"),
}


def parse_csv(values: Iterable[str]) -> List[str]:
    out: List[str] = []
    for raw in values:
        for part in (raw or "").split(","):
            part = part.strip()
            if part:
                out.append(part)
    return out


def resolve_model(model_name: str) -> Tuple[str, str]:
    key = (model_name or "").strip()
    if key in MODEL_ALIASES:
        return MODEL_ALIASES[key]
    if "/" in key:
        if key.startswith("qwen/") or key.startswith("deepseek/"):
            return key.split("/", 1)[1], "config"
        if key.startswith("google/"):
            return key.split("/", 1)[1], "google"
        return key, "openrouter"
    return key, "config"


def build_env(
    model_name: str,
    provider: str,
    dataset_path: str,
    results_file: str,
    sample_size: int | None,
    defense_mode: str = "rule_defense",
    defense_results_dir: str | None = None,
    sample_seed: int | None = None,
) -> Dict[str, str]:
    importlib.reload(project_config)
    env = os.environ.copy()
    env["ENABLE_DEFENSE"] = "true"
    env["DEFENSE_MODE"] = normalize_defense_mode(defense_mode)
    env["DATASET_FILE"] = dataset_path
    env["RESULTS_FILE"] = results_file
    env["DEFENSE_RESULTS_DIR"] = defense_results_dir or defense_config.DEFENSE_RESULTS_DIR
    env["AGENT_MODEL"] = model_name
    if sample_size is not None:
        env["SAMPLE_SIZE"] = str(sample_size)
    if sample_seed is not None:
        env["SAMPLE_SEED"] = str(sample_seed)

    if provider == "openrouter":
        env["AGENT_API_KEY"] = os.getenv("OPENROUTER_API_KEY") or getattr(project_config, "OPENROUTER_API_KEY", "")
        env["AGENT_BASE_URL"] = os.getenv("OPENROUTER_BASE_URL") or getattr(project_config, "OPENROUTER_BASE_URL", "")
    elif provider == "google":
        env["AGENT_API_KEY"] = (
            os.getenv("GEMINI_API_KEY")
            or os.getenv("GOOGLE_API_KEY")
            or getattr(project_config, "GEMINI_API_KEY", "")
            or getattr(project_config, "GOOGLE_API_KEY", "")
        )
        env["AGENT_BASE_URL"] = (
            os.getenv("GEMINI_BASE_URL")
            or getattr(project_config, "GEMINI_BASE_URL", "")
            or "https://generativelanguage.googleapis.com/v1beta/openai/"
        )
    else:
        env["AGENT_API_KEY"] = getattr(project_config, "API_KEY", os.getenv("API_KEY", ""))
        env["AGENT_BASE_URL"] = getattr(project_config, "BASE_URL", os.getenv("BASE_URL", ""))

    if "qwen" in model_name.lower() and env.get("QWEN_ENABLE_THINKING") is None:
        env["QWEN_ENABLE_THINKING"] = "true"

    return env


def main() -> None:
    parser = argparse.ArgumentParser(description="Run one released Rule, Guard, or AgentDoG Defense slice, or a custom dataset.")
    parser.add_argument("--model", action="append", default=[], help="Model alias or raw model id. Repeatable or comma-separated.")
    parser.add_argument(
        "--table",
        action="append",
        default=[],
        help="Released slice alias (for example table1_memory) or dataset path. Repeatable or comma-separated.",
    )
    parser.add_argument(
        "--mode",
        default="rule_defense",
        choices=sorted(SUPPORTED_DEFENSE_MODES),
        help="Defense mode. The paper-facing names are rule_defense, guard_defense, and agentdog_defense.",
    )
    parser.add_argument("--sample-size", type=int, default=None, help="Optional sample size override.")
    parser.add_argument("--sample-seed", type=int, default=None, help="Optional deterministic sample seed.")
    parser.add_argument(
        "--results-dir",
        default=defense_config.DEFENSE_RESULTS_DIR,
        help="Results path passed to run_batch.py, typically outputs/defense_eval relative to the repo root.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print resolved runs without executing them.")
    parser.add_argument("--list-tables", action="store_true", help="List built-in table aliases and exit.")
    args = parser.parse_args()

    if args.list_tables:
        for spec in list_tables():
            print(f"{spec.key}: {spec.dataset_path} | {spec.description}")
        return

    models = parse_csv(args.model) or ["qwen3.5-plus"]
    tables = resolve_tables(parse_csv(args.table) or ["table3_memory"])
    results_dir = PROJECT_ROOT / args.results_dir
    results_dir.mkdir(parents=True, exist_ok=True)

    for table in tables:
        for model_alias in models:
            resolved_model, provider = resolve_model(model_alias)
            model_slug = resolved_model.split("/", 1)[-1].replace("-", "_").replace(".", "_")
            defense_mode = normalize_defense_mode(args.mode)
            stem = f"{table.key}_{defense_mode}_{model_slug}.json"
            relative_results = str(Path(args.results_dir) / stem)
            env = build_env(
                model_name=resolved_model,
                provider=provider,
                dataset_path=table.dataset_path,
                results_file=relative_results,
                sample_size=args.sample_size,
                defense_mode=defense_mode,
                defense_results_dir=args.results_dir,
                sample_seed=args.sample_seed,
            )

            print(
                f"[DefenseRun] table={table.key} dataset={table.dataset_path} "
                f"model={resolved_model} provider={provider} mode={defense_mode}"
            )
            print(f"[DefenseRun] results_base={relative_results}")
            if args.dry_run:
                continue

            subprocess.run(
                [sys.executable, "run_batch.py"],
                cwd=str(PROJECT_ROOT),
                env=env,
                check=True,
            )


if __name__ == "__main__":
    main()
