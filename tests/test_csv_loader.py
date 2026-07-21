from pathlib import Path
from app.database.csv_loader import load_csv


def test_load_csv():
    csv_path = Path("sample_data/Employee.csv")

    df = load_csv(csv_path)

    assert df is not None
    assert not df.empty