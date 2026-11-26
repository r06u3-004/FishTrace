from sqlalchemy import UniqueConstraint

from app.models import IntelResult


def test_expected_tables_exist(schema_inspector):
    expected = {
        "activity_events",
        "analysis_results",
        "analyst_notes",
        "attachments",
        "auth_results",
        "campaign_investigations",
        "campaigns",
        "emails",
        "indicator_sightings",
        "indicators",
        "integration_configs",
        "intel_results",
        "investigations",
        "reports",
        "users",
    }

    assert expected.issubset(set(schema_inspector.get_table_names()))


def test_indicator_uniqueness(schema_inspector):
    constraints = schema_inspector.get_unique_constraints("indicators")

    assert any(item["name"] == "uq_indicators_type_normalized" for item in constraints)


def test_intel_result_uniqueness_is_declared():
    constraints = [item for item in IntelResult.__table__.constraints if isinstance(item, UniqueConstraint)]

    assert any(item.name == "uq_intel_results_indicator_provider_queried" for item in constraints)
