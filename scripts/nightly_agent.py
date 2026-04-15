"""Nightly agent — self-scorecard for innersource-scorecard."""

from __future__ import annotations

import json
import sys
from datetime import date, datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

REPO_ROOT = Path(__file__).parent.parent


def self_scorecard() -> None:
    from scorecard.core.engine import score_repo
    result = score_repo(REPO_ROOT, "innersource-scorecard")
    out = REPO_ROOT / "docs" / "self-scorecard.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps({
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "date": date.today().isoformat(),
        "repo": result.repo,
        "overall_score": result.overall_score,
        "grade": result.grade,
        "dimensions": {d.name: {"score": d.score, "passed": d.passed, "total": d.total} for d in result.dimensions},
        "recommendations": result.recommendations[:5],
    }, indent=2))
    print(f"[agent] Self-scorecard: {result.grade} ({result.overall_score}/100)")


def refresh_changelog() -> None:
    changelog = REPO_ROOT / "CHANGELOG.md"
    if not changelog.exists():
        return
    today = date.today().isoformat()
    content = changelog.read_text()
    if today not in content:
        content = content.replace("## [Unreleased]", f"## [Unreleased]\n\n_Last checked: {today}_", 1)
        changelog.write_text(content)
    print("[agent] Refreshed CHANGELOG timestamp")


if __name__ == "__main__":
    print(f"[agent] Starting nightly agent - {date.today().isoformat()}")
    self_scorecard()
    refresh_changelog()
    print("[agent] Done.")