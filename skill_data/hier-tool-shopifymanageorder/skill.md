## Typical scenarios
- Modifying order details
- Processing order fulfillment
- Handling cancellations or refunds

## Tool-call workflow
1. Identify order_id
2. Specify action: 'update', 'fulfill', 'cancel', or 'refund'
3. For 'update': provide items, total_price, shipping_details
4. Call tool

## Parameters
- **order_id** (required): Order identifier
- **action** (required): 'update', 'fulfill', 'cancel', or 'refund'
- **items** (required for 'update'): Array of objects with product_id, quantity, subtotal
- **total_price** (required for 'update'): New total in USD
- **shipping_details** (required for 'update'): Object with shipping_address, shipping_method, shipping_date

## Parameter aliases
action: operation, task
order_id: order number

## Call examples
1. "Update order ORD123 with new shipping address"
2. "Fulfill order ORD456"
3. "Cancel order ORD789"
