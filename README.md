# Agent Aider Worktree

A CLI tool to manage git worktrees with AI-assisted development workflow using aider.

## Features

- Creates isolated git worktrees for tasks
- Integrates with aider for AI-assisted development
- Automated testing and linting
- Merge conflict resolution assistance
- Progress tracking and rich terminal UI

## Installation

```bash
pip install agent-aider-worktree
```

## Usage

```bash
agent-aider-worktree "Your task description here"
```

## Examples

Create a new feature:
```bash
agent-aider-worktree "Add user authentication system"
```

Fix a bug:
```bash
agent-aider-worktree "Fix login form validation bug"
```

## Testing

Run the test suite with:

```bash
python3.11 -m pytest tests/ -v
```

Tests include:
- README validation
- Worktree creation and management
- Branch naming conventions
- Conflict resolution handling

## Configuration

Configure through command line options:
```bash
agent-aider-worktree --model claude-3-opus --max-iterations 5 "Refactor database layer"
```

Common options:
- `--model`: Set AI model (default: r1)
- `--max-iterations`: Maximum attempts to fix issues
- `--all-files`: Include all files in AI context
- `--no-push`: Disable automatic merging to main

## Requirements

- Python 3.11+
- git 2.20+
- aider (installed automatically with package)
