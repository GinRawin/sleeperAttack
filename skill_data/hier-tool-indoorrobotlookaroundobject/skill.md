## Typical scenarios
- Finding items near a workbench.
- Seeing what's on a table.
- Examining surroundings of a specific object.

## Tool-call workflow
1. Identify target `object_id` from `FindObjects`.
2. Call to see nearby objects.
3. Use results for further searches or operations.

## Parameters
- **object_id (Required)**: ID of central object to examine around.

## Parameter aliases
- object_id: target, center, focal object

## Call examples
1. "Look around the desk."
2. "What's near the refrigerator?"
3. "Examine area around the sofa."
4. "Check what's surrounding the toolbox."
