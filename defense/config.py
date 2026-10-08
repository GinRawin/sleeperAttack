"""Configuration for Rule, Guard, and AgentDoG Defense."""

import os

try:
    import config as project_config
except Exception:
    project_config = None


def _env_flag(name: str, default: str = "false") -> bool:
    return os.getenv(name, default).strip().lower() in {"1", "true", "yes", "on"}


def _project_default(name: str, fallback: str = "") -> str:
    if project_config is None:
        return fallback
    value = getattr(project_config, name, fallback)
    return fallback if value is None else str(value)


DEFENSE_MODE = os.getenv("DEFENSE_MODE", "rule_defense").strip() or "rule_defense"
ENABLE_DEFENSE = _env_flag("ENABLE_DEFENSE", "false")
DEFENSE_RESULTS_DIR = os.getenv("DEFENSE_RESULTS_DIR", "outputs/defense_eval")
MAX_EVENT_LOG = int(os.getenv("DEFENSE_MAX_EVENT_LOG", "120"))
LLAMA_GUARD_MODEL = os.getenv("LLAMA_GUARD_MODEL", "meta-llama/llama-guard-4-12b").strip()
LLAMA_GUARD_API_KEY = os.getenv(
    "LLAMA_GUARD_API_KEY",
    os.getenv("OPENROUTER_API_KEY", _project_default("OPENROUTER_API_KEY", "")),
).strip()
LLAMA_GUARD_BASE_URL = os.getenv(
    "LLAMA_GUARD_BASE_URL",
    os.getenv("OPENROUTER_BASE_URL", _project_default("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")),
).strip()
LLAMA_GUARD_TIMEOUT = float(os.getenv("LLAMA_GUARD_TIMEOUT", "30"))

AGENTDOG_MODEL = os.getenv("AGENTDOG_MODEL", "agentdog").strip()
AGENTDOG_BASE_URLS = [
    item.strip()
    for item in os.getenv("AGENTDOG_BASE_URLS", os.getenv("AGENTDOG_BASE_URL", "")).split(",")
    if item.strip()
]
AGENTDOG_API_KEY = os.getenv("AGENTDOG_API_KEY", "EMPTY").strip() or "EMPTY"
AGENTDOG_TIMEOUT = float(os.getenv("AGENTDOG_TIMEOUT", "60"))
AGENTDOG_MAX_TOKENS = int(os.getenv("AGENTDOG_MAX_TOKENS", "160"))
AGENTDOG_WRITE_MAX_TOKENS = int(os.getenv("AGENTDOG_WRITE_MAX_TOKENS", "24"))
