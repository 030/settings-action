# settings-action

Settings Action that will configure the settings of a GitHub repository.

## usage

Create a `~/.github/workflows/settings-guard.yml` file:

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
      - uses: 030/settings-action@v0.2.0
        env:
          GH_TOKEN: ${{ secrets.SETTINGS_GUARD }}
        with:
          project: 030/settings-guard
          description: "Settings Action configures the settings of a GitHub repository."
          settings_delete_branch_on_merge: true
          settings_discussions: false
          # ensure that at least one of the following settings_merge_x options
          # is true and that the first of these keys is set to true
          settings_merge_squash: true
          settings_merge_commit: false
          settings_merge_rebase: false
          settings_projects: false
          settings_wiki: false
```

variables:

| Option                | Description                                   |
| --------------------- | --------------------------------------------- |
| description           | Change the description of a GitHub repository |
| project               | The owner/repo                                |
| settings_discussions  | Enable the discussions tab or not             |
| settings_merge_commit | Enable merge commit                           |
| settings_merge_rebase | Enable merge request rebase                   |
| settings_merge_squash | Enable merge request squash                   |
| settings_projects     | Whether the project tab should be enabled     |
| settings_wiki         | Wiki enabled or not                           |
