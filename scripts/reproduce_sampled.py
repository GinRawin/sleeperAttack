#!/usr/bin/env python3
"""Sample paired original benchmark slices, run them, and resume saved progress."""
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
import random
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
STRATEGIES = {
    "PIE": "proactive_information_elicitation",
    "LIP": "latent_instruction_planting",
    "PIC": "persistent_information_corruption",
}
STATES = ("session", "memory", "skill")


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    with temp.open("w", encoding="utf-8") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
    temp.replace(path)


def make_sample(fraction, seed):
    manifest = {"fraction": fraction, "seed": seed, "sampling": "paired_case_ids",
                "session_mode": "original_shared_session", "slices": []}
    subsets = {}
    for alias, strategy in STRATEGIES.items():
        by_state = {}
        hashes = {}
        for state in STATES:
            path = ROOT / "datasets" / strategy / f"{state}.json"
            content = path.read_bytes()
            data = json.loads(content)
            rows = data["cases"] if isinstance(data, dict) else data
            mapping = {row["case_id"]: row for row in rows}
            if len(mapping) != len(rows):
                raise ValueError(f"Duplicate case IDs: {path}")
            if any(len(row["turns"]) != 2 or not row.get("eval_config") for row in rows):
                raise ValueError(f"Expected two-turn original cases with eval_config: {path}")
            by_state[state] = mapping
            hashes[state] = hashlib.sha256(content).hexdigest()
        ids = sorted(by_state["session"])
        if any(set(mapping) != set(ids) for mapping in by_state.values()):
            raise ValueError(f"State IDs do not align: {strategy}")
        count = max(1, math.floor(len(ids) * fraction + 0.5))
        chosen = random.Random(f"{seed}:{strategy}").sample(ids, count)
        for state in STATES:
            key = f"{alias}/{state}"
            subsets[key] = [by_state[state][case_id] for case_id in chosen]
            manifest["slices"].append({
                "key": key, "strategy": strategy, "state": state,
                "source": f"datasets/{strategy}/{state}.json",
                "source_sha256": hashes[state], "population": len(ids),
                "sample_size": count, "case_ids": chosen,
            })
    manifest["total_instances"] = sum(item["sample_size"] for item in manifest["slices"])
    manifest["total_base_cases"] = sum(len(subsets[f"{alias}/session"]) for alias in STRATEGIES)
    return manifest, subsets


def summarize(manifest, records):
    def aggregate(keys):
        planned = sum(s["sample_size"] for s in manifest["slices"] if s["key"] in keys)
        rows = [row for key in keys for row in records.get(key, [])]
        done = len(rows)
        successes = sum(bool(row["final_output"]["attack_success"]) for row in rows)
        errors = sum(not row["execution_status"]["success"] for row in rows)
        eval_errors = sum(bool(row["execution_status"].get("evaluation_error")) for row in rows)
        return {"planned": planned, "completed": done, "pending": planned - done,
                "attack_successes": successes, "execution_failures": errors,
                "evaluation_errors": eval_errors,
                "asr_completed": successes / done if done else None,
                "asr": successes / planned if planned and done == planned else None}
    keys = [s["key"] for s in manifest["slices"]]
    return {"overall": aggregate(keys),
            "by_strategy": {alias: aggregate([key for key in keys if key.startswith(alias + "/")])
                            for alias in STRATEGIES},
            "by_slice": {key: aggregate([key]) for key in keys}}


def save_run_config(output_dir, settings, completed_instances):
    """Allow RPM tuning on resume, retaining the previous configuration as evidence."""
    settings_path = output_dir / "run_config.json"
    if settings_path.exists():
        previous = json.loads(settings_path.read_text())
        changed = [key for key in set(previous) | set(settings)
                   if key != "settings" and previous.get(key) != settings.get(key)]
        old_values = previous.get("settings", {})
        new_values = settings.get("settings", {})
        changed += ["settings." + key for key in set(old_values) | set(new_values)
                    if old_values.get(key) != new_values.get(key)]
        if changed:
            rpm_key = "LLM_REQUESTS_PER_MINUTE"
            if set(changed) != {"settings." + rpm_key} or rpm_key not in old_values or rpm_key not in new_values:
                raise ValueError("Resume configuration differs in " + ", ".join(sorted(changed)) +
                                 "; only RPM may change in an existing experiment")
            history_path = output_dir / "run_config_history.json"
            history = json.loads(history_path.read_text()) if history_path.exists() else []
            history.append({"recorded_at": datetime.now().astimezone().isoformat(),
                            "completed_instances": completed_instances,
                            "previous_config": previous, "config": settings})
            write_json(history_path, history)
            print(f"[RESUME] RPM {old_values[rpm_key]} -> {new_values[rpm_key]}; "
                  f"preserving {completed_instances} saved instances", flush=True)
    write_json(settings_path, settings)


