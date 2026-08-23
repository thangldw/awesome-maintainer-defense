# Getting started

The auditor requires Python 3.10 or newer. It has no runtime dependencies and needs neither a GitHub token nor network access. Run it against a repository checkout you are authorized to inspect.

## Source checkout

```bash
git clone https://github.com/thangldw/awesome-maintainer-defense.git
cd awesome-maintainer-defense
make standalone
python3 dist/maintainer-defense-kit.py audit .
```

`make standalone` builds the executable artifact used by release packages. The audit reads policy, workflow, and local Git evidence; it does not execute code or write to the target.

## PyPI with pipx

```bash
pipx install maintainer-defense-kit==1.1.1
maintainer-defense audit /path/to/repository
```

## Standalone with checksum verification

On POSIX systems:

```bash
curl -fLO https://github.com/thangldw/awesome-maintainer-defense/releases/download/v1.1.1/maintainer-defense-kit.py
curl -fLO https://github.com/thangldw/awesome-maintainer-defense/releases/download/v1.1.1/maintainer-defense-kit.py.sha256
shasum -a 256 -c maintainer-defense-kit.py.sha256
python3 maintainer-defense-kit.py audit /path/to/repository
```

On PowerShell:

```powershell
Invoke-WebRequest https://github.com/thangldw/awesome-maintainer-defense/releases/download/v1.1.1/maintainer-defense-kit.py -OutFile maintainer-defense-kit.py
Invoke-WebRequest https://github.com/thangldw/awesome-maintainer-defense/releases/download/v1.1.1/maintainer-defense-kit.py.sha256 -OutFile maintainer-defense-kit.py.sha256
$Expected = ((Get-Content maintainer-defense-kit.py.sha256 -Raw).Trim() -split '\s+')[0].ToLowerInvariant()
$Actual = (Get-FileHash maintainer-defense-kit.py -Algorithm SHA256).Hash.ToLowerInvariant()
if ($Actual -ne $Expected) { Write-Error "SHA-256 mismatch"; exit 1 }
python maintainer-defense-kit.py audit C:\path\to\repository
```

## Interpret the first audit

Human output starts with severity counts. Each finding contains a stable rule ID, source location, observed evidence, threat scenario, and safe remediation. Confirm that the file is active and that any missing control is not enforced outside the checkout before accepting a finding.

Use JSON for automation and SARIF for compatible code-scanning systems:

```bash
maintainer-defense audit . --format json --output maintainer-defense.json
maintainer-defense audit . --format sarif --output maintainer-defense.sarif
maintainer-defense audit . --fail-on high
```

`--fail-on` exits with status 2 when the effective report contains a finding at or above the chosen severity. Invalid input or configuration exits with status 1.

## Generate a reviewable patch

```bash
maintainer-defense fix . --output recommended.patch
git apply --check recommended.patch
```

The command emits a patch only. Review it, test it, and obtain the repository owner's approval before applying it.

Next: [CLI reference](AUDITOR.md), [configuration](CONFIGURATION.md), [rule review](AUDITOR_RULES.md), and [operational playbook](PLAYBOOK.md).
