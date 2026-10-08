from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from defense import config as defense_config
from defense.guard import SUPPORTED_DEFENSE_MODES, normalize_defense_mode
from defense.run_defense import build_env, parse_csv, resolve_model


@dataclass(frozen=True)
class EvaluationRun:
    alias_table: str
    canonical_table: str
    state: str
    dataset_path: str


TABLE_STATE_RUNS: Dict[str, List[EvaluationRun]] = {
    "table1": [
        EvaluationRun("table1", "latent_instruction_planting", "single", "datasets/latent_instruction_planting/single.json"),
        EvaluationRun("table1", "latent_instruction_planting", "session", "datasets/latent_instruction_planting/session.json"),
        EvaluationRun("table1", "latent_instruction_planting", "skill", "datasets/latent_instruction_planting/skill.json"),
        EvaluationRun("table1", "latent_instruction_planting", "memory", "datasets/latent_instruction_planting/memory.json"),
    ],
    "table2": [
        EvaluationRun("table2", "proactive_information_elicitation", "single", "datasets/proactive_information_elicitation/single.json"),
        EvaluationRun("table2", "proactive_information_elicitation", "session", "datasets/proactive_information_elicitation/session.json"),
        EvaluationRun("table2", "proactive_information_elicitation", "skill", "datasets/proactive_information_elicitation/skill.json"),
        EvaluationRun("table2", "proactive_information_elicitation", "memory", "datasets/proactive_information_elicitation/memory.json"),
    ],
    "table3": [
        EvaluationRun("table3", "persistent_information_corruption", "single", "datasets/persistent_information_corruption/single.json"),
        EvaluationRun("table3", "persistent_information_corruption", "session", "datasets/persistent_information_corruption/session.json"),
        EvaluationRun("table3", "persistent_information_corruption", "skill", "datasets/persistent_information_corruption/skill.json"),
        EvaluationRun("table3", "persistent_information_corruption", "memory", "datasets/persistent_information_corruption/memory.json"),
    ],
}

ALL_STATES = ("single", "session", "skill", "memory")
DEFAULT_STATES = ("session", "skill", "memory")


def resolve_tables(values: Iterable[str]) -> List[str]:
    requested = parse_csv(values) or ["table1", "table2", "table3"]
    invalid = [name for name in requested if name not in TABLE_STATE_RUNS]
    if invalid:
        raise KeyError(f"Unknown table aliases: {', '.join(invalid)}")
    return requested


def resolve_states(values: Iterable[str]) -> List[str]:
    requested = parse_csv(values) or list(DEFAULT_STATES)
    invalid = [name for name in requested if name not in ALL_STATES]
    if invalid:
        raise KeyError(f"Unknown states: {', '.join(invalid)}")
    return requested


def iter_runs(tables: List[str], states: List[str]) -> List[EvaluationRun]:
    selected: List[EvaluationRun] = []
    for table in tables:
        for spec in TABLE_STATE_RUNS[table]:
            if spec.state in states:
                selected.append(spec)
    return selected


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Run the released Rule, Guard, and AgentDoG Defense matrix for LIP, PIE, and PIC. "
            "By default, it evaluates the session, memory, and skill states used in the defense experiment."
        )
    )
    parser.add_argument("--model", action="append", default=[])
    parser.add_argument("--mode", action="append", default=[])
    parser.add_argument("--table", action="append", default=[])
    parser.add_argument("--state", action="append", default=[], help="Agent state; use single to include the direct baseline.")
    parser.add_argument("--surface", action="append", default=[], help=argparse.SUPPRESS)
    parser.add_argument("--sample-size", type=int, default=50)
    parser.add_argument("--sample-seed", type=int, default=20260709)
    parser.add_argument(
        "--results-dir",
        default=str(Path(defense_config.DEFENSE_RESULTS_DIR) / "matrix"),
        help="Results path passed to run_batch.py, typically outputs/defense_eval/matrix relative to the repo root.",
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    tables = resolve_tables(args.table)
    states = resolve_states([*args.state, *args.surface])
    raw_modes = parse_csv(args.mode) or ["rule_defense", "guard_defense", "agentdog_defense"]
    invalid_modes = [mode for mode in raw_modes if mode not in SUPPORTED_DEFENSE_MODES]
    if invalid_modes:
        raise KeyError(f"Unknown defense modes: {', '.join(invalid_modes)}")
    modes = [normalize_defense_mode(mode) for mode in raw_modes]

    models = parse_csv(args.model) or ["qwen3.5-plus"]
    runs = iter_runs(tables, states)

    print(f"[Matrix] tables={tables}")
    print(f"[Matrix] states={states}")
    print(f"[Matrix] modes={modes}")
    print(f"[Matrix] models={models}")
    print(f"[Matrix] sample_size={args.sample_size}")
    print(f"[Matrix] sample_seed={args.sample_seed}")
    print(f"[Matrix] results_dir={args.results_dir}")
    print(f"[Matrix] total_jobs={len(runs) * len(modes) * len(models)}")

    for mode in modes:
        for model_alias in models:
            resolved_model, provider = resolve_model(model_alias)
            model_slug = resolved_model.split("/", 1)[-1].replace("-", "_").replace(".", "_")
            for run in runs:
                result_rel = str(
                    Path(args.results_dir)
                    / mode
                    / run.canonical_table
                    / run.state
                    / f"{run.canonical_table}_{run.state}_{mode}_{model_slug}.json"
                )
                env = build_env(
                    model_name=resolved_model,
                    provider=provider,
                    dataset_path=run.dataset_path,
                    results_file=result_rel,
                    sample_size=args.sample_size,
                    defense_mode=mode,
                    defense_results_dir=args.results_dir,
                    sample_seed=args.sample_seed,
                )
                print(
                    "[MatrixRun] "
                    f"alias_table={run.alias_table} canonical_table={run.canonical_table} "
                    f"state={run.state} mode={mode} model={resolved_model} "
                    f"dataset={run.dataset_path} results={result_rel}"
                )
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
