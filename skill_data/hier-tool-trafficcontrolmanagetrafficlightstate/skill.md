## Typical user scenarios
- Changing a traffic signal immediately
- Scheduling a temporary signal override window
- Updating either vehicle or pedestrian light states

## Tool-call workflow
1. Collect the target `intersection_id`.
2. Collect the exact `traffic_light_id`, such as `vehicle-north-south`.
3. Set `traffic_light_state` to a valid state for that light type.
4. Add `start_time` and `end_time` only for scheduled changes; omit `start_time` for immediate changes.
5. Call the tool after checking the time window and target signal.

## Parameters
- **Required**: `intersection_id`, `traffic_light_id`, `traffic_light_state`
- **Optional**: `start_time`, `end_time`

## Parameter aliases
- intersection_id/intersection ID/location ID
- traffic_light_id/light ID/signal ID
- traffic_light_state/state/light color/signal state
- start_time/start
- end_time/end/stop time

## Call examples
1. "Set vehicle-north-south at intersection int-204 to red now."
2. "Change pedestrian-east-west at intersection int-204 to walk from 2026-04-01 08:00:00 to 2026-04-01 08:02:00."
3. "Set vehicle-east-west at intersection int-204 to hazard until 2026-04-01 23:00:00."
