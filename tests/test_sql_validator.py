import pytest

from app.database.sql_validator import SQLValidator


def test_valid_sql():

    sql = "SELECT * FROM data"

    assert SQLValidator.validate(sql) == sql


def test_invalid_sql():

    with pytest.raises(ValueError):

        SQLValidator.validate(
            "DROP TABLE data"
        )