"""Test cases for core functionality"""

import sys
from pathlib import Path
from unittest.mock import Mock

sys.path.insert(0, str(Path(__file__).parent.parent))

from agent_aider_worktree.core import get_repo_name, run_command  # pylint: disable=wrong-import-position


def test_get_repo_name_ssh_url(mocker):
    """Test repo name extraction from SSH URL"""
    mock_result = Mock()
    mock_result.returncode = 0
    mock_result.stdout = "git@github.com:testuser/test-repo.git"
    mocker.patch("agent_aider_worktree.core.run_command", return_value=mock_result)
    repo_name = get_repo_name("/fake/path")
    assert repo_name == "test-repo"


def test_get_repo_name_https_url(mocker):
    """Test repo name extraction from HTTPS URL"""
    mock_result = Mock()
    mock_result.returncode = 0
    mock_result.stdout = "https://github.com/testuser/https-repo.git"
    mocker.patch("agent_aider_worktree.core.run_command", return_value=mock_result)
    repo_name = get_repo_name("/fake/path")
    assert repo_name == "https-repo"


def test_get_repo_name_failure(mocker):
    """Test repo name fallback when command fails"""
    mock_result = Mock()
    mock_result.returncode = 1
    mocker.patch("agent_aider_worktree.core.run_command", return_value=mock_result)
    repo_name = get_repo_name("/fake/path")
    assert repo_name == "unknown_repo"

def test_get_repo_name_ssh_url_with_subgroups(mocker):
    """Test repo name extraction from SSH URL with subgroups"""
    mock_result = Mock()
    mock_result.returncode = 0
    mock_result.stdout = "git@gitlab.com:mygroup/subgroup/myrepo.git"
    mocker.patch("agent_aider_worktree.core.run_command", return_value=mock_result)
    repo_name = get_repo_name("/fake/path")
    assert repo_name == "myrepo"

def test_get_repo_name_https_url_with_www(mocker):
    """Test repo name extraction from HTTPS URL with www"""
    mock_result = Mock()
    mock_result.returncode = 0
    mock_result.stdout = "https://www.github.com/orgname/reponame.git"
    mocker.patch("agent_aider_worktree.core.run_command", return_value=mock_result)
    repo_name = get_repo_name("/fake/path")
    assert repo_name == "reponame"

def test_get_repo_name_empty_remote_url(mocker):
    """Test repo name fallback when remote URL is empty"""
    mock_result = Mock()
    mock_result.returncode = 0
    mock_result.stdout = ""
    mocker.patch("agent_aider_worktree.core.run_command", return_value=mock_result)
    repo_name = get_repo_name("/fake/path")
    assert repo_name == "unknown_repo"


def test_run_command_success():
    """Test successful command execution"""
    result = run_command("echo 'test'", cwd="/tmp")
    assert result.returncode == 0
    assert "test" in result.stdout


def test_run_command_failure():
    """Test failed command execution"""
    result = run_command("exit 1", cwd="/tmp", check=False)
    assert result.returncode == 1
