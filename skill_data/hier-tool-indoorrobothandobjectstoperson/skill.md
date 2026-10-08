## Typical scenarios
- Delivering a drink to someone.
- Handing tools to a worker.
- Passing documents to a colleague.

## Tool-call workflow
1. Ensure robot has grabbed objects (check `GetCurrentState`).
2. Verify person is in room (use `FindPeople`).
3. Call with object IDs and person ID.

## Parameters
- **object_ids (Required)**: List of grabbed object IDs to hand over.
- **person_id (Required)**: ID of recipient person in current room.

## Parameter aliases
- object_ids: items, things, grabbed objects
- person_id: recipient, person, who

## Call examples
1. "Hand the coffee to Sarah."
2. "Give John the documents."
3. "Pass me the remote."
4. "Hand over the tools to the technician."
