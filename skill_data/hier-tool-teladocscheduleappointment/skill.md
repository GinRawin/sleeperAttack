## Typical user scenarios
- User needs to book a routine checkup.
- User wants to schedule a follow-up visit.
- User has new symptoms and needs an appointment.

## Tool-call workflow
1. Get doctor_id from user.
2. Get appointment date in 'YYYY-MM-DD' format.
3. Get appointment time in 'HH:mm' format.
4. Get reason for appointment.
5. Call tool with all four parameters.
6. Confirm appointment scheduling.

## Required/optional parameters
- doctor_id (required): Unique doctor identifier.
- date (required): Appointment date in 'YYYY-MM-DD'.
- time (required): Appointment time in 'HH:mm'.
- reason (required): Appointment reason.

## Parameter aliases
- doctor_id: doctor, physician, provider
- date: appointment_date, booking_date, day
- time: appointment_time, booking_time, hour
- reason: purpose, issue, concern, symptoms

## Call examples
- "Schedule with doctor DR123 on 2024-06-15 at 14:30 for routine checkup."
- "Book appointment with doctor PHY456 on June 20 at 10:00 for follow-up."
- "Make appointment with doctor DOC789 tomorrow at 15:00 for cough."
- "Schedule visit with doctor DR101 next Monday at 9:30 for allergy concerns."
