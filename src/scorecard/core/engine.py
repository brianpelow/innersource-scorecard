"""Scorecard scoring engine."""

from __future__ import annotations

from pathlib import Path
from datetime import datetime, timezone

from scorecard.checks.discoverability import run_discoverability_checks
from scorecard.checks.documentation import run_documentation_checks
from scorecard.checks.contribution import run_contribution_checks
from scorecard.checks.adoption import run_adoption_checks
from scorecard.models.result import ScorecardResult, DimensionScore, score_to_grade

DIMENSION_WEIGHTS = {
    "discoverability": 0.25,
    "documentation": 0.30,
    "contribution": 0.25,
    "adoption": 0.20,
}


def score_repo(repo_path: Path, repo_name: str, github_stats: dict | None = None) -> ScorecardResult:
    """Run all scorecard checks and compute composite score."""
    result = ScorecardResult(
        repo=repo_name,
        scanned_at=datetime.now(timezone.utc).isoformat(),
    )

    disc_checks = run_discoverability_checks(repo_path)
    result.discoverability = _score_dimension("discoverability", disc_checks, 0.25)

    doc_checks = run_documentation_checks(repo_path)
    result.documentation = _score_dimension("documentation", doc_checks, 0.30)

    contrib_checks = run_contribution_checks(repo_path)
    result.contribution = _score_dimension("contribution", contrib_checks, 0.25)

    adopt_checks = run_adoption_checks(repo_path, github_stats)
    result.adoption = _score_dimension("adoption", adopt_checks, 0.20)

    overall = int(
        result.discoverability.score * 0.25 +
        result.documentation.score * 0.30 +
        result.contribution.score * 0.25 +
        result.adoption.score * 0.20
    )
    result.overall_score = overall
    result.grade = score_to_grade(overall)
    result.recommendations = _build_recommendations(result)

    return result


def _score_dimension(name: str, checks: list, weight: float) -> DimensionScore:
    """Score a single dimension from its checks."""
    if not checks:
        return DimensionScore(name=name, score=0, weight=weight)

    total_weight = sum(c.weight for c in checks)
    passed_weight = sum(c.weight for c in checks if c.passed)
    score = int(passed_weight / total_weight * 100) if total_weight > 0 else 0

    return DimensionScore(
        name=name,
        score=score,
        weight=weight,
        checks=checks,
        passed=sum(1 for c in checks if c.passed),
        total=len(checks),
    )


def _build_recommendations(result: ScorecardResult) -> list[str]:
    """Build prioritized improvement recommendations."""
    recs = []
    for dim in result.dimensions:
        for check in dim.checks:
            if not check.passed and check.detail:
                recs.append(f"[{dim.name.title()}] {check.detail}")

    recs.sort(key=lambda r: 0 if "README" in r or "CI" in r or "LICENSE" in r else 1)
    return recs[:10]