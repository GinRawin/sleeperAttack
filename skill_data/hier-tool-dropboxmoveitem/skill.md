## Typical scenarios
- Organizing files into different folders
- Moving completed projects to archive
- Restructuring your Dropbox layout

## Tool-call workflow
1. Identify item to move
2. Specify destination folder
3. Call DropboxMoveItem

## Parameters
**Required:**
- item_path: Item to move
- destination_folder_path: Where to move it

## Parameter aliases
item_path: file, folder, source, from
destination_folder_path: destination, to, target, new_location

## Call examples
1. "Move /Drafts/Proposal.docx to /Final/"
2. "Move folder /OldProjects/ to /Archive/"
3. "Move /Temp/image.png to /Photos/"
4. "Move /Work/Report.pdf to /Completed/"
