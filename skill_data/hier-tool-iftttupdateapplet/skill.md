## Typical user scenarios
- Changing trigger conditions
- Modifying action parameters
- Updating outdated automations

## Tool-call workflow
1. Use IFTTTSearchApplets to find applet_id
2. Use IFTTTSearchTriggers and IFTTTSearchActions for new settings
3. Call IFTTTUpdateApplet

## Required parameters
- **applet_id**: Applet identifier from IFTTTSearchApplets
- **trigger_service_name**: New service name
- **trigger_name**: New trigger name
- **trigger_parameters**: New trigger parameters
- **action_service_name**: New service name
- **action_name**: New action name
- **action_parameters**: New action parameters

## Parameter aliases
- applet_id: ID, applet identifier, automation ID
- trigger_service_name: new trigger service, updated source
- action_service_name: new action service, updated target

## Call examples
1. "Update applet applet123 to use different email address"
2. "Modify applet456 to trigger on different condition"
3. "Update applet789 with new action parameters"
