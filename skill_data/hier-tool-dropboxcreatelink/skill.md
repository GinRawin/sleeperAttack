## Typical scenarios
- Sharing a document with clients
- Providing access to a folder of resources
- Creating view-only links for presentations

## Tool-call workflow
1. Identify the item to share
2. Choose access level (view/comment/edit)
3. Call DropboxCreateLink

## Parameters
**Required:**
- item_path: Path to the file or folder
- access_level: 'view', 'comment', or 'edit'

## Parameter aliases
item_path: file, folder, path, item
access_level: permission, access, level, rights

## Call examples
1. "Create an edit link for /Work/Proposal.docx"
2. "Generate view-only link for /Photos/Vacation/"
3. "Share /Projects/Design/ with comment access"
4. "Create link for my resume with edit permission"
