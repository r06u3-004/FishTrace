from datetime import UTC, datetime
from uuid import uuid4

import pytest

from fishtrace_engine import (
    AnalysisRequest,
    AnalysisStatus,
    AttachmentAnalysis,
    AttachmentAnalysisStatus,
    AuthenticationResult,
    AuthStatus,
    EmailAnalysisResult,
    EmailAnalyzer,
    Evidence,
    EvidenceType,
    Finding,
    FindingCategory,
    FindingSeverity,
    Indicator,
    IndicatorType,
    RiskAssessment,
    RiskLevel,
)
from fishtrace_engine.exceptions import ContractValidationError


def _aware_timestamp() -> datetime:
    return datetime(2026, 11, 26, 12, 0, tzinfo=UTC)


def test_email_analysis_result_requires_identifying_fields() -> None:
    with pytest.raises(TypeError):
        EmailAnalysisResult(engine_version="0.1.0")
    with pytest.raises(TypeError):
        EmailAnalysisResult(original_filename="sample.eml")


def test_enum_validation() -> None:
    assert AuthStatus("pass") is AuthStatus.PASS
    assert IndicatorType("sha256") is IndicatorType.SHA256
    with pytest.raises(ValueError):
        AuthStatus("UNKNOWN_STATUS")


def test_timestamp_must_be_timezone_aware() -> None:
    with pytest.raises(ContractValidationError, match="timezone-aware"):
        Evidence(
            id=uuid4(),
            type=EvidenceType.HEADER,
            value="Received: ...",
            source_location="headers",
            collected_at=datetime(2026, 11, 26, 12, 0),
        )

    evidence = Evidence(
        id=uuid4(),
        type=EvidenceType.HEADER,
        value="Received: ...",
        source_location="headers",
        collected_at=_aware_timestamp(),
    )
    assert evidence.collected_at.tzinfo is not None


def test_evidence_references_are_serialized() -> None:
    finding_id = uuid4()
    evidence = Evidence(
        id=uuid4(),
        type=EvidenceType.RAW_EMAIL,
        value="preserved-bytes",
        source_location="evidence/sample.eml",
        collected_at=_aware_timestamp(),
        sha256="0" * 64,
        related_finding_ids=(finding_id,),
    )

    data = evidence.to_dict()
    assert data["related_finding_ids"] == [str(finding_id)]
    assert data["sha256"] == "0" * 64


def test_indicator_preserves_original_value() -> None:
    indicator = Indicator(
        id=uuid4(),
        type=IndicatorType.DOMAIN,
        original_value="EXAMPLe.COM.",
        normalized_value="example.com",
        source_location="body",
    )

    data = indicator.to_dict()
    assert data["original_value"] == "EXAMPLe.COM."
    assert data["normalized_value"] == "example.com"
    assert indicator.extracted_at.tzinfo is not None


def test_authentication_missing_information_is_not_failure() -> None:
    auth = AuthenticationResult(spf="none", dkim="not_checked")

    assert auth.spf is AuthStatus.NONE
    assert auth.dkim is AuthStatus.NOT_CHECKED
    assert auth.dmarc is AuthStatus.NOT_CHECKED
    assert auth.spf_alignment is AuthStatus.NOT_CHECKED


def test_invalid_authentication_status_is_rejected() -> None:
    with pytest.raises(ContractValidationError, match="authentication status"):
        AuthenticationResult(spf="PASSED")


def test_risk_assessment_structure_and_validation() -> None:
    finding_id = uuid4()
    risk = RiskAssessment(
        level=RiskLevel.MEDIUM,
        confidence=0.65,
        contributing_finding_ids=(finding_id,),
        reasons=("Authentication is inconclusive.",),
        recommendations=("Verify the message with the reporting user.",),
    )

    data = risk.to_dict()
    assert data["level"] == "medium"
    assert data["contributing_finding_ids"] == [str(finding_id)]
    assert data["score"] is None

    with pytest.raises(ContractValidationError, match="score_model"):
        RiskAssessment(score=50.0)
    with pytest.raises(ContractValidationError, match="confidence"):
        RiskAssessment(confidence=1.1)


def test_sha256_validation_rejects_invalid_values() -> None:
    with pytest.raises(ContractValidationError, match="SHA-256"):
        AttachmentAnalysis(filename="sample.bin", sha256="not-a-hash", size_bytes=10)


def test_full_result_serializes_to_json_compatible_primitives() -> None:
    finding_id = uuid4()
    finding = Finding(
        id=finding_id,
        category=FindingCategory.HEADER,
        title="Unexpected relay",
        description="A relay domain differs from the sender domain.",
        severity=FindingSeverity.HIGH,
        confidence=0.8,
        evidence_ids=(uuid4(),),
        detection_source="contract-test",
        observed_at=_aware_timestamp(),
    )
    attachment = AttachmentAnalysis(
        filename="document.bin",
        sha256="1" * 64,
        size_bytes=42,
        status=AttachmentAnalysisStatus.NOT_ANALYZED,
    )
    result = EmailAnalysisResult(
        original_filename="sample.eml",
        engine_version="0.1.0",
        status=AnalysisStatus.COMPLETED,
        findings=(finding,),
        attachments=(attachment,),
        risk=RiskAssessment(level=RiskLevel.HIGH, contributing_finding_ids=(finding_id,)),
        limitations=("Header sources were not independently verified.",),
    )

    data = result.to_dict()
    assert data["status"] == "completed"
    assert data["findings"][0]["severity"] == "high"
    assert data["attachments"][0]["sha256"] == "1" * 64
    assert data["risk"]["level"] == "high"


def test_analyzer_protocol_accepts_conforming_consumer() -> None:
    class ContractConformingAnalyzer:
        engine_version = "0.1.0"

        def analyze(self, request: AnalysisRequest) -> EmailAnalysisResult:
            return EmailAnalysisResult(
                original_filename=request.filename,
                engine_version=self.engine_version,
            )

    analyzer = ContractConformingAnalyzer()
    assert isinstance(analyzer, EmailAnalyzer)
    result = analyzer.analyze(AnalysisRequest(raw_eml=b"subject: test", filename="sample.eml"))
    assert result.original_filename == "sample.eml"
