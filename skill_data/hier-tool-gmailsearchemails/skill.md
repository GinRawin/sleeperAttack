## Typical scenarios
- Finding emails from specific sender
- Searching for emails with keywords
- Filtering emails by date range
- Locating emails in certain folders

## Tool-call workflow
1. Set search criteria (leave empty for no filter)
2. Format date_range as JSON with start_date/end_date
3. Specify limit (default 5)
4. Call tool with parameters

## Parameters
**Required but can be empty:** keywords, folders, date_range, from_, to, labels
**Required:** limit (default 5)

## Parameter aliases
keywords: search terms, phrases
folders: locations, categories
date_range: time period, date filter
from_: sender, from address
to: recipient, to address
labels: tags, categories
limit: max results, number to return

## Call examples
1. "Search emails with 'invoice' keyword from last week"
2. "Find emails from boss@company.com in inbox"
3. "Search for important emails in sent folder"
