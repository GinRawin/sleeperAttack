## Typical scenarios
- Looking up past shipments
- Finding all shipments to a specific customer
- Searching shipments by date or reference

## Tool-call workflow
1. Determine search criteria (customer name, date, reference, etc.)
2. Call tool with search_term
3. Review returned shipment results

## Parameters
**Required:**
- search_term: Text to search in shipment details

## Parameter aliases
- search_term: customer/date/reference/tracking

## Call examples
1. "Find shipments to Jane Doe"
2. "Search for yesterday's shipments"
3. "Look up order #12345 shipments"
4. "Find all international shipments"
