# Agent Aider Worktree

A CLI tool to manage git worktrees with AI-assisted development workflows using the [aider](https://github.com/paul-gauthier/aider) library.

## Installation

### Poetry Installation

First install Poetry if you haven't already:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Then install the package:
```bash
git clone https://github.com/yourusername/agent-aider-worktree.git
cd agent-aider-worktree
poetry install
poetry shell  # Optional: activate virtual environment
```

### PyPI Installation (when published)
```bash
pip install agent-aider-worktree
```

## Development

```bash
poetry install --with dev  # Install dev dependencies
poetry run pytest  # Run tests
```

## Usage

```bash
poetry run agent-aider-worktree "Your task description here"
```

## Examples

Create a new feature:
```bash
poetry run agent-aider-worktree "Add user authentication system"
```

Fix a bug:
```bash
poetry run agent-aider-worktree "Fix login form validation bug"
```

## Configuration

Configure through command line options:
```bash
poetry run agent-aider-worktree --model claude-3-opus --max-iterations 5 "Refactor database layer"
```

Common options:
- `--model`: Set AI model (default: r1)
- `--max-iterations`: Maximum attempts to fix issues
- `--all-files`: Include all files in AI context
- `--no-push`: Disable automatic merging to main

## Usage

To use the CLI tool after installation:
```bash
poetry run agent-aider-worktree --help
```

## Requirements

- Python 3.11+
- git 2.20+
- Poetry 1.8+
- aider (installed automatically with package)
