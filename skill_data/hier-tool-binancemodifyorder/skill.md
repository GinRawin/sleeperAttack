## Typical scenarios
- Adjust order price based on market changes
- Change order quantity
- Update order parameters before execution

## Workflow
1. Get order_id, new_price, and new_quantity from user
2. Call BinanceModifyOrder

## Parameters
- **order_id (required)**: Unique order identifier
- **new_price (required)**: Updated price
- **new_quantity (required)**: Updated quantity

## Parameter aliases
- order_id: order ID, order number
- new_price: updated price, new rate
- new_quantity: updated amount, new size

## Call examples
1. "Change order XYZ789 price to $45000"
2. "Update order ABC123 quantity to 0.75"
3. "Modify order DEF456 to price $3000 and quantity 5"
