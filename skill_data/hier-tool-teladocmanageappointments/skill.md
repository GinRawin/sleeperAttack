## Typical user scenarios
- User needs to check appointment details.
- User wants to reschedule an appointment.
- User needs to cancel an upcoming appointment.

## Tool-call workflow
1. Get appointment_id from user.
2. Determine action: 'view', 'update', or 'cancel'.
3. If 'update', get new date and time.
4. Call tool with appropriate parameters.
5. Confirm the action completion.

## Required/optional parameters
- appointment_id (required): Unique appointment identifier.
- action (required): 'view', 'update', or 'cancel'.
- date (required if action='update'): New date in 'YYYY-MM-DD' format.
- time (required if action='update'): New time in 'HH:mm' format.

## Parameter aliases
- appointment_id: appointment, booking, meeting_id
- action: operation, task, what_to_do
- date: new_date, reschedule_date, appointment_date
- time: new_time, reschedule_time, appointment_time

## Call examples
- "View appointment APPT001."
- "Update appointment APPT002 to 2024-06-15 at 14:30."
- "Cancel appointment APPT003."
- "Reschedule appointment APPT004 to June 20 at 10:00 AM."
