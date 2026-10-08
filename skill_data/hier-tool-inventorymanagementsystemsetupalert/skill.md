## Typical scenarios
- Setting low stock notifications
- Modifying existing alert thresholds
- Removing obsolete alerts

## Tool-call workflow
1. Determine operation: 'add', 'update', or 'delete'
2. For 'add': provide item_id or category, threshold
3. For 'update': provide alert_id with new threshold
4. For 'delete': provide alert_id
5. Call tool with appropriate parameters

## Parameters
**Required:**
- alert_id: For 'update' and 'delete' operations
- item_id: For 'add' operation (if monitoring specific item)
- category: For 'add' operation (if monitoring category)
- threshold: Positive integer stock level
- operation: One of ['add', 'update', 'delete']

## Parameter aliases
- alert_id: notification_id/alert_number
- threshold: minimum_stock/alert_level/low_stock_level

## Call examples
1. "Alert me when widget stock drops below 10"
2. "Update alert ALERT-123 to threshold 5"
3. "Delete alert for discontinued product"
4. "Set category alert for electronics below 20 units"
