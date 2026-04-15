"""Adoption signal checks."""

from __future__ import annotations

from pathlib import Path
from scorecard.models.result import CheckResult


def run_adoption_checks(repo_path: Path, github_stats: dict | None = None) -> list[CheckResult]:
    """Check adoption signals for the repo."""
    checks = []
    stats = github_stats or {}

    has_recent_commit = _check_recent_activity(repo_path)
    checks.append(CheckResult(name="Recent commit activity", dimension="adoption",
        passed=has_recent_commit, weight=3,
        detail="" if has_recent_commit else "No recent commits detected"))

    has_tests = (repo_path / "tests").exists() and \
        any(repo_path.rglob("test_*.py"))
    checks.append(CheckResult(name="Test suite present", dimension="adoption",
        passed=has_tests, weight=3,
        detail="" if has_tests else "Add a test suite to build contributor confidence"))

    has_docker = (repo_path / "Dockerfile").exists() or \
        (repo_path / "docker-compose.yml").exists()
    checks.append(CheckResult(name="Docker support present", dimension="adoption",
        passed=has_docker, weight=2,
        detail="" if has_docker else "Add Dockerfile or docker-compose.yml for easy local setup"))

    stars = stats.get("stargazers_count", 0)
    checks.append(CheckResult(name="Has GitHub stars", dimension="adoption",
        passed=stars > 0, weight=1,
        detail=f"{stars} stars" if stars > 0 else "No stars yet"))

    has_nightly = _check_nightly_agent(repo_path)
    checks.append(CheckResult(name="Nightly agent workflow present", dimension="adoption",
        passed=has_nightly, weight=2,
        detail="" if has_nightly else "Add nightly agent workflow for autonomous activity"))

    return checks


def _check_recent_activity(repo_path: Path) -> bool:
    changelog = repo_path / "CHANGELOG.md"
    if changelog.exists():
        import re
        content = changelog.read_text(errors="ignore")
        dates = re.findall(r"\d{4}-\d{2}-\d{2}", content)
        if dates:
            from datetime import date
            try:
                latest = max(date.fromisoformat(d) for d in dates)
                return (date.today() - latest).days < 180
            except ValueError:
                pass
    return (repo_path / ".git").exists()


def _check_nightly_agent(repo_path: Path) -> bool:
    workflows = repo_path / ".github" / "workflows"
    if not workflows.exists():
        return False
    for wf in workflows.glob("*.yml"):
        content = wf.read_text(errors="ignore")
        if "cron" in content and ("nightly" in content.lower() or "agent" in content.lower()):
            return True
    return False