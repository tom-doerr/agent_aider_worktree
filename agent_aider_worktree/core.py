"""Core functionality for Agent Aider Worktree"""

import os
import time
import subprocess
from typing import NamedTuple
from rich.console import Console
from rich.panel import Panel

console = Console()


def get_repo_name(repo_path):
    """Get the repository name from the git remote URL."""
    result = run_command("git remote get-url origin", cwd=repo_path)
    if result.returncode != 0:
        return "unknown_repo"

    remote_url = result.stdout.strip()
    repo_name = remote_url.split("/")[-1].replace(".git", "")
    return repo_name


def run_tests(worktree_path):
    """Run pytest and return True if all tests pass."""
    console.print(Panel("[bold]Running Tests[/bold]", style="blue"))
    result = run_command("pytest", cwd=worktree_path, check=False)
    if result.returncode == 0:
        console.print(Panel("[bold]All Tests Passed![/bold]", style="green"))
    else:
        console.print(Panel("[bold]Tests Failed[/bold]", style="red"))
    return result.returncode == 0


class CommandResult(NamedTuple):
    """Result container for command execution outcomes"""

    returncode: int
    stdout: str
    stderr: str


def run_command(cmd, cwd=None, capture_output=True, check=True, env=None):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            shell=True,
            text=True,
            capture_output=capture_output,
            check=check,
            env=env or os.environ.copy(),
        )
        return CommandResult(
            result.returncode, result.stdout.strip(), result.stderr.strip()
        )
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]Command failed:[/bold red] {cmd}")
        console.print(f"[red]Error:[/red] {e.stderr}")
        return CommandResult(e.returncode, e.stdout, e.stderr)


def create_worktree(repo_path, task_name):
    """Create a new git worktree for the task."""
    # (Keep the exact same implementation as in agent-aider-worktree.py)
    repo_name = get_repo_name(repo_path)
    worktree_base = os.path.expanduser(f"~/worktrees/{repo_name}")

    os.makedirs(worktree_base, exist_ok=True)
    safe_task_name = "".join(c if c.isalnum() else "_" for c in task_name)
    safe_task_name = safe_task_name[:50]
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    worktree_path = os.path.join(worktree_base, f"{safe_task_name}_{timestamp}")

    result = run_command("git branch --show-current", cwd=repo_path)
    current_branch = result.stdout.strip()
    branch_name = f"task/{safe_task_name}_{timestamp}"
    console.print(f"[bold green]Creating new branch:[/bold green] {branch_name}")
    run_command(f"git branch {branch_name}", cwd=repo_path)
    console.print(f"[bold green]Creating worktree at:[/bold green] {worktree_path}")
    run_command(f"git worktree add {worktree_path} {branch_name}", cwd=repo_path)
    return worktree_path, branch_name, current_branch


def run_aider(worktree_path, task, _args, _model="r1"):
    """Run aider with the given task."""
    console.print(Panel(f"[bold]Running aider with task:[/bold]\n{task}", style="cyan"))
    # Actual implementation from agent-aider-worktree.py would go here
    # Placeholder implementation for testing:
    console.print("[dim]Mocking aider execution[/dim]")
    return True


def merge_and_push(worktree_path, main_repo_path, branch_name, main_branch, args):
    """Merge changes from main, then push if no conflicts."""
    try:
        run_command(f"git checkout {main_branch}", cwd=main_repo_path)
        run_command("git pull", cwd=main_repo_path)
        run_command(f"git pull origin {main_branch}", cwd=worktree_path, check=False)
        status = run_command("git status", cwd=worktree_path)
        if (
            "You have unmerged paths" in status.stdout
            or "fix conflicts" in status.stdout
        ):
            console.print("[bold red]Merge conflicts detected...[/bold red]")
            conflict_task = (
                f"Please resolve the merge conflicts. Original task: {args.task}"
            )
            run_aider(worktree_path, conflict_task, args, model=args.model)
            status = run_command("git status", cwd=worktree_path)
            if (
                "You have unmerged paths" in status.stdout
                or "fix conflicts" in status.stdout
            ):
                console.print("[bold red]Merge conflicts unresolved[/bold red]")
                return False
        run_command("git commit -am 'Merge from main'", cwd=worktree_path, check=False)
        tests_pass = run_tests(worktree_path)
        if not tests_pass:
            fix_task = f"Fix failing tests. Original task: {args.task}"
            run_aider(worktree_path, fix_task, args, model=args.model)
            tests_pass = run_tests(worktree_path)
            if not tests_pass:
                return False
        run_command(f"git push -u origin {branch_name}", cwd=worktree_path)
        result = run_command(
            f"git checkout {main_branch} && git merge {branch_name} && git push",
            cwd=main_repo_path,
            check=False,
        )
        if result.returncode != 0:
            return False
        return True
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]Error during merge:[/bold red] {str(e)}")
        return False
