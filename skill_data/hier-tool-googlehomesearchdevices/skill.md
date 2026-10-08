## Typical user scenarios
- Finding specific device types
- Discovering all connected devices
- Locating devices for control

## Tool-call workflow
1. Call GoogleHomeSearchDevices (with or without device_type)
2. Use returned device_ids for other operations

## Required parameters
- **device_type**: Optional filter (e.g., "light", "thermostat", "plug")

## Parameter aliases
- device_type: type, category, kind

## Call examples
1. "Find all my lights"
2. "Search for thermostats"
3. "Show all connected devices"
