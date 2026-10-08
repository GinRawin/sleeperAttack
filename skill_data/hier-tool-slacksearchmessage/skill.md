## Typical scenarios
- Finding past discussions
- Locating specific information
- Searching for file references

## Tool-call workflow
1. Enter search query
2. Specify channel/user to search within (optional)
3. Set sender filter (optional)
4. Set max_results (default 10)
5. Call tool with parameters

## Parameters
**Required:** query
**Required but can be empty:** in0, from_0
**Required:** max_results (default 10)

## Parameter aliases
query: search term, keyword, phrase
in0: within, in channel/user
from_0: from user, sender
max_results: limit, number of results

## Call examples
1. "Search for 'deadline' in #project"
2. "Find messages from @boss about budget"
3. "Search all messages for 'meeting notes', max 20"
