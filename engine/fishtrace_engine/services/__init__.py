"""Integration contracts shared by backend, CLI and future report generation."""

from fishtrace_engine.services.protocols import AnalysisRequest, EmailAnalyzer

__all__ = ["AnalysisRequest", "EmailAnalyzer"]
