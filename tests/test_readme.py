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
    assert (
        "pip install agent-aider-worktree" in installation_section.lower()
    ), "Missing correct pip installation command"


def test_readme_usage_section_formatting():
    """Verify usage section has proper code formatting with valid examples"""
    with open("README.md", "r", encoding="utf-8") as f:
        readme = f.read()

    # Extract usage section content
    usage_section = readme.split("## Usage")[1].split("##")[0]
    # Check for bash code blocks
    code_blocks = [block for block in usage_section.split("```") if block.strip()]
    bash_blocks = [block for block in code_blocks if block.startswith("bash")]
    assert len(bash_blocks) > 0, "No bash code blocks found in usage section"
    # Check for required command in any of the bash blocks
    command_found = any(
        "agent-aider-worktree.py" in block 
        for block in bash_blocks
    )
    assert command_found, "Missing example command in bash code blocks of usage section"
    # Verify command formatting in first bash block
    first_bash_block = bash_blocks[0]
    assert "agent-aider-worktree" in first_bash_block, \
        "Missing agent-aider-worktree command in first bash example"
    assert '"' in first_bash_block or "'" in first_bash_block, \
        "Task argument should be properly quoted in example command"
