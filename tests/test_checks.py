"""Tests for scorecard checks."""

import tempfile
from pathlib import Path
from scorecard.checks.discoverability import run_discoverability_checks
from scorecard.checks.documentation import run_documentation_checks
from scorecard.checks.contribution import run_contribution_checks
from scorecard.checks.adoption import run_adoption_checks


def make_full_repo(tmpdir: str) -> Path:
    """Create a well-structured repo for testing."""
    path = Path(tmpdir)
    (path / "README.md").write_text("# Test Repo\n\n## Overview\n\nThis is a test.\n\n## Quick start\n\nRun it.\n")
    (path / "LICENSE").write_text("Apache 2.0")
    (path / "CONTRIBUTING.md").write_text("# Contributing\n\nHow to contribute.")
    (path / "CHANGELOG.md").write_text("# Changelog\n\n## [0.1.0] - 2026-04-12\n\n### Added\n- Initial release")
    (path / ".gitignore").write_text("*.pyc\n.venv/\n")
    (path / ".gitattributes").write_text("* text=auto\n")
    (path / "docs" / "adr").mkdir(parents=True)
    (path / ".github" / "workflows").mkdir(parents=True)
    (path / ".github" / "ISSUE_TEMPLATE").mkdir(parents=True)
    (path / ".github" / "CODEOWNERS").write_text("* @brianpelow\n")
    (path / ".github" / "pull_request_template.md").write_text("## Summary\n")
    (path / ".github" / "workflows" / "ci.yml").write_text("name: CI\non:\n  push:\n    branches: [main]\n")
    (path / ".github" / "workflows" / "nightly-agent.yml").write_text(
        "name: Nightly agent\non:\n  schedule:\n    - cron: '0 2 * * *'\njobs:\n  agent:\n    runs-on: ubuntu-latest\n"
    )
    (path / "tests").mkdir()
    (path / "tests" / "test_main.py").write_text("def test_example(): pass\n")
    (path / "uv.lock").write_text("# lock file\n")
    return path


def test_discoverability_full_repo() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        path = make_full_repo(tmpdir)
        checks = run_discoverability_checks(path)
        passed = [c for c in checks if c.passed]
        assert len(passed) >= 3


def test_discoverability_empty_repo() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        checks = run_discoverability_checks(Path(tmpdir))
        passed = [c for c in checks if c.passed]
        assert len(passed) == 0


def test_documentation_full_repo() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        path = make_full_repo(tmpdir)
        checks = run_documentation_checks(path)
        passed = [c for c in checks if c.passed]
        assert len(passed) >= 3


def test_contribution_full_repo() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        path = make_full_repo(tmpdir)
        checks = run_contribution_checks(path)
        passed = [c for c in checks if c.passed]
        assert len(passed) >= 4


def test_adoption_full_repo() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        path = make_full_repo(tmpdir)
        checks = run_adoption_checks(path)
        passed = [c for c in checks if c.passed]
        assert len(passed) >= 2


def test_all_dimensions_return_checks() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir)
        assert len(run_discoverability_checks(path)) > 0
        assert len(run_documentation_checks(path)) > 0
        assert len(run_contribution_checks(path)) > 0
        assert len(run_adoption_checks(path)) > 0