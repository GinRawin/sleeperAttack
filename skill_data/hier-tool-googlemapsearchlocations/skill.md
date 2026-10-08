## Typical Scenarios
- Finding nearby restaurants, shops, or services
- Searching for places with specific features or ratings
- Discovering places within a certain distance

## Workflow
1. Set search parameters (keywords, filters)
2. Tool returns matching locations
3. Results include distance, rating, and open status

## Parameters
**Required:**
- `keywords`: Search terms (e.g., 'coffee', 'pharmacy', 'park')

**Optional:**
- `open_now`: Filter for currently open places (true/false)
- `min_rating`: Minimum star rating (0-5)
- `base_location_address`: Search center address (defaults to current location)
- `max_distance`: Search radius in miles
- `max_results`: Maximum number of results (default 10)

## Parameter Aliases
Users may say: find/nearby/around, open/currently open, rating/stars/score, within/distance/radius

## Call Examples
1. "Find coffee shops open now within 2 miles"
2. "Search for pharmacies with 4+ star rating near my office"
3. "Show top 5 Italian restaurants within 5 miles of here"
