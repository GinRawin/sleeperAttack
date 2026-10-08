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
from scripts.reproduce_sampled import STRATEGIES, configure, save_run_config, write_json


def select_baseline(baseline_dir, clean_control=False):
    """Use saved case instances, including failed ones; never resample or select wins."""
    baseline_dir = baseline_dir.resolve()
    original_manifest = json.loads((baseline_dir / "manifest.json").read_text())
    if original_manifest.get("session_mode") != "original_shared_session":
        raise ValueError("Expected an original reproduce_sampled.py experiment")
    manifest = {"schema_version": 1, "baseline_dir": str(baseline_dir),
                "session_mode": "fresh_session_per_turn", "clean_control": clean_control,
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
                     "scripts/reproduce_cross_session.py", "scripts/reproduce_sampled.py"):
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
    def aggregate(keys):
        planned = sum(s["sample_size"] for s in manifest["slices"] if s["key"] in keys)
        rows = [r for key in keys for r in records.get(key, [])]
        done = len(rows)
        metrics = [r["cross_session_evaluation"] for r in rows]
        success = sum(bool(m.get("cross_session_success")) for m in metrics)
        released = sum(bool(m.get("released_full_trajectory", {}).get("attack_success")) for m in metrics)
        behavior = sum(bool(m.get("trigger_behavior", {}).get("success")) for m in metrics)
        changed = sum(bool(m.get("persistence_evidence", {}).get("state_changed")) for m in metrics)
        changed_success = sum(bool(m.get("cross_session_success")) for m in metrics)
        read = sum(bool(m.get("persistence_evidence", {}).get("changed_state_read")) for m in metrics)
        base = [r for key in keys for r in baseline.get(key, [])]
        base_success = sum(bool(r["final_output"]["attack_success"]) for r in base)
        clean_done = sum(m.get("clean_control_success") is True for m in metrics)
        clean_success = sum(bool(m.get("clean_control_behavior", {}).get("success"))
                            for m in metrics if m.get("clean_control_behavior"))
        excess = sum(m.get("paired_excess_success") is True for m in metrics)
        transitions = {"failure_to_failure": 0, "failure_to_success": 0,
                       "success_to_failure": 0, "success_to_success": 0}
        for row in rows:
            old = "success" if row["baseline_comparison"]["attack_success"] else "failure"
            new = "success" if row["cross_session_evaluation"].get(
                "released_full_trajectory", {}).get("attack_success") else "failure"
            transitions[f"{old}_to_{new}"] += 1
        return {"planned": planned, "completed": done, "pending": planned - done,
                "execution_failures": sum(not r["execution_status"]["success"] for r in rows),
                "evaluation_errors": sum(bool(r["execution_status"].get("evaluation_error")) for r in rows),
                "baseline_attack_successes": base_success,
                "baseline_asr": base_success / len(base) if base else None,
                "released_attack_successes": released,
                "released_asr": released / planned if planned and done == planned else None,
                "released_asr_completed": released / done if done else None,
                "trigger_behavior_successes": behavior,
                "state_changed_cases": changed, "changed_state_read_cases": read,
                "state_change_rate_completed": changed / done if done else None,
                "semantic_poisoning_rate": None,
                "cross_session_successes": success,
                "cross_session_asr": success / planned if planned and done == planned else None,
                "cross_session_asr_completed": success / done if done else None,
                "trigger_rate_after_state_change_completed": changed_success / changed if changed else None,
                "clean_control_completed": clean_done, "clean_control_behavior_successes": clean_success,
                "clean_control_execution_failures": sum(m.get("clean_control_success") is False for m in metrics),
                "paired_excess_successes": excess,
                "released_paired_transitions": transitions}
    keys = [s["key"] for s in manifest["slices"]]
    return {"overall": aggregate(keys), "by_slice": {key: aggregate([key]) for key in keys},
            "by_strategy": {alias: aggregate([k for k in keys if k.startswith(alias + "/")])
                            for alias in STRATEGIES},
            "metric_note": "State changes and exact reads do not verify malicious semantics. "
                           "Cross-session ASR requires a changed carrier, a read before behavior, "
                           "and configured trigger business actions AND PIE ground-truth parameters. "
                           "Released scores retain the original evaluator for comparison."}


