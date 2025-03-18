"""Agent Aider Worktree package"""

from .main import main
from .cli import setup_arg_parser
from .core import create_worktree, merge_and_push

__all__ = ["main", "setup_arg_parser", "create_worktree", "merge_and_push"]
