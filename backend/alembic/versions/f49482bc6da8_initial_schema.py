"""initial schema

Revision ID: f49482bc6da8
Revises:
Create Date: 2026-11-26 21:29:33.584574
"""

from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

revision: str = "f49482bc6da8"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "campaigns",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("classification", sa.String(length=120), nullable=True),
        sa.Column(
            "status",
            sa.Enum("active", "monitoring", "archived", name="campaignstatus", native_enum=False, length=32),
            nullable=False,
        ),
        sa.Column(
            "severity",
            sa.Enum("low", "medium", "high", "critical", name="severity", native_enum=False, length=16),
            nullable=False,
        ),
        sa.Column("first_seen", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_seen", sa.DateTime(timezone=True), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_campaigns")),
    )
    op.create_index(op.f("ix_campaigns_name"), "campaigns", ["name"], unique=True)
    op.create_index(op.f("ix_campaigns_status"), "campaigns", ["status"], unique=False)
    op.create_table(
        "indicators",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column(
            "type",
            sa.Enum(
                "ipv4",
                "ipv6",
                "domain",
                "url",
                "email",
                "md5",
                "sha1",
                "sha256",
                name="indicatortype",
                native_enum=False,
                length=32,
            ),
            nullable=False,
        ),
        sa.Column("value", sa.Text(), nullable=False),
        sa.Column("normalized_value", sa.Text(), nullable=False),
        sa.Column("classification", sa.String(length=64), nullable=True),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("first_seen", sa.DateTime(timezone=True), nullable=False),
        sa.Column("last_seen", sa.DateTime(timezone=True), nullable=False),
        sa.Column("reputation_json", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_indicators")),
        sa.UniqueConstraint("type", "normalized_value", name="uq_indicators_type_normalized"),
    )
    op.create_index(op.f("ix_indicators_type"), "indicators", ["type"], unique=False)
    op.create_index("ix_indicators_type_value", "indicators", ["type", "normalized_value"], unique=False)
    op.create_table(
        "integration_configs",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("provider", sa.String(length=64), nullable=False),
        sa.Column("enabled", sa.Boolean(), nullable=False),
        sa.Column("encrypted_api_key", sa.LargeBinary(), nullable=True),
        sa.Column("base_url", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_integration_configs")),
    )
    op.create_index(op.f("ix_integration_configs_provider"), "integration_configs", ["provider"], unique=True)
    op.create_table(
        "users",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("username", sa.String(length=64), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.Text(), nullable=False),
        sa.Column(
            "role",
            sa.Enum("analyst", "senior_analyst", "administrator", name="userrole", native_enum=False, length=32),
            nullable=False,
        ),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_users_role"), "users", ["role"], unique=False)
    op.create_index(op.f("ix_users_username"), "users", ["username"], unique=True)
    op.create_table(
        "intel_results",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("indicator_id", sa.Uuid(), nullable=False),
        sa.Column("provider", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("data_json", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("queried_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("error", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(
            ["indicator_id"],
            ["indicators.id"],
            name=op.f("fk_intel_results_indicator_id_indicators"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_intel_results")),
    )
    op.create_index(op.f("ix_intel_results_indicator_id"), "intel_results", ["indicator_id"], unique=False)
    op.create_table(
        "investigations",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column(
            "status",
            sa.Enum("open", "in_progress", "closed", name="investigationstatus", native_enum=False, length=32),
            nullable=False,
        ),
        sa.Column(
            "severity",
            sa.Enum("low", "medium", "high", "critical", name="severity", native_enum=False, length=16),
            nullable=False,
        ),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("owner_id", sa.Uuid(), nullable=True),
        sa.Column("opened_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("closed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(
            ["owner_id"], ["users.id"], name=op.f("fk_investigations_owner_id_users"), ondelete="SET NULL"
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_investigations")),
    )
    op.create_index(op.f("ix_investigations_owner_id"), "investigations", ["owner_id"], unique=False)
    op.create_index(op.f("ix_investigations_severity"), "investigations", ["severity"], unique=False)
    op.create_index(op.f("ix_investigations_status"), "investigations", ["status"], unique=False)
    op.create_table(
        "activity_events",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("investigation_id", sa.Uuid(), nullable=True),
        sa.Column("actor", sa.String(length=128), nullable=False),
        sa.Column("event_type", sa.String(length=64), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("payload_json", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("occurred_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(
            ["investigation_id"],
            ["investigations.id"],
            name=op.f("fk_activity_events_investigation_id_investigations"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_activity_events")),
    )
    op.create_index(op.f("ix_activity_events_event_type"), "activity_events", ["event_type"], unique=False)
    op.create_index(op.f("ix_activity_events_investigation_id"), "activity_events", ["investigation_id"], unique=False)
    op.create_index(op.f("ix_activity_events_occurred_at"), "activity_events", ["occurred_at"], unique=False)
    op.create_table(
        "analyst_notes",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("investigation_id", sa.Uuid(), nullable=False),
        sa.Column("author_id", sa.Uuid(), nullable=True),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(
            ["author_id"], ["users.id"], name=op.f("fk_analyst_notes_author_id_users"), ondelete="SET NULL"
        ),
        sa.ForeignKeyConstraint(
            ["investigation_id"],
            ["investigations.id"],
            name=op.f("fk_analyst_notes_investigation_id_investigations"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_analyst_notes")),
    )
    op.create_index(op.f("ix_analyst_notes_investigation_id"), "analyst_notes", ["investigation_id"], unique=False)
    op.create_table(
        "campaign_investigations",
        sa.Column("campaign_id", sa.Uuid(), nullable=False),
        sa.Column("investigation_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(
            ["campaign_id"],
            ["campaigns.id"],
            name=op.f("fk_campaign_investigations_campaign_id_campaigns"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["investigation_id"],
            ["investigations.id"],
            name=op.f("fk_campaign_investigations_investigation_id_investigations"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("campaign_id", "investigation_id", name=op.f("pk_campaign_investigations")),
    )
    op.create_table(
        "emails",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("investigation_id", sa.Uuid(), nullable=False),
        sa.Column("subject", sa.String(length=512), nullable=True),
        sa.Column("sender", sa.String(length=512), nullable=True),
        sa.Column("recipients", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("date_headers", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("parsed_json", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("raw_evidence_sha256", sa.String(length=64), nullable=False),
        sa.Column("raw_evidence_path", sa.Text(), nullable=False),
        sa.Column("received_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(
            ["investigation_id"],
            ["investigations.id"],
            name=op.f("fk_emails_investigation_id_investigations"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_emails")),
    )
    op.create_index(op.f("ix_emails_investigation_id"), "emails", ["investigation_id"], unique=False)
    op.create_index(op.f("ix_emails_raw_evidence_sha256"), "emails", ["raw_evidence_sha256"], unique=False)
    op.create_table(
        "indicator_sightings",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("indicator_id", sa.Uuid(), nullable=False),
        sa.Column("investigation_id", sa.Uuid(), nullable=False),
        sa.Column("source", sa.Text(), nullable=False),
        sa.Column("context", sa.Text(), nullable=True),
        sa.Column("observed_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(
            ["indicator_id"],
            ["indicators.id"],
            name=op.f("fk_indicator_sightings_indicator_id_indicators"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["investigation_id"],
            ["investigations.id"],
            name=op.f("fk_indicator_sightings_investigation_id_investigations"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_indicator_sightings")),
    )
    op.create_index(op.f("ix_indicator_sightings_indicator_id"), "indicator_sightings", ["indicator_id"], unique=False)
    op.create_index(
        op.f("ix_indicator_sightings_investigation_id"), "indicator_sightings", ["investigation_id"], unique=False
    )
    op.create_table(
        "reports",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("investigation_id", sa.Uuid(), nullable=False),
        sa.Column("format", sa.Enum("html", "json", name="reportformat", native_enum=False, length=16), nullable=False),
        sa.Column("path", sa.Text(), nullable=False),
        sa.Column("sha256", sa.String(length=64), nullable=False),
        sa.Column("generated_by", sa.String(length=128), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(
            ["investigation_id"],
            ["investigations.id"],
            name=op.f("fk_reports_investigation_id_investigations"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_reports")),
    )
    op.create_index(op.f("ix_reports_investigation_id"), "reports", ["investigation_id"], unique=False)
    op.create_index(op.f("ix_reports_sha256"), "reports", ["sha256"], unique=False)
    op.create_table(
        "analysis_results",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("email_id", sa.Uuid(), nullable=False),
        sa.Column("engine_version", sa.String(length=32), nullable=False),
        sa.Column("findings_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("risk_score", sa.Float(), nullable=False),
        sa.Column(
            "risk_level",
            sa.Enum("low", "medium", "high", "critical", name="severity", native_enum=False, length=16),
            nullable=False,
        ),
        sa.Column("completed_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(
            ["email_id"], ["emails.id"], name=op.f("fk_analysis_results_email_id_emails"), ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_analysis_results")),
    )
    op.create_index(op.f("ix_analysis_results_email_id"), "analysis_results", ["email_id"], unique=False)
    op.create_table(
        "attachments",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("email_id", sa.Uuid(), nullable=False),
        sa.Column("filename", sa.Text(), nullable=True),
        sa.Column("mime_type", sa.String(length=255), nullable=True),
        sa.Column("size", sa.Integer(), nullable=False),
        sa.Column("md5", sa.String(length=32), nullable=False),
        sa.Column("sha1", sa.String(length=40), nullable=False),
        sa.Column("sha256", sa.String(length=64), nullable=False),
        sa.Column("flags_json", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("disposition", sa.String(length=64), nullable=True),
        sa.ForeignKeyConstraint(
            ["email_id"], ["emails.id"], name=op.f("fk_attachments_email_id_emails"), ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_attachments")),
    )
    op.create_index(op.f("ix_attachments_email_id"), "attachments", ["email_id"], unique=False)
    op.create_index(op.f("ix_attachments_md5"), "attachments", ["md5"], unique=False)
    op.create_index(op.f("ix_attachments_sha1"), "attachments", ["sha1"], unique=False)
    op.create_index(op.f("ix_attachments_sha256"), "attachments", ["sha256"], unique=False)
    op.create_table(
        "auth_results",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("email_id", sa.Uuid(), nullable=False),
        sa.Column(
            "spf_status",
            sa.Enum(
                "verified",
                "failed",
                "unavailable",
                "inconclusive",
                "not_applicable",
                name="authstatus",
                native_enum=False,
                length=24,
            ),
            nullable=False,
        ),
        sa.Column(
            "dkim_status",
            sa.Enum(
                "verified",
                "failed",
                "unavailable",
                "inconclusive",
                "not_applicable",
                name="authstatus",
                native_enum=False,
                length=24,
            ),
            nullable=False,
        ),
        sa.Column(
            "dmarc_status",
            sa.Enum(
                "verified",
                "failed",
                "unavailable",
                "inconclusive",
                "not_applicable",
                name="authstatus",
                native_enum=False,
                length=24,
            ),
            nullable=False,
        ),
        sa.Column(
            "spf_alignment",
            sa.Enum(
                "verified",
                "failed",
                "unavailable",
                "inconclusive",
                "not_applicable",
                name="authstatus",
                native_enum=False,
                length=24,
            ),
            nullable=False,
        ),
        sa.Column(
            "dkim_alignment",
            sa.Enum(
                "verified",
                "failed",
                "unavailable",
                "inconclusive",
                "not_applicable",
                name="authstatus",
                native_enum=False,
                length=24,
            ),
            nullable=False,
        ),
        sa.Column("raw_json", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("evaluated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(
            ["email_id"], ["emails.id"], name=op.f("fk_auth_results_email_id_emails"), ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_auth_results")),
    )
    op.create_index(op.f("ix_auth_results_email_id"), "auth_results", ["email_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_auth_results_email_id"), table_name="auth_results")
    op.drop_table("auth_results")
    op.drop_index(op.f("ix_attachments_sha256"), table_name="attachments")
    op.drop_index(op.f("ix_attachments_sha1"), table_name="attachments")
    op.drop_index(op.f("ix_attachments_md5"), table_name="attachments")
    op.drop_index(op.f("ix_attachments_email_id"), table_name="attachments")
    op.drop_table("attachments")
    op.drop_index(op.f("ix_analysis_results_email_id"), table_name="analysis_results")
    op.drop_table("analysis_results")
    op.drop_index(op.f("ix_reports_sha256"), table_name="reports")
    op.drop_index(op.f("ix_reports_investigation_id"), table_name="reports")
    op.drop_table("reports")
    op.drop_index(op.f("ix_indicator_sightings_investigation_id"), table_name="indicator_sightings")
    op.drop_index(op.f("ix_indicator_sightings_indicator_id"), table_name="indicator_sightings")
    op.drop_table("indicator_sightings")
    op.drop_index(op.f("ix_emails_raw_evidence_sha256"), table_name="emails")
    op.drop_index(op.f("ix_emails_investigation_id"), table_name="emails")
    op.drop_table("emails")
    op.drop_table("campaign_investigations")
    op.drop_index(op.f("ix_analyst_notes_investigation_id"), table_name="analyst_notes")
    op.drop_table("analyst_notes")
    op.drop_index(op.f("ix_activity_events_occurred_at"), table_name="activity_events")
    op.drop_index(op.f("ix_activity_events_investigation_id"), table_name="activity_events")
    op.drop_index(op.f("ix_activity_events_event_type"), table_name="activity_events")
    op.drop_table("activity_events")
    op.drop_index(op.f("ix_investigations_status"), table_name="investigations")
    op.drop_index(op.f("ix_investigations_severity"), table_name="investigations")
    op.drop_index(op.f("ix_investigations_owner_id"), table_name="investigations")
    op.drop_table("investigations")
    op.drop_index(op.f("ix_intel_results_indicator_id"), table_name="intel_results")
    op.drop_table("intel_results")
    op.drop_index(op.f("ix_users_username"), table_name="users")
    op.drop_index(op.f("ix_users_role"), table_name="users")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
    op.drop_index(op.f("ix_integration_configs_provider"), table_name="integration_configs")
    op.drop_table("integration_configs")
    op.drop_index("ix_indicators_type_value", table_name="indicators")
    op.drop_index(op.f("ix_indicators_type"), table_name="indicators")
    op.drop_table("indicators")
    op.drop_index(op.f("ix_campaigns_status"), table_name="campaigns")
    op.drop_index(op.f("ix_campaigns_name"), table_name="campaigns")
    op.drop_table("campaigns")
