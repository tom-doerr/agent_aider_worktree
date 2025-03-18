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
    assert "## Usage" in readme, "Missing Usage section in README.md"
    assert "## License" in readme, "Missing License section in README.md"
    assert "MIT License" in readme, "Missing license information"

def test_readme_installation_instructions():
    """Validate installation instructions are correct"""
    with open("README.md", "r", encoding="utf-8") as f:
        readme = f.read()
        
    installation_section = readme.split("## Installation")[1].split("##")[0]
    assert "pip install agent-aider-worktree" in installation_section.lower(), "Missing correct pip installation command"

def test_readme_usage_section_formatting():
    """Verify usage section has proper code formatting"""
    with open("README.md", "r", encoding="utf-8") as f:
        readme = f.read()
    
    usage_section = readme.split("## Usage")[1].split("##")[0]
    assert "```bash" in usage_section, "Missing bash code block in usage section"
    assert "agent-aider-worktree.py" in usage_section, "Missing example command in usage section"
