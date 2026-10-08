**Typical Scenarios:**
- Purchasing shares
- Selling stock positions
- Setting limit orders

**Workflow:**
1. Confirm account type
2. Specify buy/sell action
3. Choose order type
4. Identify stock ticker
5. Set quantity and price limit

**Parameters:**
- account (required): 'self-directed TFSA' or 'self-directed non-registered'
- action (required): 'buy' or 'sell'
- order_type (required): 'limit_order' or 'market_order'
- ticker (required): Stock symbol
- quantity (required): Number of shares
- price_limit (required): Price for limit orders

**Parameter Aliases:**
- account: account_type/type/acct
- action: transaction/side
- order_type: order/type
- ticker: symbol/stock
- quantity: shares/amount/number
- price_limit: price/limit/target

**Call Examples:**
1. "Buy 10 shares of AAPL at market" → account: 'self-directed TFSA', action: 'buy', order_type: 'market_order', ticker: 'AAPL', quantity: '10', price_limit: ''
2. "Sell 5 MSFT with limit $400" → account: 'self-directed non-registered', action: 'sell', order_type: 'limit_order', ticker: 'MSFT', quantity: '5', price_limit: '400'
3. "Purchase 20 GOOGL limit $150" → account: 'self-directed TFSA', action: 'buy', order_type: 'limit_order', ticker: 'GOOGL', quantity: '20', price_limit: '150'
