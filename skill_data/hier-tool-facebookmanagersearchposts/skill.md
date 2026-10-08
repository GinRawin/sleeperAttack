## Typical Scenarios
- Finding old posts
- Searching for specific content
- Researching user's posting history

## Workflow
1. Identify user_id
2. Define search keyword
3. Set max_results (default: 10)
4. Call tool to search posts

## Parameters
**Required:**
- `user_id`: Facebook user identifier
- `keyword`: Search term
- `max_results`: Maximum results to return (default: 10)

**Aliases:** user_id → user/ID, keyword → search/term, max_results → limit/count/number

## Examples
1. "Search my posts for 'vacation'"
2. "Find posts by user 12345 containing 'birthday'"
3. "Look for 'recipe' in user ABCDE's posts, max 5 results"
