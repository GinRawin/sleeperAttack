## Typical user scenarios
- User needs a new prescription for a diagnosed condition.
- User wants to refill an existing medication.
- User's doctor recommended a new medication.

## Tool-call workflow
1. Get medication_name from user.
2. Get dosage from user.
3. Get doctor_id from user.
4. Call tool with all three parameters.
5. Confirm prescription request submission.

## Required/optional parameters
- medication_name (required): Name of medication.
- dosage (required): Medication dosage.
- doctor_id (required): Doctor identifier for review.

## Parameter aliases
- medication_name: drug, medicine, prescription_name
- dosage: dose, strength, amount
- doctor_id: doctor, physician, prescribing_doctor

## Call examples
- "Request prescription for Amoxicillin 500mg from doctor DR123."
- "Ask doctor PHY456 for Lisinopril 10mg refill."
- "Request new prescription: Metformin 850mg from doctor DOC789."
- "Get refill of Atorvastatin 20mg from doctor DR101."
