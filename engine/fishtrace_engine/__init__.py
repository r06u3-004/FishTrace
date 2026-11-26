"""Independent FishTrace forensic engine contracts."""

from fishtrace_engine.models import (
    AnalysisStatus,
    AttachmentAnalysis,
    AttachmentAnalysisStatus,
    AuthenticationResult,
    AuthStatus,
    EmailAnalysisResult,
    EmailMetadata,
    Evidence,
    EvidenceType,
    Finding,
    FindingCategory,
    FindingSeverity,
    Indicator,
    IndicatorType,
    RiskAssessment,
    RiskLevel,
    SerializableModel,
)
from fishtrace_engine.services import AnalysisRequest, EmailAnalyzer

__version__ = "0.1.0"

__all__ = [
    "__version__",
    "AnalysisRequest",
    "AnalysisStatus",
    "AttachmentAnalysis",
    "AttachmentAnalysisStatus",
    "AuthStatus",
    "AuthenticationResult",
    "EmailAnalyzer",
    "EmailAnalysisResult",
    "EmailMetadata",
    "Evidence",
    "EvidenceType",
    "Finding",
    "FindingCategory",
    "FindingSeverity",
    "Indicator",
    "IndicatorType",
    "RiskAssessment",
    "RiskLevel",
    "SerializableModel",
]
