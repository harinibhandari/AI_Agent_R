import pandas as pd

from app.database.duckdb_manager import DuckDBManager


def test_duckdb_load_dataframe():

    df = pd.DataFrame({
        "Name": ["Alice", "Bob"],
        "Age": [22, 30]
    })

    db = DuckDBManager()

    db.load_dataframe(df)

    conn = db.get_connection()

    count = conn.execute(
        "SELECT COUNT(*) FROM data"
    ).fetchone()[0]

    assert count == 2

    db.close()