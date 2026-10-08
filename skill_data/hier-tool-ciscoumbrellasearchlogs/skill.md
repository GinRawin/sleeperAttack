## Typical scenarios
- Find logs related to specific incidents
- Search for blocked/allowed events
- Investigate security events within date ranges

## Workflow
1. Define search criteria
2. Set date range if needed
3. Specify event type if filtering
4. Call tool with parameters

## Parameters
- **keyword** (required): Search keyword
- **start_date** (required): Start date (YYYY-MM-DD)
- **end_date** (required): End date (YYYY-MM-DD)
- **event_type** (required): 'allowed' or 'blocked'
- **max_results** (required): Maximum results (default 10)

## Parameter aliases
keyword: search_term, query, term
event_type: type, event, status
max_results: limit, count, results_limit

## Call examples
- "Search logs for phishing attempts last week"
- "Find blocked events for facebook.com"
- "Search allowed traffic for March"
