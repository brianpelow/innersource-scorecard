"""Scorecard result models."""

from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Optional


class CheckResult(BaseModel):
    """Result of a single scorecard check."""

    name: str
    dimension: str
    passed: bool
    weight: int = Field(1, description="Relative weight of this check")
    detail: str = ""


class DimensionScore(BaseModel):
    """Score for a single scorecard dimension."""

    name: str
    score: int = Field(0, description="0-100 dimension score")
    weight: float = Field(0.25, description="Weight in overall score")
    checks: list[CheckResult] = Field(default_factory=list)
    passed: int = 0
    total: int = 0


class ScorecardResult(BaseModel):
    """Complete scorecard result for a repository."""

    repo: str
    overall_score: int = 0
    grade: str = "F"
    discoverability: DimensionScore = Field(default_factory=lambda: DimensionScore(name="discoverability"))
    documentation: DimensionScore = Field(default_factory=lambda: DimensionScore(name="documentation"))
    contribution: DimensionScore = Field(default_factory=lambda: DimensionScore(name="contribution"))
    adoption: DimensionScore = Field(default_factory=lambda: DimensionScore(name="adoption"))
    recommendations: list[str] = Field(default_factory=list)
    scanned_at: str = ""

    @property
    def dimensions(self) -> list[DimensionScore]:
        return [self.discoverability, self.documentation, self.contribution, self.adoption]


def score_to_grade(score: int) -> str:
    if score >= 90:
        return "A"
    elif score >= 75:
        return "B"
    elif score >= 60:
        return "C"
    elif score >= 45:
        return "D"
    return "F"