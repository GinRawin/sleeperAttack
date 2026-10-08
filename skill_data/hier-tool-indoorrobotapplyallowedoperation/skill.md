## Typical scenarios
- Cutting food with a grabbed knife.
- Placing a grabbed cup on a table.
- Opening a drawer with a grabbed key.

## Tool-call workflow
1. Use `IndoorRobotGetAllowedOperations` to get valid `operation_id` and required `arguments` for your `target_object_id`.
2. Call this tool with the exact IDs and argument dictionary from step 1.

## Parameters
- **target_object_id (Required)**: ID of object to operate on. Get from `FindObjects`.
- **operation_id (Required)**: ID of operation. Must come from `GetAllowedOperations`.
- **arguments (Required)**: Dictionary matching the operation's requirements from `GetAllowedOperations`.

## Parameter aliases
- target_object_id: target, object, item
- operation_id: action, task, op
- arguments: args, parameters, options

## Call examples
1. "Cut the apple with the knife."
2. "Place the book on the shelf."
3. "Open the window."
4. "Turn on the TV."
