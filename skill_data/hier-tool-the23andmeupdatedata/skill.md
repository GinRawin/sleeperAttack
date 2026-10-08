## Typical user scenarios
- User has new genetic test results to add.
- User wants to correct or supplement existing genetic data.
- User needs to update ancestry or health predisposition information.

## Tool-call workflow
1. Get new_data object from user with fields: ancestry, traits, health_predispositions, carrier_status.
2. Confirm each data field update.
3. Call tool with new_data parameter.
4. Confirm data update.

## Required/optional parameters
- new_data (required): Object with ancestry, traits, health_predispositions, and carrier_status fields.

## Parameter aliases
- new_data: updated_data, genetic_info, dna_data, profile_update

## Call examples
- "Update ancestry to 40% European, 60% Asian."
- "Add new health predisposition: increased risk for diabetes."
- "Update traits: add lactose intolerance."
- "Set carrier_status for cystic fibrosis to positive."
