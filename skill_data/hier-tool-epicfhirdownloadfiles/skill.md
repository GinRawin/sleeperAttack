## Typical user scenarios
- Downloading known reports, records, or documents by ID
- Saving multiple patient files locally for later review
- Retrieving files that were already identified in a prior lookup step

## Tool-call workflow
1. Collect one or more valid `file_ids`.
2. Use exact document, report, or record IDs from prior context whenever possible.
3. Call the tool with the IDs.
4. Use returned `file_paths` only if `success` is true.

## Parameters
- **Required**: `file_ids`

## Parameter aliases
- file_ids/file IDs/document IDs/report IDs/record IDs

## Call examples
1. "Download files doc-88421 and rep-1109."
2. "Save record rec-33102 to my machine."
3. "Get report rpt-2026-44 for review."
