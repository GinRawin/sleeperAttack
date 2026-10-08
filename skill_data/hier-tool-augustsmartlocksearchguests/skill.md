## Typical user scenarios
- Finding a guest to modify their access
- Verifying if someone is in the system
- Looking up guest IDs for other operations

## Tool-call workflow
1. Get name keyword to search
2. Call AugustSmartLockSearchGuests
3. Use results for other operations (grant/revoke/delete)

## Required parameters
- **name_keyword**: Part of guest name (e.g., "John", "Smith")

## Parameter aliases
- name_keyword: name, search term, guest name

## Call examples
1. "Search for guests named John"
2. "Find guests with Smith in their name"
3. "Search for guest containing Mike"
