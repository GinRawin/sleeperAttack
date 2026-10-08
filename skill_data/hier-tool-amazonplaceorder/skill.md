## Typical scenarios
- Finalizing purchase after cart review
- Buying all cart items at once

## Tool-call workflow
1. Verify cart contents
2. Provide shipping address
3. Provide payment method
4. Call tool (empties cart after order)

## Parameters
- **shipping_address** (required): Object with name, phone_number, address
- **payment_method** (required): Object with card_number, expiry_date, CVV

## Parameter aliases
shipping_address: delivery address, ship to
payment_method: payment details, card info

## Call examples
1. "Place my Amazon order with my saved address and Visa card"
2. "Checkout my cart with new shipping details"
