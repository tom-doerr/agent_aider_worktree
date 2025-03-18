"""CLI configuration for Agent Aider Worktree"""

import argparse
import os


def setup_arg_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser"""
    parser = argparse.ArgumentParser(
        description="Create git worktree, run AI-assisted coding until tests pass",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "Add user authentication feature"
  %(prog)s -p /path/to/repo "Fix bug in login form"
  %(prog)s --model claude-3-opus "Implement new feature"
  %(prog)s --inner-loop 5 "Refactor database code"
        """,
    )

    parser.add_argument("task", help="The task description to pass to aider")
    parser.add_argument(
        "-p",
        "--path",
        default=".",
        type=lambda p: p if os.path.exists(p) else argparse.ArgumentTypeError(f"Path {p} does not exist"),
        help="Path to the main git repository (default: current directory)",
    )
    parser.add_argument(
        "--no-push",
        action="store_true",
        help="Don't push changes back to main repository",
    )
    parser.add_argument(
        "--model",
        default="r1",
        choices=["r1", "claude-3-opus"],
        help="Model to use with aider (default: r1)",
    )
    parser.add_argument(
        "--max-iterations",
        type=int,
        default=10,
        help="Maximum number of iterations to run (default: 10)",
    )
    parser.add_argument(
        "--inner-loop",
        type=int,
        default=3,
        help="Number of inner loop iterations to run (default: 3)",
    )
    parser.add_argument(
        "--all-files",
        action="store_true",
        help="Include all files in the repository instead of just Python files",
    )
    parser.add_argument(
        "--no-python-files",
        action="store_true",
        help="Disable automatic inclusion of Python files",
    )

    return parser
