import json
import re

import click

PERMISSIONS = ("pull", "triage", "push", "maintain", "admin")
# GitHub usernames: letters, digits and single hyphens. Team slugs: lowercase
# letters, digits, hyphens and underscores. Both end up in an API path, so
# nothing else is let through.
USERNAME = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?$")
TEAM_SLUG = re.compile(r"^[a-z0-9][a-z0-9_-]*$")


@click.group()
def cli():
    pass


@cli.command()
@click.option("--enforce-admins", default=True)
@click.option("--required-conversation-resolution", default=True)
@click.option("--required-approving-review-count", default=1)
def branch_protection_rules(
    enforce_admins,
    required_conversation_resolution,
    required_approving_review_count,
):
    required_conversation_resolution = required_conversation_resolution
    required_pull_request_reviews = None
    required_status_checks = None
    restrictions = None
    data = {
        "enforce_admins": enforce_admins,
        "required_conversation_resolution": required_conversation_resolution,
        "required_pull_request_reviews": required_pull_request_reviews,
        "required_status_checks": required_status_checks,
        "restrictions": restrictions,
    }
    if required_approving_review_count > 0:
        required_pull_request_reviews = {
            "required_pull_request_reviews": {
                "required_approving_review_count": required_approving_review_count
            }
        }
        data.update(required_pull_request_reviews)

    json_data = json.dumps(data, indent=4)
    print(json_data)
    with open("update-branch-protection-rule.json", "w") as f:
        json.dump(data, f, indent=2)


@cli.command()
@click.option(
    "--allowed-actions",
    default="all",
    type=click.Choice(["all", "local_only", "selected"]),
)
@click.option("--github-owned-allowed", default=True, type=bool)
@click.option("--verified-allowed", default=False, type=bool)
@click.option(
    "--patterns-allowed",
    default="",
    help="comma-separated list, e.g. OWNER/*,OWNER/repo@sha",
)
@click.option("--require-sha-pinning", default=False, type=bool)
def actions_permissions(
    allowed_actions,
    github_owned_allowed,
    verified_allowed,
    patterns_allowed,
    require_sha_pinning,
):
    # https://docs.github.com/en/rest/actions/permissions?apiVersion=2022-11-28#set-github-actions-permissions-for-a-repository
    # sha_pinning_required belongs on this endpoint's payload, not on
    # /actions/permissions/selected-actions.
    permissions_data = {
        "enabled": True,
        "allowed_actions": allowed_actions,
        "sha_pinning_required": require_sha_pinning,
    }
    print(json.dumps(permissions_data, indent=4))
    with open("update-actions-permissions.json", "w") as f:
        json.dump(permissions_data, f, indent=2)

    if allowed_actions == "selected":
        # https://docs.github.com/en/rest/actions/permissions?apiVersion=2022-11-28#set-allowed-actions-and-reusable-workflows-for-a-repository
        selected_data = {
            "github_owned_allowed": github_owned_allowed,
            "verified_allowed": verified_allowed,
            "patterns_allowed": [p for p in patterns_allowed.split(",") if p],
        }
        print(json.dumps(selected_data, indent=4))
        with open("update-actions-selected-actions.json", "w") as f:
            json.dump(selected_data, f, indent=2)


def parse_access(value, name_pattern, option):
    """Parse 'name:permission,...' into (name, permission) pairs."""
    entries = []
    for entry in value.split(","):
        entry = entry.strip()
        if not entry:
            continue
        name, sep, permission = entry.partition(":")
        if not sep or not name_pattern.match(name):
            raise click.BadParameter(
                f"'{entry}' is not 'name:permission'", param_hint=option
            )
        if permission not in PERMISSIONS:
            raise click.BadParameter(
                f"'{entry}' has permission '{permission}', expected one of "
                f"{', '.join(PERMISSIONS)}",
                param_hint=option,
            )
        entries.append((name, permission))
    return entries


@cli.command()
@click.option(
    "--collaborators",
    default="",
    help="comma-separated list, e.g. alice:push,bob:admin",
)
@click.option(
    "--teams",
    default="",
    help="comma-separated list, e.g. maintainers:maintain",
)
def access(collaborators, teams):
    """Validate the access inputs and print one 'kind name permission' line
    per entry, for action.yml to turn into API calls."""
    lines = [
        f"collaborator {name} {permission}"
        for name, permission in parse_access(
            collaborators, USERNAME, "'--collaborators'"
        )
    ] + [
        f"team {name} {permission}"
        for name, permission in parse_access(teams, TEAM_SLUG, "'--teams'")
    ]
    for line in lines:
        click.echo(line)


if __name__ == "__main__":
    cli()
