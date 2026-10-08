**Typical Scenarios:**
- Reviewing recent trades
- Tracking dividend payments
- Tax documentation preparation

**Workflow:**
1. Specify account type
2. Set date range
3. Limit results if needed

**Parameters:**
- account (required): 'non-registered', 'TFSA', or 'RRSP'
- start_date (required): Format 'yyyy-mm-dd'
- end_date (required): Format 'yyyy-mm-dd'
- max_results (required): Number 1-50

**Parameter Aliases:**
- account: account_type/type/acct
- start_date: from/begin/start
- end_date: to/until/end
- max_results: limit/count/number

**Call Examples:**
1. "Show last 10 TFSA transactions" → account: 'TFSA', start_date: '2024-01-01', end_date: '2024-03-15', max_results: '10'
2. "List RRSP trades this year" → account: 'RRSP', start_date: '2024-01-01', end_date: '2024-03-15', max_results: '20'
3. "Recent non-registered activity" → account: 'non-registered', start_date: '2024-02-01', end_date: '2024-03-15', max_results: '15'
