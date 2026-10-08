"""Batch runner for the anonymous main-experiment release."""
import asyncio
import argparse
import sys
import os
from pathlib import Path
import json
import importlib
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.dont_write_bytecode = True

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root.parent))

import config
importlib.reload(config)

from src.data_manager import DataManager
from src.tool_manager import ToolAdapter
from src.agent_runner import AgentRunner
from src.evaluator import Evaluator, strip_export_fields
from config import (
    AGENT_MODEL, AGENT_API_KEY, AGENT_BASE_URL,
    SIMULATOR_MODEL, SIMULATOR_API_KEY, SIMULATOR_BASE_URL,
    MAX_CONCURRENT_CASES, TRACING_API_KEY, VERBOSE_LOGGING,
)

RESULTS_DIR = project_root / config.RESULTS_DIR
DATASET_FILE = project_root / config.DATASET_FILE
RESULTS_FILE = project_root / config.RESULTS_FILE

RESULTS_DIR.mkdir(exist_ok=True)


def _get_sample_size():
    v = os.getenv("SAMPLE_SIZE", "").strip()
    if not v:
        return None
    try:
        n = int(v)
        return n if n > 0 else None
    except ValueError:
        return None


def _get_rerun_config():
    rerun_file = os.getenv("RERUN_RESULTS_FILE", "").strip()
    rerun_dataset = os.getenv("RERUN_DATASET_FILE", "").strip()
    raw_case_ids = os.getenv("RERUN_CASE_IDS", "").strip()
    case_ids = {part.strip() for part in raw_case_ids.split(",") if part.strip()}
    return (
        Path(rerun_file) if rerun_file else None,
        case_ids,
        Path(rerun_dataset) if rerun_dataset else None,
    )


def _print_tool_results(case_result):

    return


def _normalize_legacy_cli_args(argv):
    if argv and argv[0] == "single":
        normalized = ["--single"]
        if len(argv) > 1:
            normalized.append(argv[1])
        return normalized
    return argv


def _parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Run a batch experiment on a specified dataset.")
    parser.add_argument("--dataset", help="Dataset JSON path. Relative paths are resolved from the project root.")
    parser.add_argument("--results", help="Output JSON path. Relative paths are resolved from the project root.")
    parser.add_argument("--sample-size", type=int, help="Optional sample size override.")
    parser.add_argument("--max-concurrent", type=int, help="Optional concurrency override for case execution.")
    parser.add_argument(
        "--single",
        nargs="?",
        const="",
        metavar="CASE_ID",
        help="Run a single case. If CASE_ID is omitted, the first case is used.",
    )
    return parser.parse_args(_normalize_legacy_cli_args(argv or []))


def _resolve_path(value, default):
    if not value:
        return Path(default)
    candidate = Path(value)
    if not candidate.is_absolute():
        candidate = project_root / candidate
    return candidate.resolve()


def _build_case_metrics(eval_result, defense_report=None):
    details = strip_export_fields(eval_result.details or {})
    if defense_report:
        details["defense_report"] = defense_report
    return {
        "attack_success": eval_result.attack_success,
        "failure_reason": eval_result.failure_reason,
        "score": eval_result.score,
        "asr_score": details.get("asr_score"),
        "details": details,
    }


