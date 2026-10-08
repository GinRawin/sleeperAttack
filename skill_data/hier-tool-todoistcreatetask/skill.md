## Typical user scenarios
- Adding to-do items
- Creating project tasks
- Setting reminders for activities

## Tool-call workflow
1. Provide required `task_name`, `description`, `due_date` (YYYY-MM-DD), and `priority` (1-4).
2. Call the tool.

## Parameters
- **Required**: `task_name`, `description`, `due_date`, `priority`

## Parameter aliases
- task_name/task/title/name
- description/details/notes
- due_date/due/by/deadline
- priority/importance/urgency (1=highest, 4=lowest)

## Call examples
1. "Create task 'Buy groceries' due tomorrow priority 2"
2. "Add 'Finish report' due Friday with description 'Q4 analysis' priority 1"
