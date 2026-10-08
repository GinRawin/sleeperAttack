"""Diagnostic snapshots for the otherwise unchanged cross-session benchmark."""
from . import virtual_tools, skill_registry


def snapshot():
    return {"memory": virtual_tools.export_memory_state(),
            "skills": skill_registry.get_registry().export_state()}
