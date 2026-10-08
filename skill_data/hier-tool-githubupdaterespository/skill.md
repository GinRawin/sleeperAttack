## Typical user scenarios
- Renaming an owned repository
- Updating repository description text
- Changing repository visibility between public and private

## Tool-call workflow
1. Collect the target `repo_id`.
2. Set only the fields that need to change: `name`, `description`, and/or `visibility`.
3. Use `visibility` only with `public` or `private`.
4. Call the tool after confirming the desired repository state.

## Parameters
- **Required**: `repo_id`
- **Optional**: `name`, `description`, `visibility`

## Parameter aliases
- repo_id/repository ID/repo
- name/repository name/new repo name
- description/repo description/about text
- visibility/public private/access level

## Call examples
1. "Rename repo repo-12345 to compliance-audit."
2. "Set repo repo-12345 visibility to private."
3. "Update repo repo-12345 description to Internal release automation scripts."