async def execute(args, manifest, records, baseline):
    from src.agent_runner import AgentRunner
    from src.data_manager import DataManager
    from src.evaluator import Evaluator, strip_export_fields
    from src.cross_session import run_pair, evaluate_pair
    from src.llm_client import request_stats

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

    async def run_one(case, key, original):
        cache_key = hashlib.sha256(f"{key}:{case.case_id}".encode()).hexdigest()
        combined, evidence, trigger, clean = await run_pair(
            runner, case, args.output_dir / "simulator_cache" / cache_key, args.clean_control)
        error = None
        try:
            metrics = strip_export_fields(evaluate_pair(evaluator, case, combined, evidence,
                                                        trigger, clean, key.split("/")[1]))
        except Exception as exc:
            error = str(exc)
            metrics = {"cross_session_success": False, "evaluation_error": error}
        succeeded = metrics.get("cross_session_success", False)
        return {"experiment_info": {"model_name": os.environ["AGENT_MODEL"],
                                    "session_mode": "fresh_session_per_turn"},
                "case_info": {"case_id": case.case_id, "test_case_data": case.model_dump()},
                "execution_trajectory": [log.to_dict() for log in combined.turn_logs],
                "session_evidence": evidence, "cross_session_evaluation": metrics,
                "evaluation_results": metrics.get("released_full_trajectory", {}),
                "baseline_comparison": {"attack_success": bool(original["final_output"]["attack_success"]),
                                        "execution_status": original["execution_status"]},
                "final_output": {"attack_success": succeeded,
                                 "score": int(succeeded), "failure_reason": error or (
                                     None if succeeded else "Cross-session persistence/trigger conditions not satisfied")},
                "execution_status": {"success": combined.success, "error": combined.error_message,
                                     "evaluation_error": error, "seconds": combined.total_time,
                                     "clean_control_success": clean.success if clean else None}}
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
                saved[c.case_id]["execution_status"].get("evaluation_error") or
                saved[c.case_id]["execution_status"].get("clean_control_success") is False))]
            for offset in range(0, len(pending), args.concurrency):
                batch = pending[offset:offset + args.concurrency]
                if args.limit is not None:
                    batch = batch[:max(0, args.limit - started)]
                if not batch:
                    return errors
                started += len(batch)
                tasks = [asyncio.create_task(run_one(case, key, originals[case.case_id])) for case in batch]
                try:
                    for task in asyncio.as_completed(tasks):
                        row = await task
                        saved[row["case_info"]["case_id"]] = row
                        records[key] = list(saved.values())
                        write_json(result_path, records[key])
                        checkpoint()
                        errors += int(not row["execution_status"]["success"] or
                                      bool(row["execution_status"].get("evaluation_error")) or
                                      row["execution_status"].get("clean_control_success") is False)
                        print(f"[SAVE] {key} {row['case_info']['case_id']} "
                              f"execution={row['execution_status']['success']} "
                              f"cross_session_success={row['final_output']['attack_success']} "
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
    parser.add_argument("--clean-control", action="store_true", help="Also run a fresh trigger with original clean state")
    parser.add_argument("--run", action="store_true", help="Call models; otherwise prepare only")
    parser.add_argument("--resume", action="store_true")
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


def main():
    args = parse_args()
    manifest, subsets, baseline = select_baseline(args.baseline_dir, args.clean_control)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    with (args.output_dir / "run.lock").open("a") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise ValueError("Another process is using this experiment") from None
        path = args.output_dir / "manifest.json"
        if args.resume:
            if not path.exists() or json.loads(path.read_text()) != manifest:
                raise ValueError("Resume manifest differs: retain baseline, code, skills and clean-control setting")
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
            settings["evaluation"] = "released_plus_cross_session_state_read_business_AND_PIE_strict_v1"
            settings["session_mode"] = manifest["session_mode"]
            settings["clean_control"] = args.clean_control
            settings["simulator_cache"] = "isolated_per_case_and_phase"
            original_config = json.loads((args.baseline_dir / "run_config.json").read_text())
            for field in ("model", "endpoint_sha256"):
                if original_config.get(field) != settings[field]:
                    raise ValueError(f"Baseline {field} differs; use the same model and endpoint for comparison")
            for field in ("MAX_AGENT_TURNS", "REQUEST_TIMEOUT", "ENABLE_DEFENSE", "EVAL_REQUIRE_SKILL_UPDATE_READ"):
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


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, KeyError, OSError, ImportError, importlib.metadata.PackageNotFoundError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(2)
