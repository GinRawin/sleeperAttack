## Typical scenarios
- Updating stock quantities
- Changing product information
- Correcting item details
- Updating supplier information

## Tool-call workflow
1. Verify item exists using GetItemDetails
2. Gather updated information
3. Call tool with item_id and updated fields

## Parameters
**Required:**
- item_id: Unique item identifier
- item_name: Non-empty string (if updating)
- category: Non-empty string (if updating)
- quantity: Positive integer (if updating)
- supplier: Non-empty string (if updating)
- description: Non-empty string (if updating)

## Parameter aliases
- item_id: product_id/stock_id/item_number
- quantity: stock/amount/units

## Call examples
1. "Update item INV-123 quantity to 50"
2. "Change widget supplier to NewCorp"
3. "Update product description"
4. "Modify item category to electronics"
