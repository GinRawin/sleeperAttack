## Typical scenarios
- Updating status for vacation
- Changing profile information
- Setting availability status

## Tool-call workflow
1. Set status_text and status_emoji
2. Choose presence (auto/away)
3. Format profile as JSON string
4. Call tool with parameters

## Parameters
**Required but can be empty:** status_text, status_emoji, presence, profile

## Parameter aliases
status_text: status message, current status
status_emoji: status icon, emoji
presence: availability, online status
profile: user info, personal details

## Call examples
1. "Set status to 'Out of office' with palm tree emoji"
2. "Update profile with new title and email"
3. "Set presence to away"
