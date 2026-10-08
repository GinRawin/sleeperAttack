## Typical scenarios
- Looking for specific products
- Filtering inventory by category
- Finding items for restocking

## Tool-call workflow
1. Determine search criteria (keyword, category, or both)
2. Set pagination if needed (defaults: page=1, results_per_page=10)
3. Call tool with search parameters

## Parameters
**Required:**
- keyword: Non-empty string (if provided)
- category: Non-empty string (if provided)
- page: Positive integer (default: 1)
- results_per_page: Positive integer (default: 10)

## Parameter aliases
- keyword: search_term/product_name
- category: type/group/classification

## Call examples
1. "Search for 'widget' in inventory"
2. "Find electronics category items"
3. "Search office supplies on page 3"
4. "Look for chairs with 25 per page"
