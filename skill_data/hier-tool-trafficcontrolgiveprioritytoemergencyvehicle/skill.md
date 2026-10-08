## Typical user scenarios
- Clearing an ambulance route through several intersections
- Scheduling signal priority for a fire truck convoy
- Coordinating emergency response travel windows

## Tool-call workflow
1. Collect the list of target `intersection_ids`.
2. Collect the `start_time` in `YYYY-MM-DD HH:MM:SS` format.
3. Collect the `end_time` in `YYYY-MM-DD HH:MM:SS` format.
4. Call the tool once the route and time window are confirmed.

## Parameters
- **Required**: `intersection_ids`, `start_time`, `end_time`

## Parameter aliases
- intersection_ids/intersection list/route intersections
- start_time/priority start time
- end_time/priority end time

## Call examples
1. "Give emergency priority at intersections int-204 and int-205 from 2026-04-05 08:15:00 to 2026-04-05 08:25:00."
2. "Schedule ambulance signal priority for int-11, int-12, and int-13 for the next ten minutes."
3. "Set a future emergency route window for intersections on the hospital corridor."
