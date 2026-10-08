## Typical scenarios
- Collaborating on documents with colleagues
- Sharing photos with family members
- Granting access to project files

## Tool-call workflow
1. Identify item to share
2. Specify recipient email
3. Choose access level
4. Call DropboxShareItem

## Parameters
**Required:**
- item_path: Item to share
- recipient_email: User's email address
- access_level: 'view', 'comment', or 'edit'

## Parameter aliases
item_path: file, folder, item, path
recipient_email: email, to, recipient, user
access_level: permission, access, level, rights

## Call examples
1. "Share /Work/Project.docx with john@example.com with edit access"
2. "Give view permission to /Photos/ to family@email.com"
3. "Share /Reports/ with team@company.com, comment access"
4. "Send edit access for /Design/ to client@business.com"
