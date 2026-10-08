## Typical user scenarios
- Modifying task details
- Changing due dates
- Updating priorities
- Marking tasks complete

## Tool-call workflow
1. Provide required `task_id` and fields to update.
2. Call the tool.

## Parameters
- **Required**: `task_id`, `task_name`, `description`, `due_date`, `priority`, `status`

## Parameter aliases
- task_id/task/ID
- task_name/task/title/name
- description/details/notes
- due_date/due/by/deadline
- priority/importance (1=highest, 4=lowest)
- status/state/progress ('in progress' or 'completed')

## Call examples
1. "Update task 'abc123' to priority 1 and due tomorrow"
2. "Mark task 'xyz789' as completed"
