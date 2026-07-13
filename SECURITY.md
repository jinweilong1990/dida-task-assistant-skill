# Security policy

## Never commit credentials or personal records

Do not commit, paste into an issue, or include in screenshots:

- Dida365 Client Secret, access token, refresh token, cookies, or API keys.
- `config.json`, `.env`, local `records.json`, `events.jsonl`, or `inbox.md`.
- Real task titles, descriptions, project IDs, or exported personal data.

The project intentionally stores user configuration and records outside the Skill folder. If a credential was ever committed, rotate it in the Dida365 developer console and revoke/re-authorize the affected access token before publishing again.

## Reporting a vulnerability

Do not open a public issue for an active credential exposure. Contact the repository maintainer privately with a minimal, redacted reproduction and wait for acknowledgement before disclosure.
