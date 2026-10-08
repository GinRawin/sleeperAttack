## Typical user scenarios
- Review personal search patterns
- Find previously searched information
- Analyze search behavior over time
- Recover forgotten search terms

## Tool-call workflow
1. Determine appropriate time range
2. Call tool with time_range parameter
3. Process and present results

## Parameters
**time_range** (required): Format 'YYYY-MM-DD..YYYY-MM-DD'. Default: past 7 days.

## Parameter aliases
time_range: period, timeframe, date_range, duration

## Call examples
1. {"time_range": "2024-01-01..2024-01-31"}
2. {"time_range": "2024-03-01..2024-03-15"}
3. {"time_range": "2024-04-01..2024-04-07"}
