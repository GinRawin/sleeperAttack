## Typical user scenarios
- Listing existing clinical documents for a patient
- Creating a new note, summary, or other clinical document
- Updating or deleting a specific document by ID

## Tool-call workflow
1. Collect `patient_id` first.
2. Set `action` to `list`, `create`, `update`, or `delete`.
3. Provide `document_id` for `update` and `delete`.
4. Provide `document_data` for `create` and `update`, typically including type, date, summary, and details.
5. Use `max_results` only when listing documents.

## Parameters
- **Required**: `patient_id`, `action`
- **Conditional**: `document_id` for `update` and `delete`
- **Conditional**: `document_data` for `create` and `update`
- **Optional**: `max_results` for `list`

## Parameter aliases
- patient_id/patient ID/chart ID
- action/operation
- document_id/document ID/note ID
- document_data/document details/clinical note data
- max_results/limit/result count

## Call examples
1. "List 10 clinical documents for patient pt-44521."
2. "Create a progress note for patient pt-44521 dated 2026-04-12."
3. "Delete document doc-77110 for patient pt-44521."
