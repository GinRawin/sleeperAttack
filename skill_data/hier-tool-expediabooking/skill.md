## Typical scenarios
- Booking selected flight options
- Reserving chosen accommodations

## Tool-call workflow
1. Select option_ids (all same type: flights OR accommodations)
2. Provide payment_method
3. For flights: provide travellers array
4. Call tool

## Parameters
- **option_ids** (required): Array of flight/accommodation IDs
- **payment_method** (required): Object with card_number, expiry_date, CVV
- **travellers** (required for flights): Array with name, date_of_birth, passport_number, passport_expiry_date

## Parameter aliases
option_ids: selection IDs, chosen options
payment_method: payment details, card info
travellers: passengers, guests

## Call examples
1. "Book flight options FLT123 and FLT456 with my Visa"
2. "Reserve hotel options HOT789 with my Mastercard"
