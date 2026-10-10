import json

from click.testing import CliRunner

from main import cli


def test_branch_protection_rules_default_output(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()

    result = runner.invoke(cli, ["branch-protection-rules"])

    assert result.exit_code == 0

    output_file = tmp_path / "update-branch-protection-rule.json"
    assert output_file.exists()

    data = json.loads(output_file.read_text())
    assert data["enforce_admins"] is True
    assert data["required_conversation_resolution"] is True
    assert data["required_pull_request_reviews"] == {
        "required_approving_review_count": 1
    }
    assert data["required_status_checks"] is None
    assert data["restrictions"] is None


def test_branch_protection_rules_zero_required_approving_review_count(
    tmp_path, monkeypatch
):
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()

    result = runner.invoke(
        cli,
        [
            "branch-protection-rules",
            "--required-approving-review-count",
            "0",
        ],
    )

    assert result.exit_code == 0

    data = json.loads(
        (tmp_path / "update-branch-protection-rule.json").read_text()
    )
    # required_pull_request_reviews stays None when the count is 0
    assert data["required_pull_request_reviews"] is None


def test_actions_permissions_all_does_not_write_selected_actions_file(
    tmp_path, monkeypatch
):
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()

    result = runner.invoke(
        cli,
        [
            "actions-permissions",
            "--allowed-actions",
            "all",
            "--require-sha-pinning",
            "true",
        ],
    )

    assert result.exit_code == 0

    permissions_file = tmp_path / "update-actions-permissions.json"
    assert permissions_file.exists()

    data = json.loads(permissions_file.read_text())
    assert data == {
        "enabled": True,
        "allowed_actions": "all",
        "sha_pinning_required": True,
    }

    # selected-actions payload is only relevant when allowed_actions == "selected"
    assert not (tmp_path / "update-actions-selected-actions.json").exists()


def test_actions_permissions_selected_writes_both_files(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()

    result = runner.invoke(
        cli,
        [
            "actions-permissions",
            "--allowed-actions",
            "selected",
            "--github-owned-allowed",
            "true",
            "--verified-allowed",
            "false",
            "--patterns-allowed",
            "030/*,actions/checkout@*",
            "--require-sha-pinning",
            "true",
        ],
    )

    assert result.exit_code == 0

    permissions_data = json.loads(
        (tmp_path / "update-actions-permissions.json").read_text()
    )
    assert permissions_data == {
        "enabled": True,
        "allowed_actions": "selected",
        "sha_pinning_required": True,
    }

    selected_data = json.loads(
        (tmp_path / "update-actions-selected-actions.json").read_text()
    )
    assert selected_data == {
        "github_owned_allowed": True,
        "verified_allowed": False,
        "patterns_allowed": ["030/*", "actions/checkout@*"],
    }
    # sha_pinning_required must never end up in the selected-actions payload
    assert "sha_pinning_required" not in selected_data


def test_actions_permissions_empty_patterns_allowed_filtered_out(
    tmp_path, monkeypatch
):
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()

    result = runner.invoke(
        cli,
        [
            "actions-permissions",
            "--allowed-actions",
            "selected",
            "--patterns-allowed",
            "",
        ],
    )

    assert result.exit_code == 0

    selected_data = json.loads(
        (tmp_path / "update-actions-selected-actions.json").read_text()
    )
    assert selected_data["patterns_allowed"] == []


def test_actions_permissions_rejects_invalid_allowed_actions(
    tmp_path, monkeypatch
):
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()

    result = runner.invoke(
        cli,
        ["actions-permissions", "--allowed-actions", "not-a-real-choice"],
    )

    assert result.exit_code != 0


def test_access_prints_collaborators_and_teams():
    runner = CliRunner()

    result = runner.invoke(
        cli,
        [
            "access",
            "--collaborators",
            "alice:push, bob-2:admin,",
            "--teams",
            "maintainers:maintain,ci_bots:triage",
        ],
    )

    assert result.exit_code == 0
    assert result.output.splitlines() == [
        "collaborator alice push",
        "collaborator bob-2 admin",
        "team maintainers maintain",
        "team ci_bots triage",
    ]


def test_access_empty_inputs_print_nothing():
    runner = CliRunner()

    result = runner.invoke(cli, ["access"])

    assert result.exit_code == 0
    assert result.output == ""


def test_access_rejects_unknown_permission():
    runner = CliRunner()

    result = runner.invoke(cli, ["access", "--collaborators", "alice:write"])

    assert result.exit_code != 0
    assert "permission 'write'" in result.output


def test_access_rejects_entry_without_permission():
    runner = CliRunner()

    result = runner.invoke(cli, ["access", "--teams", "maintainers"])

    assert result.exit_code != 0
    assert "'maintainers' is not 'name:permission'" in result.output


def test_access_rejects_names_that_are_not_a_single_path_segment():
    runner = CliRunner()

    for option, value in [
        ("--collaborators", "../alice:push"),
        ("--collaborators", "al ice:push"),
        ("--teams", "030/maintainers:maintain"),
        ("--teams", "Maintainers:maintain"),
    ]:
        result = runner.invoke(cli, ["access", option, value])

        assert result.exit_code != 0, value
