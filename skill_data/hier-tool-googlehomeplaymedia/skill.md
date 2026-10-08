## Typical user scenarios
- Playing specific songs
- Streaming podcasts
- Listening to radio stations

## Tool-call workflow
1. Use GoogleHomeSearchDevices to find device_id
2. Use GoogleHomeListDeviceActions to see media parameters
3. Call GoogleHomePlayMedia

## Required parameters
- **media**: Media to play (song, podcast, station)
- **device_id**: Device identifier from GoogleHomeSearchDevices
- **parameters**: Media parameters from GoogleHomeListDeviceActions

## Parameter aliases
- media: song, podcast, station, content
- device_id: device, speaker, player
- parameters: settings, options, details

## Call examples
1. "Play jazz music on living room speaker"
2. "Play news podcast on kitchen device"
3. "Play classical radio station"
