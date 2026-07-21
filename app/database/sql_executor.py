"""
sql_executor.py

Executes SQL queries on DuckDB.
"""

import pandas as pd
import duckdb


class SQLExecutor:

    def __init__(self, connection: duckdb.DuckDBPyConnection):
        self.connection = connection

    def execute(self, sql: str) -> pd.DataFrame:
        """
        Execute SQL and return results as a DataFrame.
        """

        result = self.connection.execute(sql).fetchdf()

        return result