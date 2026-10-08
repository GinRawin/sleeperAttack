**Typical Scenarios:**
- Checking current balance
- Verifying account status
- Reviewing account details before transactions

**Workflow:**
1. Identify the account type from user request
2. Call tool with appropriate account_type parameter

**Parameters:**
- account_type (required): Must be one of: 'checking', 'savings', 'mutual fund TFSA', 'mutual fund non-registered', 'self-directed TFSA', 'self-directed non-registered', 'mortgage', 'credit_card'

**Parameter Aliases:**
- account_type: account/type/account_type

**Call Examples:**
1. "Check my savings account balance" → account_type: 'savings'
2. "Show my credit card details" → account_type: 'credit_card'
3. "Get TFSA mutual fund info" → account_type: 'mutual fund TFSA'
