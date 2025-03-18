# pylint: skip-file
# Agent Aider Worktree [![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Agent Aider Worktree is a CLI tool that manages git worktrees with AI-assisted development workflow using [aider](https://github.com/paul-gauthier/aider).

## Features

- Creates isolated git worktrees for tasks
- Integrates with aider for AI-assisted development
- Automated testing and linting
- Merge conflict resolution assistance
- Progress tracking and rich terminal UI

## Installation

Install using pip:

```bash
pip install agent-aider-worktree
```

Requirements:
- Python 3.11+
- git 2.20+

## Usage

```bash
agent-aider-worktree "Your task description here"
```

Key features:
- Automatically creates isolated git worktree
- Runs tests and linters continuously
- Integrates with aider for AI-assisted coding

Example workflow:
```bash
# Create a new feature branch
agent-aider-worktree "Add user authentication feature"

# Fix existing code (using shorter alias)
agent-aider-worktree --model claude-3-opus "Repair broken login form validation"
```

> [!NOTE]
> You can use `aaw` as a shortcut alias for `agent-aider-worktree` after installation

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

## Contributing

Contributions are welcome! Please open an issue first to discuss proposed changes.

## License

MIT License - See [LICENSE](LICENSE) for details

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
