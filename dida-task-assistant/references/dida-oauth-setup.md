# Dida365 OAuth setup

Use this reference only when the user needs to connect their own Dida365 account.

1. Visit `https://developer.dida365.com/` and create an application in the user's own developer account.
2. Register `http://localhost:8080/callback` as the redirect URL, or choose another local URL and pass the exact same value to `scripts/configure.py --redirect-uri`.
3. Run `python3 scripts/configure.py` and enter the user's Client ID and Client Secret locally. The secret is masked in status output and stored outside the repository.
4. Run `python3 scripts/auth.py`; the user signs in to Dida365 in the browser and approves `tasks:read tasks:write`.

Troubleshooting:

- A redirect mismatch means the developer portal and local configuration do not use the identical URL.
- A port conflict can be resolved by choosing a different free port in both places.
- A 401 response means re-run `auth.py`; do not paste a token into chat or source code.
