# Publication Checklist

## Repository

- [ ] Repository is created as private
- [ ] About description, topics, and README are set
- [ ] Default branch is `main`
- [ ] Validation workflow passes
- [ ] Initial tag is not created before validation

## Source protection

- [ ] `python tools/import_and_analyze.py` passes
- [ ] Source immutability is `PASS`
- [ ] Every imported file has a source SHA-256
- [ ] Claude Code, Hermes, and Codex originals are unchanged

## Portability

- [ ] No personal absolute paths
- [ ] No client identifiers not approved for sharing
- [ ] No runtime ownership contracts
- [ ] Required and optional dependencies are explicit
- [ ] Missing-tool fallback exists

## Security

- [ ] Secret scan passes
- [ ] No token, cookie, OAuth state, email archive, or private API
- [ ] No automatic external send/upload/publish/delete
- [ ] File-moving tools default to dry-run

## Plugin quality

- [ ] Marketplace JSON is valid
- [ ] All plugin manifests are valid
- [ ] Every skill has valid frontmatter and matching directory name
- [ ] Installation instructions are verified in a clean Claude Code environment
- [ ] One smoke scenario per plugin passes

## Remote verification

- [ ] Commit is pushed
- [ ] Remote default branch contains the expected commit
- [ ] Raw README and marketplace manifest are reachable
- [ ] GitHub Actions is green
- [ ] Install from the remote marketplace succeeds
