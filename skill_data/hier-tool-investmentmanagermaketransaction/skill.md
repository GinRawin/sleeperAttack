**Typical Scenarios:**
- Purchasing mutual funds
- Selling investment holdings
- Rebalancing portfolio

**Workflow:**
1. Confirm account type
2. Specify buy/sell action
3. Identify investment name
4. Set transaction amount

**Parameters:**
- account (required): 'non-registered', 'TFSA', or 'RRSP'
- action (required): 'buy' or 'sell'
- name (required): Investment option name
- amount (required): USD amount

**Parameter Aliases:**
- account: account_type/type/acct
- action: transaction/order/trade
- name: investment/fund/security
- amount: value/sum/total

**Call Examples:**
1. "Buy $1000 of ABC Growth Fund" → account: 'TFSA', action: 'buy', name: 'ABC Growth Fund', amount: '1000'
2. "Sell $500 from XYZ Balanced" → account: 'non-registered', action: 'sell', name: 'XYZ Balanced Fund', amount: '500'
3. "Purchase $2000 in DEF Income" → account: 'RRSP', action: 'buy', name: 'DEF Income Fund', amount: '2000'
