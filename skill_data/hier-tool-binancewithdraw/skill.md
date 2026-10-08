## Typical scenarios
- Withdraw cryptocurrency to external wallet
- Cash out fiat to bank account
- Transfer funds out of exchange

## Workflow
1. Use BinanceRetrieveAccounts for bank account IDs
2. Get currency, amount, destination_address (crypto) or to_account_id (fiat) from user
3. Call BinanceWithdraw

## Parameters
- **currency (required)**: USD, BTC, ETH, etc.
- **amount (required)**: Withdrawal amount
- **destination_address (required)**: Crypto address (for crypto withdrawals)
- **to_account_id (required)**: Bank account ID (for fiat withdrawals)

## Parameter aliases
- currency: withdrawal type, asset
- amount: withdrawal amount, sum
- destination_address: wallet address, crypto address
- to_account_id: bank account, recipient account

## Call examples
1. "Withdraw 0.1 BTC to my wallet address"
2. "Send $1000 to my bank account"
3. "Withdraw 2 ETH to external wallet"