async def main(args=None):


    args = args or _parse_args([])
    rerun_path, rerun_case_ids, rerun_dataset_file = _get_rerun_config()
    is_rerun = rerun_path is not None and len(rerun_case_ids or []) > 0
    sample_size = args.sample_size if args and args.sample_size is not None else _get_sample_size()
    max_concurrent = args.max_concurrent if args and args.max_concurrent is not None else MAX_CONCURRENT_CASES

    if is_rerun:
        effective_result_file = Path(rerun_path).resolve()
        cli_dataset = getattr(args, "dataset", None)
        dataset_source = rerun_dataset_file or cli_dataset or config.DATASET_FILE
        effective_dataset_file = _resolve_path(dataset_source, DATASET_FILE)
    else:
        effective_dataset_file = _resolve_path(getattr(args, "dataset", None), DATASET_FILE)
        if getattr(args, "results", None):
            effective_result_file = _resolve_path(args.results, RESULTS_FILE)
        else:
            effective_result_file = RESULTS_FILE

    effective_result_file.parent.mkdir(parents=True, exist_ok=True)
    os.environ["DATASET_FILE"] = str(effective_dataset_file)
    os.environ["RESULTS_FILE"] = str(effective_result_file)

    print("=== Attack Simulation Pipeline ===")
    if is_rerun:
        print("[RERUN MODE] Only running specified case(s) and writing back in place.")
    print(f"Dataset: {effective_dataset_file}")
    print(f"Results: {effective_result_file}")
    if sample_size is not None:
        print(f"Sample size: {sample_size}")
    print(f"Max concurrent: {max_concurrent}")
    if is_rerun:
        print(f"Rerun case_ids: {rerun_case_ids}")
    print()

    try:

        print("1. Initializing components...")


        data_mgr = DataManager(str(effective_dataset_file), str(effective_result_file), model_name=AGENT_MODEL, sample_size=sample_size)


        tool_mgr = ToolAdapter()


        runner = AgentRunner(
            api_key=AGENT_API_KEY,
            base_url=AGENT_BASE_URL,
            model_name=AGENT_MODEL,
            tracing_api_key=TRACING_API_KEY,
            simulator_model=SIMULATOR_MODEL,
            simulator_api_key=SIMULATOR_API_KEY,
            simulator_base_url=SIMULATOR_BASE_URL
        )

        print(f"[OK] Agent Model: {AGENT_MODEL}")
        print(f"[OK] Simulator Model: {SIMULATOR_MODEL}")


        evaluator = Evaluator()

        print("[OK] Components initialized")


        print("\n2. Loading test cases...")
        test_cases = data_mgr.load_test_cases(case_ids=rerun_case_ids if is_rerun else None)
        print(f"[OK] Loaded {len(test_cases)} test cases")

        if not test_cases:
            print("[ERROR] No test cases found. Please check your dataset file.")
            return


        print(f"\n3. Running experiments (max concurrent: {max_concurrent})...")
        case_results = await runner.run_batch(
            test_cases,
            tool_mgr,
            max_concurrent=max_concurrent,
        )
        print("[OK] Experiments completed")


        print("\n4. Evaluating results...")
        evaluation_results = []
        case_map = {tc.case_id: tc for tc in test_cases}
        eval_workers = int(os.getenv("EVAL_MAX_WORKERS", "50"))


        print("\n5. Saving results...")
        with ThreadPoolExecutor(max_workers=eval_workers) as executor:
            future_map = {}
            for case_result in case_results:
                test_case = case_map.get(case_result.case_id)
                if not test_case:
                    print(f"[WARN] No test case found for result {case_result.case_id}")
                    continue
                fut = executor.submit(evaluator.evaluate_case, test_case, case_result)
                future_map[fut] = (case_result, test_case)

            total_cases = len(future_map)
            completed_idx = 0

            for fut in as_completed(future_map):
                case_result, test_case = future_map[fut]
                completed_idx += 1
                try:
                    eval_result = fut.result()
                except Exception as e:
                    print(f"[WARN] Evaluate case {case_result.case_id} failed: {e}")
                    from src.evaluator import EvaluationResult
                    eval_result = EvaluationResult(
                        case_id=case_result.case_id,
                        attack_success=False,
                        failure_reason=f"evaluation_error: {e}",
                        score=0.0,
                        details={"evaluation_error": str(e)}
                    )

                evaluation_results.append(eval_result)


                test_case_data = {
                    "case_id": test_case.case_id,
                    "visible_tools": test_case.visible_tools,
                    "visible_skills": getattr(test_case, "visible_skills", None) or [],
                    "skill_init_updates": [
                        update.model_dump() if hasattr(update, "model_dump") else dict(update)
                        for update in (getattr(test_case, "skill_init_updates", None) or [])
                    ],
                    "case_injection": getattr(test_case, "case_injection", None),
                    "attacker_info": getattr(test_case, "attacker_info", None),
                    "harmful_goal_categories": getattr(test_case, "harmful_goal_categories", []),
                    "harmful_goal": getattr(test_case, "harmful_goal", None),
                    "harmful_tools": getattr(test_case, "harmful_tools", []),
                    "memory_init": getattr(test_case, "memory_init", None),

                    "eval_config": getattr(test_case, "eval_config", None),
                    "user_prior_knowledge": getattr(test_case, "user_prior_knowledge", None),
                    "ground_truth_params": getattr(test_case, "ground_truth_params", None),
                    "ask_user_for": getattr(test_case, "ask_user_for", None),
                    "target_tool_actions": [a.model_dump() for a in getattr(test_case, "target_tool_actions", [])],
                    "turns": [
                        {
                            "turn_id": turn.turn_id,
                            "user_input": turn.user_input,
                            "injection_config": {
                                "enabled": turn.injection_config.enabled,
                                "target_tool": turn.injection_config.target_tool,
                                "position": turn.injection_config.position,
                                "content": turn.injection_config.content
                            } if turn.injection_config else None
                        } for turn in test_case.turns
                    ]
                }


                case_metrics = _build_case_metrics(
                    eval_result,
                    defense_report=getattr(case_result, "defense_report", None),
                )


                _print_tool_results(case_result)

                if is_rerun:
                    ok = data_mgr.update_result_in_place(
                        case_result.case_id,
                        [log.to_dict() for log in case_result.turn_logs],
                        case_metrics,
                        test_case_data,
                        model_name=AGENT_MODEL
                    )
                    if not ok:
                        print(f"[WARN] update_result_in_place failed for case {case_result.case_id}")
                else:
                    data_mgr.save_result(
                        case_result.case_id,
                        [log.to_dict() for log in case_result.turn_logs],
                        case_metrics,
                        test_case_data,
                        model_name=AGENT_MODEL
                    )
                print(f"[SAVE] case {case_result.case_id} saved ({completed_idx}/{total_cases})")

        print("[OK] Results saved")


        evaluation_metrics = evaluator.calculate_metrics(evaluation_results)
        print("\n" + "="*50)
        print("EXPERIMENT SUMMARY")
        print("="*50)
        print(f"Total Cases: {evaluation_metrics['total_cases']}")
        print(f"Successful Attacks: {evaluation_metrics['successful_attacks']}")
        print(f"Attack Success Rate (ASR): {evaluation_metrics['attack_success_rate']:.3f}")
        print(f"Results saved to: {effective_result_file}")


        tool_stats = tool_mgr.get_tool_stats()
        if tool_stats:
            print(f"\nTool Usage Statistics:")
            for tool_name, count in tool_stats.items():
                print(f"  {tool_name}: {count} calls")

    except Exception as e:
        print(f"[ERROR] Error during execution: {e}")
        if VERBOSE_LOGGING:
            import traceback
            traceback.print_exc()
        sys.exit(1)


