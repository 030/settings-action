# settings-action

Settings Action that will configure the settings of a GitHub repository.

## Usage

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
      - uses: 030/settings-action@v0.6.0
        env:
          GH_TOKEN: ${{ secrets.SETTINGS_GUARD }}
        with:
          debug: false
          description: "Settings Action configures the settings of a GitHub repository."
          project: 030/settings-guard
          settings_delete_branch_on_merge: true
          settings_discussions: false
          settings_merge_commit: false
          settings_merge_rebase: false
          settings_merge_squash: true
          settings_protect_main_branch: true
          settings_protect_main_branch_enforce_admins: true
          settings_projects: false
          settings_wiki: false
```

use the following variables:

| Option                                      | Description                                   |
| ------------------------------------------- | --------------------------------------------- |
| debug                                       | Enable debug logging                          |
| description                                 | Change the description of a GitHub repository |
| project                                     | The owner/repo                                |
| settings_delete_branch_on_merge             | Delete a branch on merge or not               |
| settings_discussions                        | Enable the discussions tab or not             |
| settings_merge_commit                       | Enable merge commit                           |
| settings_merge_rebase                       | Enable merge request rebase                   |
| settings_merge_squash                       | Enable merge request squash                   |
| settings_protect_main_branch                | Protect the main branch or not                |
| settings_protect_main_branch_enforce_admins | Enforce branch protection for admins          |
| settings_projects                           | Whether the project tab should be enabled     |
| settings_wiki                               | Wiki enabled or not                           |

and create a token with read and admin permissions and store it as a
`SETTINGS_GUARD` variable in the variables menu.

## Testing

- [Install](https://github.com/cli/cli?tab=readme-ov-file#installation) gh cli.
- Create a read only token.
- Login: `gh auth login` and `choose token` option.
- Check [these graphql samples](https://gist.github.com/duboisf/68fb6e22ac0a2165ca298074f0e3b553)
  that can be useful while testing.
