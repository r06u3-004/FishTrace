from enum import StrEnum


class UserRole(StrEnum):
    analyst = "analyst"
    senior_analyst = "senior_analyst"
    administrator = "administrator"


class InvestigationStatus(StrEnum):
    open = "open"
    in_progress = "in_progress"
    closed = "closed"


class Severity(StrEnum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class CampaignStatus(StrEnum):
    active = "active"
    monitoring = "monitoring"
    archived = "archived"


class IndicatorType(StrEnum):
    ipv4 = "ipv4"
    ipv6 = "ipv6"
    domain = "domain"
    url = "url"
    email = "email"
    md5 = "md5"
    sha1 = "sha1"
    sha256 = "sha256"


class AuthStatus(StrEnum):
    verified = "verified"
    failed = "failed"
    unavailable = "unavailable"
    inconclusive = "inconclusive"
    not_applicable = "not_applicable"


class ReportFormat(StrEnum):
    html = "html"
    json = "json"
