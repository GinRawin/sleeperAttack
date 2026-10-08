## Typical scenarios
- Sending immediate SMS
- Scheduling messages for later
- Setting up recurring reminders
- Bulk messaging

## Tool-call workflow
1. Format to_phone_numbers as list in E.164
2. Write message content
3. Set scheduled_time if needed (format: YYYY-MM-DD HH:mm:ss)
4. Set is_recurring and recurrence if needed
5. Call tool with parameters

## Parameters
**Required:** to_phone_numbers, message, is_recurring
**Optional:** scheduled_time
**Required if recurring:** recurrence (RRULE format)

## Parameter aliases
to_phone_numbers: recipients, phone numbers
message: content, text, SMS
scheduled_time: send later, schedule time
is_recurring: repeat, recurring
recurrence: repeat rule, schedule pattern

## Call examples
1. "Send 'Meeting reminder' to +12345678901"
2. "Schedule SMS to team for tomorrow 9 AM"
3. "Set up daily reminder SMS at 8 AM"
4. "Send bulk SMS to client list"
