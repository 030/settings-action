import json
import click


@click.command()
@click.option('--enforce-admins', default=True)
@click.option('--required-conversation-resolution', default=True)
@click.option('--required-approving-review-count', default=1)
def branch_protection_rules(enforce_admins, required_conversation_resolution, required_approving_review_count):
    required_conversation_resolution = required_conversation_resolution
    required_pull_request_reviews = {"required_approving_review_count": required_approving_review_count}
    required_status_checks = None
    restrictions = None

    data = {
        "enforce_admins": enforce_admins,
        "required_conversation_resolution": required_conversation_resolution,
        "required_pull_request_reviews": required_pull_request_reviews,
        "required_status_checks": required_status_checks,
        "restrictions": restrictions
    }

    json_data = json.dumps(data, indent=4)
    print(json_data)

    with open('update-branch-protection-rule.json', 'w') as f:
        json.dump(data, f, indent=2)


if __name__ == '__main__':
    branch_protection_rules()
