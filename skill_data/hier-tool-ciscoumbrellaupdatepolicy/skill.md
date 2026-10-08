## Typical scenarios
- Update policy names or descriptions
- Change policy types (whitelist/blacklist)
- Add or remove domains from policies

## Workflow
1. Get policy ID to update
2. Prepare new parameters
3. Call tool with all parameters

## Parameters
- **policy_id** (required): Policy identifier
- **policy_name** (required): New policy name
- **policy_description** (required): New description
- **policy_type** (required): New type ('whitelist'/'blacklist')
- **domains** (required): New domain array

## Parameter aliases
policy_id: id, policy identifier
domains: domain_list, websites, sites

## Call examples
- "Update policy POL-12345 with new domains"
- "Change policy name and description"
- "Switch policy from whitelist to blacklist"
