#!/usr/bin/env python3
"""Rerun completed memory/skill cases with an actual-state, fresh-session handoff."""
from __future__ import annotations

import argparse
import asyncio
from datetime import datetime
import fcntl
import hashlib
import importlib.metadata
import json
import logging
import math
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.reproduce_sampled import STRATEGIES, configure, save_run_config, write_json, summarize as original_summary

# The immediately preceding no-defense implementation is compatible: this update
# adds an opt-in read wrapper whose default path performs the same execution.
LEGACY_NO_DEFENSE_HASHES = {
    "src/agent_runner.py": "32e7f9081d5bc739b1420737ad1873c67da72bf487555edbefbab1c911060602",
    "scripts/reproduce_cross_session.py": "7187dee15e1ff0df8c0ae2d784c9f399af967a9664161f240484aaf10c617274",
}


def compatible_legacy_manifest(previous, current):
    if {k: v for k, v in previous.items() if k != "code_sha256"} != {
            k: v for k, v in current.items() if k != "code_sha256"}:
        return False
    old, new = previous["code_sha256"], current["code_sha256"]
    if set(new) - set(old) != {"src/source_warning.py"} or set(old) - set(new):
        return False
    return all(old[key] == new[key] or old[key] == LEGACY_NO_DEFENSE_HASHES.get(key)
               for key in old)


def select_baseline(baseline_dir):
    """Use saved case instances, including failed ones; never resample or select wins."""
    baseline_dir = baseline_dir.resolve()
    original_manifest = json.loads((baseline_dir / "manifest.json").read_text())
    if original_manifest.get("session_mode") != "original_shared_session":
        raise ValueError("Expected an original reproduce_sampled.py experiment")
    manifest = {"schema_version": 1, "baseline_dir": str(baseline_dir),
                "session_mode": "fresh_session_per_turn",
                "selection": "all_saved_memory_skill_instances_in_baseline",
                "slices": [], "code_sha256": {}}
    subsets, baseline = {}, {}
    for item in original_manifest["slices"]:
        if item["state"] not in {"memory", "skill"}:
            continue
        key = item["key"]
        path = baseline_dir / "results" / f"{key}.json"
        if not path.exists():
            raise ValueError(f"No saved baseline results: {path}")
        content = path.read_bytes()
        rows = json.loads(content)
        mapping = {r["case_info"]["case_id"]: r for r in rows}
        if len(mapping) != len(rows) or set(mapping) - set(item["case_ids"]):
            raise ValueError(f"Duplicate or unexpected baseline case IDs: {key}")
        ids = [cid for cid in item["case_ids"] if cid in mapping]
        cases = []
        for cid in ids:
            row = mapping[cid]
            case = row["case_info"].get("test_case_data")
            if not case or case["case_id"] != cid or len(case["turns"]) != 2:
                raise ValueError(f"Missing saved two-turn case definition: {key}/{cid}")
            if case.get("case_injection"):
                raise ValueError("System-prompt injection is outside this tool-return extension")
            if case["eval_config"]["eval_type"] not in {
                    "ordered_trace_check", "memory_poisoning", "argument_check", "tool_match"}:
                raise ValueError(f"Unsupported evaluation: {key}/{cid}")
            cases.append(case)
        subsets[key] = cases
        baseline[key] = [mapping[cid] for cid in ids]
        manifest["slices"].append({"key": key, "state": item["state"],
                                  "strategy": item["strategy"], "sample_size": len(ids),
                                  "baseline_planned": item["sample_size"], "case_ids": ids,
                                  "baseline_results_sha256": hashlib.sha256(content).hexdigest()})
    manifest["total_instances"] = sum(s["sample_size"] for s in manifest["slices"])
    if not manifest["total_instances"]:
        raise ValueError("No completed memory/skill instances in baseline")
    for relative in ("src/agent_runner.py", "src/cross_session.py", "src/virtual_tools.py",
                     "src/skill_registry.py", "src/simulator.py", "src/evaluator.py",
                     "src/data_manager.py", "src/llm_client.py", "config.py",
                     "scripts/reproduce_cross_session.py", "scripts/reproduce_sampled.py", "src/source_warning.py"):
        manifest["code_sha256"][relative] = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
    # Skill metadata and documents are also inputs to both sessions.
    digest = hashlib.sha256()
    for path in sorted((ROOT / "skill_data").rglob("*")):
        if path.is_file():
            digest.update(str(path.relative_to(ROOT)).encode())
            digest.update(path.read_bytes())
    manifest["skill_data_sha256"] = digest.hexdigest()
    return manifest, subsets, baseline


