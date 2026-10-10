# settings-action

[![GitHub release](https://img.shields.io/github/v/release/030/settings-action)](https://github.com/030/settings-action/releases)
[![License](https://img.shields.io/github/license/030/settings-action)](LICENSE)

<img src="./assets/logos/settings-action.png" width="250"></a>

Settings Action that will configure the settings of a GitHub repository.

## Quickstart

1. Create a `~/.github/workflows/settings-guard.yml` file:

   ```bash
   ---
   name: settings-guard
   'on':
     schedule:
       - cron: '42 6 * * *'
   permissions: {}
   jobs:
     settings-action:
       runs-on: ubuntu-22.04
       steps:
         - uses: 030/settings-action@v0.8.0
           env:
             GH_TOKEN: ${{ secrets.SETTINGS_GUARD }}
           with:
             debug: false
             description: "Settings Action configures the settings of a GitHub repository."
             project: 030/settings-guard
             settings_actions_allowed_actions: "selected"
             settings_actions_github_owned_allowed: true
             settings_actions_verified_allowed: false
             settings_actions_patterns_allowed: "030/*"
             settings_actions_require_sha_pinning: true
             settings_default_workflow_permissions: "read"
             settings_delete_branch_on_merge: true
             settings_discussions: false
             settings_github_workflows_can_approve_pull_request_reviews: true
             settings_merge_commit: false
             settings_merge_rebase: false
             settings_merge_squash: true
             settings_protect_main_branch: true
             settings_protect_main_branch_enforce_admins: true
             settings_protect_main_branch_required_approving_review_count: 1
             settings_projects: false
             settings_wiki: false
             topics: composite-action,github-project-setup,github-settings,settings-as-code
   ```

1. Create a token with read and admin permissions on the repository.
1. Store it as a `SETTINGS_GUARD` secret in the repository settings.

## Documentation

- [Inputs](docs/inputs.md): every option the action accepts.
- [Testing](docs/testing.md): testing the action locally.
