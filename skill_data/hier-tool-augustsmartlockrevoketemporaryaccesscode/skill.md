## Typical user scenarios
- Revoking code after service completion
- Invalidating lost or compromised codes
- Ending temporary access early

## Tool-call workflow
1. Get the access code to revoke
2. Call AugustSmartLockRevokeTemporaryAccessCode
3. Confirm revocation

## Required parameters
- **access_code**: The temporary code to revoke (e.g., "123456")

## Parameter aliases
- access_code: code, temporary code, passcode

## Call examples
1. "Revoke temporary code 123456"
2. "Invalidate access code 789012"
3. "Revoke code ABC123"
