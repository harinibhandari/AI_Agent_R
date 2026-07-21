import pandas as pd
import pytest

from app.database.csv_loader import load_csv


def test_load_csv_from_path(tmp_path):
    csv_path = tmp_path / "sample.csv"
    csv_path.write_text("Name,Age,City\nAlice,30,Delhi\nBob,25,Mumbai\n")

    df = load_csv(str(csv_path))

    assert not df.empty
    assert list(df.columns) == ["Name", "Age", "City"]
    assert len(df) == 2


def test_load_csv_missing_file_raises_file_not_found_error(tmp_path):
    missing_path = tmp_path / "does_not_exist.csv"

    with pytest.raises(FileNotFoundError):
        load_csv(str(missing_path))


def test_load_csv_empty_file_raises_value_error(tmp_path):
    csv_path = tmp_path / "empty.csv"
    csv_path.write_text("")

    with pytest.raises(ValueError):
        load_csv(str(csv_path))


def test_load_csv_accepts_file_like_object(tmp_path):
    import io

    buffer = io.StringIO("Name,Age\nAlice,30\n")
    df = load_csv(buffer)

    assert not df.empty
    assert "Name" in df.columns