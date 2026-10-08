## Typical user scenarios
- Finding closest available units for new incident
- Checking resource availability in area
- Planning backup resource allocation
- Assessing coverage for specific location

## Tool-call workflow
1. Specify location to search around
2. Optionally filter by resource_type
3. Set max_results limit
4. Call tool to find resources

## Parameters
**Required:**
- location: Center point street address
- resource_type: 'Fire', 'Medical', 'Police' (optional)
- max_results: Maximum number to return (default 10)

**Parameter aliases:**
location/address/center_point, resource_type/unit_type/service_type, max_results/limit/count/number

## Call examples
1. "Find nearby medical units around 123 Hospital Road"
2. "Locate closest fire trucks to 456 Burning Building Avenue"
3. "Find all police units near 789 Downtown Plaza, limit to 5"
4. "Search for emergency resources around 321 Park Street"
