"""Configuration for innersource-scorecard."""

from __future__ import annotations

import os
from pydantic import BaseModel, Field


class ScorecardConfig(BaseModel):
    """Runtime configuration for innersource-scorecard."""

    github_token: str = Field("", description="GitHub API token")
    anthropic_api_key: str = Field("", description="Anthropic API key")
    industry: str = Field("fintech", description="Industry context")

    @classmethod
    def from_env(cls) -> "ScorecardConfig":
        return cls(
            github_token=os.environ.get("GITHUB_TOKEN", ""),
            anthropic_api_key=os.environ.get("ANTHROPIC_API_KEY", ""),
            industry=os.environ.get("SCORECARD_INDUSTRY", "fintech"),
        )

    @property
    def has_github(self) -> bool:
        return bool(self.github_token)