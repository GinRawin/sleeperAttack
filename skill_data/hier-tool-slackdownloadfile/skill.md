## Typical scenarios
- Saving shared documents
- Downloading images from conversations
- Archiving important files

## Tool-call workflow
1. Get file_id from Slack
2. Choose save_path location
3. Call tool with parameters

## Parameters
**Required:** file_id, save_path

## Parameter aliases
file_id: file identifier, document ID
save_path: download location, file path

## Call examples
1. "Download file F123 to /documents/"
2. "Save image file to desktop"
3. "Get presentation file to downloads folder"
