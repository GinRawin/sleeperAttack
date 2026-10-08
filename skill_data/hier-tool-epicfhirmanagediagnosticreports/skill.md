## Typical user scenarios
- Listing diagnostic reports for a patient
- Creating or updating a lab or imaging report
- Deleting an outdated report entry

## Tool-call workflow
1. Collect the patient's `patient_id`.
2. Set `action` to `list`, `create`, `update`, or `delete`.
3. Add `report_id` for update or delete.
4. Add `report_data` for create or update.
5. Add `max_results` when listing and the user wants a limit.

## Parameters
- **Required**: `patient_id`, `action`
- **Optional**: `report_id`, `report_data`, `max_results`

## Parameter aliases
- patient_id/patient ID/MRN
- action/list or create or update or delete
- report_id/report ID/diagnostic report identifier
- report_data/report payload/report details
- max_results/result limit

## Call examples
1. "List diagnostic reports for patient PAT-441."
2. "Update report RPT-100 for patient PAT-441 with new interpretation text."
3. "Delete diagnostic report LAB-22 for patient patient-123."