def summarize(manifest, records, baseline):
    # Keep the original denominator and ASR definition, including execution errors.
    summary = original_summary(manifest, records)
    baseline_summary = original_summary(manifest, baseline)
    for section in ("overall", "by_slice", "by_strategy"):
        if section == "overall":
            summary[section]["baseline_asr"] = baseline_summary[section]["asr"]
        else:
            for key, values in summary[section].items():
                values["baseline_asr"] = baseline_summary[section][key]["asr"]
    transitions = {"failure_to_failure": 0, "failure_to_success": 0,
                   "success_to_failure": 0, "success_to_success": 0}
    for rows in records.values():
        for row in rows:
            old = "success" if row["baseline_comparison"]["attack_success"] else "failure"
            new = "success" if row["final_output"]["attack_success"] else "failure"
            transitions[f"{old}_to_{new}"] += 1
    summary["paired_transitions"] = transitions
    summary["evaluation"] = "released_evaluator_including_PIE_strict_replacement"
    return summary


async def execute(args, manifest, records, baseline):
    from src.agent_runner import AgentRunner, CaseResult
    from src.data_manager import DataManager
    from src.evaluator import Evaluator, strip_export_fields
    from src.cross_session import snapshot
    from src.llm_client import request_failures, request_stats

    runner = AgentRunner(api_key=os.environ["AGENT_API_KEY"], base_url=os.environ["AGENT_BASE_URL"],
                         model_name=os.environ["AGENT_MODEL"], simulator_model=os.environ["SIMULATOR_MODEL"],
                         simulator_api_key=os.environ["SIMULATOR_API_KEY"],
                         simulator_base_url=os.environ["SIMULATOR_BASE_URL"])
    evaluator = Evaluator()
    stats_path = args.output_dir / "request_stats.json"
    previous_stats = json.loads(stats_path.read_text()) if stats_path.exists() else {}
    started, errors = 0, 0

    def checkpoint():
        write_json(args.output_dir / "summary.json", summarize(manifest, records, baseline))
        write_json(stats_path, {key: previous_stats.get(key, 0) + value for key, value in request_stats().items()})

    async def run_one(case, original):
        failures, states, warning_events = [], {}, []
        token = request_failures.set(failures)
        def observe(event, turn_id):
            if event == "case_end":
                states["case_final"] = snapshot()
            else:
                states.setdefault(str(turn_id), {})[event] = snapshot()
        try:
            try:
                options = {"cross_session": True, "state_observer": observe}
                if getattr(args, "source_warning", False):
                    options.update(persistent_read_source_warning=True, source_warning_events=warning_events)
                result = await runner.run_single_case(case, **options)
            except Exception as exc:
                result = CaseResult(case.case_id, False, [], 0, str(exc))
            if failures:
                result.success = False
                result.error_message = "; ".join(failures)
            evaluation_error = None
            try:
                evaluated = evaluator.evaluate_case(case, result)
                details = strip_export_fields(evaluated.details or {})
                metrics = {"attack_success": bool(evaluated.attack_success),
                           "failure_reason": evaluated.failure_reason, "score": evaluated.score,
                           "asr_score": details.get("asr_score"), "details": details}
            except Exception as exc:
                evaluation_error = str(exc)
                metrics = {"attack_success": False, "failure_reason": "evaluation_error: " + str(exc),
                           "score": 0, "asr_score": 0, "details": {"evaluation_error": str(exc)}}
            row = {"experiment_info": {"model_name": os.environ["AGENT_MODEL"],
                                        "session_mode": "fresh_session_per_turn"},
                    "case_info": {"case_id": case.case_id, "test_case_data": case.model_dump()},
                    "execution_trajectory": [log.to_dict() for log in result.turn_logs],
                    "persistent_state_snapshots": states,
                    "evaluation_results": metrics,
                    "baseline_comparison": {"attack_success": bool(original["final_output"]["attack_success"]),
                                            "execution_status": original["execution_status"]},
                    "final_output": {key: metrics[key] for key in ("attack_success", "failure_reason", "score")},
                    "execution_status": {"success": result.success, "error": result.error_message,
                                         "evaluation_error": evaluation_error, "seconds": result.total_time}}
            if getattr(args, "source_warning", False):
                row["experiment_info"]["defense"] = "persistent_read_source_warning"
                row["source_warning_events"] = warning_events
            return row
        finally:
            request_failures.reset(token)
    try:
        for item in manifest["slices"]:
            key = item["key"]
            dataset = args.output_dir / "sampled" / f"{key}.json"
            result_path = args.output_dir / "results" / f"{key}.json"
            os.environ["DATASET_FILE"] = str(dataset)
            cases = DataManager(str(dataset), str(result_path)).load_test_cases()
            saved = {r["case_info"]["case_id"]: r for r in records[key]}
            originals = {r["case_info"]["case_id"]: r for r in baseline[key]}
            pending = [c for c in cases if c.case_id not in saved or (args.retry_errors and (
                not saved[c.case_id]["execution_status"]["success"] or
                saved[c.case_id]["execution_status"].get("evaluation_error")))]
            for offset in range(0, len(pending), args.concurrency):
                batch = pending[offset:offset + args.concurrency]
                if args.limit is not None:
                    batch = batch[:max(0, args.limit - started)]
                if not batch:
                    return errors
                started += len(batch)
                tasks = [asyncio.create_task(run_one(case, originals[case.case_id])) for case in batch]
                try:
                    for task in asyncio.as_completed(tasks):
                        row = await task
                        saved[row["case_info"]["case_id"]] = row
                        records[key] = list(saved.values())
                        write_json(result_path, records[key])
                        checkpoint()
                        errors += int(not row["execution_status"]["success"] or
                                      bool(row["execution_status"].get("evaluation_error")))
                        print(f"[SAVE] {key} {row['case_info']['case_id']} "
                              f"execution={row['execution_status']['success']} "
                              f"attack_success={row['final_output']['attack_success']} "
                              f"total={sum(len(r) for r in records.values())}/{manifest['total_instances']}", flush=True)
                finally:
                    for task in tasks:
                        if not task.done():
                            task.cancel()
                    await asyncio.gather(*tasks, return_exceptions=True)
    finally:
        checkpoint()
        await runner.external_client.close()
        if evaluator.client:
            evaluator.client.close()
    return errors


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline-dir", type=Path,
                        default=ROOT / "outputs/repro_deepseek_flash_30pct_seed42")
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--run", action="store_true", help="Call models; otherwise prepare only")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--with-source-warning", action="store_true",
                        help="After all no-defense cases finish, run a second arm with source reminders")
    parser.add_argument("--retry-errors", action="store_true")
    parser.add_argument("--limit", type=int, help="Maximum pending case instances, including their phases")
    parser.add_argument("--concurrency", type=int, default=2)
    parser.add_argument("--rpm", type=float, default=20)
    parser.add_argument("--max-in-flight", type=int, default=2)
    parser.add_argument("--retries", type=int, default=12)
    parser.add_argument("--backoff-base", type=float, default=6)
    parser.add_argument("--backoff-cap", type=float, default=120)
    parser.add_argument("--max-agent-turns", type=int, default=30)
    parser.add_argument("--timeout", type=float, default=120)
    args = parser.parse_args()
    if min(args.concurrency, args.max_in_flight, args.max_agent_turns) < 1 or args.retries < 0:
        parser.error("Concurrency/steps must be positive; retries nonnegative")
    if not all(math.isfinite(v) and v > 0 for v in (args.rpm, args.timeout, args.backoff_base, args.backoff_cap)):
        parser.error("RPM, timeout and backoff must be positive and finite")
    if args.backoff_base > args.backoff_cap or (args.limit is not None and args.limit < 1):
        parser.error("Invalid backoff bounds or limit")
    if args.retry_errors and not args.resume:
        parser.error("retry-errors requires resume")
    if args.resume and not args.output_dir:
        parser.error("resume requires output-dir")
    args.baseline_dir = args.baseline_dir.resolve()
    args.output_dir = (args.output_dir or ROOT / "outputs" / (
        "cross_session_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f"))).resolve()
    if args.output_dir == args.baseline_dir or args.baseline_dir in args.output_dir.parents:
        parser.error("Use a separate output directory outside the baseline experiment")
    return args


