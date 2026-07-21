from config import validate_config
from database.csv_loader import load_csv
from database.duckdb_manager import DuckDBManager
from database.schema_reader import SchemaReader
from agent.sql_agent import SQLAgent


def main():

    validate_config()

    csv_path = input("Enter CSV path: ")

    df = load_csv(csv_path)

    print("\nCSV Loaded Successfully!")

    db = DuckDBManager()

    db.load_dataframe(df)

    print("Data loaded into DuckDB successfully!\n")

    connection = db.get_connection()

    schema_reader = SchemaReader(connection)

    schema = schema_reader.get_schema()

    print("Database Schema:\n")

    print(schema)

    print("Tables in database:")

    print(connection.execute("SHOW TABLES").fetchall())

    print("\nFirst 5 rows from DuckDB:\n")

    result = connection.execute(
        "SELECT * FROM data LIMIT 5"
    ).fetchdf()

    print(result)

    # --------------------------
    # AI SQL Generation
    # --------------------------

    sql_agent = SQLAgent()

    question = input("\nAsk a question: ")

    generated_sql = sql_agent.generate_sql(
        schema=schema,
        question=question
    )

    print("\nGenerated SQL:\n")

    print(generated_sql)

    db.close()


if __name__ == "__main__":
    main()