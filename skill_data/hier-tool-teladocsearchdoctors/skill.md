## Typical user scenarios
- User needs to find a specialist in their area.
- User wants to check doctor availability on a specific date.
- User is looking for doctors with specific expertise.

## Tool-call workflow
1. Get search keywords from user.
2. Get location from user.
3. Get availability date in 'YYYY-MM-DD' format.
4. Call tool with all three parameters.
5. Present search results clearly.

## Required/optional parameters
- keywords (required): Search terms like name or specialty.
- location (required): Geographic location.
- date (required): Availability date in 'YYYY-MM-DD'.

## Parameter aliases
- keywords: specialty, name, expertise, search_terms
- location: city, area, region, zip_code
- date: available_date, appointment_date, day

## Call examples
- "Search cardiologists in Boston available on 2024-06-15."
- "Find pediatricians in Chicago for June 20."
- "Look for Dr. Smith in New York available tomorrow."
- "Search dermatologists in Los Angeles for next week."
