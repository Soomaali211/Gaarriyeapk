"""Evidence-gated foundation for the Gaarriye meter engine."""

from .contracts import AnalysisModes, AnalysisResult, LineResult
from .engine import analyze_poem

__all__ = [
    "AnalysisModes",
    "AnalysisResult",
    "LineResult",
    "analyze_poem",
]
