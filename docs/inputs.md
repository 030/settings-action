# Inputs

The inputs of the action, as used in the
[Quickstart](../README.md#quickstart) workflow:

| Option                                                       | Description                                                                                                                            |
| ------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------- |
| collaborators                                                | Comma-separated `username:permission` list to grant access, e.g. `alice:push,bob:admin`. See [Access](#access)                         |
| debug                                                        | Enable debug logging                                                                                                                   |
| description                                                  | Change the description of a GitHub repository                                                                                          |
| project                                                      | The owner/repo                                                                                                                         |
| settings_actions_allowed_actions                             | Actions permissions: `all`, `local_only`, or `selected`. Use `selected` to allow OWNER + specific non-OWNER actions/reusable workflows |
| settings_actions_github_owned_allowed                        | When `settings_actions_allowed_actions` is `selected`, whether GitHub-owned actions (e.g. `actions/checkout`) are allowed              |
| settings_actions_verified_allowed                            | When `settings_actions_allowed_actions` is `selected`, whether actions from verified creators are allowed                              |
| settings_actions_patterns_allowed                            | When `settings_actions_allowed_actions` is `selected`, comma-separated list of allowed actions/reusable workflows (e.g. `030/*`)       |
| settings_actions_require_sha_pinning                         | Require actions to be pinned to a full-length commit SHA                                                                               |
| settings_default_workflow_permissions                        | Set the default workflow permissions to read or write                                                                                  |
| settings_delete_branch_on_merge                              | Delete a branch on merge or not                                                                                                        |
| settings_discussions                                         | Enable the discussions tab or not                                                                                                      |
| settings_github_workflows_can_approve_pull_request_reviews   | Whether workflows can approve pull requests                                                                                            |
| settings_merge_commit                                        | Enable merge commit                                                                                                                    |
| settings_merge_rebase                                        | Enable merge request rebase                                                                                                            |
| settings_merge_squash                                        | Enable merge request squash                                                                                                            |
| settings_protect_main_branch                                 | Protect the main branch or not                                                                                                         |
| settings_protect_main_branch_enforce_admins                  | Enforce branch protection for admins                                                                                                   |
| settings_protect_main_branch_required_approving_review_count | The number of approvals that is required before a PR can be merged                                                                     |
| settings_projects                                            | Whether the project tab should be enabled                                                                                              |
| settings_wiki                                                | Wiki enabled or not                                                                                                                    |
| teams                                                        | Comma-separated `team-slug:permission` list of teams in the owner's organization, e.g. `maintainers:maintain`. See [Access](#access)   |
| topics                                                       | The topic(s) that will appear in the about menu of a project                                                                           |

## Access

`collaborators` and `teams` grant access to the repository. The permission is
one of `pull`, `triage`, `push`, `maintain` or `admin`; any other value, or an
entry that is not `name:permission`, fails the step before anything is
granted. Leave both empty to skip the step.

- A user who is not a collaborator yet gets an invitation.
- `teams` takes team slugs of the organization that owns the repository, so it
  does not work for repositories owned by a user.
- The token needs admin on the repository and, for `teams`, permission to
  manage the team in the organization (organization owner or team
  maintainer).

Access is additive only, by design: a collaborator or team that is not listed
keeps its access. Removing unlisted access would undo every grant made in the
GitHub UI and could lock people out after a typo, so revoking access stays a
manual step.
