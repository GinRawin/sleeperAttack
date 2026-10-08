## Typical scenarios
- Planning air travel
- Comparing flight options

## Tool-call workflow
1. Provide origin and destination
2. Specify departure_date and return_date
3. Provide travellers information
4. Specify travel_class
5. Optional: set max_results (default 5, max 10)
6. Optional: apply filters
7. Call tool

## Parameters
- **origin** (required): Departure location (airport code or city)
- **destination** (required): Arrival location (airport code or city)
- **departure_date** (required): Departure date (YYYY-MM-DD)
- **return_date** (required): Return date (YYYY-MM-DD)
- **travellers** (required): Object with adults, children, infants counts
- **travel_class** (required): 'economy', 'premium_economy', 'business', or 'first_class'
- **max_results** (required): Maximum results to return
- **filters** (optional): Object with min_price, max_price, stops_filter, airline, departure_time, arrival_time

## Parameter aliases
origin: from, departure city
destination: to, arrival city
travellers: passengers, travelers

## Call examples
1. "Search flights from NYC to London in business class"
2. "Find economy flights from LAX to Tokyo with 1 stop maximum"
