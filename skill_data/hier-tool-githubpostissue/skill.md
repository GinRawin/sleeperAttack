## Typical user scenarios
- Opening a bug report or incident ticket
- Creating a tracking issue for a task or follow-up
- Recording a problem with clear reproduction details

## Tool-call workflow
1. Collect the target `repo_id`.
2. Write a concise `title` that identifies the issue.
3. Add `body` when context, steps, or logs are useful.
4. Call the tool once the repository and issue text are ready.

## Parameters
- **Required**: `repo_id`, `title`
- **Optional**: `body`

## Parameter aliases
- repo_id/repository ID/repo
- title/issue title/subject
- body/description/details

## Call examples
1. "Create an issue in repo repo-12345 titled Fix OAuth callback timeout."
2. "Open an incident issue in repo repo-9001 with deployment logs in the body."
3. "Post a tracking issue in repo repo-441 for the Q2 cleanup work."
