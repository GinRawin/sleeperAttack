## Typical scenarios
- User wants to add funds to trade cryptocurrencies
- Funding exchange account with USD/EUR/GBP
- Preparing for upcoming trading activity

## Workflow
1. Use BinanceRetrieveAccounts to get account IDs
2. Get currency, amount, and from_account_id from user
3. Call BinanceDeposit

## Parameters
- **currency (required)**: USD, EUR, GBP, etc.
- **amount (required)**: Deposit amount
- **from_account_id (required)**: Bank account ID from RetrieveAccounts

## Parameter aliases
- currency: fiat, money type, deposit currency
- amount: deposit amount, funding amount, sum
- from_account_id: bank account, source account, account ID

## Call examples
1. "Deposit $1000 from my main bank account"
2. "Add 500 EUR to my Binance account"
3. "Fund my account with 200 GBP"
