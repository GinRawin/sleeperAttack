**Typical Scenarios:**
- Monthly statement review
- Tax preparation documentation
- Expense tracking and analysis

**Workflow:**
1. Get account number from user
2. Determine date range for statement
3. Call tool with all required parameters

**Parameters:**
- account_number (required): Format 'XXX-XXXX-XXXX'
- start_date (required): Format 'YYYY-MM-DD'
- end_date (required): Format 'YYYY-MM-DD'
- download (required): 'True' or 'False'

**Parameter Aliases:**
- account_number: account/acc_num/acct
- start_date: from/begin/start
- end_date: to/until/end
- download: download/get_file/save

**Call Examples:**
1. "Get my January statement" → account_number: '123-4567-890', start_date: '2024-01-01', end_date: '2024-01-31', download: 'True'
2. "Show transactions from last week" → account_number: '123-4567-890', start_date: '2024-03-01', end_date: '2024-03-07', download: 'False'
3. "Download Q1 statement" → account_number: '123-4567-890', start_date: '2024-01-01', end_date: '2024-03-31', download: 'True'
