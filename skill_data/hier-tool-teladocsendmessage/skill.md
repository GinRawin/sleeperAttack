## Typical user scenarios
- User has follow-up questions after a consultation.
- User needs to provide additional information to their doctor.
- User wants to ask about medication side effects.

## Tool-call workflow
1. Get consultation_id from user.
2. Get message_content from user.
3. Call tool with both parameters.
4. Present doctor's response to user.

## Required/optional parameters
- consultation_id (required): Unique consultation identifier.
- message_content (required): Message text to send.

## Parameter aliases
- consultation_id: consult_id, session_id, appointment_id
- message_content: message, question, text, query

## Call examples
- "Send message to consultation CON123: 'Is this medication safe with alcohol?'"
- "Ask in consultation CON456: 'My symptoms have worsened.'"
- "Message doctor in consultation CON789 about side effects."
- "Send follow-up question in consultation CON101: 'When should I come back?'"
