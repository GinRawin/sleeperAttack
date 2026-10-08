## Typical user scenarios
- Opening a known patient record by ID
- Reviewing demographics, medications, allergies, or conditions
- Fetching patient details after a search step

## Tool-call workflow
1. Collect the patient's `patient_id`.
2. Call the tool once the patient identifier is confirmed.

## Parameters
- **Required**: `patient_id`

## Parameter aliases
- patient_id/patient ID/MRN/record ID

## Call examples
1. "Get EpicFHIR patient details for patient PAT-441."
2. "Open the patient record for MRN-8871."
3. "Retrieve demographics and medications for patient patient-123."
