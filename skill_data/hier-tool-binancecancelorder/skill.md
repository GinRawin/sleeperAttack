## Typical scenarios
- User wants to cancel a pending limit order
- Market conditions changed, making order undesirable
- Order was placed with incorrect parameters

## Workflow
1. Get order ID from user
2. Call BinanceCancelOrder with order_id

## Parameters
- **order_id (required)**: Unique order identifier

## Parameter aliases
- order_id: order ID, order number, transaction ID

## Call examples
1. "Cancel order ABC123"
2. "I need to cancel my pending Bitcoin order"
3. "Stop order DEF456"
