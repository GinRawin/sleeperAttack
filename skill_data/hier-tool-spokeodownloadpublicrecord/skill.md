## Typical user scenarios
- Downloading a previously identified public record
- Saving a record locally for review or handoff
- Exporting a single record by exact person and record identifiers

## Tool-call workflow
1. Collect the target `unique_id` for the person.
2. Collect the exact `record_id` to download.
3. Choose a valid `local_file_path` where the file should be written.
4. Call the tool and confirm `download_status` before using the file downstream.

## Parameters
- **Required**: `unique_id`, `record_id`, `local_file_path`

## Parameter aliases
- unique_id/person ID/profile ID
- record_id/record ID/public record ID
- local_file_path/save path/output file/path

## Call examples
1. "Download record rec-5566 for person spk-2024-001 to C:/tmp/record.pdf."
2. "Save record court-991 for person spk-77 to C:/exports/court-991.txt."
3. "Download public record prop-1209 for spk-2024-001 to C:/records/prop-1209.json."
