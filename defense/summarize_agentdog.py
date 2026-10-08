from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


STRATEGY_LABELS = {
    "latent_instruction_planting": "LIP",
    "proactive_information_elicitation": "PIE",
    "persistent_information_corruption": "PIC",
}

MODEL_LABELS = {
    "qwen3.5-plus": "qwen/qwen3.5-plus",
    "gemini-3-flash-preview": "google/gemini-3-flash-preview",
    "gemini-3-pro-preview": "google/gemini-3-pro-preview",
    "google/gemini-3-flash-preview": "google/gemini-3-flash-preview",
    "meta-llama/llama-3.3-70b-instruct": "meta-llama/llama-3.3-70b-instruct",
}


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _safe_rate(num: float, den: float) -> float | None:
    if den <= 0:
        return None
    return num / den


def _iter_result_files(root: Path) -> Iterable[Path]:
    if root.is_file():
        yield root
        return
    yield from sorted(root.rglob("*.json"))


def _parse_path(path: Path) -> Tuple[str, str, str] | None:
    parts = path.parts
    for strategy in STRATEGY_LABELS:
        if strategy in parts:
            idx = parts.index(strategy)
            if idx + 1 < len(parts):
                state = parts[idx + 1]
                return strategy, STRATEGY_LABELS[strategy], state
    stem = path.stem
    for strategy in STRATEGY_LABELS:
        if strategy in stem:
            for state in ("session", "memory", "skill", "single"):
                if f"_{state}_" in stem:
                    return strategy, STRATEGY_LABELS[strategy], state
    return None


def _extract_model(item: Dict[str, Any]) -> str:
    raw = (item.get("experiment_info") or {}).get("model_name") or ""
    return MODEL_LABELS.get(raw, raw)


def _extract_case_stats(item: Dict[str, Any]) -> Dict[str, Any]:
    evaluation = item.get("evaluation_results") or {}
    details = evaluation.get("details") or {}
    report = details.get("defense_report") or {}
    events = report.get("events") or []
    blocked_actions = int(report.get("blocked_actions") or 0)
    reviewed_actions = int(report.get("reviewed_actions") or 0)
    reviewed_tool_outputs = int(report.get("reviewed_tool_outputs") or 0)
    flagged_tool_outputs = int(report.get("flagged_tool_outputs") or 0)
    guard_errors = sum(1 for event in events if event.get("decision") == "guard_error_allow")
    return {
        "attack_success": 1 if float(evaluation.get("attack_success") or 0.0) > 0 else 0,
        "reviewed_actions": reviewed_actions,
        "blocked_actions": blocked_actions,
        "case_blocked": 1 if blocked_actions > 0 else 0,
        "reviewed_tool_outputs": reviewed_tool_outputs,
        "flagged_tool_outputs": flagged_tool_outputs,
        "case_warned": 1 if flagged_tool_outputs > 0 else 0,
        "guard_errors": guard_errors,
    }


def _load_reference(path: Path | None) -> Dict[str, Any]:
    if not path:
        return {}
    if not path.exists():
        raise FileNotFoundError(path)
    data = _read_json(path)
    return data.get("model_strategy") or {}


def _reference_values(reference: Dict[str, Any], model: str, strategy: str) -> Dict[str, Any]:
    row = (reference.get(model) or {}).get(strategy) or {}
    return {
        "NoDefense_ASR_ref": row.get("ASR"),
        "BSR_under_attack_ref": row.get("BSR_under_attack"),
        "BSR_ref_total": row.get("total"),
    }


def _finalize_group(row: Dict[str, Any]) -> Dict[str, Any]:
    n = row["N"]
    reviewed = row["reviewed_actions"]
    blocked = row["blocked_actions"]
    reviewed_outputs = row["reviewed_tool_outputs"]
    flagged_outputs = row["flagged_tool_outputs"]
    guard_errors = row["guard_errors"]
    row["AgentDoG_ASR"] = _safe_rate(row["attack_success"], n)
    row["case_block_rate"] = _safe_rate(row["case_blocked"], n)
    row["action_block_rate"] = _safe_rate(blocked, reviewed)
    row["case_warning_rate"] = _safe_rate(row["case_warned"], n)
    row["tool_warning_rate"] = _safe_rate(flagged_outputs, reviewed_outputs)
    row["guard_error_rate"] = _safe_rate(guard_errors, reviewed_outputs or reviewed)
    return row


