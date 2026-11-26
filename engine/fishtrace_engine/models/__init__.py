"""Typed, infrastructure-independent forensic contracts."""

from fishtrace_engine.models.attachments import AttachmentAnalysis, AttachmentAnalysisStatus
from fishtrace_engine.models.authentication import AuthenticationResult, AuthStatus
from fishtrace_engine.models.base import SerializableModel, utc_now
from fishtrace_engine.models.email import AnalysisStatus, EmailAnalysisResult, EmailMetadata
from fishtrace_engine.models.evidence import Evidence, EvidenceType
from fishtrace_engine.models.findings import Finding, FindingCategory, FindingSeverity
from fishtrace_engine.models.indicators import Indicator, IndicatorType
from fishtrace_engine.models.risk import RiskAssessment, RiskLevel

__all__ = [
    "AnalysisStatus",
    "AttachmentAnalysis",
    "AttachmentAnalysisStatus",
    "AuthStatus",
    "AuthenticationResult",
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
    "utc_now",
]
