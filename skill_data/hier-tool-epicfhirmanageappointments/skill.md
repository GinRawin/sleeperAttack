## Typical user scenarios
- Listing upcoming appointments for a patient
- Creating a new visit or follow-up appointment
- Updating or deleting an existing appointment

## Tool-call workflow
1. Collect `patient_id` first.
2. Set `action` to `list`, `create`, `update`, or `delete`.
3. Provide `appointment_id` for `update` and `delete`.
4. Provide `appointment_data` for `create` and `update`, including date, time, location, and doctor_id.
5. Use `max_results` only when listing appointments.

## Parameters
- **Required**: `patient_id`, `action`
- **Conditional**: `appointment_id` for `update` and `delete`
- **Conditional**: `appointment_data` for `create` and `update`
- **Optional**: `max_results` for `list`

## Parameter aliases
- patient_id/patient ID/chart ID
- action/operation
- appointment_id/visit ID/appointment ID
- appointment_data/appointment details/visit details
- max_results/limit/result count

## Call examples
1. "List up to 5 appointments for patient pt-44521."
2. "Create an appointment for patient pt-44521 on 2026-04-18 at 09:30 with doctor dr-778 at Main Clinic."
3. "Delete appointment appt-90012 for patient pt-44521."
