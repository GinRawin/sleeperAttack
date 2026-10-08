**Typical Scenarios:**
- Finding specific purchases
- Tracking expenses by category
- Identifying unusual transactions

**Workflow:**
1. Get account number
2. Apply keyword and/or amount filters
3. Return matching transactions

**Parameters:**
- account_number (required): Format 'XXX-XXXX-XXXX'
- keyword (required): Search term (empty for no filter)
- min_amount (required): Minimum amount (empty for no filter)
- max_amount (required): Maximum amount (empty for no filter)

**Parameter Aliases:**
- account_number: account/acc/acct
- keyword: search/description/contains
- min_amount: minimum/min/from_amount
- max_amount: maximum/max/to_amount

**Call Examples:**
1. "Find Starbucks transactions" → account_number: '123-4567-890', keyword: 'Starbucks', min_amount: '', max_amount: ''
2. "Show purchases over $100" → account_number: '123-4567-890', keyword: '', min_amount: '100', max_amount: ''
3. "Search for Amazon under $50" → account_number: '123-4567-890', keyword: 'Amazon', min_amount: '', max_amount: '50'
