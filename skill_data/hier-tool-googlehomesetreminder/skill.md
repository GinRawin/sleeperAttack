## Typical user scenarios
- Setting medication reminders
- Creating appointment alerts
- Scheduling task notifications

## Tool-call workflow
1. Determine reminder text and time
2. Call GoogleHomeSetReminder
3. Confirm creation

## Required parameters
- **reminder_text**: Reminder content (e.g., "Take medication")
- **date_time**: Reminder time in YYYY-MM-DD HH:MM format

## Parameter aliases
- reminder_text: text, message, note
- date_time: time, when, schedule

## Call examples
1. "Remind me to call mom at 3 PM"
2. "Set reminder for meeting tomorrow at 10 AM"
3. "Create reminder to water plants at 8 AM daily"
