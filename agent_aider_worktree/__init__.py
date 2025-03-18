"""Agent Aider Worktree package"""

from .core import create_worktree, merge_and_push
from .cli import setup_arg_parser
from agent-aider-worktree import main

__all__ = ["main", "setup_arg_parser", "create_worktree", "merge_and_push"]