def configure(args):
    missing = [key for key in ("F_DEEPSEEK_MODEL", "F_DEEPSEEK_BASE_URL", "F_DEEPSEEK_API_KEY")
               if not os.getenv(key, "").strip()]
    if missing:
        raise ValueError("Missing environment variables: " + ", ".join(missing))
    # Direct access for the entire benchmark process, including the rule judge's
    # optional client. Parent-shell proxy variables remain unchanged.
    for key in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "http_proxy", "https_proxy", "all_proxy"):
        os.environ.pop(key, None)
    os.environ["NO_PROXY"] = "*"
    os.environ["no_proxy"] = "*"
    for role in ("AGENT", "SIMULATOR"):
        for field in ("MODEL", "BASE_URL", "API_KEY"):
            os.environ[f"{role}_{field}"] = os.environ[f"F_DEEPSEEK_{field}"]
    values = {
        "ENABLE_DEFENSE": "false", "EVAL_REQUIRE_SKILL_UPDATE_READ": "true",
        "MAX_AGENT_TURNS": str(args.max_agent_turns), "REQUEST_TIMEOUT": str(args.timeout),
        "LLM_REQUESTS_PER_MINUTE": str(args.rpm), "LLM_MAX_IN_FLIGHT": str(args.max_in_flight),
        "LLM_429_MAX_RETRIES": str(args.retries), "LLM_RETRY_BASE_SECONDS": str(args.backoff_base),
        "LLM_RETRY_MAX_SECONDS": str(args.backoff_cap),
        "SIMULATOR_CACHE_FILE": str(args.output_dir / "simulator_cache.json"),
        "SKILL_DATA_DIR": str(ROOT / "skill_data"),
    }
    os.environ.update(values)
    # Public experiment configuration only; no key or URL is written to artifacts.
    return {"model": os.environ["F_DEEPSEEK_MODEL"],
            "network": "direct_no_proxy",
            "endpoint_sha256": hashlib.sha256(os.environ["F_DEEPSEEK_BASE_URL"].encode()).hexdigest(),
            "case_concurrency": args.concurrency, "settings": values,
            "evaluation": "released_evaluator_including_PIE_strict_replacement"}


async def execute(args, manifest, records):
    # Import after mapping the F_DEEPSEEK variables, since config is read at import.
    from src.agent_runner import AgentRunner, CaseResult
    from src.data_manager import DataManager
    from src.evaluator import Evaluator, strip_export_fields
    from src.llm_client import request_failures, request_stats
    from src.tool_manager import ToolAdapter

    runner = AgentRunner(api_key=os.environ["AGENT_API_KEY"],
                         base_url=os.environ["AGENT_BASE_URL"], model_name=os.environ["AGENT_MODEL"],
                         simulator_model=os.environ["SIMULATOR_MODEL"],
                         simulator_api_key=os.environ["SIMULATOR_API_KEY"],
                         simulator_base_url=os.environ["SIMULATOR_BASE_URL"])
    evaluator = Evaluator()
    tools = ToolAdapter()
    request_baseline = json.loads((args.output_dir / "request_stats.json").read_text()) \
        if (args.output_dir / "request_stats.json").exists() else {}
    started = 0
    new_errors = 0

    async def run_one(case):
        failures = []
        token = request_failures.set(failures)
        try:
            try:
                result = await runner.run_single_case(case, tools)
            except Exception as exc:
                result = CaseResult(case.case_id, False, [], 0, str(exc))
            if failures:
                # The original simulator can swallow exceptions into tool fallbacks.
                # Exhausted 429s are infrastructure failures, never synthetic successes.
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
            return {"experiment_info": {"model_name": os.environ["AGENT_MODEL"]},
                    "case_info": {"case_id": case.case_id, "test_case_data": case.model_dump()},
                    "execution_trajectory": [log.to_dict() for log in result.turn_logs],
                    "evaluation_results": metrics,
                    "final_output": {key: metrics[key] for key in ("attack_success", "failure_reason", "score")},
                    "execution_status": {"success": result.success, "error": result.error_message,
                                         "evaluation_error": evaluation_error, "seconds": result.total_time}}
        finally:
            request_failures.reset(token)

    def checkpoint():
        write_json(args.output_dir / "summary.json", summarize(manifest, records))
        write_json(args.output_dir / "request_stats.json",
                   {key: request_baseline.get(key, 0) + value for key, value in request_stats().items()})

    try:
        for item in manifest["slices"]:
            key = item["key"]
            result_path = args.output_dir / "results" / f"{key}.json"
            dataset_path = args.output_dir / "sampled" / f"{key}.json"
            os.environ["DATASET_FILE"] = str(dataset_path)
            cases = DataManager(str(dataset_path), str(result_path)).load_test_cases()
            saved = {row["case_info"]["case_id"]: row for row in records[key]}
            pending = [case for case in cases if case.case_id not in saved or (
                args.retry_errors and (not saved[case.case_id]["execution_status"]["success"] or
                                       saved[case.case_id]["execution_status"].get("evaluation_error")))]
            for offset in range(0, len(pending), args.concurrency):
                batch = pending[offset:offset + args.concurrency]
                if args.limit is not None:
                    batch = batch[:max(0, args.limit - started)]
                if not batch:
                    return new_errors
                started += len(batch)
                tasks = [asyncio.create_task(run_one(case)) for case in batch]
                try:
                    for completed in asyncio.as_completed(tasks):
                        row = await completed
                        case_id = row["case_info"]["case_id"]
                        saved[case_id] = row
                        records[key] = list(saved.values())
                        write_json(result_path, records[key])
                        checkpoint()
                        new_errors += int(not row["execution_status"]["success"] or
                                          bool(row["execution_status"].get("evaluation_error")))
                        print(f"[SAVE] {key} {case_id} execution={row['execution_status']['success']} "
                              f"attack_success={row['final_output']['attack_success']} "
                              f"total={sum(len(rows) for rows in records.values())}/{manifest['total_instances']}",
                              flush=True)
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
    return new_errors


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--fraction", type=float, default=0.3)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--run", action="store_true", help="Call models; otherwise only prepare samples")
    parser.add_argument("--resume", action="store_true", help="Use the same manifest and skip saved cases")
    parser.add_argument("--retry-errors", action="store_true", help="With resume, replace infrastructure/evaluation errors")
    parser.add_argument("--limit", type=int, help="Run at most this many pending instances (smoke check)")
    parser.add_argument("--concurrency", type=int, default=2)
    parser.add_argument("--rpm", type=float, default=20)
    parser.add_argument("--max-in-flight", type=int, default=2)
    parser.add_argument("--retries", type=int, default=12, help="Retries per HTTP request after 429")
    parser.add_argument("--backoff-base", type=float, default=6)
    parser.add_argument("--backoff-cap", type=float, default=120)
    parser.add_argument("--max-agent-turns", type=int, default=30)
    parser.add_argument("--timeout", type=float, default=120)
    args = parser.parse_args()
    if not 0 < args.fraction <= 1 or not math.isfinite(args.fraction):
        parser.error("fraction must be in (0, 1]")
    if min(args.concurrency, args.max_in_flight, args.max_agent_turns) < 1 or args.retries < 0:
        parser.error("Concurrency/steps must be positive; retries must be nonnegative")
    if not (0 < args.rpm < float('inf') and 0 < args.timeout < float('inf') and
            0 < args.backoff_base <= args.backoff_cap < float('inf')):
        parser.error("RPM, timeout and backoff bounds must be positive and finite")
    if args.limit is not None and args.limit < 1:
        parser.error("limit must be positive")
    if args.retry_errors and not args.resume:
        parser.error("retry-errors requires resume")
    if args.resume and args.output_dir is None:
        parser.error("resume requires output-dir")
    args.output_dir = (args.output_dir or ROOT / "outputs" /
                       ("repro_30pct_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f"))).resolve()
    return args


