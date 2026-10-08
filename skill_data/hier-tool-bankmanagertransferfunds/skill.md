**Typical Scenarios:**
- Moving money to savings
- Paying credit card from checking
- Transferring between joint accounts

**Workflow:**
1. Identify source and destination accounts
2. Confirm transfer amount
3. Execute transfer

**Parameters:**
- from_account_number (required): Format 'XXX-XXXX-XXXX'
- to_account_number (required): Format 'XXX-XXXX-XXXX'
- amount (required): Positive number

**Parameter Aliases:**
- from_account_number: source/from/transfer_from
- to_account_number: destination/to/transfer_to
- amount: transfer/sum/total

**Call Examples:**
1. "Transfer $500 to savings" → from_account_number: '123-4567-890', to_account_number: '123-4567-891', amount: '500'
2. "Move $1000 to my joint account" → from_account_number: '123-4567-890', to_account_number: '123-4567-892', amount: '1000'
3. "Send $250 to my TFSA" → from_account_number: '123-4567-890', to_account_number: '123-4567-893', amount: '250'
