from config import validate_config
from database.csv_loader import load_csv
from database.duckdb_manager import DuckDBManager


def main():
    # Validate environment variables
    validate_config()

    # Get CSV path
    csv_path = input("Enter CSV path: ")

    # Load CSV
    df = load_csv(csv_path)

    print("\nCSV Loaded Successfully!")

    # Create DuckDB manager
    db = DuckDBManager()

    # Load DataFrame into DuckDB
    db.load_dataframe(df)

    print("Data loaded into DuckDB successfully!\n")

    # Get database connection
    connection = db.get_connection()

    # Show available tables
    print("Tables in database:")
    print(connection.execute("SHOW TABLES").fetchall())

    print("\nFirst 5 rows from DuckDB:\n")

    result = connection.execute(
        "SELECT * FROM data LIMIT 5"
    ).fetchdf()

    print(result)

    db.close()


if __name__ == "__main__":
    main()