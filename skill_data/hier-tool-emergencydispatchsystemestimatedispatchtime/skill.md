## Typical user scenarios
- Checking ETA for dispatched unit
- Planning resource allocation
- Estimating response times for new incidents
- Coordinating multiple unit arrivals

## Tool-call workflow
1. Identify resource_id to track
2. Specify destination_location
3. Call tool for time estimate

## Parameters
**Required:**
- resource_id: ID of dispatch resource
- destination_location: Target street address

**Parameter aliases:**
resource_id/unit_id/vehicle_id, destination_location/target/address/where_to

## Call examples
1. "Estimate time for ambulance AMB001 to reach 123 Main Street"
2. "How long for fire truck FTK005 to get to 456 Oak Avenue?"
3. "Check ETA for police unit POL123 to 789 Pine Road"
4. "Estimate dispatch time for resource RES456 to destination"
