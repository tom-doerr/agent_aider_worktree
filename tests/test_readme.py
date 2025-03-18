"""Test cases for README.md validation"""

import re
import subprocess
import argparse
from pathlib import Path
from agent_aider_worktree import main


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
    # Check README exists first
    assert Path("README.md").exists()
    with open("README.md", "r", encoding="utf-8") as f:
        readme = f.read()

    # Extract usage section content
    usage_section = readme.split("## Usage")[1].split("##")[0]
    # Check for bash code blocks
    code_blocks = [block for block in usage_section.split("```") if block.strip()]
    bash_blocks = [block for block in code_blocks if block.startswith("bash")]
    assert len(bash_blocks) > 0, "No bash code blocks found in usage section"
    # Check for required command patterns in bash blocks
    required_patterns = [r"agent-aider-worktree(\s+--[\w-]+)*\s+['\"][^\"']+['\"]"]

    pattern_found = False
    for block in bash_blocks:
        if any(re.search(pattern, block) for pattern in required_patterns):
            pattern_found = True
            # Verify command formatting
            assert (
                '"' in block or "'" in block
            ), f"Task argument should be properly quoted in example command: {block}"
            assert (
                "agent-aider-worktree" in block
            ), f"Missing agent-aider-worktree command in bash example: {block}"
            assert (
                len(block.split()) >= 2
            ), f"Command should include a task argument: {block}"

    assert (
        pattern_found
    ), "Missing valid example command in bash code blocks of usage section"


def test_help_output_examples():
    """Test that the help output contains valid examples"""
    result = subprocess.run(
        ["agent-aider-worktree.py", "--help"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    help_output = result.stdout

    # Verify example commands exist and are properly formatted
    examples = [
        "Add user authentication feature",
        "Fix bug in login form",
        "Implement new feature",
        "Refactor database code",
    ]

    for example in examples:
        assert example in help_output, f"Missing example in help output: {example}"

    # Verify command format with different arguments
    assert re.search(r"agent-aider-worktree --model \w+ \"\w+.*\"", help_output)
    assert re.search(r"agent-aider-worktree -p \S+ \"\w+.*\"", help_output)


def test_arg_parser_configuration():
    """Test that all command-line arguments are properly configured"""
    # Create parser from main script
    parser = argparse.ArgumentParser()
    main.setup_arg_parser(parser)

    # Verify required positional argument (pylint: disable=protected-access)
    assert (
        "task" in parser._positionals._actions[1].dest
    )  # pylint: disable=protected-access
    assert parser._positionals._actions[1].required  # pylint: disable=protected-access

    # Verify path argument
    path_arg = [a for a in parser._actions if a.dest == "path"][
        0
    ]  # pylint: disable=protected-access
    assert path_arg.default == "."
    assert (
        path_arg.help == "Path to the main git repository (default: current directory)"
    )

    # Verify model argument
    model_arg = [a for a in parser._actions if a.dest == "model"][
        0
    ]  # pylint: disable=protected-access
    assert model_arg.default == "r1"

    # Verify max iterations
    max_iter_arg = [a for a in parser._actions if a.dest == "max_iterations"][
        0
    ]  # pylint: disable=protected-access
    assert max_iter_arg.default == 10
    assert max_iter_arg.type == int
