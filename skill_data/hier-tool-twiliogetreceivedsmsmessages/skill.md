## Typical scenarios
- Checking incoming messages
- Reviewing customer responses
- Monitoring SMS communications

## Tool-call workflow
1. Set filters (optional): from_phone_number, datetime_range, keywords
2. Set max_results (optional)
3. Call tool with parameters

## Parameters
**Required but can be empty:** from_phone_number, datetime_range, keywords
**Optional:** max_results

## Parameter aliases
from_phone_number: sender, from number
datetime_range: time period, date range
keywords: search terms, phrases
max_results: limit, number of messages

## Call examples
1. "Get received SMS from last 24 hours"
2. "Find messages from +12345678901 with 'urgent'"
3. "Show last 10 received messages"
