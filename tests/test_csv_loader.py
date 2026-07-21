import os

from app.database.csv_loader import load_csv


def test_csv_loader():

    csv_path = "sample_data/Employee.csv"

    df = load_csv(csv_path)

    assert df is not None
    assert len(df) > 0
    assert "Age" in df.columns