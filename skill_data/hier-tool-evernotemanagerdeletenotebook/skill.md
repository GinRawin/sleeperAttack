## Typical user scenarios
- Removing completed project notebooks
- Consolidating notebook categories
- Deleting empty or unused notebooks

## Tool-call workflow
1. Confirm deletion with user (notebook must be empty).
2. Provide required `notebook_id`.
3. Call the tool.

## Parameters
- **Required**: `notebook_id`

## Parameter aliases
- notebook_id/notebook/folder/ID

## Call examples
1. "Delete notebook 'def456'"
2. "Remove the folder with ID 'folder-789'"