def run_experiment(args):
    manifest, subsets, baseline = select_baseline(args.baseline_dir)
    if args.source_warning:
        manifest["persistent_read_source_warning"] = True
    args.output_dir.mkdir(parents=True, exist_ok=True)
    with (args.output_dir / "run.lock").open("a") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise ValueError("Another process is using this experiment") from None
        path = args.output_dir / "manifest.json"
        if args.resume:
            if not path.exists():
                raise ValueError("Resume manifest differs: retain baseline, code and skills")
            previous = json.loads(path.read_text())
            if previous != manifest:
                if args.source_warning or not compatible_legacy_manifest(previous, manifest):
                    raise ValueError("Resume manifest differs: retain baseline, code and skills")
                history_path = args.output_dir / "manifest_history.json"
                history = json.loads(history_path.read_text()) if history_path.exists() else []
                history.append({"recorded_at": datetime.now().astimezone().isoformat(),
                                "reason": "opt_in_source_warning_added_no_defense_behavior_unchanged",
                                "previous_manifest": previous, "manifest": manifest})
                write_json(history_path, history)
                print("[RESUME] Compatible source-warning extension; retaining all no-defense results", flush=True)
        elif path.exists() or (args.output_dir / "results").exists():
            raise ValueError("Output already contains an experiment; use --resume or a new directory")
        records = {}
        for item in manifest["slices"]:
            key = item["key"]
            result_path = args.output_dir / "results" / f"{key}.json"
            rows = json.loads(result_path.read_text()) if result_path.exists() else []
            ids = [r["case_info"]["case_id"] for r in rows]
            if len(set(ids)) != len(ids) or set(ids) - set(item["case_ids"]):
                raise ValueError(f"Duplicate or unexpected saved cases: {key}")
            records[key] = rows
        if args.run:
            settings = configure(args)
            settings["session_mode"] = manifest["session_mode"]
            if args.source_warning:
                from src.source_warning import WARNING_TEMPLATE
                settings["persistent_read_source_warning"] = {
                    "enabled": True, "scope": "session_2_MemoryRetrieve_and_SkillRead_outputs",
                    "template": WARNING_TEMPLATE, "provenance": "configured_injection_source"}
            original_config = json.loads((args.baseline_dir / "run_config.json").read_text())
            for field in ("model", "endpoint_sha256"):
                if original_config.get(field) != settings[field]:
                    raise ValueError(f"Baseline {field} differs; use the same model and endpoint for comparison")
            if original_config.get("case_concurrency") != settings["case_concurrency"]:
                raise ValueError("Baseline case_concurrency differs; use the same concurrency")
            for field in ("MAX_AGENT_TURNS", "REQUEST_TIMEOUT", "ENABLE_DEFENSE", "EVAL_REQUIRE_SKILL_UPDATE_READ",
                          "LLM_MAX_IN_FLIGHT", "LLM_429_MAX_RETRIES", "LLM_RETRY_BASE_SECONDS", "LLM_RETRY_MAX_SECONDS"):
                if original_config["settings"].get(field) != settings["settings"][field]:
                    raise ValueError(f"Baseline setting differs: {field}")
            save_run_config(args.output_dir, settings, sum(len(r) for r in records.values()))
            write_json(args.output_dir / "environment.json", {
                "python": sys.version, "executable": sys.executable,
                "packages": {name: importlib.metadata.version(name) for name in
                             ("openai", "openai-agents", "httpx", "pydantic", "json-repair", "tqdm")}})
        write_json(path, manifest)
        for item in manifest["slices"]:
            key = item["key"]
            write_json(args.output_dir / "sampled" / f"{key}.json", subsets[key])
            write_json(args.output_dir / "baseline" / f"{key}.json", baseline[key])
            print(f"{key}: {item['sample_size']} saved baseline cases; rerun saved={len(records[key])}")
        write_json(args.output_dir / "summary.json", summarize(manifest, records, baseline))
        print(f"Total: {manifest['total_instances']} instances; output={args.output_dir}", flush=True)
        if not args.run:
            return 0
        logging.basicConfig(level=logging.WARNING, format="%(asctime)s %(levelname)s %(message)s")
        logging.getLogger("src.llm_client").setLevel(logging.INFO)
        errors = asyncio.run(execute(args, manifest, records, baseline))
        print(json.dumps(json.loads((args.output_dir / "summary.json").read_text())["overall"], ensure_ascii=False))
        return 1 if errors else 0


