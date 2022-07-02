Change Log
=====================================

**0.1.1**

- Added the ability to add annotations to transactions. The Monzo API is broken for custom keys
- Various spelling isssues in notes

**0.1.0**

- Fixed viewer when authentication is not already setup

**0.0.10**

- Fixed incorrect key for spend_today in balance (thanks @psleep)
- Various bug fixes to Viewer
- Added ability to fetch transactions using viewer
- Added MonzoPermissionsError exception to Account
- Increased debug logging
- Now passing client id and client secret to handlers
- Various documentation fixes

**0.0.9**

- Minor release resolving github actions issue

**0.0.8**

- Minor release resolving github actions issue

**0.0.7**

- Resolved a packaging issue. Previous versions now obsolete

**0.0.6**

- Started to implement an API viewer, currently can aid in getting an access token
- Documentation improvements

**0.0.5**

- Improved error handling
- Created documentation (https://monzo-api.readthedocs.io)

**0.0.4**

- Fixed missing return in style property of pot class
- Updated auth_step_02.py to output token details that can be copied and pasted easily
- Implemented listeners process for when new tokens are retrieved including 2 listeners (echo, FileSystem)
- Implemented fetching a single translation
- Implemented fetching transaction list

**0.0.3**

- Fixed assignment of type rather than variable for AUth in 2 endpoints
- Fixed docstring for balance fetch method
- Implemented creating, listing and deleting webhooks
- Implemented listing, depositing into and withdrawing from pots

**0.0.2**

- Fixed error in API URL causing extra forward slash
- Implemented listing accounts
- Implemented reading balances
- Implemented posting feed items

**0.0.1**

- Initial minimal release
