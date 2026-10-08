## Typical scenarios
- Customer wants to change delivery address
- Business needs to cancel unshipped order
- Rescheduling pickup time
- Returning package to sender

## Tool-call workflow
1. Check shipment status first (must be 'pending' for cancel/reschedule, 'in_transit' for redirect/return)
2. Call tool with appropriate operation
3. Provide required additional parameters based on operation

## Parameters
**Required:**
- shipment_id: Unique shipment identifier
- operation: One of ['cancel', 'reschedule_pickup', 'redirect', 'return_to_sender']
- new_receipient_information: Required for 'redirect' operation
- new_pickup_time: Required for 'reschedule_pickup' operation (format 'YYYY-MM-DD:HH:MM:SS')

## Parameter aliases
- operation: action/task/change
- new_receipient_information: new_address/new_destination
- new_pickup_time: new_collection_time

## Call examples
1. "Cancel shipment ABC123"
2. "Redirect package to new address"
3. "Reschedule pickup for tomorrow"
4. "Return this shipment to sender"
