## Typical user scenarios
- Discovering device capabilities
- Preparing to control a device
- Checking available settings

## Tool-call workflow
1. Get device_id from GoogleHomeSearchDevices
2. Call GoogleHomeListDeviceActions
3. Use results to call GoogleHomeControlDevice

## Required parameters
- **device_id**: Device identifier from GoogleHomeSearchDevices

## Parameter aliases
- device_id: device, device identifier, ID

## Call examples
1. "What can I do with device device123?"
2. "List actions for living room lights"
3. "Show available commands for thermostat"
