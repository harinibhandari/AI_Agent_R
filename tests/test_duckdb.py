import pandas as pd

from app.database.duckdb_manager import DuckDBManager


def test_duckdb():

    df = pd.DataFrame({

        "Name": ["A", "B"],

        "Age": [20, 30]

    })

    db = DuckDBManager()

    db.load_dataframe(df)

    conn = db.get_connection()

    result = conn.execute(

        "SELECT COUNT(*) FROM data"

    ).fetchone()[0]

    assert result == 2

    db.close()