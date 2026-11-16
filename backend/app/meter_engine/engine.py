"""Evidence-gated orchestration entry point.

No executable, source-verified metrical rules are supplied in this package.
Therefore this foundation must not calculate weights or produce a meter verdict.
"""

from .contracts import AnalysisModes, AnalysisResult, LineResult

ENGINE_VERSION = "0.1.0-foundation"


def analyze_poem(
    text: str,
    *,
    genre_id: str | None = None,
    modes: AnalysisModes | None = None,
) -> AnalysisResult:
    """Prepare a provenance-aware analysis response without inventing scansion.

    This function is intentionally fail-closed. Until verified executable rules and
    regression examples are connected, every non-empty line remains UNVERIFIED.
    """
    selected_modes = modes or AnalysisModes()

    if not text or not text.strip():
        return AnalysisResult(
            status="UNVERIFIED",
            analysis_performed=False,
            genre_id=genre_id,
            enabled_rule_classes=tuple(selected_modes.enabled_classes()),
            rules_applied=(),
            lines=(),
            engine_version=ENGINE_VERSION,
            explanation_code="EMPTY_TEXT",
        )

    raw_lines = text.splitlines()
    # Preserve meaningful blank-line positions for line numbering, but do not
    # report whitespace-only lines as scannable verse lines.
    verse_lines = [
        (index, line)
        for index, line in enumerate(raw_lines, start=1)
        if line.strip()
    ]

    if not selected_modes.is_valid():
        line_results = tuple(
            LineResult(
                line_number=index,
                original=line,
                status="INVALID_CONFIGURATION",
                explanation_code="NO_ANALYSIS_CLASS_ENABLED",
            )
            for index, line in verse_lines
        )
        return AnalysisResult(
            status="INVALID_CONFIGURATION",
            analysis_performed=False,
            genre_id=genre_id,
            enabled_rule_classes=(),
            rules_applied=(),
            lines=line_results,
            engine_version=ENGINE_VERSION,
            explanation_code="NO_ANALYSIS_CLASS_ENABLED",
        )

    line_results = tuple(
        LineResult(
            line_number=index,
            original=line,
            status="UNVERIFIED",
            explanation_code="NO_VERIFIED_EXECUTABLE_RULES",
        )
        for index, line in verse_lines
    )

    return AnalysisResult(
        status="UNVERIFIED",
        analysis_performed=False,
        genre_id=genre_id,
        enabled_rule_classes=tuple(selected_modes.enabled_classes()),
        rules_applied=(),
        lines=line_results,
        engine_version=ENGINE_VERSION,
        explanation_code="NO_VERIFIED_EXECUTABLE_RULES",
    )
