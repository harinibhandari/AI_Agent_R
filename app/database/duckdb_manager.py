"""
duckdb_manager.py

Creates an in-memory DuckDB database and loads
a Pandas DataFrame as a SQL table.
"""

import duckdb
import pandas as pd


class DuckDBManager:
    """
    Manages an in-memory DuckDB connection.
    """

    def __init__(self):
        """
        Create an in-memory DuckDB database.
        """
        self.connection = duckdb.connect(database=":memory:")

    def load_dataframe(self, dataframe: pd.DataFrame, table_name: str = "data"):
        self.connection.register("temp_df", dataframe)

        self.connection.execute(f"""
            CREATE OR REPLACE TABLE {table_name} AS
            SELECT *
            FROM temp_df
        """)

    def get_connection(self):
        """
        Return DuckDB connection.
        """
        return self.connection

    def close(self):
        """
        Close database connection.
        """
        self.connection.close()