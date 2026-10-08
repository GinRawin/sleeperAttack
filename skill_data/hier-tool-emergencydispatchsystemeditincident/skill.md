## Typical user scenarios
- Updating incident severity or description
- Changing incident status (active/closed)
- Reassigning resources to an incident
- Correcting incident type classification

## Tool-call workflow
1. Identify incident_id to edit
2. Determine which fields need updating
3. Provide new values for required parameters

## Parameters
**Required:**
- incident_id: ID of incident to edit
- incident_type: New type if changing
- incident_severity: New severity if changing
- incident_description: New description if changing
- incident_status: New status if changing
- resource_ids: New resource list if reassigning

**Parameter aliases:**
incident_id/case_id/emergency_id, status/state/condition, resources/units/assigned_units

## Call examples
1. "Update incident ABC123 to high severity"
2. "Close incident DEF456 and reassign resources"
3. "Change incident GHI789 type from medical to police"
4. "Update description for incident JKL012"
