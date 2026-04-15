"""innersource-scorecard CLI entry point."""

from __future__ import annotations

import json
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from scorecard.core.config import ScorecardConfig
from scorecard.core.engine import score_repo
from scorecard.models.result import score_to_grade

app = typer.Typer(name="innersource-scorecard", help="Inner-source health scorecard.")
console = Console()


@app.command("score")
def score(
    repo: str = typer.Argument(..., help="Repo path or name (e.g. brianpelow/repoforge)"),
    output_json: bool = typer.Option(False, "--json", help="Output as JSON"),
) -> None:
    """Score a repository against the inner-source health rubric."""
    config = ScorecardConfig.from_env()
    repo_path = Path(repo) if Path(repo).exists() else Path(".")
    repo_name = repo

    result = score_repo(repo_path, repo_name)

    if output_json:
        print(json.dumps(result.model_dump(), indent=2))
        return

    grade_color = {"A": "green", "B": "cyan", "C": "yellow", "D": "orange3", "F": "red"}.get(result.grade, "white")

    console.print(Panel.fit(
        f"Grade: [{grade_color}]{result.grade}[/{grade_color}]  Score: [bold]{result.overall_score}/100[/bold]\n"
        f"Repo: {result.repo}",
        title="Inner-source scorecard",
        border_style="blue",
    ))

    table = Table(border_style="dim", show_header=True)
    table.add_column("Dimension", style="bold")
    table.add_column("Score", justify="center")
    table.add_column("Grade", justify="center")
    table.add_column("Checks")

    for dim in result.dimensions:
        g = score_to_grade(dim.score)
        color = {"A": "green", "B": "cyan", "C": "yellow", "D": "orange3", "F": "red"}.get(g, "white")
        table.add_row(
            dim.name.title(),
            f"{dim.score}",
            f"[{color}]{g}[/{color}]",
            f"{dim.passed}/{dim.total} passed",
        )

    console.print(table)

    if result.recommendations:
        console.print("\n[bold]Top recommendations:[/bold]")
        for i, rec in enumerate(result.recommendations[:5], 1):
            console.print(f"  {i}. [dim]{rec}[/dim]")


@app.command("batch")
def batch(
    path: str = typer.Argument(".", help="Directory containing repos to score"),
    limit: int = typer.Option(20, "--limit", "-n"),
) -> None:
    """Score all repos in a directory."""
    base = Path(path)
    repos = [d for d in base.iterdir() if d.is_dir() and not d.name.startswith(".")][:limit]

    if not repos:
        console.print("[yellow]No repositories found.[/yellow]")
        return

    table = Table(title=f"Inner-source scorecard — {path}", border_style="dim")
    table.add_column("Repo", style="cyan")
    table.add_column("Score", justify="center")
    table.add_column("Grade", justify="center")

    for repo_dir in sorted(repos):
        result = score_repo(repo_dir, repo_dir.name)
        g = result.grade
        color = {"A": "green", "B": "cyan", "C": "yellow", "D": "orange3", "F": "red"}.get(g, "white")
        table.add_row(repo_dir.name, str(result.overall_score), f"[{color}]{g}[/{color}]")

    console.print(table)


def main() -> None:
    app()


if __name__ == "__main__":
    main()