"""Test cases for README.md validation"""

from pathlib import Path


def test_readme_exists():
    """Check that README.md exists"""
    assert Path("README.md").exists(), "README.md file not found"


def test_readme_contents():
    """Check README.md is not empty and contains key sections"""
    readme = Path("README.md").read_text(encoding="utf-8")
    assert len(readme) >= 500, "README.md seems too short"
    assert "# Agent Aider Worktree" in readme, "Missing main header in README.md"
    assert "## Installation" in readme, "Missing Installation section in README.md"
    assert "### Poetry Installation" in readme, "Missing Poetry installation instructions"
    assert "## Usage" in readme, "Missing Usage section in README.md"
