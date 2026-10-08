## Typical user scenarios
- User wants to share data with a health research app.
- User needs to connect genetic data to a fitness service.
- User is authorizing a medical app to access their genetics.

## Tool-call workflow
1. Get valid app_id from user.
2. Confirm user wants to share data with this specific app.
3. Call tool with app_id parameter.
4. Confirm sharing completion.

## Required/optional parameters
- app_id (required): Valid identifier of registered third-party application.

## Parameter aliases
- app_id: application_id, app, service_id, partner_id

## Call examples
- "Share my data with app HEALTH123."
- "Authorize application FITNESS456 to access my genetics."
- "Grant access to my genetic data for app RESEARCH789."
- "Share with third-party app MEDICAL101."
