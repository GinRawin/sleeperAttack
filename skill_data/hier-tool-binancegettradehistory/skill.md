## Typical scenarios
- Review completed trades
- Calculate profit/loss
- Trade performance analysis

## Workflow
1. Get date_range and pair from user
2. Call BinanceGetTradeHistory

## Parameters
- **date_range (required)**: Start and end dates as ['YYYY-MM-DD', 'YYYY-MM-DD']
- **pair (required)**: BTCUSD, ETHUSD, etc.

## Parameter aliases
- date_range: time period, date range, timeframe
- pair: trading pair, currency pair, market

## Call examples
1. "Show my BTCUSD trades from last month"
2. "Get all executed trades yesterday"
3. "What ETH trades completed this week?"
