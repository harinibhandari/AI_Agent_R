"""
main.py

Entry point for the AI CSV Data Q&A Agent.
"""

from config import validate_config
from database.csv_loader import load_csv
from database.duckdb_manager import DuckDBManager
from database.schema_reader import SchemaReader
from database.sql_validator import SQLValidator
from database.sql_executor import SQLExecutor
from agent.sql_agent import SQLAgent


def main():
    # -----------------------------
    # Validate configuration
    # -----------------------------
    validate_config()

    # -----------------------------
    # Get CSV path
    # -----------------------------
    csv_path = input("Enter CSV path: ")

    # -----------------------------
    # Load CSV
    # -----------------------------
    df = load_csv(csv_path)

    print("\n✅ CSV Loaded Successfully!")

    # -----------------------------
    # Create DuckDB database
    # -----------------------------
    db = DuckDBManager()

    db.load_dataframe(df)

    print("✅ Data loaded into DuckDB successfully!")

    # -----------------------------
    # Get DuckDB connection
    # -----------------------------
    connection = db.get_connection()

    # -----------------------------
    # Read database schema
    # -----------------------------
    schema_reader = SchemaReader(connection)

    schema = schema_reader.get_schema()

    print("\nDatabase Schema:\n")
    print(schema)

    # -----------------------------
    # Create SQL Agent
    # -----------------------------
    sql_agent = SQLAgent()

    # -----------------------------
    # Ask user question
    # -----------------------------
    question = input("\nAsk a question: ")

    # -----------------------------
    # Generate SQL
    # -----------------------------
    generated_sql = sql_agent.generate_sql(
        schema=schema,
        question=question
    )

    print("\nGenerated SQL:\n")
    print(generated_sql)

    # -----------------------------
    # Validate SQL
    # -----------------------------
    validated_sql = SQLValidator.validate(generated_sql)

    print("\nValidated SQL:\n")
    print(validated_sql)

    # -----------------------------
    # Execute SQL
    # -----------------------------
    executor = SQLExecutor(connection)

    result = executor.execute(validated_sql)

    print("\nQuery Result:\n")
    print(result)

    # -----------------------------
    # Close database
    # -----------------------------
    db.close()


if __name__ == "__main__":
    main()