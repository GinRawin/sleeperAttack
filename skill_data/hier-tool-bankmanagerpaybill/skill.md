**Typical Scenarios:**
- Paying utility bills
- Making credit card payments
- Settling service provider invoices

**Workflow:**
1. Identify payee and service account number
2. Confirm payment amount and date
3. Specify funding account
4. Execute payment

**Parameters:**
- from_account_number (required): Format 'XXX-XXXX-XXXX'
- payee_id (required): Format 'P-XXXXXX'
- service_account_number (required): User's account with payee
- payment_date (required): Format 'YYYY-MM-DD'
- amount (required): Positive number

**Parameter Aliases:**
- from_account_number: source/from/pay_from
- payee_id: payee/recipient/biller
- service_account_number: account_num/customer_id/acct
- payment_date: date/when/schedule
- amount: payment/sum/total

**Call Examples:**
1. "Pay $150 to Hydro One" → from_account_number: '123-4567-890', payee_id: 'P-123456', service_account_number: 'CUST789', payment_date: '2024-03-15', amount: '150'
2. "Schedule Rogers payment for next week" → from_account_number: '123-4567-890', payee_id: 'P-654321', service_account_number: 'ACC123', payment_date: '2024-03-20', amount: '89.99'
3. "Pay my credit card bill" → from_account_number: '123-4567-890', payee_id: 'P-987654', service_account_number: 'CARD456', payment_date: '2024-03-10', amount: '500'
