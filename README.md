# Awesome Maintainer Defense

[English](README.md) · [Tiếng Việt](README.vi.md) · [日本語](README.ja.md)

Awesome Maintainer Defense is an offline, read-only repository auditor and a set of reversible maintainer controls. It inspects local governance files and GitHub Actions trust boundaries without a token or network request. It does not execute repository code, inspect live GitHub settings, or identify who wrote a contribution.

## Quickstart

Python 3.10 or newer is required.

```bash
make standalone
python3 dist/maintainer-defense-kit.py audit .
```

The audit prints evidence, severity, and a stable rule ID. A finding is a review lead, not proof that a repository is compromised or a contributor is malicious.

## What the auditor checks

- Missing security, ownership, structured-intake, dependency-update, and branch-policy evidence.
- Excessive workflow token authority, mutable Action references, privileged execution of pull-request input, shell interpolation, and unsafe cross-workflow artifacts.
- Destructive moderation, identity/history proxies, and missing appeal paths.

The rule registry and review requirements are in [Auditor rules](docs/AUDITOR_RULES.md).

## From finding to reviewed patch

`fix` generates a unified diff and never edits the target repository:

```bash
python3 dist/maintainer-defense-kit.py fix . --output recommended.patch
git apply --check recommended.patch
```

Review the evidence and patch in repository context. Apply it only through the repository's normal ownership and CI process.

## Evidence boundaries

Tested contracts cover deterministic detection, JSON/SARIF output, patch-only remediation, installer conflict handling, and shipped workflow invariants. The project does not claim field accuracy across representative repositories, live GitHub-settings coverage, compliance, or proof of authorship or intent. See [Kit assurance](docs/KIT_ASSURANCE.md) and [Threat model](docs/THREAT_MODEL.md).

## Install options

PyPI with an isolated application environment:

```bash
pipx install maintainer-defense-kit==1.1.1
maintainer-defense audit .
```

Verified standalone on POSIX systems:

```bash
curl -fLO https://github.com/thangldw/awesome-maintainer-defense/releases/download/v1.1.1/maintainer-defense-kit.py
curl -fLO https://github.com/thangldw/awesome-maintainer-defense/releases/download/v1.1.1/maintainer-defense-kit.py.sha256
shasum -a 256 -c maintainer-defense-kit.py.sha256
python3 maintainer-defense-kit.py audit .
```

Verified standalone on PowerShell:

```powershell
Invoke-WebRequest https://github.com/thangldw/awesome-maintainer-defense/releases/download/v1.1.1/maintainer-defense-kit.py -OutFile maintainer-defense-kit.py
Invoke-WebRequest https://github.com/thangldw/awesome-maintainer-defense/releases/download/v1.1.1/maintainer-defense-kit.py.sha256 -OutFile maintainer-defense-kit.py.sha256
$Expected = ((Get-Content maintainer-defense-kit.py.sha256 -Raw).Trim() -split '\s+')[0].ToLowerInvariant()
$Actual = (Get-FileHash maintainer-defense-kit.py -Algorithm SHA256).Hash.ToLowerInvariant()
if ($Actual -ne $Expected) { Write-Error "SHA-256 mismatch"; exit 1 }
python maintainer-defense-kit.py audit .
```

Release channels and recovery rules are documented in [Distribution](docs/DISTRIBUTION.md).

## Documentation

- [Getting started](docs/GETTING_STARTED.md)
- [Auditor CLI](docs/AUDITOR.md)
- [Configuration](docs/CONFIGURATION.md)
- [Operational playbook](docs/PLAYBOOK.md)
- [Documentation map](docs/README.md)

## Curated catalog

The catalog is a secondary, evidence-reviewed index of maintainer-defense resources. Inclusion is not an endorsement. Review permissions, data boundaries, maximum effects, maintenance state, and licensing before adoption. See the generated [catalog](docs/CATALOG.md).

## Contributing and support

Read [Contributing](CONTRIBUTING.md) before proposing a rule, product change, translation, or catalog entry. Use [Support](SUPPORT.md) for public requests and [Security](SECURITY.md) for private vulnerability reporting.

## License

Released under the [MIT License](LICENSE).
