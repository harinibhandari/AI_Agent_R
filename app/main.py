"""
main.py

Entry point for the AI CSV Data Q&A Agent.
"""

import time

from config import validate_config

from database.csv_loader import load_csv
from database.duckdb_manager import DuckDBManager
from database.schema_reader import SchemaReader
from database.sql_validator import SQLValidator
from database.sql_executor import SQLExecutor

from agent.sql_agent import SQLAgent
from agent.answer_agent import AnswerAgent

from logger.qa_logger import QALogger


def main():
    # Validate configuration
    validate_config()

    # Load CSV
    csv_path = input("Enter CSV path: ").strip()

    df = load_csv(csv_path)
    print("\n✅ CSV Loaded Successfully!")

    # Load into DuckDB
    db = DuckDBManager()
    db.load_dataframe(df)
    print("✅ Data loaded into DuckDB successfully!")

    connection = db.get_connection()

    # Read schema
    schema_reader = SchemaReader(connection)
    schema = schema_reader.get_schema()

    print("\nDatabase Schema:\n")
    print(schema)

    # Create reusable objects
    sql_agent = SQLAgent()
    answer_agent = AnswerAgent()
    executor = SQLExecutor(connection)
    logger = QALogger()

    # Keep asking questions
    while True:

        question = input("\nAsk a question (or type 'exit' to quit): ").strip()

        if question.lower() == "exit":
            print("\n👋 Thank you for using AI CSV Data Q&A Agent!")
            break

        start_time = time.time()

        try:
            # Generate SQL
            generated_sql = sql_agent.generate_sql(
                schema=schema,
                question=question
            )

            print("\nGenerated SQL:\n")
            print(generated_sql)

            # Validate SQL
            validated_sql = SQLValidator.validate(generated_sql)

            print("\nValidated SQL:\n")
            print(validated_sql)

            # Execute SQL
            result = executor.execute(validated_sql)

            print("\nQuery Result:\n")
            print(result)

            # Generate Answer
            answer = answer_agent.generate_answer(
                question=question,
                sql=validated_sql,
                result=result
            )

            print("\nFinal Answer:\n")
            print(answer)

            execution_time = round(
                (time.time() - start_time) * 1000,
                2
            )

            print(f"\nExecution Time: {execution_time} ms")

            # Save Log
            logger.log(
                question=question,
                sql=validated_sql,
                answer=answer,
                execution_time_ms=execution_time
            )

            print("✅ QA Log saved successfully!")

        except Exception as e:
            print(f"\n❌ Error: {e}")

    # Close database
    db.close()


if __name__ == "__main__":
    main()