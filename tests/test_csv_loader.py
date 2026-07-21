from app.database.csv_loader import load_csv


def test_load_csv():

    df = load_csv("sample_data/Employee.csv")

    assert df is not None
    assert not df.empty
    assert "Age" in df.columns
    assert len(df.columns) > 0