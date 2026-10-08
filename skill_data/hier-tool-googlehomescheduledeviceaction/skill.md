## Typical user scenarios
- Scheduling lights to turn on at sunset
- Setting thermostat adjustments for specific times
- Programming smart plugs

## Tool-call workflow
1. Use GoogleHomeSearchDevices to find device_id
2. Use GoogleHomeListDeviceActions to see available actions
3. Call GoogleHomeScheduleDeviceAction

## Required parameters
- **device_id**: Device identifier from GoogleHomeSearchDevices
- **action**: Action from GoogleHomeListDeviceActions
- **date_time**: Scheduled time in YYYY-MM-DD HH:MM format
- **parameters**: Parameters matching the action requirements

## Parameter aliases
- device_id: device, device identifier, ID
- action: command, function, operation
- date_time: time, schedule, when
- parameters: settings, options, values

## Call examples
1. "Schedule lights to turn on at 7 PM"
2. "Set thermostat to 68 degrees at 10 PM"
3. "Schedule plug to turn off at midnight"
