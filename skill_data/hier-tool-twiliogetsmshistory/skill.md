## Typical scenarios
- Reviewing sent messages
- Checking delivery history
- Auditing SMS communications

## Tool-call workflow
1. Set filters (optional): to_phone_number, datetime_range, keywords
2. Set max_results (optional)
3. Call tool with parameters

## Parameters
**Required but can be empty:** to_phone_number, datetime_range, keywords
**Optional:** max_results

## Parameter aliases
to_phone_number: recipient, to number
datetime_range: time period, date range
keywords: search terms, phrases
max_results: limit, number of messages

## Call examples
1. "Get SMS sent to +12345678901"
2. "Find sent messages from last week with 'reminder'"
3. "Show last 20 sent SMS"
