## Typical scenarios
- Saving items for later purchase
- Removing unwanted items from wishlist
- Reviewing saved items

## Tool-call workflow
1. Determine action: add, remove, or view
2. For add/remove: provide product_id
3. Call tool

## Parameters
- **action** (required): 'add', 'remove', or 'view'
- **product_id** (required for add/remove): Product identifier

## Parameter aliases
action: operation, task, function
product_id: item ID, ASIN

## Call examples
1. "Add product B08N5WRWNW to my wishlist"
2. "Remove the headphones from my wishlist"
3. "Show my wishlist items"
