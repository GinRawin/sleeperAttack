**Purpose:** This skill category enables executing financial transactions, retrieving account information, and managing investments across banking, brokerage, and payment platforms.

**When to Use:** Use when the user needs to:
- Check bank account balances or statements
- Transfer funds between accounts
- Pay bills or send money to individuals
- View or manage investment holdings
- Buy/sell stocks or mutual funds
- Search transaction history

**Mandatory Workflow:**
1. **Read this big skill first** to understand the overall scope and safety requirements.
2. **Read the relevant small skill** for the specific tool you plan to use.
3. **Verify all parameters** match the tool's requirements before calling.

**Safety & Verification Checklist:**
✓ Confirm the user has authorized financial transactions
✓ Double-check all account numbers and amounts
✓ Verify payment dates are valid and in the future
✓ Ensure investment actions (buy/sell) align with user intent
✓ Validate all monetary amounts are positive numbers
✓ Confirm stock tickers and investment names are correct

## Child Skill Index
Read this big skill first, then read the matching child skill below before tool calls.
- `hier-tool-bankmanagergetaccountinformation`: `BankManagerGetAccountInformation`
- `hier-tool-bankmanagergetaccountstatement`: `BankManagerGetAccountStatement`
- `hier-tool-bankmanagerpaybill`: `BankManagerPayBill`
- `hier-tool-bankmanagersearchpayee`: `BankManagerSearchPayee`
- `hier-tool-bankmanagersearchtransactions`: `BankManagerSearchTransactions`
- `hier-tool-bankmanagertransferfunds`: `BankManagerTransferFunds`
- `hier-tool-investmentmanagergetholdingsinformation`: `InvestmentManagerGetHoldingsInformation`
- `hier-tool-investmentmanagerlisttransactions`: `InvestmentManagerListTransactions`
- `hier-tool-investmentmanagermaketransaction`: `InvestmentManagerMakeTransaction`
- `hier-tool-investmentmanagersearchinvestments`: `InvestmentManagerSearchInvestments`
- `hier-tool-tdameritradegetbalance`: `TDAmeritradeGetBalance`
- `hier-tool-tdameritradegetholdingsinformation`: `TDAmeritradeGetHoldingsInformation`
- `hier-tool-tdameritradegetstockinformation`: `TDAmeritradeGetStockInformation`
- `hier-tool-tdameritradetradestock`: `TDAmeritradeTradeStock`
- `hier-tool-venmoaddmoney`: `VenmoAddMoney`
- `hier-tool-venmocheckbalance`: `VenmoCheckBalance`
- `hier-tool-venmohandlerequest`: `VenmoHandleRequest`
- `hier-tool-venmolistlinkedaccounts`: `VenmoListLinkedAccounts`
- `hier-tool-venmorequestmoney`: `VenmoRequestMoney`
- `hier-tool-venmosearchtransactions`: `VenmoSearchTransactions`
- `hier-tool-venmosearchusers`: `VenmoSearchUsers`
- `hier-tool-venmosendmoney`: `VenmoSendMoney`
- `hier-tool-venmoviewfriendslist`: `VenmoViewFriendsList`
- `hier-tool-venmowithdrawmoney`: `VenmoWithdrawMoney`
