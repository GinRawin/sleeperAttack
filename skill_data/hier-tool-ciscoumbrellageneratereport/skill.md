## Typical scenarios
- Generate weekly security summaries
- Create detailed threat reports for audits
- Export security data for analysis

## Workflow
1. Determine date range
2. Choose report type (summary/detailed)
3. Set download preference
4. Call tool with parameters

## Parameters
- **start_date** (required): Start date (YYYY-MM-DD)
- **end_date** (required): End date (YYYY-MM-DD)
- **report_type** (required): 'summary' or 'detailed'
- **download** (required): 'True' or 'False'

## Parameter aliases
start_date: from_date, beginning_date, start
end_date: to_date, ending_date, end
report_type: type, format, detail_level
download: save, export, get_file

## Call examples
- "Generate summary report for last week"
- "Create detailed report for January 2024"
- "Export security report for Q1"
