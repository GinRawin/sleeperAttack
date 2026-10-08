## Typical scenarios
- Adding new items to store inventory
- Launching new products

## Tool-call workflow
1. Provide product name and description
2. Set price (USD)
3. Specify inventory quantity
4. Add extra_details if needed
5. Call tool

## Parameters
- **name** (required): Product name
- **description** (required): Product description
- **price** (required): Price in USD
- **inventory** (required): Stock quantity
- **extra_details** (required): Additional product information

## Parameter aliases
name: product title, item name
price: cost, amount
inventory: stock, quantity available

## Call examples
1. "Create a new product 'Wireless Earbuds' for $99.99"
2. "Add 'Organic Coffee' to my store with 50 units in stock"
