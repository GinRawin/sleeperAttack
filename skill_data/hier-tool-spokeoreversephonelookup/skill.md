## Typical user scenarios
- Identifying the owner of a phone number
- Checking who a caller number belongs to
- Enriching a contact from a single phone number

## Tool-call workflow
1. Collect the target `phone_number`.
2. Use a normalized or clearly formatted number when possible.
3. Call the tool once you have the exact number to resolve.
4. Read the returned `lookup_result` for identity details.

## Parameters
- **Required**: `phone_number`

## Parameter aliases
- phone_number/phone number/caller number

## Call examples
1. "Look up +1-415-555-8123."
2. "Who owns 415-555-8123?"
3. "Run a reverse phone lookup for +44 20 7946 0958."
