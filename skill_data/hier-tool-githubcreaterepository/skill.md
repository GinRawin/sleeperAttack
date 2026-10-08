## Typical user scenarios
- Creating a new public or private repository
- Starting a codebase for a product, demo, or experiment
- Setting up a repo with a short description for collaborators

## Tool-call workflow
1. Collect the repository `name`.
2. Set `visibility` to `public` or `private`.
3. Add `description` if the user wants one.
4. Call the tool once the repository name and visibility are clear.

## Parameters
- **Required**: `name`, `visibility`
- **Optional**: `description`

## Parameter aliases
- name/repository name/repo name
- visibility/access level/public or private
- description/repo description/summary

## Call examples
1. "Create a private repository named acme-checkout."
2. "Create a public repo called city-traffic-dashboard with a short description."
3. "Set up a private repo named lab-notes and describe it as internal experiments."
