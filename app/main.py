"""
main.py

Entry point for the AI CSV Data Q&A Agent.
"""

import time

try:
    from app.config import validate_config

    from app.database.csv_loader import load_csv
    from app.database.duckdb_manager import DuckDBManager
    from app.database.schema_reader import SchemaReader
    from app.database.sql_validator import SQLValidator
    from app.database.sql_executor import SQLExecutor

    from app.agent.sql_agent import SQLAgent
    from app.agent.answer_agent import AnswerAgent
    from app.agent.question_suggester import QuestionSuggester

    from app.logger.qa_logger import QALogger

except ImportError:

    from config import validate_config

    from database.csv_loader import load_csv
    from database.duckdb_manager import DuckDBManager
    from database.schema_reader import SchemaReader
    from database.sql_validator import SQLValidator
    from database.sql_executor import SQLExecutor

    from agent.sql_agent import SQLAgent
    from agent.answer_agent import AnswerAgent
    from agent.question_suggester import QuestionSuggester

    from logger.qa_logger import QALogger

def main():

    # -------------------------------------
    # Validate Environment
    # -------------------------------------
    validate_config()

    # -------------------------------------
    # Load CSV
    # -------------------------------------
    csv_path = input("Enter CSV path: ").strip()

    df = load_csv(csv_path)

    print("\n✅ CSV Loaded Successfully!")

    # -------------------------------------
    # Load into DuckDB
    # -------------------------------------
    db = DuckDBManager()
    db.load_dataframe(df)

    print("✅ Data loaded into DuckDB successfully!")

    connection = db.get_connection()

    # -------------------------------------
    # Read Schema
    # -------------------------------------
    schema_reader = SchemaReader(connection)
    schema = schema_reader.get_schema()

    print("\n" + "=" * 70)
    print("📋 DATASET SCHEMA")
    print("=" * 70)
    print(schema)

    # -------------------------------------
    # Suggest Questions
    # -------------------------------------
    print("\n🤖 Analyzing dataset...")

    suggester = QuestionSuggester()

    try:
        questions = suggester.suggest_questions(schema)

        print("\n📌 Suggested Questions\n")
        print(questions)

    except Exception as e:
        print(f"\n⚠ Could not generate suggestions: {e}")

    # -------------------------------------
    # Initialize Components
    # -------------------------------------
    sql_agent = SQLAgent()
    answer_agent = AnswerAgent()
    executor = SQLExecutor(connection)
    logger = QALogger()

    # -------------------------------------
    # Interactive Loop
    # -------------------------------------
    while True:

        question = input(
            "\nAsk a question (type exit/quit/q to quit): "
        ).strip()

        if question.lower() in ["exit", "quit", "q"]:
            print("\n👋 Thank you for using AI CSV Data Q&A Agent!")
            break

        start_time = time.time()

        try:

            # ---------------------------------
            # Generate SQL
            # ---------------------------------
            generated_sql = sql_agent.generate_sql(
                schema=schema,
                question=question
            )

            # ---------------------------------
            # Validate SQL
            # ---------------------------------
            validated_sql = SQLValidator.validate(
                generated_sql
            )

            # ---------------------------------
            # Execute SQL
            # ---------------------------------
            result = executor.execute(
                validated_sql
            )

            # ---------------------------------
            # Generate Answer
            # ---------------------------------
            answer = answer_agent.generate_answer(
                question=question,
                sql=validated_sql,
                result=result
            )

            execution_time = round(
                (time.time() - start_time) * 1000,
                2
            )

            # ---------------------------------
            # Professional Output
            # ---------------------------------
            print("\n" + "=" * 70)
            print("🤖 AI CSV Data Q&A Agent")
            print("=" * 70)

            print("\n📝 Question:")
            print(question)

            print("\n💻 Generated SQL:")
            print(validated_sql)

            print("\n📊 Query Result:")
            print(result.to_string(index=False))

            print("\n💡 Answer:")
            print(answer)

            print(f"\n⏱ Execution Time: {execution_time} ms")

            print("=" * 70)

            # ---------------------------------
            # Save Log
            # ---------------------------------
            logger.log(
                question=question,
                sql=validated_sql,
                answer=answer,
                execution_time_ms=execution_time
            )

            print("✅ QA Log saved successfully!")

        except FileNotFoundError:
            print("\n❌ CSV file not found.")

        except ValueError as e:
            print(f"\n❌ Validation Error: {e}")

        except Exception as e:
            print(f"\n❌ Error: {e}")

    # -------------------------------------
    # Close Database
    # -------------------------------------
    db.close()


if __name__ == "__main__":
    main()