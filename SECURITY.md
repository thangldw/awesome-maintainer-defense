# Security policy

## Supported code

Security fixes are maintained for the latest published release and the current default branch. Older artifacts may remain downloadable but are not supported.

## Private reporting

Report suspected vulnerabilities through this repository's GitHub private vulnerability reporting interface. Include the affected version or commit, affected file, realistic impact, a minimal reproduction, and any known mitigation.

Do not place credentials, personal data, or unpatched exploit details in a public issue. If private reporting is unavailable, contact the repository owner through the private contact route on their GitHub profile.

## Scope boundary

This policy covers the auditor, installer, packaged skills, shipped workflows, build and release automation, and release artifacts. Catalog entries are independent projects; report their vulnerabilities to their own maintainers.

## Safe handling

Verify release checksums, review generated patches before application, pin third-party Actions to reviewed commits, and test workflow changes in a non-critical repository. A clean local audit does not establish that live GitHub settings or external services are secure.
