"""Runtime hooks for Rule, Guard, and AgentDoG Defense."""

from __future__ import annotations

import contextvars
import json
import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from . import config
from . import prompts


CANONICAL_DEFENSE_MODES = {"rule_defense", "guard_defense", "agentdog_defense"}
DEFENSE_MODE_ALIASES = {
    "prompt_guard": "rule_defense",
    "llama_guard": "guard_defense",
    "agentdog": "agentdog_defense",
    "agentdog_write_check": "agentdog_defense",
}
SUPPORTED_DEFENSE_MODES = CANONICAL_DEFENSE_MODES | set(DEFENSE_MODE_ALIASES)
_llama_guard_client = None
_llama_guard_client_signature: tuple[str, str] | None = None
_agentdog_clients: list[Any] = []
_agentdog_client_signature: tuple[str, str, tuple[str, ...]] | None = None
_agentdog_next_index = 0


@dataclass
class DefenseState:
    case_id: str = ""
    model_name: str = ""
    turn_id: int = 0
    current_user_input: str = ""
    reviewed_tool_outputs: int = 0
    flagged_tool_outputs: int = 0
    reviewed_actions: int = 0
    blocked_actions: int = 0
    events: List[Dict[str, Any]] = field(default_factory=list)


_state_var: contextvars.ContextVar[Optional[DefenseState]] = contextvars.ContextVar(
    "_defense_state", default=None
)


def is_enabled() -> bool:
    return config.ENABLE_DEFENSE and _mode() in CANONICAL_DEFENSE_MODES


def normalize_defense_mode(mode: str) -> str:
    normalized = (mode or "").strip().lower() or "rule_defense"
    return DEFENSE_MODE_ALIASES.get(normalized, normalized)


def _mode() -> str:
    return normalize_defense_mode(config.DEFENSE_MODE)


def begin_case(case_id: str, model_name: str, dataset_path: str) -> None:
    del dataset_path
    if not is_enabled():
        _state_var.set(None)
        return
    _state_var.set(
        DefenseState(
            case_id=case_id,
            model_name=model_name,
        )
    )


def begin_turn(turn_id: int, user_input: str, visible_tools: Optional[List[str]] = None) -> None:
    del visible_tools
    state = _state_var.get()
    if state is None:
        return
    state.turn_id = turn_id
    state.current_user_input = user_input or ""


def finish_case() -> Optional[Dict[str, Any]]:
    state = _state_var.get()
    _state_var.set(None)
    if state is None:
        return None
    return {
        "enabled": True,
        "mode": _mode(),
        "case_id": state.case_id,
        "model_name": state.model_name,
        "reviewed_tool_outputs": state.reviewed_tool_outputs,
        "flagged_tool_outputs": state.flagged_tool_outputs,
        "reviewed_actions": state.reviewed_actions,
        "blocked_actions": state.blocked_actions,
        "events": state.events[-config.MAX_EVENT_LOG :],
    }


def build_agent_instruction_suffix(visible_tools: Optional[List[str]] = None) -> str:
    del visible_tools
    if not is_enabled():
        return ""
    return "\n" + prompts.render_agent_guard_prompt(_mode()).strip() + "\n"


