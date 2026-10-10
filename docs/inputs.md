# Inputs

The inputs of the action, as used in the
[Quickstart](../README.md#quickstart) workflow:

| Option                                                       | Description                                                                                                                            |
| ------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------- |
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
| topics                                                       | Comma-separated topics of a project. Replaces all topics: topics that are not listed are removed                                       |
