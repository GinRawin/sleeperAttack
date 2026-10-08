## Typical scenarios
- Buy cryptocurrency with limit or market order
- Sell cryptocurrency holdings
- Execute trading strategy

## Workflow
1. Get pair, order_type, side, quantity, and price (if limit order) from user
2. Call BinancePlaceOrder

## Parameters
- **pair (required)**: BTCUSD, ETHUSD, etc.
- **order_type (required)**: limit or market
- **side (required)**: buy or sell
- **quantity (required)**: Trade amount
- **price (optional)**: Required for limit orders

## Parameter aliases
- pair: trading pair, market
- order_type: order type, limit/market
- side: buy/sell, direction
- quantity: amount, size, volume
- price: rate, limit price

## Call examples
1. "Buy 0.1 BTC at $45000 limit"
2. "Sell 5 ETH market order"
3. "Place limit buy for 0.5 BTC at $44000"
