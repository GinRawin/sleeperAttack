## Typical user scenarios
- Listing patient records for review
- Creating a new patient record
- Updating core record fields such as medications, allergies, or conditions

## Tool-call workflow
1. Collect `patient_id` first.
2. Set `action` to `list`, `create`, `update`, or `delete`.
3. Provide `record_data` for `create` and `update`, including only the fields you intend to set.
4. Use `max_results` only when listing records.
5. Confirm the intended patient before modifying any record content.

## Parameters
- **Required**: `patient_id`, `action`
- **Conditional**: `record_data` for `create` and `update`
- **Optional**: `max_results` for `list`

## Parameter aliases
- patient_id/patient ID/chart ID
- action/operation
- record_data/record details/patient data
- max_results/limit/result count

## Call examples
1. "List records for patient pt-44521."
2. "Update patient pt-44521 with a penicillin allergy."
3. "Create a record for patient pt-99871 with demographic and medication details."
