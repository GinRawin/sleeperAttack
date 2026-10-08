## Typical user scenarios
- Collaborating on notes with team members
- Restricting access to sensitive notes
- Granting edit permissions to colleagues

## Tool-call workflow
1. Provide required `note_id`, `email`, and `level`.
2. `level` must be: 'not_accessible', 'read_only', or 'can_edit'.
3. Call the tool.

## Parameters
- **Required**: `note_id`, `email`, `level`

## Parameter aliases
- note_id/note/ID
- email/user/recipient/colleague
- level/permission/access/rights

## Call examples
1. "Share note 'abc123' with john@email.com as read-only"
2. "Give edit access to note 'xyz789' for sarah@company.com"
