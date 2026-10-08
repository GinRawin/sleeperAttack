## Typical scenarios
- Finding hotels for vacation
- Searching rental properties

## Tool-call workflow
1. Provide city and location
2. Specify check-in/check-out dates
3. Provide guests information
4. Optional: set max_results (default 5, max 10)
5. Optional: apply filters
6. Call tool

## Parameters
- **city** (required): City name
- **location** (required): Location within city
- **check_in_date** (required): Check-in date (YYYY-MM-DD)
- **check_out_date** (required): Check-out date (YYYY-MM-DD)
- **guests** (required): Object with adults, children counts
- **max_results** (required): Maximum results to return
- **filters** (optional): Object with min_price, max_price, accommodation_type, room_type, min_rating, free_cancellation, free_breakfast, allow_smoking, allow_pets

## Parameter aliases
city: destination city
location: area, district
guests: number of people, occupancy

## Call examples
1. "Search hotels in Paris for 2 adults from June 1-7"
2. "Find apartments in Tokyo for 4 people with free cancellation"
