"""Stable, provenance-aware contracts for meter analysis.

This module deliberately contains no metrical assumptions or scansion rules.
"""

from dataclasses import asdict, dataclass
from typing import Literal


AnalysisStatus = Literal[
    "VERIFIED",
    "NON_CONFORMING",
    "AMBIGUOUS",
    "UNVERIFIED",
    "INVALID_CONFIGURATION",
]

@dataclass(frozen=True)
class AnalysisModes:
    """Three independent rule classes; each can be enabled independently."""

    gaarriye: bool = True
    researchers: bool = False
    compatible_other: bool = False

    def enabled_classes(self) -> list[str]:
        enabled: list[str] = []
        if self.gaarriye:
            enabled.append("GAARRIYE_PRIMARY")
        if self.researchers:
            enabled.append("RESEARCHER_INTERPRETATION")
        if self.compatible_other:
            enabled.append("COMPATIBLE_OTHER_RULE")
        return enabled

    def is_valid(self) -> bool:
        return bool(self.enabled_classes())


@dataclass(frozen=True)
class LineResult:
    line_number: int
    original: str
    status: AnalysisStatus
    explanation_code: str
    rules_applied: tuple[str, ...] = ()

    def to_dict(self) -> dict:
        data = asdict(self)
        data["rules_applied"] = list(self.rules_applied)
        return data


@dataclass(frozen=True)
class AnalysisResult:
    status: AnalysisStatus
    analysis_performed: bool
    genre_id: str | None
    enabled_rule_classes: tuple[str, ...]
    rules_applied: tuple[str, ...]
    lines: tuple[LineResult, ...]
    engine_version: str
    explanation_code: str

    def to_dict(self) -> dict:
        return {
            "status": self.status,
            "analysis_performed": self.analysis_performed,
            "genre_id": self.genre_id,
            "enabled_rule_classes": list(self.enabled_rule_classes),
            "rules_applied": list(self.rules_applied),
            "lines": [line.to_dict() for line in self.lines],
            "engine_version": self.engine_version,
            "explanation_code": self.explanation_code,
        }
