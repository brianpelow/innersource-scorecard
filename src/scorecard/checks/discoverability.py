"""Discoverability checks."""

from __future__ import annotations

from pathlib import Path
from scorecard.models.result import CheckResult


def run_discoverability_checks(repo_path: Path) -> list[CheckResult]:
    """Check how discoverable and self-describing the repo is."""
    checks = []

    readme = (repo_path / "README.md").exists() or (repo_path / "readme.md").exists()
    checks.append(CheckResult(name="README present", dimension="discoverability",
        passed=readme, weight=3, detail="" if readme else "Missing README.md"))

    readme_path = repo_path / "README.md"
    readme_substantial = False
    if readme_path.exists():
        content = readme_path.read_text(errors="ignore")
        readme_substantial = len(content) >= 500 and "##" in content
    checks.append(CheckResult(name="README has sections", dimension="discoverability",
        passed=readme_substantial, weight=2,
        detail="" if readme_substantial else "README lacks sections or is too short"))

    license_present = (repo_path / "LICENSE").exists() or (repo_path / "LICENSE.md").exists()
    checks.append(CheckResult(name="LICENSE present", dimension="discoverability",
        passed=license_present, weight=3, detail="" if license_present else "Missing LICENSE file"))

    gitignore = (repo_path / ".gitignore").exists()
    checks.append(CheckResult(name=".gitignore present", dimension="discoverability",
        passed=gitignore, weight=1, detail="" if gitignore else "Missing .gitignore"))

    has_description = _check_description(repo_path)
    checks.append(CheckResult(name="Repo has description", dimension="discoverability",
        passed=has_description, weight=2,
        detail="" if has_description else "Add a GitHub repo description"))

    return checks


def _check_description(repo_path: Path) -> bool:
    readme = repo_path / "README.md"
    if not readme.exists():
        return False
    content = readme.read_text(errors="ignore")
    lines = [l.strip() for l in content.splitlines() if l.strip()]
    return len(lines) >= 3 and any(len(l) > 30 for l in lines[1:4])