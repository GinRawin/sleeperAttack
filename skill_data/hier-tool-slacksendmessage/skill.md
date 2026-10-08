## Typical scenarios
- Sending team announcements
- Sharing files with colleagues
- Direct messaging team members

## Tool-call workflow
1. Choose recipient (channel starts with #, user starts with @)
2. Write message content
3. Add file_path if sending file (optional)
4. Call tool with parameters

## Parameters
**Required:** recipient, message
**Optional:** file_path

## Parameter aliases
recipient: to, channel/user, destination
message: content, text, note
file_path: attachment, file, document

## Call examples
1. "Send 'Meeting at 3 PM' to #general"
2. "Message @john about the report"
3. "Send document to #team with message 'Here's the file'"
