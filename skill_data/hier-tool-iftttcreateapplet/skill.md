## Typical user scenarios
- Automating social media posts
- Creating email notifications
- Setting up smart home automations

## Tool-call workflow
1. Use IFTTTSearchConnectedServices to find services
2. Use IFTTTSearchTriggers to find trigger
3. Use IFTTTSearchActions to find action
4. Call IFTTTCreateApplet

## Required parameters
- **trigger_service_name**: Service name from IFTTTSearchConnectedServices
- **trigger_name**: Trigger from IFTTTSearchTriggers
- **trigger_parameters**: JSON object matching trigger requirements
- **action_service_name**: Service name from IFTTTSearchConnectedServices
- **action_name**: Action from IFTTTSearchActions
- **action_parameters**: JSON object matching action requirements

## Parameter aliases
- trigger_service_name: trigger service, source service
- trigger_name: trigger, event, condition
- action_service_name: action service, target service
- action_name: action, result, task

## Call examples
1. "Create applet: when I post on Twitter, send me an email"
2. "Make automation: if weather says rain, turn on lights"
3. "Create rule: new email triggers phone notification"
