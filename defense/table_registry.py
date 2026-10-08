"""Released dataset aliases for the defense experiments."""

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List


@dataclass(frozen=True)
class TableSpec:
    key: str
    dataset_path: str
    description: str


PROJECT_ROOT = Path(__file__).resolve().parent.parent

CANONICAL_TABLES: Dict[str, TableSpec] = {
    "table1_single": TableSpec(
        key="table1_single",
        dataset_path="datasets/latent_instruction_planting/single.json",
        description="Latent Instruction Planting (LIP) single-turn baseline.",
    ),
    "table1_session": TableSpec(
        key="table1_session",
        dataset_path="datasets/latent_instruction_planting/session.json",
        description="Latent Instruction Planting (LIP) with session state.",
    ),
    "table1_skill": TableSpec(
        key="table1_skill",
        dataset_path="datasets/latent_instruction_planting/skill.json",
        description="Latent Instruction Planting (LIP) with skill state.",
    ),
    "table1_memory": TableSpec(
        key="table1_memory",
        dataset_path="datasets/latent_instruction_planting/memory.json",
        description="Latent Instruction Planting (LIP) with memory state.",
    ),
    "table2_single": TableSpec(
        key="table2_single",
        dataset_path="datasets/proactive_information_elicitation/single.json",
        description="Proactive Information Elicitation (PIE) single-turn baseline.",
    ),
    "table2_session": TableSpec(
        key="table2_session",
        dataset_path="datasets/proactive_information_elicitation/session.json",
        description="Proactive Information Elicitation (PIE) with session state.",
    ),
    "table2_skill": TableSpec(
        key="table2_skill",
        dataset_path="datasets/proactive_information_elicitation/skill.json",
        description="Proactive Information Elicitation (PIE) with skill state.",
    ),
    "table2_memory": TableSpec(
        key="table2_memory",
        dataset_path="datasets/proactive_information_elicitation/memory.json",
        description="Proactive Information Elicitation (PIE) with memory state.",
    ),
    "table3_single": TableSpec(
        key="table3_single",
        dataset_path="datasets/persistent_information_corruption/single.json",
        description="Persistent Information Corruption (PIC) single-turn baseline.",
    ),
    "table3_session": TableSpec(
        key="table3_session",
        dataset_path="datasets/persistent_information_corruption/session.json",
        description="Persistent Information Corruption (PIC) with session state.",
    ),
    "table3_skill": TableSpec(
        key="table3_skill",
        dataset_path="datasets/persistent_information_corruption/skill.json",
        description="Persistent Information Corruption (PIC) with skill state.",
    ),
    "table3_memory": TableSpec(
        key="table3_memory",
        dataset_path="datasets/persistent_information_corruption/memory.json",
        description="Persistent Information Corruption (PIC) with memory state.",
    ),
}

ALIASES: Dict[str, str] = {
    "latent_instruction_planting_single": "table1_single",
    "latent_instruction_planting_session": "table1_session",
    "latent_instruction_planting_skill": "table1_skill",
    "latent_instruction_planting_memory": "table1_memory",
    "proactive_information_elicitation_single": "table2_single",
    "proactive_information_elicitation_session": "table2_session",
    "proactive_information_elicitation_skill": "table2_skill",
    "proactive_information_elicitation_memory": "table2_memory",
    "persistent_information_corruption_single": "table3_single",
    "persistent_information_corruption_session": "table3_session",
    "persistent_information_corruption_skill": "table3_skill",
    "persistent_information_corruption_memory": "table3_memory",
}


def list_tables() -> List[TableSpec]:
    return [CANONICAL_TABLES[k] for k in sorted(CANONICAL_TABLES)]


def resolve_table(name: str) -> TableSpec:
    key = (name or "").strip()
    if key in CANONICAL_TABLES:
        return CANONICAL_TABLES[key]
    if key in ALIASES:
        return CANONICAL_TABLES[ALIASES[key]]

    candidate = Path(key)
    if not candidate.is_absolute():
        candidate = PROJECT_ROOT / candidate
    if candidate.exists():
        return TableSpec(
            key=candidate.stem,
            dataset_path=str(candidate.relative_to(PROJECT_ROOT)),
            description="Custom dataset path supplied by the user.",
        )
    raise KeyError(f"Unknown table alias or dataset path: {name}")


def resolve_tables(names: Iterable[str]) -> List[TableSpec]:
    return [resolve_table(name) for name in names]
