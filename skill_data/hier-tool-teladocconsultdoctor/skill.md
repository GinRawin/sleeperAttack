## Typical user scenarios
- User has symptoms and needs medical advice.
- User wants a second opinion on a health issue.
- User needs to discuss test results with a doctor.

## Tool-call workflow
1. Obtain doctor_id (from previous search or user input).
2. Get reason for consultation from user.
3. Call tool with both parameters.
4. Confirm consultation initiation to user.

## Required/optional parameters
- doctor_id (required): Unique doctor identifier.
- reason (required): Consultation reason (e.g., "cold symptoms", "allergy concerns").

## Parameter aliases
- doctor_id: doctor, physician, provider, doc_id
- reason: purpose, issue, concern, symptoms

## Call examples
- "Start a consultation with doctor DR123 about my cough."
- "Consult with physician PHY456 regarding allergy concerns."
- "Begin doctor appointment with ID DOC789 for fever symptoms."
- "Talk to doctor DR101 about my recent test results."
