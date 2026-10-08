## Typical scenarios
- Deleting spam or promotional emails
- Cleaning up old conversations
- Removing sensitive emails

## Tool-call workflow
1. Identify email IDs to delete
2. Format as array string
3. Confirm deletion with user
4. Call tool with email_ids

## Parameters
**Required:** email_ids (array string)

## Parameter aliases
email_ids: message IDs, email identifiers, message references

## Call examples
1. "Delete emails with IDs ['msg123', 'msg456']"
2. "Remove these three spam messages"
3. "Clear out old newsletter emails"
