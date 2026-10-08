## Typical scenarios
- Review past trading activity
- Audit order execution
- Analyze trading patterns

## Workflow
1. Get date_range and pair from user
2. Call BinanceGetOrderHistory

## Parameters
- **date_range (required)**: Start and end dates as ['YYYY-MM-DD', 'YYYY-MM-DD']
- **pair (required)**: BTCUSD, ETHUSD, etc. (or empty for all pairs)

## Parameter aliases
- date_range: time period, date range, timeframe
- pair: trading pair, currency pair, market

## Call examples
1. "Show my BTCUSD orders from last week"
2. "Get all orders between Jan 1 and Jan 31"
3. "What ETH trades did I make yesterday?"
