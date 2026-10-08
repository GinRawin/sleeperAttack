## Typical user scenarios
- Looking up a patient by name or medical record number
- Finding a patient record before opening details
- Searching with demographic or condition keywords

## Tool-call workflow
1. Collect the `search_term`.
2. Add `max_results` if the user wants a tighter limit.
3. Call the tool once the search term is clear.

## Parameters
- **Required**: `search_term`
- **Optional**: `max_results`

## Parameter aliases
- search_term/patient search/query/name or ID
- max_results/result limit/how many matches

## Call examples
1. "Search EpicFHIR patients for John Doe."
2. "Find patients matching MRN-4488 with a max of 5 results."
3. "Search patients using the term diabetes and return up to 10 matches."
