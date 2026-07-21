import pytest

from app.database.sql_validator import SQLValidator


@pytest.mark.parametrize("sql", [
    "SELECT * FROM data",
    "SELECT COUNT(*) FROM data",
    "WITH recent AS (SELECT * FROM data) SELECT * FROM recent",
])
def test_valid_queries_pass_through_unchanged(sql):
    assert SQLValidator.validate(sql) == sql


def test_strips_markdown_code_fences():
    sql = "```sql\nSELECT * FROM data\n```"
    assert SQLValidator.validate(sql) == "SELECT * FROM data"


def test_allows_and_strips_trailing_semicolon():
    assert SQLValidator.validate("SELECT * FROM data;") == "SELECT * FROM data"


def test_rejects_query_not_starting_with_select_or_with():
    with pytest.raises(ValueError):
        SQLValidator.validate("PRAGMA table_info(data)")


def test_invalid_drop():
    with pytest.raises(ValueError):
        SQLValidator.validate("DROP TABLE data")


def test_invalid_delete():
    with pytest.raises(ValueError):
        SQLValidator.validate("DELETE FROM data")


@pytest.mark.parametrize("keyword", [
    "INSERT", "UPDATE", "DELETE", "DROP", "ALTER",
    "CREATE", "TRUNCATE", "MERGE", "CALL",
    "COPY", "ATTACH", "DETACH", "PRAGMA",
])
def test_rejects_every_forbidden_keyword(keyword):
    with pytest.raises(ValueError):
        SQLValidator.validate(f"SELECT * FROM data WHERE 1=1; {keyword} something")


def test_rejects_multiple_statements():
    with pytest.raises(ValueError):
        SQLValidator.validate("SELECT * FROM data; SELECT * FROM data")


def test_does_not_false_positive_on_keyword_inside_column_name():
    # "createdAt" contains "create" but not the whole word CREATE —
    # the \b word-boundary check should not flag this.
    sql = "SELECT createdAt FROM data"
    assert SQLValidator.validate(sql) == sql