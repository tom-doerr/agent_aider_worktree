# Agent Aider Worktree

<!-- lint-disable -->
*A CLI tool* that manages git worktrees with AI-assisted development workflows using aider
<!-- lint-enable -->

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
- `--max-iterations`: Maximum attempts to fix issues (default: 10)
- `--all-files`: Include all files in AI context
- `--no-push`: Disable automatic merging to main
- `--verbose`: Show detailed debugging output

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository on GitHub
2. Create a new branch for your feature
3. Submit a pull request with your changes
4. Ensure all tests pass and documentation is updated

## License

MIT License - see [LICENSE](LICENSE) file for full text.

## Requirements

- **Python 3.11+** - Latest stable version recommended
- **git 2.20+** - Required for worktree functionality
- **aider** - AI pair programming tool (installed automatically)
