"""Documentation quality checks."""

from __future__ import annotations

from pathlib import Path
from scorecard.models.result import CheckResult


def run_documentation_checks(repo_path: Path) -> list[CheckResult]:
    """Check documentation quality and completeness."""
    checks = []

    contributing = (repo_path / "CONTRIBUTING.md").exists()
    checks.append(CheckResult(name="CONTRIBUTING.md present", dimension="documentation",
        passed=contributing, weight=3,
        detail="" if contributing else "Add CONTRIBUTING.md to guide contributors"))

    changelog = (repo_path / "CHANGELOG.md").exists()
    checks.append(CheckResult(name="CHANGELOG.md present", dimension="documentation",
        passed=changelog, weight=2,
        detail="" if changelog else "Add CHANGELOG.md to track changes"))

    adr_dir = (repo_path / "docs" / "adr").exists()
    checks.append(CheckResult(name="ADR directory present", dimension="documentation",
        passed=adr_dir, weight=2,
        detail="" if adr_dir else "Add docs/adr/ for Architecture Decision Records"))

    has_examples = (repo_path / "docs" / "examples").exists() or (repo_path / "examples").exists()
    checks.append(CheckResult(name="Examples directory present", dimension="documentation",
        passed=has_examples, weight=2,
        detail="" if has_examples else "Add examples/ or docs/examples/ directory"))

    readme_path = repo_path / "README.md"
    has_quickstart = False
    if readme_path.exists():
        content = readme_path.read_text(errors="ignore").lower()
        has_quickstart = "quick start" in content or "getting started" in content or "installation" in content
    checks.append(CheckResult(name="README has quick start", dimension="documentation",
        passed=has_quickstart, weight=3,
        detail="" if has_quickstart else "Add a Quick start or Getting started section to README"))

    return checks