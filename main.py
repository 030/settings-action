import json
import click


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


if __name__ == "__main__":
    cli()
