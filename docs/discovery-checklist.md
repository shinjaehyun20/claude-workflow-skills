# Public Release Checklist

Use this checklist before making a workflow-skill change publicly available.

## Repository package

- [ ] README has a clear audience, quick start, and package link.
- [ ] Registry, package directory, fixture, expected contract, and verification record agree.
- [ ] The package has no personal paths, customer identifiers, credentials, private endpoints, or private runtime dependencies.
- [ ] Static validation, Python compilation, and whitespace checks pass.
- [ ] A fresh Claude Code behavior smoke is recorded separately from static validation.

## GitHub surface

- [ ] Repository description explains the audience and value in one sentence.
- [ ] Relevant topics are set in the GitHub About panel.
- [ ] README, license, contributing guide, and security policy render correctly on the default branch.
- [ ] The pushed branch and pull request show only the intended files.
- [ ] After merge, raw file URLs and the default-branch commit are read back.

## Safety boundary

- [ ] Do not publish secrets, internal records, screenshots, or organization-specific workflow data.
- [ ] Do not claim behavior verification when only static validation has run.
- [ ] Do not claim a release is public until the remote default branch and its files are read back.
