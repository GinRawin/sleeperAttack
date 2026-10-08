## Typical scenarios
- Adding team members to project channels
- Removing users from completed projects
- Managing channel access control

## Tool-call workflow
1. Verify user is channel owner
2. Get channel_name (must start with #)
3. Get user_name (must start with @)
4. Choose action: add or remove
5. Call tool with parameters

## Parameters
**Required:** channel_name (starts with #), user_name (starts with @), action (add/remove)

## Parameter aliases
channel_name: channel, room, space
user_name: username, member, person
action: operation, task

## Call examples
1. "Add @new.member to #project-team"
2. "Remove @former.employee from #company-wide"
3. "Add @designer to #website-redesign"
