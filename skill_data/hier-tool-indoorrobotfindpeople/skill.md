## Typical scenarios
- Finding a specific person to deliver an item.
- Checking if a room is occupied.
- Locating all people in a room.

## Tool-call workflow
1. Ensure robot is in correct room.
2. Call with person's name or description.
3. Use returned person IDs for interactions like `HandObjectsToPerson`.

## Parameters
- **query (Required)**: Name or description of person(s). Leave empty to find all people.

## Parameter aliases
- query: person, name, who, description

## Call examples
1. "Find John in this room."
2. "Look for someone wearing a blue shirt."
3. "See who's here."
4. "Find all people in the room."
