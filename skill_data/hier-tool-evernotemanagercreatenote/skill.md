## Typical user scenarios
- Taking meeting notes
- Saving research information
- Drafting documents with attachments

## Tool-call workflow
1. Provide required `title` and `content`.
2. Optionally add `attachments` (file paths) and `notebook_id`.
3. Call the tool.

## Parameters
- **Required**: `title`, `content`
- **Optional**: `attachments`, `notebook_id`

## Parameter aliases
- title/subject/heading
- content/body/text/details
- attachments/files/documents
- notebook_id/notebook/folder

## Call examples
1. "Create a note titled 'Meeting Notes' with content 'Discussed Q3 goals'"
2. "Save this document as a note called 'Project Brief' in notebook '12345'"
