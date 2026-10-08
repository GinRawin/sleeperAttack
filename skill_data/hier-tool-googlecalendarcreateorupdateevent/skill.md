## Typical user scenarios
- Scheduling meetings
- Creating appointments
- Updating event details
- Setting recurring events

## Tool-call workflow
1. For new events: provide `event_name`, `content`, `start_time`, `end_time`, `timezone`, `location`, `attendees`, `recurrence`.
2. For updates: provide `event_id` plus fields to change.
3. Use ISO 8601 format for dates.
4. Call the tool.

## Parameters
- **Required**: `event_id` (for updates), `event_name`, `content`, `start_time`, `end_time`, `timezone`, `location`, `attendees`, `recurrence`

## Parameter aliases
- event_id/event/ID
- event_name/title/name
- content/description/details
- start_time/start/begin
- end_time/end/finish
- timezone/tz/zone
- location/place/where
- attendees/participants/guests
- recurrence/repeat/schedule

## Call examples
1. "Create meeting 'Team Sync' tomorrow 2-3 PM UTC-5 with john@email.com"
2. "Update event 'abc123' to new time 3-4 PM"
