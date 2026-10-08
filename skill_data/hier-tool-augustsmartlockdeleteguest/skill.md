## Typical user scenarios
- Removing former house cleaners
- Revoking access for moved-out roommates
- Cleaning up old guest entries

## Tool-call workflow
1. Get guest IDs to delete (from previous operations)
2. Call AugustSmartLockDeleteGuest
3. Confirm deletion

## Required parameters
- **guest_ids**: Array of guest IDs (e.g., "["guest123","guest456"]")

## Parameter aliases
- guest_ids: IDs, guest identifiers, user IDs

## Call examples
1. "Delete guests with IDs guest123 and guest456"
2. "Remove guest ID guest789 from system"
3. "Delete these guest IDs: ["guest111","guest222"]"
