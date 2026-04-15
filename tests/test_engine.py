"""Tests for the scoring engine."""

import tempfile
from pathlib import Path
from scorecard.core.engine import score_repo
from scorecard.models.result import score_to_grade


def test_score_empty_repo() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        result = score_repo(Path(tmpdir), "test/repo")
        assert result.repo == "test/repo"
        assert result.overall_score >= 0
        assert result.grade in ("A", "B", "C", "D", "F")
        assert result.scanned_at != ""


def test_score_well_structured_repo() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir)
        (path / "README.md").write_text("# Test\n\n## Overview\n\nDesc.\n\n## Quick start\n\nRun.\n")
        (path / "LICENSE").write_text("Apache 2.0")
        (path / "CONTRIBUTING.md").write_text("# Contributing")
        (path / "CHANGELOG.md").write_text("# Changelog\n\n## [0.1.0] - 2026-04-12")
        (path / ".gitignore").write_text("*.pyc")
        (path / ".gitattributes").write_text("* text=auto")
        (path / "docs" / "adr").mkdir(parents=True)
        (path / ".github" / "workflows").mkdir(parents=True)
        (path / ".github" / "workflows" / "ci.yml").write_text("name: CI\non:\n  push:\n")
        (path / ".github" / "CODEOWNERS").write_text("* @owner")
        (path / ".github" / "pull_request_template.md").write_text("## Summary")
        (path / "tests").mkdir()
        (path / "tests" / "test_main.py").write_text("def test_x(): pass")
        result = score_repo(path, "test/repo")
        assert result.overall_score >= 50


def test_score_has_four_dimensions() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        result = score_repo(Path(tmpdir), "test/repo")
        assert len(result.dimensions) == 4


def test_recommendations_are_strings() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        result = score_repo(Path(tmpdir), "test/repo")
        for rec in result.recommendations:
            assert isinstance(rec, str)
            assert len(rec) > 0