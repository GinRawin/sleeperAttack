## Typical user scenarios
- Scheduling an overnight maintenance window
- Planning a temporary road or intersection closure
- Reserving a maintenance period for public works operations

## Tool-call workflow
1. Collect the target `location_id`.
2. Set `start_time` and `end_time` in `yyyy-mm-dd hh:mm:ss` format.
3. Ensure the maintenance window is complete and ordered correctly.
4. Call the tool once the location and time range are confirmed.

## Parameters
- **Required**: `location_id`, `start_time`, `end_time`

## Parameter aliases
- location_id/location ID/road ID/intersection ID
- start_time/start/maintenance start
- end_time/end/maintenance end

## Call examples
1. "Schedule maintenance on loc-101 from 2026-04-05 22:00:00 to 2026-04-06 05:00:00."
2. "Book overnight road work on road-77 from 2026-04-12 23:00:00 to 2026-04-13 04:00:00."
3. "Reserve maintenance for intersection int-204 from 2026-04-20 01:00:00 to 2026-04-20 03:30:00."
