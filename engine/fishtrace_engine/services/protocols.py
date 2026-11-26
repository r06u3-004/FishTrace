"""Integration protocols and request contracts for engine consumers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, runtime_checkable

from fishtrace_engine.models import EmailAnalysisResult


@dataclass(frozen=True, slots=True)
class AnalysisRequest:
    """Input handed to an engine analyzer; analyzers own all parsing logic."""

    raw_eml: bytes
    filename: str


@runtime_checkable
class EmailAnalyzer(Protocol):
    """Contract implemented by future forensic analyzers."""

    engine_version: str

    def analyze(self, request: AnalysisRequest) -> EmailAnalysisResult: ...
