## Typical Scenarios
- Correcting post content
- Changing post visibility
- Updating information in posts

## Workflow
1. Locate post_id
2. Prepare new content
3. Select new privacy setting
4. Call tool to update post

## Parameters
**Required:**
- `post_id`: Exact Facebook post identifier
- `new_content`: Updated post text
- `new_privacy_setting`: 'public', 'friends', or 'only me'

**Aliases:** post_id → post/ID, new_content → content/text, new_privacy_setting → privacy/visibility

## Examples
1. "Update post 12345 with 'Correction: Event is tomorrow' and set to public"
2. "Change post ABCDE content to 'Updated information' and friends only"
3. "Modify post XYZ to private with new text"