def main():
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    with (args.output_dir / "run.lock").open("a") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise ValueError("Another process is already using this output directory") from None
        manifest, subsets = make_sample(args.fraction, args.seed)
        manifest_path = args.output_dir / "manifest.json"
        if args.resume:
            if not manifest_path.exists() or json.loads(manifest_path.read_text()) != manifest:
                raise ValueError("Resume manifest differs: keep fraction, seed and source data unchanged")
        elif manifest_path.exists() or (args.output_dir / "results").exists():
            raise ValueError("Output already contains an experiment; use --resume or a new directory")
        write_json(manifest_path, manifest)
        records = {}
        for item in manifest["slices"]:
            key = item["key"]
            write_json(args.output_dir / "sampled" / f"{key}.json", subsets[key])
            path = args.output_dir / "results" / f"{key}.json"
            rows = json.loads(path.read_text()) if path.exists() else []
            saved_ids = [row["case_info"]["case_id"] for row in rows]
            if len(set(saved_ids)) != len(saved_ids) or set(saved_ids) - set(item["case_ids"]):
                raise ValueError(f"Duplicate or unexpected saved cases in {path}")
            records[key] = rows
            print(f"{key}: {item['sample_size']}/{item['population']}; saved={len(rows)}")
        print(f"Total: {manifest['total_instances']} instances, {manifest['total_base_cases']} base IDs")
        print(f"Output: {args.output_dir}", flush=True)
        write_json(args.output_dir / "summary.json", summarize(manifest, records))
        if not args.run:
            return 0
        settings = configure(args)
        save_run_config(args.output_dir, settings, sum(len(rows) for rows in records.values()))
        write_json(args.output_dir / "environment.json", {
            "python": sys.version, "executable": sys.executable,
            "packages": {name: importlib.metadata.version(name) for name in
                         ("openai", "openai-agents", "httpx", "pydantic", "json-repair", "tqdm")},
        })
        logging.basicConfig(level=logging.WARNING, format="%(asctime)s %(levelname)s %(message)s")
        logging.getLogger("src.llm_client").setLevel(logging.INFO)
        errors = asyncio.run(execute(args, manifest, records))
        summary = json.loads((args.output_dir / "summary.json").read_text())
        print(json.dumps(summary["overall"], ensure_ascii=False), flush=True)
        return 1 if errors else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, ImportError, importlib.metadata.PackageNotFoundError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(2)
