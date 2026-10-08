## Typical scenarios
- Customer asks for shipping costs before purchase
- Business needs to compare shipping options
- Calculating costs for different package sizes

## Tool-call workflow
1. Gather complete package details
2. Collect sender and recipient information
3. Specify pickup time and special handling needs
4. Call tool with all required parameters

## Parameters
**Required:**
- package_details: JSON with description, weight (grams), dimensions (h*w*d in cm)
- sender_information: Full name, valid address, contact number
- recipient_information: Full name, valid address, contact number
- pickup_time: Format 'YYYY-MM-DD:HH:MM:SS'
- special_handling: One or more of ['signature_required', 'fragile', 'oversized', 'dangerous_goods', 'temperature_sensitive']

## Parameter aliases
- package_details: parcel/package/shipment_details
- pickup_time: collection_time/pickup_date
- special_handling: special_requirements/extra_services

## Call examples
1. "Get a quote for shipping a 500g book"
2. "How much to ship fragile electronics overnight?"
3. "Quote for temperature-sensitive medical supplies"
4. "Get shipping estimate for 2kg package"
