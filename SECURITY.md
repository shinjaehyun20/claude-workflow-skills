# Security Policy

## Supported version

Only the latest tagged release is supported.

## Do not include

- passwords, tokens, API keys, cookies, OAuth state
- private client documents or screenshots
- personal absolute paths or email addresses
- undocumented private service endpoints
- scripts that upload, publish, send, delete, or move files without an explicit user gate

## Reporting

Report suspected secrets or unsafe automation privately to the repository owner. Do not open a public issue containing sensitive content. Include only the minimum reproduction detail needed to assess the issue.

## Safe defaults

- read-only source access
- dry-run before file movement
- public release only after package review and remote read-back
- no hooks or MCP servers in v0.1
- no automatic external submission
