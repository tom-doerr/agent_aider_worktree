"""Test cases for CLI functionality"""

import sys
from pathlib import Path
import argparse
import subprocess
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
from agent_aider_worktree import (
    setup_arg_parser,
)


def test_arg_parser_valid_arguments():
    """Test argument parser with valid inputs"""
    parser = setup_arg_parser()
    # Test valid arguments
    args = parser.parse_args(["test task", "--path", "/tmp", "--model", "gpt4"])
    assert args.task == "test task"
    assert args.path == "/tmp"
    assert args.model == "gpt4"
    assert args.no_push is False
    assert args.max_iterations == 10


def test_arg_parser_invalid_arguments():
    """Test argument parser with invalid inputs"""
    parser = setup_arg_parser()
    with pytest.raises(SystemExit):
        parser.parse_args([])  # Missing required task argument


def test_cli_help_output():
    """Test the help output contains required information"""
    result = subprocess.run(
        ["./agent-aider-worktree.py", "--help"],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    help_output = result.stdout

    assert "Create git worktree" in help_output
    assert "--path" in help_output
    assert "--model" in help_output
    assert "examples" in help_output.lower()


def test_main_execution_with_help(capsys):
    """Test main execution with --help flag"""
    with pytest.raises(SystemExit):
        subprocess.run(["./agent-aider-worktree.py", "--help"], check=False)
    captured = capsys.readouterr()
    assert "Create git worktree" in captured.out


def test_create_worktree_directory_creation(mocker, tmp_path):
    """Test worktree directory creation logic"""
    mocker.patch("subprocess.run")
    test_repo = tmp_path / "testrepo"
    test_repo.mkdir()

    (test_repo / ".git").mkdir()  # Create fake git repo

    from agent_aider_worktree import (
        create_worktree,
    )  # pylint: disable=import-outside-toplevel

    worktree_path, branch_name, main_branch = create_worktree(
        str(test_repo), "test task"
    )

    assert "test_task" in worktree_path
    assert "test_task" in branch_name
    assert main_branch  # Should get current branch name


def test_merge_and_push_logic(mocker):
    """Test merge and push workflow"""
    mock_run = mocker.patch("subprocess.run")
    mocker.patch("os.path.exists", return_value=True)

    from agent_aider_worktree import (
        merge_and_push,
    )  # pylint: disable=import-outside-toplevel

    # Mock successful merge
    mock_run.return_value.returncode = 0
    assert (
        merge_and_push("/tmp", "/repo", "branch", "main", argparse.Namespace()) is True
    )

    # Mock failed merge
    mock_run.return_value.returncode = 1
    assert (
        merge_and_push("/tmp", "/repo", "branch", "main", argparse.Namespace()) is False
    )


def test_file_inclusion_logic():
    """Test file inclusion arguments work as expected"""
    parser = setup_arg_parser()

    # Test --all-files
    args = parser.parse_args(["task", "--all-files"])
    assert args.all_files is True

    # Test --no-python-files
    args = parser.parse_args(["task", "--no-python-files"])
    assert args.no_python_files is True


def test_invalid_model_handling():
    """Test handling of invalid model names"""
    parser = setup_arg_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["test task", "--model", "invalid-model"])

def test_invalid_path_handling():
    """Test handling of non-existent paths"""
    parser = setup_arg_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["test task", "--path", "/non/existent/path"])

def test_edge_cases():
    """Test edge case handling"""
    parser = setup_arg_parser()

    # Test very long task description
    long_task = "a" * 1000
    args = parser.parse_args([long_task])
    assert args.task == long_task
    # Test special characters in task
    special_task = "Fix $weird & characters! #123"
    args = parser.parse_args([special_task])
    assert args.task == special_task
