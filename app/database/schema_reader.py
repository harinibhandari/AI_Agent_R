"""
schema_reader.py

Reads the schema of a DuckDB table.
"""

import duckdb


class SchemaReader:
    """
    Reads table schema from DuckDB.
    """

    def __init__(self, connection: duckdb.DuckDBPyConnection):
        self.connection = connection

    def get_schema(self, table_name: str = "data") -> str:
        """
        Returns a formatted schema for the specified table.

        Args:
            table_name (str): Name of the table.

        Returns:
            str: Formatted schema.
        """

        query = f"""
        DESCRIBE {table_name};
        """

        schema = self.connection.execute(query).fetchall()

        schema_text = f"Table: {table_name}\n\nColumns:\n"

        for column in schema:
            column_name = column[0]
            data_type = column[1]

            schema_text += f"- {column_name} ({data_type})\n"

        return schema_text