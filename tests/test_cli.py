"""Test cases for CLI functionality"""

import argparse
import os
import subprocess
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
import pytest
from agent_aider_worktree.cli import setup_arg_parser  # pylint: disable=wrong-import-position
from agent_aider_worktree.core import create_worktree, merge_and_push  # pylint: disable=wrong-import-position


def test_arg_parser_valid_arguments():
    """Test argument parser with valid inputs"""
    parser = setup_arg_parser()
    # Test valid arguments
    args = parser.parse_args(
        ["test task", "--path", "/tmp", "--model", "claude-3-opus"]
    )
    assert args.task == "test task"
    assert args.path == "/tmp"
    assert args.model == "claude-3-opus"
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


def test_main_execution_with_help():
    """Test main execution with --help flag"""
    result = subprocess.run(
        ["./agent-aider-worktree.py", "--help"],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    assert result.returncode == 0
    assert "Create git worktree" in result.stdout


def test_create_worktree_directory_creation(mocker, tmp_path):
    """Test worktree directory creation logic"""
    mocker.patch("agent_aider_worktree.core.run_command")
    test_repo = tmp_path / "testrepo"
    test_repo.mkdir()

    (test_repo / ".git").mkdir()  # Create fake git repo

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

    # Mock successful merge
    mock_run.return_value.returncode = 0
    # Include task in mock args
    mock_args = argparse.Namespace(task="test task", model="r1")
    assert merge_and_push("/tmp", "/repo", "branch", "main", mock_args) is True

    # Mock failed merge
    mock_run.return_value.returncode = 1
    assert merge_and_push("/tmp", "/repo", "branch", "main", mock_args) is False


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
        # Should raise error when path doesn't exist
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


def test_worktree_creation_with_special_chars(mocker):
    """Test worktree creation with special characters in task name"""
    mocker.patch("agent_aider_worktree.core.run_command")

    test_repo = "/tmp/testrepo"
    os.makedirs(test_repo, exist_ok=True)
    os.makedirs(os.path.join(test_repo, ".git"), exist_ok=True)

    task = "Test @#$%^&*()_+-=[]{}|;':,./<>?"
    worktree_path, branch_name, _ = create_worktree(test_repo, task)

    assert "test_" in worktree_path.lower()
    assert "test_" in branch_name.lower()


def test_merge_conflict_resolution(mocker):
    """Test merge conflict resolution workflow"""
    mock_run = mocker.patch("subprocess.run")
    mocker.patch("os.path.exists", return_value=True)
    # Simulate merge conflict then resolution
    mock_run.side_effect = [
        # Checkout main
        subprocess.CompletedProcess(args=[], returncode=0, stdout="", stderr=""),
        # Pull main
        subprocess.CompletedProcess(args=[], returncode=0, stdout="", stderr=""),
        # Pull worktree
        subprocess.CompletedProcess(args=[], returncode=0, stdout="", stderr=""),
        # First merge attempt fails
        subprocess.CompletedProcess(
            args=[], returncode=1, stdout="merge conflict", stderr=""
        ),
        # Conflict resolution
        subprocess.CompletedProcess(args=[], returncode=0, stdout="merged", stderr=""),
        # Status check
        subprocess.CompletedProcess(args=[], returncode=0, stdout="", stderr=""),
        # Push branch
        subprocess.CompletedProcess(args=[], returncode=0, stdout="", stderr=""),
        # Final merge
        subprocess.CompletedProcess(args=[], returncode=0, stdout="", stderr=""),
    ]

    mock_args = argparse.Namespace(task="test task", model="r1")
    assert merge_and_push("/tmp", "/repo", "branch", "main", mock_args) is True
