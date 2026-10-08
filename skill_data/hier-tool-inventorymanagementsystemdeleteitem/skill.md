## Typical scenarios
- Discontinuing product
- Removing obsolete stock
- Correcting inventory errors

## Tool-call workflow
1. Verify item exists using GetItemDetails or SearchItems
2. Confirm deletion is intended
3. Call tool with item_id

## Parameters
**Required:**
- item_id: Unique item identifier

## Parameter aliases
- item_id: product_id/stock_id/item_number

## Call examples
1. "Delete item ID INV-789"
2. "Remove obsolete product from inventory"
3. "Delete discontinued item"
4. "Remove item ABC123"
