## Typical user scenarios
- Finding specific tasks
- Filtering by priority
- Searching completed items
- Locating overdue tasks

## Tool-call workflow
1. Provide `keywords`, `due_date` (YYYY-MM-DD), `priority` (1-4), `status` ('in progress' or 'completed'), and `max_results`.
2. Call the tool.

## Parameters
- **Required**: `keywords`, `due_date`, `priority`, `status`, `max_results`

## Parameter aliases
- keywords/search/terms
- due_date/due/by
- priority/importance (1=highest, 4=lowest)
- status/state/progress
- max_results/limit/count

## Call examples
1. "Find tasks with 'meeting' due this week priority 1-2"
2. "Search completed tasks about 'project'"
