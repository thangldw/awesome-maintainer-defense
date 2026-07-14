# Workflow-hardening starter kit

This kit adds two independent checks:

- dependency review for newly introduced vulnerabilities and license policy;
- zizmor static analysis for GitHub Actions workflows.

Both Actions are pinned to full commit SHAs. Review those commits and upstream release notes before updating. Dependency Review is available for public repositories and private repositories with GitHub Advanced Security. The zizmor workflow is configured without Advanced Security and reports through the job log.

The workflows use `pull_request`, not `pull_request_target`, and receive read-only repository permissions. They inspect untrusted content but do not run the project's build or package-manager commands.

Adjust vulnerability severity and license policy to your project. A passing result is not proof that a contribution is safe.
