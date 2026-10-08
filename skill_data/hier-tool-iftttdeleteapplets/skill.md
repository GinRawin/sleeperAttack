## Typical user scenarios
- Removing outdated automations
- Cleaning up unused applets
- Deleting test applets

## Tool-call workflow
1. Use IFTTTSearchApplets to find applet_ids
2. Call IFTTTDeleteApplets
3. Confirm deletion

## Required parameters
- **applet_ids**: Array of applet IDs (e.g., "["applet123","applet456"]")

## Parameter aliases
- applet_ids: IDs, applet identifiers, automation IDs

## Call examples
1. "Delete applets with IDs applet123 and applet456"
2. "Remove applet ID applet789"
3. "Delete these applet IDs: ["applet111","applet222"]"
