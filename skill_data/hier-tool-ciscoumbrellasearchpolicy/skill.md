## Typical scenarios
- Find policies containing specific terms
- Search for whitelist/blacklist policies
- Locate policies for review or modification

## Workflow
1. Define search keyword
2. Specify policy type if filtering
3. Set result limit
4. Call tool with parameters

## Parameters
- **keyword** (required): Search keyword
- **type** (required): 'whitelist', 'blacklist', or empty for all
- **max_results** (required): Maximum results (default 10)

## Parameter aliases
keyword: search_term, query, term
type: policy_type, list_type, category
max_results: limit, count, results_limit

## Call examples
- "Search for social media policies"
- "Find whitelist policies with 'approved'"
- "Search all policies containing 'test'"
