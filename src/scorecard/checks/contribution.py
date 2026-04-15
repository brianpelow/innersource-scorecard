"""Contribution friction checks."""

from __future__ import annotations

from pathlib import Path
from scorecard.models.result import CheckResult


def run_contribution_checks(repo_path: Path) -> list[CheckResult]:
    """Check how easy it is to contribute to the repo."""
    checks = []

    ci_present = (repo_path / ".github" / "workflows").exists() and \
        any((repo_path / ".github" / "workflows").glob("*.yml"))
    checks.append(CheckResult(name="CI workflow present", dimension="contribution",
        passed=ci_present, weight=3,
        detail="" if ci_present else "Add GitHub Actions CI workflow"))

    pr_template = (repo_path / ".github" / "pull_request_template.md").exists()
    checks.append(CheckResult(name="PR template present", dimension="contribution",
        passed=pr_template, weight=2,
        detail="" if pr_template else "Add .github/pull_request_template.md"))

    codeowners = (repo_path / ".github" / "CODEOWNERS").exists() or \
        (repo_path / "CODEOWNERS").exists()
    checks.append(CheckResult(name="CODEOWNERS defined", dimension="contribution",
        passed=codeowners, weight=2,
        detail="" if codeowners else "Add CODEOWNERS to define review ownership"))

    issue_templates = (repo_path / ".github" / "ISSUE_TEMPLATE").exists()
    checks.append(CheckResult(name="Issue templates present", dimension="contribution",
        passed=issue_templates, weight=1,
        detail="" if issue_templates else "Add .github/ISSUE_TEMPLATE/ directory"))

    gitattributes = (repo_path / ".gitattributes").exists()
    checks.append(CheckResult(name=".gitattributes present", dimension="contribution",
        passed=gitattributes, weight=1,
        detail="" if gitattributes else "Add .gitattributes for consistent line endings"))

    has_lockfile = any((repo_path / f).exists() for f in
        ["uv.lock", "poetry.lock", "package-lock.json", "yarn.lock"])
    checks.append(CheckResult(name="Dependency lock file present", dimension="contribution",
        passed=has_lockfile, weight=2,
        detail="" if has_lockfile else "Add a dependency lock file for reproducible builds"))

    return checks