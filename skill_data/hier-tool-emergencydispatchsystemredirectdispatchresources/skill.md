## Typical user scenarios
- Redirecting units to higher priority incident
- Creating new incident at different location
- Reassigning resources dynamically
- Handling evolving emergency situations

## Tool-call workflow
1. Identify resource_ids to redirect
2. Choose target_type: 'Incident' or 'Location'
3. Provide incident_id_or_new_location accordingly
4. Call tool to execute redirection

## Parameters
**Required:**
- resource_ids: List of resource IDs to redirect
- target_type: 'Incident' or 'Location'
- incident_id_or_new_location: Incident ID or new street address

**Parameter aliases:**
resource_ids/units/vehicles, target_type/destination_type, incident_id_or_new_location/target/where_to

## Call examples
1. "Redirect ambulance AMB001 to incident INC456"
2. "Send police units P123,P124 to new location 789 Crisis Street"
3. "Redirect fire truck FTK007 to location 321 Fire Avenue"
4. "Reassign resources R001,R002 to incident EMG789"