def evaluate_persistent_write(tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    if not is_enabled() or _mode() != "agentdog_defense":
        return {"allowed": True}
    return _review_persistent_write_with_agentdog(tool_name, arguments or {})


def _review_persistent_write_with_agentdog(tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    state = _state_var.get()
    if state is not None:
        state.reviewed_actions += 1
    payload = {
        "current_user_request": state.current_user_input if state else "",
        "tool_name": tool_name,
        "write_arguments": arguments or {},
    }
    try:
        response_text = _call_agentdog_write_check(payload)
    except Exception as exc:
        _record_event(
            kind="agentdog_defense_write_check",
            tool_name=tool_name,
            decision="guard_error_allow",
            reason=f"agentdog_defense_write_check_error: {exc}",
            payload={
                "arguments_preview": _preview_value(arguments, limit=300),
            },
        )
        return {"allowed": True, "guard_error": str(exc)}

    normalized = _normalize_llama_guard_label(response_text)
    if normalized != "unsafe":
        _record_event(
            kind="agentdog_defense_write_check",
            tool_name=tool_name,
            decision="allow",
            reason="AgentDoG Defense judged the write safe",
            payload={
                "arguments_preview": _preview_value(arguments, limit=300),
                "guard_response": _preview_value(response_text, limit=120),
            },
        )
        return {"allowed": True, "guard_response": response_text}

    if state is not None:
        state.blocked_actions += 1
    reason = _preview_value(response_text, limit=300) or "AgentDoG Defense judged the write unsafe"
    _record_event(
        kind="agentdog_defense_write_check",
        tool_name=tool_name,
        decision="block_write",
        reason=reason,
        payload={
            "arguments_preview": _preview_value(arguments, limit=300),
        },
    )
    return {
        "allowed": False,
        "blocked_by_defense": True,
        "defense_action": "block_persistent_write",
        "reason": reason,
        "message": "Persistent write was not applied.",
        "guard_response": response_text,
    }


def evaluate_tool_action(tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    del tool_name, arguments
    return {"allowed": True}


def review_tool_return(tool_name: str, tool_description: str, result: Any) -> Any:
    if not is_enabled() or _mode() not in {"guard_defense", "agentdog_defense"}:
        return result
    if _mode() == "agentdog_defense":
        return _review_tool_return_with_agentdog_guard(tool_name, tool_description, result)
    return _review_tool_return_with_llama_guard(tool_name, tool_description, result)


def _review_tool_return_with_llama_guard(tool_name: str, tool_description: str, result: Any) -> Any:
    return _review_tool_return_with_label_guard(
        guard_name="guard_defense",
        call_fn=_call_llama_guard_tool_return,
        tool_name=tool_name,
        tool_description=tool_description,
        result=result,
    )


def _review_tool_return_with_agentdog_guard(tool_name: str, tool_description: str, result: Any) -> Any:
    return _review_tool_return_with_label_guard(
        guard_name="agentdog_defense",
        call_fn=_call_agentdog_tool_return,
        tool_name=tool_name,
        tool_description=tool_description,
        result=result,
    )


def _review_tool_return_with_label_guard(
    guard_name: str,
    call_fn,
    tool_name: str,
    tool_description: str,
    result: Any,
) -> Any:
    if result is None:
        return result

    state = _state_var.get()
    user_input = state.current_user_input if state else ""
    payload = {
        "current_user_request": user_input,
        "tool_name": tool_name,
        "tool_description": tool_description or "",
        "tool_result": result,
    }
    try:
        response_text = call_fn(payload)
    except Exception as exc:
        _record_event(
            kind=f"{guard_name}_tool_return",
            tool_name=tool_name,
            decision="guard_error_allow",
            reason=f"{guard_name}_error: {exc}",
            payload={
                "tool_description": (tool_description or "")[:300],
                "result_preview": _preview_value(result, limit=300),
            },
        )
        return result

    normalized = _normalize_llama_guard_label(response_text)
    if state is not None:
        state.reviewed_tool_outputs += 1
    if normalized != "unsafe":
        return result

    annotated = _annotate_tool_result_warning(result, tool_name, f"{guard_name} flagged return content")
    _record_event(
        kind=f"{guard_name}_tool_return",
        tool_name=tool_name,
        decision="warn_tool_result",
        reason=f"{guard_name} flagged return content",
        payload={
            "tool_description": (tool_description or "")[:300],
            "result_preview": _preview_value(result, limit=300),
        },
    )
    if state is not None:
        state.flagged_tool_outputs += 1
    return annotated


def _call_llama_guard_tool_return(payload: Dict[str, Any]) -> str:
    client = _get_llama_guard_client()
    user_prompt = (
        "Review the returned tool content.\n"
        f"{json.dumps(payload, ensure_ascii=False, indent=2)}\n"
    )
    response = client.chat.completions.create(
        model=config.LLAMA_GUARD_MODEL,
        messages=[
            {"role": "system", "content": prompts.GUARD_DEFENSE_TOOL_RETURN_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.0,
    )
    return str(response.choices[0].message.content or "").strip()


def _call_agentdog_tool_return(payload: Dict[str, Any]) -> str:
    client = _get_agentdog_client()
    user_prompt = (
        "Review the returned tool content.\n"
        f"{json.dumps(payload, ensure_ascii=False, indent=2)}\n"
    )
    response = client.chat.completions.create(
        model=config.AGENTDOG_MODEL,
        messages=[
            {"role": "system", "content": prompts.GUARD_DEFENSE_TOOL_RETURN_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.0,
        max_tokens=config.AGENTDOG_MAX_TOKENS,
    )
    return str(response.choices[0].message.content or "").strip()


def _call_agentdog_write_check(payload: Dict[str, Any]) -> str:
    client = _get_agentdog_client()
    user_prompt = (
        "Review the proposed persistent write.\n"
        f"{json.dumps(payload, ensure_ascii=False, indent=2)}\n"
    )
    response = client.chat.completions.create(
        model=config.AGENTDOG_MODEL,
        messages=[
            {"role": "system", "content": prompts.AGENTDOG_DEFENSE_WRITE_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.0,
        max_tokens=config.AGENTDOG_WRITE_MAX_TOKENS,
    )
    return str(response.choices[0].message.content or "").strip()


def _normalize_llama_guard_label(content: str) -> str:
    text = (content or "").strip()
    if not text:
        return "safe"

    first_line = text.splitlines()[0].strip().lower()
    if first_line in {"safe", "unsafe"}:
        return first_line

    lower = text.lower()
    unsafe_markers = (
        "unsafe",
        "malicious",
        "should not be trusted",
        "not be trusted",
        "not trusted",
        "do not trust",
    )
    if any(marker in lower for marker in unsafe_markers):
        return "unsafe"
    if "safe" in lower:
        return "safe"
    return "safe"


def _get_llama_guard_client():
    global _llama_guard_client
    global _llama_guard_client_signature

    api_key = config.LLAMA_GUARD_API_KEY or os.getenv("LLAMA_GUARD_API_KEY", "") or "EMPTY"
    base_url = config.LLAMA_GUARD_BASE_URL or os.getenv("LLAMA_GUARD_BASE_URL", "")
    signature = (api_key, base_url)

    if _llama_guard_client is not None and signature == _llama_guard_client_signature:
        return _llama_guard_client

    from openai import OpenAI

    client_kwargs: Dict[str, Any] = {"timeout": config.LLAMA_GUARD_TIMEOUT, "api_key": api_key}
    if base_url:
        client_kwargs["base_url"] = base_url

    _llama_guard_client = OpenAI(**client_kwargs)
    _llama_guard_client_signature = signature
    return _llama_guard_client


def _get_agentdog_client():
    global _agentdog_clients
    global _agentdog_client_signature
    global _agentdog_next_index

    base_urls = tuple(config.AGENTDOG_BASE_URLS)
    if not base_urls:
        raise RuntimeError("AGENTDOG_BASE_URL or AGENTDOG_BASE_URLS must be set for DEFENSE_MODE=agentdog_defense")
    signature = (config.AGENTDOG_API_KEY, config.AGENTDOG_MODEL, base_urls)
    if _agentdog_clients and signature == _agentdog_client_signature:
        client = _agentdog_clients[_agentdog_next_index % len(_agentdog_clients)]
        _agentdog_next_index += 1
        return client

    from openai import OpenAI

    _agentdog_clients = [
        OpenAI(
            api_key=config.AGENTDOG_API_KEY or "EMPTY",
            base_url=base_url,
            timeout=config.AGENTDOG_TIMEOUT,
        )
        for base_url in base_urls
    ]
    _agentdog_client_signature = signature
    _agentdog_next_index = 1
    return _agentdog_clients[0]


def _record_event(kind: str, tool_name: str, decision: str, reason: str, payload: Optional[Dict[str, Any]] = None) -> None:
    state = _state_var.get()
    if state is None:
        return
    state.events.append(
        {
            "turn_id": state.turn_id,
            "kind": kind,
            "tool_name": tool_name,
            "decision": decision,
            "reason": reason,
            "payload_preview": _preview_value(payload or {}, limit=400),
        }
    )
    if len(state.events) > config.MAX_EVENT_LOG:
        state.events = state.events[-config.MAX_EVENT_LOG :]


def _preview_value(value: Any, limit: int = 400) -> str:
    try:
        text = json.dumps(value, ensure_ascii=False)
    except Exception:
        text = repr(value)
    if len(text) > limit:
        return text[: limit - 3] + "..."
    return text


def _annotate_tool_result_warning(result: Any, tool_name: str, reason: str) -> Any:
    warning = prompts.TOOL_RESULT_WARNING_MESSAGE
    if isinstance(result, dict):
        result["guard_status"] = "warning"
        result["guard_warning"] = warning
        result["guard_reason"] = reason
        result["guard_source_tool"] = tool_name
        return result
    return {
        "data": result,
        "guard_status": "warning",
        "guard_warning": warning,
        "guard_reason": reason,
        "guard_source_tool": tool_name,
    }
