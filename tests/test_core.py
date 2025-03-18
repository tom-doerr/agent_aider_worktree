"""Test cases for core functionality"""

import sys
from pathlib import Path
from unittest.mock import Mock

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest

from agent_aider_worktree.core import get_repo_name, run_command

def test_get_repo_name_ssh_url(mocker):
    """Test repo name extraction from SSH URL"""
    mock_result = Mock()
    mock_result.returncode = 0
    mock_result.stdout = "git@github.com:testuser/test-repo.git"
    mocker.patch('agent_aider_worktree.core.run_command', return_value=mock_result)
    repo_name = get_repo_name("/fake/path")
    assert repo_name == "test-repo"

def test_get_repo_name_https_url(mocker):
    """Test repo name extraction from HTTPS URL"""
    mock_result = Mock()
    mock_result.returncode = 0
    mock_result.stdout = "https://github.com/testuser/https-repo.git"
    mocker.patch('agent_aider_worktree.core.run_command', return_value=mock_result)
    repo_name = get_repo_name("/fake/path")
    assert repo_name == "https-repo"

def test_get_repo_name_failure(mocker):
    """Test repo name fallback when command fails"""
    mock_result = Mock()
    mock_result.returncode = 1
    mocker.patch('agent_aider_worktree.core.run_command', return_value=mock_result)
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