async def run_single_case(case_id: str = None, dataset_file: str = None, results_file: str = None, sample_size: int = None):


    print(f"=== Running Single Case: {case_id or 'first'} ===")

    try:

        effective_dataset_file = _resolve_path(dataset_file, DATASET_FILE)
        effective_result_file = _resolve_path(results_file, RESULTS_FILE)
        effective_result_file.parent.mkdir(parents=True, exist_ok=True)
        sample_size = sample_size if sample_size is not None else _get_sample_size()
        os.environ["DATASET_FILE"] = str(effective_dataset_file)
        os.environ["RESULTS_FILE"] = str(effective_result_file)
        data_mgr = DataManager(str(effective_dataset_file), str(effective_result_file), model_name=AGENT_MODEL, sample_size=sample_size)

        tool_mgr = ToolAdapter()
        runner = AgentRunner(
            AGENT_API_KEY,
            AGENT_BASE_URL,
            AGENT_MODEL,
            tracing_api_key=TRACING_API_KEY,
            simulator_model=SIMULATOR_MODEL,
            simulator_api_key=SIMULATOR_API_KEY,
            simulator_base_url=SIMULATOR_BASE_URL
        )
        evaluator = Evaluator()


        test_cases = data_mgr.load_test_cases()
        if not test_cases:
            print("[ERROR] No test cases found.")
            return


        if case_id:
            test_case = next((tc for tc in test_cases if tc.case_id == case_id), None)
            if not test_case:
                print(f"[ERROR] Case {case_id} not found.")
                return
        else:
            test_case = test_cases[0]

        print(f"Running case: {test_case.case_id}")


        case_result = await runner.run_single_case(test_case, tool_mgr)


        eval_result = evaluator.evaluate_case(test_case, case_result)


        print(f"\nSuccess: {case_result.success}")
        print(f"Turns: {len(case_result.turn_logs)}")
        print(f"Attack Success: {eval_result.attack_success}")

        for log in case_result.turn_logs:
            print(f"\nTurn {log.turn_id}:")
            print(f"  User: {log.user_input}")
            print(f"  Agent: {log.agent_response}")
            print(f"  Tools: {[tc['tool_name'] for tc in log.tool_calls] if log.tool_calls else []}")
            print(f"  Injection: {log.injection_applied}")


        print("\n" + "="*50)
        print("Saving results...")


        _print_tool_results(case_result)


        test_case_data = {
            "case_id": test_case.case_id,
            "visible_tools": test_case.visible_tools,
            "visible_skills": getattr(test_case, "visible_skills", None) or [],
            "case_injection": getattr(test_case, "case_injection", None),
            "attacker_info": getattr(test_case, "attacker_info", None),
            "harmful_goal_categories": getattr(test_case, "harmful_goal_categories", []),
            "harmful_goal": getattr(test_case, "harmful_goal", None),
            "harmful_tools": getattr(test_case, "harmful_tools", []),
            "memory_init": getattr(test_case, "memory_init", None),
            "eval_config": getattr(test_case, "eval_config", None),
            "user_prior_knowledge": getattr(test_case, "user_prior_knowledge", None),
            "ground_truth_params": getattr(test_case, "ground_truth_params", None),
            "ask_user_for": getattr(test_case, "ask_user_for", None),
            "target_tool_actions": [a.model_dump() for a in getattr(test_case, "target_tool_actions", [])],
            "turns": [
                {
                    "turn_id": turn.turn_id,
                    "user_input": turn.user_input,
                    "injection_config": {
                        "enabled": turn.injection_config.enabled,
                        "target_tool": turn.injection_config.target_tool,
                        "position": turn.injection_config.position,
                        "content": turn.injection_config.content
                    } if turn.injection_config else None
                } for turn in test_case.turns
            ]
        }


        case_metrics = _build_case_metrics(eval_result)

        data_mgr.save_result(
            case_result.case_id,
            [log.to_dict() for log in case_result.turn_logs],
            case_metrics,
            test_case_data,
            model_name=AGENT_MODEL
        )

        print(f"Results saved to: {effective_result_file}")
        print("="*50)

    except Exception as e:
        print(f"[ERROR] Error: {e}")
        if VERBOSE_LOGGING:
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    args = _parse_args(sys.argv[1:])
    if args.single is not None:
        case_id = args.single or None
        asyncio.run(
            run_single_case(
                case_id=case_id,
                dataset_file=args.dataset,
                results_file=args.results,
                sample_size=args.sample_size,
            )
        )
    else:
        asyncio.run(main(args))
