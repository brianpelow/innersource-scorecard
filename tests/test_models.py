"""Tests for scorecard models."""

from scorecard.models.result import CheckResult, DimensionScore, ScorecardResult, score_to_grade


def test_score_to_grade_a() -> None:
    assert score_to_grade(95) == "A"
    assert score_to_grade(90) == "A"


def test_score_to_grade_b() -> None:
    assert score_to_grade(80) == "B"
    assert score_to_grade(75) == "B"


def test_score_to_grade_c() -> None:
    assert score_to_grade(65) == "C"


def test_score_to_grade_d() -> None:
    assert score_to_grade(50) == "D"


def test_score_to_grade_f() -> None:
    assert score_to_grade(30) == "F"
    assert score_to_grade(0) == "F"


def test_check_result_defaults() -> None:
    check = CheckResult(name="test", dimension="discoverability", passed=True)
    assert check.weight == 1
    assert check.detail == ""


def test_dimension_score_defaults() -> None:
    dim = DimensionScore(name="test")
    assert dim.score == 0
    assert dim.checks == []


def test_scorecard_result_dimensions() -> None:
    result = ScorecardResult(repo="test/repo")
    assert len(result.dimensions) == 4