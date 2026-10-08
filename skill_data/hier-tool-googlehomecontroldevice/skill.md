## Typical user scenarios
- Turning lights on/off
- Adjusting thermostat temperature
- Controlling smart plugs

## Tool-call workflow
1. Use GoogleHomeSearchDevices to find device_id
2. Use GoogleHomeListDeviceActions to see available actions
3. Call GoogleHomeControlDevice with appropriate parameters

## Required parameters
- **device_id**: Device identifier from GoogleHomeSearchDevices
- **action**: Action from GoogleHomeListDeviceActions
- **parameters**: Parameters matching the action requirements

## Parameter aliases
- device_id: device, device identifier, ID
- action: command, function, operation
- parameters: settings, options, values

## Call examples
1. "Turn on living room lights"
2. "Set thermostat to 72 degrees"
3. "Turn off kitchen plug"
