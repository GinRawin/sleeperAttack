## Typical user scenarios
- Granting permanent access to family members
- Setting up temporary access for house sitters
- Managing access schedules for regular visitors

## Tool-call workflow
1. Get guest IDs (from AugustSmartLockSearchGuests or previous operations)
2. Determine if access is permanent or temporary
3. For temporary: specify start and end times
4. Call AugustSmartLockGrantGuestAccess

## Required parameters
- **guest_ids**: Array of guest IDs (e.g., "["guest123"]")
- **permanent**: "true" for permanent, "false" for temporary
- **start_time**: Required for temporary access (YYYY-MM-DD HH:mm)
- **end_time**: Required for temporary access (YYYY-MM-DD HH:mm)

## Parameter aliases
- guest_ids: IDs, guest identifiers
- permanent: permanent access, forever, always
- start_time: start, from, beginning
- end_time: end, until, expiration

## Call examples
1. "Grant permanent access to guest ID guest123"
2. "Give temporary access to guest456 from 9 AM to 5 PM today"
3. "Grant access to guests ["guest111","guest222"] permanently"
