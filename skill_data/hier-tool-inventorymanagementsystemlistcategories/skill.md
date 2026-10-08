## Typical scenarios
- Setting up new inventory structure
- Browsing product categories
- Organizing inventory view

## Tool-call workflow
1. Determine pagination needs (defaults: page=1, results_per_page=10)
2. Call tool with page and results_per_page if different from defaults
3. Review returned category list

## Parameters
**Required:**
- page: Positive integer (default: 1)
- results_per_page: Positive integer (default: 10)

## Parameter aliases
- page: page_number
- results_per_page: limit/per_page/items_per_page

## Call examples
1. "List all inventory categories"
2. "Show categories page 2 with 20 items"
3. "Browse inventory categories"
4. "List product categories"
