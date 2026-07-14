# Native controls before automation

Use GitHub's own repository and organization controls before adding third-party automation. Native controls reduce code, token, network, and vendor trust boundaries; the kit should fill remaining intake and operating gaps.

## Baseline order

1. **Structure intake.** GitHub issue forms support required fields and validation. The kit deliberately avoids default issue labels because GitHub documents that a nonexistent label is not applied. [Issue form syntax](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms)
2. **Protect merge paths.** Require pull requests, approving reviews, status checks, and code-owner review where appropriate. [Rules available in rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets) · [CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)
3. **Constrain Actions.** Default `GITHUB_TOKEN` to read-only, allow only necessary Actions, require full-SHA pinning when the setting is available, and require approval for risky fork workflows. [Repository Actions settings](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository)
4. **Create a private security route.** Enable private vulnerability reporting before pointing an issue-template contact link to repository advisories. [Private vulnerability reporting](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/configure-vulnerability-reporting/configure-for-a-repository)
5. **Prepare a time-bounded incident control.** Interaction limits can temporarily restrict comments, issues, and pull requests to existing users, contributors, or collaborators and can expire automatically. [Repository interaction limits API](https://docs.github.com/en/rest/interactions/repos)
6. **Use PR admission controls only for severe load.** GitHub announced repository settings to disable pull requests or restrict them to collaborators. These are high-impact controls; document an owner, trigger, review date, and restoration condition. [GitHub announcement](https://github.com/orgs/community/discussions/187038)
7. **For organizations, add central policy.** Actions policies can constrain workflow events and actors across repositories, but GitHub currently marks the feature as public preview. [Actions policies](https://docs.github.com/en/organizations/managing-organization-settings/actions-policies/about-actions-policies)

## Mapping to kit profiles

| Native-control state | Kit choice |
| --- | --- |
| Baseline not reviewed | Do not install yet; fix repository settings first |
| Baseline set, effectiveness unknown | `observe` |
| A measured, recoverable status gate is needed | `balanced`; make the check required only after observation |
| Dependency and workflow supply-chain checks are also required | `hardened` |
| Active abuse flood | Use time-bounded native interaction or PR access controls; do not improvise permanent automation during the incident |

Reassess native features at least every 180 days: GitHub capabilities and plan availability change, and a new native control may remove the need for a third-party Action.