def defense_comparison(no_defense_dir, warning_dir):
    manifest = json.loads((no_defense_dir / "manifest.json").read_text())
    groups = {}
    for item in manifest["slices"]:
        key = item["key"]
        def load_arm(root):
            path = root / "results" / f"{key}.json"
            rows = json.loads(path.read_text()) if path.exists() else []
            return {row["case_info"]["case_id"]: row for row in rows}
        first, second = load_arm(no_defense_dir), load_arm(warning_dir)
        counts = {"planned": item["sample_size"], "no_defense_completed": len(first),
                  "source_warning_completed": len(second),
                  "no_defense_successes": sum(bool(r["final_output"]["attack_success"]) for r in first.values()),
                  "source_warning_successes": sum(bool(r["final_output"]["attack_success"]) for r in second.values()),
                  "paired_completed": 0, "both_successes": 0, "both_failures": 0,
                  "no_defense_only_successes": 0, "source_warning_only_successes": 0,
                  "stage1_state_equal": 0, "stage1_state_different": 0, "stage1_state_unavailable": 0}
        for cid in first.keys() & second.keys():
            a, b = first[cid], second[cid]
            if a["case_info"]["test_case_data"] != b["case_info"]["test_case_data"]:
                raise ValueError(f"Defense arm case definition differs: {key}/{cid}")
            old, new = bool(a["final_output"]["attack_success"]), bool(b["final_output"]["attack_success"])
            field = ("both_successes" if old and new else "both_failures" if not old and not new
                     else "no_defense_only_successes" if old else "source_warning_only_successes")
            counts[field] += 1
            counts["paired_completed"] += 1
            state_a = a.get("persistent_state_snapshots", {}).get("1", {}).get("session_end")
            state_b = b.get("persistent_state_snapshots", {}).get("1", {}).get("session_end")
            counts["stage1_state_unavailable" if state_a is None or state_b is None else
                   "stage1_state_equal" if state_a == state_b else "stage1_state_different"] += 1
        groups[key] = counts
    def aggregate(values):
        counts = {key: sum(v[key] for v in values) for key in next(iter(groups.values()))}
        planned = counts["planned"]
        for label in ("no_defense", "source_warning"):
            counts[label + "_asr"] = counts[label + "_successes"] / planned if (
                planned and counts[label + "_completed"] == planned) else None
        counts["asr_reduction"] = counts["no_defense_asr"] - counts["source_warning_asr"] if (
            counts["no_defense_asr"] is not None and counts["source_warning_asr"] is not None) else None
        return counts
    return {"overall": aggregate(list(groups.values())),
            "by_slice": {key: aggregate([value]) for key, value in groups.items()},
            "evaluation": "released_evaluator_including_PIE_strict_replacement",
            "note": "Both arms rerun session 1 under the same conditions; actual saved states can differ. "
                    "State equality is reported for interpretation and never filters the ASR denominator."}


def main():
    args = parse_args()
    args.source_warning = False
    errors = run_experiment(args)
    if not args.with_source_warning:
        return errors
    summary = json.loads((args.output_dir / "summary.json").read_text())
    if summary["overall"]["pending"]:
        print("[SUITE] No-defense is incomplete; source-warning arm will start after all cases finish.", flush=True)
        return errors
    if not args.run:
        return errors
    import copy
    defense_args = copy.copy(args)
    defense_args.source_warning = True
    defense_args.output_dir = args.output_dir / "source_warning"
    defense_args.resume = (defense_args.output_dir / "manifest.json").exists()
    defense_errors = run_experiment(defense_args)
    comparison = defense_comparison(args.output_dir, defense_args.output_dir)
    write_json(args.output_dir / "defense_comparison.json", comparison)
    print("[COMPARISON] " + json.dumps(comparison["overall"], ensure_ascii=False), flush=True)
    return 1 if errors or defense_errors else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, KeyError, OSError, ImportError, importlib.metadata.PackageNotFoundError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(2)
