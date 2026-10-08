## Typical user scenarios
- Revoking access from former employees
- Removing permissions after service completion
- Temporary suspension of access

## Tool-call workflow
1. Get guest IDs to revoke
2. Call AugustSmartLockRevokeGuestAccess
3. Confirm revocation

## Required parameters
- **guest_ids**: Array of guest IDs (e.g., "["guest123"]")

## Parameter aliases
- guest_ids: IDs, guest identifiers, user IDs

## Call examples
1. "Revoke access for guest ID guest123"
2. "Remove access from guests ["guest456","guest789"]"
3. "Revoke permissions for guest ID guest111"
