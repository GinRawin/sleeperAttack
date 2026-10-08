**Typical Scenarios:**
- Moving funds to checking
- Cashing out balance
- Transferring to savings

**Workflow:**
1. Confirm withdrawal amount
2. Specify destination bank account
3. Execute transfer

**Parameters:**
- amount (required): Positive number
- account_id (required): Linked bank account identifier

**Parameter Aliases:**
- amount: funds/money/value
- account_id: bank_account/destination/account

**Call Examples:**
1. "Withdraw $100 to my checking" → amount: '100', account_id: 'CHK123'
2. "Transfer $250 to savings" → amount: '250', account_id: 'SAV456'
3. "Cash out $50" → amount: '50', account_id: 'CHK789'
