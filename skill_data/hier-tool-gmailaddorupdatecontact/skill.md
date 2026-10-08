## Typical scenarios
- Adding a new business contact
- Updating a contact's phone number or address
- Importing contacts from another system

## Tool-call workflow
1. Determine if creating new or updating existing contact
2. Collect required information
3. Format 'info' parameter as JSON string
4. Call tool with complete parameters

## Parameters
**Required for new contacts:** name, email
**Required for updates:** contact_id
**Optional:** remark
**Required:** info (JSON string with phone/address)

## Parameter aliases
contact_id: ID, identifier, contact reference
name: full name, contact name
email: email address, contact email
remark: note, label, tag
info: details, additional info, contact info

## Call examples
1. "Add John Doe with email john@example.com and phone 555-1234"
2. "Update contact ID 123 with new address"
3. "Create contact for Sarah with work email and remark 'client'"
4. "Add emergency contact with all details"