def summarize(results_root: Path, bsr_summary: Path | None) -> Dict[str, Any]:
    reference = _load_reference(bsr_summary)
    model_strategy: Dict[Tuple[str, str], Dict[str, Any]] = defaultdict(
        lambda: {
            "model": "",
            "strategy": "",
            "N": 0,
            "attack_success": 0,
            "reviewed_actions": 0,
            "blocked_actions": 0,
            "case_blocked": 0,
            "reviewed_tool_outputs": 0,
            "flagged_tool_outputs": 0,
            "case_warned": 0,
            "guard_errors": 0,
        }
    )
    state_level: Dict[Tuple[str, str, str], Dict[str, Any]] = defaultdict(
        lambda: {
            "model": "",
            "strategy": "",
            "state": "",
            "N": 0,
            "attack_success": 0,
            "reviewed_actions": 0,
            "blocked_actions": 0,
            "case_blocked": 0,
            "reviewed_tool_outputs": 0,
            "flagged_tool_outputs": 0,
            "case_warned": 0,
            "guard_errors": 0,
        }
    )
    files_seen: List[str] = []

    for path in _iter_result_files(results_root):
        parsed = _parse_path(path)
        if not parsed:
            continue
        _, strategy_label, state = parsed
        try:
            data = _read_json(path)
        except Exception:
            continue
        if not isinstance(data, list):
            continue
        files_seen.append(str(path))
        for item in data:
            model = _extract_model(item)
            stats = _extract_case_stats(item)
            key = (model, strategy_label)
            row = model_strategy[key]
            row["model"] = model
            row["strategy"] = strategy_label
            skey = (model, strategy_label, state)
            srow = state_level[skey]
            srow["model"] = model
            srow["strategy"] = strategy_label
            srow["state"] = state
            for target in (row, srow):
                target["N"] += 1
                target["attack_success"] += stats["attack_success"]
                target["reviewed_actions"] += stats["reviewed_actions"]
                target["blocked_actions"] += stats["blocked_actions"]
                target["case_blocked"] += stats["case_blocked"]
                target["reviewed_tool_outputs"] += stats["reviewed_tool_outputs"]
                target["flagged_tool_outputs"] += stats["flagged_tool_outputs"]
                target["case_warned"] += stats["case_warned"]
                target["guard_errors"] += stats["guard_errors"]

    model_strategy_rows = []
    for (model, strategy), row in sorted(model_strategy.items()):
        row = _finalize_group(dict(row))
        row.update(_reference_values(reference, model, strategy))
        model_strategy_rows.append(row)

    state_rows = []
    for (model, strategy, state), row in sorted(state_level.items()):
        row = _finalize_group(dict(row))
        row.update(_reference_values(reference, model, strategy))
        state_rows.append(row)

    return {
        "model_strategy": model_strategy_rows,
        "state_level": state_rows,
        "files_seen": files_seen,
    }


def _fmt_pct(value: Any) -> str:
    if value is None:
        return ""
    return f"{100 * float(value):.1f}"


def write_outputs(summary: Dict[str, Any], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "agentdog_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    columns = [
        "model",
        "strategy",
        "state",
        "N",
        "NoDefense_ASR_ref",
        "AgentDoG_ASR",
        "BSR_under_attack_ref",
        "case_block_rate",
        "action_block_rate",
        "case_warning_rate",
        "tool_warning_rate",
        "guard_error_rate",
        "reviewed_actions",
        "blocked_actions",
        "reviewed_tool_outputs",
        "flagged_tool_outputs",
    ]
    for name, rows in (("agentdog_model_strategy.csv", summary["model_strategy"]), ("agentdog_state_level.csv", summary["state_level"])):
        with (output_dir / name).open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=columns)
            writer.writeheader()
            for row in rows:
                writer.writerow({key: row.get(key) for key in columns})

    lines = []
    lines.append("# AgentDoG Summary")
    lines.append("")
    lines.append("Reference ASR/BSR columns are from the prior no-defense BSR-under-attack summary when supplied.")
    lines.append("")
    lines.append("| Model | Strategy | N | No-defense ASR ref (%) | AgentDoG ASR (%) | BSR-under-attack ref (%) | Case warning rate (%) | Tool warning rate (%) | Case block rate (%) | Guard error rate (%) |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for row in summary["model_strategy"]:
        lines.append(
            "| {model} | {strategy} | {N} | {no_def} | {agentdog} | {bsr} | {case_warn} | {tool_warn} | {case_block} | {guard_error} |".format(
                model=row["model"],
                strategy=row["strategy"],
                N=row["N"],
                no_def=_fmt_pct(row.get("NoDefense_ASR_ref")),
                agentdog=_fmt_pct(row.get("AgentDoG_ASR")),
                bsr=_fmt_pct(row.get("BSR_under_attack_ref")),
                case_warn=_fmt_pct(row.get("case_warning_rate")),
                tool_warn=_fmt_pct(row.get("tool_warning_rate")),
                case_block=_fmt_pct(row.get("case_block_rate")),
                guard_error=_fmt_pct(row.get("guard_error_rate")),
            )
        )
    (output_dir / "agentdog_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize AgentDoG defended runs.")
    parser.add_argument("--results-root", default="outputs/agentdog_full", help="Root containing AgentDoG result JSON files.")
    parser.add_argument("--bsr-summary", default="", help="Optional prior BSR summary JSON for no-defense ASR/BSR reference columns.")
    parser.add_argument("--output-dir", default="outputs/agentdog_full/reports", help="Directory for summary outputs.")
    args = parser.parse_args()

    bsr_path = Path(args.bsr_summary).resolve() if args.bsr_summary else None
    summary = summarize(Path(args.results_root).resolve(), bsr_path)
    write_outputs(summary, Path(args.output_dir).resolve())
    print(f"Wrote {len(summary['model_strategy'])} model-strategy rows and {len(summary['state_level'])} state rows.")


if __name__ == "__main__":
    main()
