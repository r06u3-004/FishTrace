"""Exception types shared by the independent forensic engine."""


class FishTraceEngineError(Exception):
    """Base class for all engine-specific errors."""


class ContractValidationError(FishTraceEngineError, ValueError):
    """Raised when a forensic contract receives invalid data."""


class AnalysisError(FishTraceEngineError):
    """Base class for analysis workflow failures."""


class UnsupportedInputError(AnalysisError):
    """Raised when input cannot be handled by the engine."""


class AnalysisIncompleteError(AnalysisError):
    """Raised when a result is incomplete and must not be treated as final."""


class IntegrationError(FishTraceEngineError):
    """Raised when application integration violates engine contracts."""
