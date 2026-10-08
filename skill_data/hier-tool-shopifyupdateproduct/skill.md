## Typical scenarios
- Modifying product details
- Updating prices or inventory

## Tool-call workflow
1. Identify product_id
2. Update name, description, price, inventory, extra_details
3. Call tool

## Parameters
- **product_id** (required): Product identifier
- **name** (required): New product name
- **description** (required): New product description
- **price** (required): New price in USD
- **inventory** (required): New inventory quantity
- **extra_details** (required): New extra details

## Parameter aliases
product_id: item ID
name: product title
price: new cost
inventory: new stock

## Call examples
1. "Update product PROD123 price to $79.99"
2. "Change inventory for headphones to 150 units"
