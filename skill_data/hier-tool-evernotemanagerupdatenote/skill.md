## Typical user scenarios
- Editing existing notes
- Adding attachments to notes
- Correcting note information

## Tool-call workflow
1. Provide required `note_id`.
2. Provide optional `title`, `content`, or `attachments` to update.
3. Call the tool.

## Parameters
- **Required**: `note_id`
- **Optional**: `title`, `content`, `attachments`

## Parameter aliases
- note_id/note/ID
- title/subject/heading
- content/body/text
- attachments/files/documents

## Call examples
1. "Update note 'abc123' with new title 'Revised Meeting Notes'"
2. "Add attachments to note 'xyz789'"
