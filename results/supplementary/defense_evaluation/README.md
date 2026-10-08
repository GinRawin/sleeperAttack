# Defense Evaluation Results

This directory contains the released 450-case defense evaluation. The sample includes 50 cases for every combination of the three attack strategies (`LIP`, `PIE`, and `PIC`) and three agent states (`session`, `memory`, and `skill`).

- `no_defense/`: runs without a defense.
- `rule_defense/`: Rule Defense runs.
- `guard_defense/`: Guard Defense runs.
- `agentdog_defense/`: AgentDoG Defense runs.
- `sample_manifest.json`: normalized case IDs with their attack strategy and agent state.
- `defense_summary.json`: overall, attack-strategy, and agent-state aggregates.
- `defense_overall.csv`, `defense_by_strategy.csv`, and `defense_by_state.csv`: tabular aggregates.
- `defense_summary.md`: paper-facing overall table.

Each result file contains 450 case-level trajectories. The case identifiers are normalized as `450_001` through `450_450`. Local paths, credentials, source identifiers, and runtime timestamps are not included.
