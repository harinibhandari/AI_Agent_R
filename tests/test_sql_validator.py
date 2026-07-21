import pytest

from app.database.sql_validator import SQLValidator


def test_valid_select():

    sql = "SELECT * FROM data"

    assert SQLValidator.validate(sql) == sql


def test_invalid_drop():

    with pytest.raises(ValueError):

        SQLValidator.validate(
            "DROP TABLE data"
        )


def test_invalid_delete():

    with pytest.raises(ValueError):

        SQLValidator.validate(
            "DELETE FROM data"
        )