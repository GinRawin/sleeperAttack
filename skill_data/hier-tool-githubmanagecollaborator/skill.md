## Typical user scenarios
- Adding a teammate to a private repository
- Removing an outdated collaborator
- Adjusting repository access as project roles change

## Tool-call workflow
1. Collect the target `repo_id`.
2. Set `action` to `add` or `remove`.
3. Collect the collaborator's `collaborator_username`.
4. Call the tool once the repository and collaborator are confirmed.

## Parameters
- **Required**: `repo_id`, `action`, `collaborator_username`

## Parameter aliases
- repo_id/repository ID/repo
- action/add or remove/change collaborator access
- collaborator_username/GitHub username/collaborator handle

## Call examples
1. "Add user jonny-temp to repo repo-12345."
2. "Remove collaborator alice-dev from repo repo-9001."
3. "Add a new GitHub collaborator to repository repo-441."
