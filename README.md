# settings-action

Settings Action that will configure the settings of a GitHub repository.

## usage

| Option               | Description                                   |
| -------------------- | --------------------------------------------- |
| description          | Change the description of a GitHub repository |
| project              | The owner/repo                                |
| settings_discussions | Enable the discussions tab or not             |
| settings_projects    | Whether the project tab should be enabled     |
| settings_wiki        | Wiki enabled or not                           |

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
          settings_discussions: false
          settings_projects: false
          settings_wiki: false
```
