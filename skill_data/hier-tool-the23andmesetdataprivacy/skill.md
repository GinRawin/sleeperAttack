## Typical user scenarios
- User wants to change data sharing permissions.
- User needs to restrict third-party access.
- User is updating privacy preferences.

## Tool-call workflow
1. Get privacy_settings object from user.
2. Confirm each setting change explicitly.
3. Call tool with privacy_settings parameter.
4. Confirm privacy update.

## Required/optional parameters
- privacy_settings (required): Object with 'share_with_third_parties' (boolean) and 'allow_download' (boolean).

## Parameter aliases
- privacy_settings: settings, preferences, permissions, privacy_options

## Call examples
- "Set privacy: don't share with third parties, allow download."
- "Update settings: share_with_third_parties=false, allow_download=true."
- "Change privacy to block all sharing and downloads."
- "Allow third-party sharing but disable downloads."
