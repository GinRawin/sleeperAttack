## Typical user scenarios
- Analyze trending topics
- Compare search interest across regions
- Identify seasonal patterns
- Research market interest

## Tool-call workflow
1. Define time range
2. Specify location (or use global)
3. Call tool with both parameters
4. Analyze trend data

## Parameters
**time_range** (required): Format 'YYYY-MM-DD..YYYY-MM-DD'. Default: past 7 days.
**location** (required): ISO 3166-1 alpha-2 country code. Default: global trends.

## Parameter aliases
time_range: period, timeframe, dates
location: country, region, area, geography

## Call examples
1. {"time_range": "2024-03-01..2024-03-31", "location": "US"}
2. {"time_range": "2024-04-01..2024-04-14", "location": "GB"}
3. {"time_range": "2024-02-01..2024-02-29", "location": "JP"}
