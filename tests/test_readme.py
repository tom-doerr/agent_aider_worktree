"""Test cases for README.md validation"""

import argparse
import re
import subprocess
import sys
import time
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent))

from agent_aider_worktree import setup_arg_parser


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
        ["./agent-aider-worktree.py", "--help"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    help_output = result.stdout

    # Verify example commands exist and are properly formatted
    # Get actual examples from help output
    examples_section = help_output.split("Examples:")[1]
    examples = [
        line.strip() for line in examples_section.split("\n") 
        if line.strip() and not line.startswith("%")
    ]
    
    # Verify exact match of expected examples
    expected_examples = [
        "agent-aider-worktree \"Add user authentication feature\"",
        "agent-aider-worktree -p /path/to/repo \"Fix bug login login form\"",
        "agent-aider-worktree --model claude-3-opus \"Implement new feature\"",
        "-a-aider-worktree --inner-loop 5 \"Refactor database code\""
    ]
    assert examples == expected_examples, "Help examples don't match expected output"

    for example in examples:
        assert example in help_output, f"Missing example in help output: {example}"

    # Verify command format with different arguments
    assert re.search(
        r"agent-aider-worktree --model \w+ \"\w+.*\"", help_output
    )  # pylint: disable=line-too-long
    assert re.search(
        r"agent-aider-worktree -p \S+ \"\w+.*\"", help_output
    )  # pylint: disable=line-too-long


def test_arg_parser_configuration():
    """Test that all command-line arguments are properly configured"""
    # Create parser from main script
    parser = setup_arg_parser()

    # Test basic parser configuration
    assert isinstance(
        parser, argparse.ArgumentParser
    ), "setup_arg_parser should return an ArgumentParser instance"
    assert parser.description.startswith(
        "Create git worktree"
    ), "Missing correct description"
    assert parser.epilog, "Missing examples section in epilog"

    # Test task argument configuration
    def get_argument(parser, dest_name):
        """Helper to safely get an argument by its dest name"""
        for action in parser._actions:  # pylint: disable=protected-access
            if action.dest == dest_name:
                return action
        raise AssertionError(f"Argument with dest '{dest_name}' not found")

    # Verify task argument is positional and required
    task_arg = get_argument(parser, "task")
    assert task_arg.required, "Task argument should be required"
    assert not task_arg.option_strings, "Task argument should be positional"
    assert (
        task_arg.help == "The task description to pass to aider"
    ), "Incorrect help message"

    # Verify path argument configuration
    path_arg = get_argument(parser, "path")
    assert path_arg.default == ".", "Default path should be current directory"
    assert path_arg.type == str, "Path argument should be string type"
    assert "-p" in path_arg.option_strings, "Missing short option for path"
    assert "--path" in path_arg.option_strings, "Missing long option for path"

    # Verify model argument configuration
    model_arg = get_argument(parser, "model")
    assert model_arg.default == "r1", "Incorrect default model"
    assert (
        model_arg.help == "Model to use with aider (default: r1)"
    ), "Incorrect help message"

    # Verify max iterations configuration
    max_iter_arg = get_argument(parser, "max_iterations")
    assert max_iter_arg.default == 10, "Incorrect default max iterations"
    assert max_iter_arg.type == int, "Max iterations should be integer type"
    assert (
        "--max-iterations" in max_iter_arg.option_strings
    ), "Missing long option for max iterations"

    # Verify boolean flags
    no_push_arg = get_argument(parser, "no_push")
    assert no_push_arg.action == "store_true", "no_push should be a boolean flag"
