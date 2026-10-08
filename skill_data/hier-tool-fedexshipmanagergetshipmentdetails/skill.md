## Typical scenarios
- Customer asks "Where's my package?"
- Business needs delivery confirmation
- Monitoring shipment progress

## Tool-call workflow
1. Obtain shipment_id from label or previous tracking
2. Call tool with shipment_id
3. Review returned status and delivery date

## Parameters
**Required:**
- shipment_id: Unique shipment identifier

## Parameter aliases
- shipment_id: tracking_number/tracking_id/package_id

## Call examples
1. "Track shipment ABC123456789"
2. "What's the status of my package?"
3. "When will shipment XYZ arrive?"
4. "Check delivery status"
