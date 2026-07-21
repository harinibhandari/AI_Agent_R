import pandas as pd

from app.database.duckdb_manager import DuckDBManager
from app.database.sql_executor import SQLExecutor


def test_sql_execution():

    df = pd.DataFrame({
        "Age": [20, 30, 40]
    })

    db = DuckDBManager()

    db.load_dataframe(df)

    executor = SQLExecutor(db.get_connection())

    result = executor.execute(
        "SELECT AVG(Age) AS avg_age FROM data"
    )

    assert result.iloc[0]["avg_age"] == 30

    db.close()