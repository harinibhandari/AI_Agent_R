# 🤖 AI CSV Data Q&A Agent

Ask natural language questions about any CSV dataset and get accurate, computation-backed answers — powered by **Groq (OpenAI GPT-OSS 120B)** and **DuckDB**.

No hallucinated numbers. Every answer is derived from a real SQL query executed against your actual data.

---

## ✨ Features

- 📂 Upload any CSV file (via CLI or Streamlit web UI)
- 🧠 Automatic schema detection
- 💡 AI-generated sample questions based on your dataset
- 🗣️ Natural language → SQL translation using Groq
- 🔒 Strict SQL validation — only safe, read-only `SELECT` queries are allowed
- ⚡ Fast in-memory query execution with DuckDB
- 📝 Business-friendly natural language answers generated from real query results
- 📊 Interactive result tables with CSV export (Streamlit UI)
- 🗂️ Automatic JSON logging of every question, SQL, answer, and execution time
- ✅ Unit-tested core (validator, executor, loader, agents) — see [Testing](#-testing)

---

## 🔄 Project Workflow

```text
                    START
                      │
                      ▼
             Upload CSV Dataset
                      │
                      ▼
        Load CSV using Pandas DataFrame
                      │
                      ▼
      Store Data in DuckDB (In-Memory)
                      │
                      ▼
        Automatically Read Database Schema
                      │
                      ▼
     Generate Sample Questions (Optional)
                      │
                      ▼
       User Enters Natural Language Query
                      │
                      ▼
        Build Prompt with Schema + Question
                      │
                      ▼
           Groq LLM Generates SQL
                      │
                      ▼
             SQL Validation Layer
        (Only Safe SELECT Queries Allowed)
                      │
                      ▼
       Execute SQL using DuckDB Engine
                      │
                      ▼
           Retrieve Query Results
                      │
                      ▼
     Groq LLM Generates Final Explanation
                      │
                      ▼
      Display:
      • Question
      • Generated SQL
      • Result Table
      • Final Answer
      • Execution Time
                      │
                      ▼
          Save QA Log (JSON File)
                      │
                      ▼
                     END
```

---

## 🏗️ System Architecture

```text
                    User
                      │
                      ▼
           Streamlit UI / CLI
                      │
                      ▼
             CSV File Upload
                      │
                      ▼
               Pandas Loader
                      │
                      ▼
          DuckDB In-Memory Database
                      │
        ┌─────────────┴─────────────┐
        │                           │
        ▼                           ▼
  Schema Reader              Question Input
        │                           │
        └─────────────┬─────────────┘
                      ▼
             Prompt Construction
                      │
                      ▼
              Groq LLM (SQL Agent)
                      │
                      ▼
              Generated SQL Query
                      │
                      ▼
              SQL Validation Layer
                      │
                      ▼
             DuckDB SQL Execution
                      │
                      ▼
                Query Result Table
                      │
                      ▼
            Groq LLM (Answer Agent)
                      │
                      ▼
      Final Answer + SQL + Result + Logs
```

---

## 🤖 What is the Agent?

> The **AI CSV Data Q&A Agent** is an intelligent data analysis assistant that accepts a CSV dataset and a natural language question, converts the question into safe SQL using a Large Language Model, executes the SQL on DuckDB, and returns accurate answers backed by real computation instead of hallucinated responses.

---

## 🚫 Hallucination Prevention

The LLM never answers directly. Instead:

1. The LLM only **generates a SQL query** from the schema and question.
2. The SQL is validated to allow only safe, read-only operations.
3. DuckDB **executes** the SQL against the uploaded CSV.
4. The Answer Agent receives the **actual query result**.
5. For simple results (empty / single value / ≤10 rows), the answer is formatted **directly from the data with plain Python** — no LLM call at all, so there is nothing to hallucinate.
6. Only for larger result sets does the Answer Agent ask the LLM to summarize the real, already-computed rows in plain English — with an explicit instruction not to invent numbers.

This guarantees every numerical answer is derived from the dataset, not guessed by the model.

---

## ⚙️ Technology Stack

| Component             | Technology                        |
|------------------------|-----------------------------------|
| Programming Language   | Python                            |
| LLM                     | Groq — `openai/gpt-oss-120b`      |
| Data Processing         | Pandas                            |
| SQL Engine              | DuckDB                            |
| Frontend                | Streamlit                         |
| Testing                 | Pytest                            |
| Logging                 | JSON                               |
| Environment              | Python Virtual Environment       |

> **Note:** this project originally used `llama-3.3-70b-versatile`. Groq deprecated that model in June 2026, so the default has been switched to `openai/gpt-oss-120b`. If you have an older `.env`, update the `MODEL` value (see [Configure environment variables](#4-configure-environment-variables)).

---

## 📁 Project Structure

```text
csv-data-qa-agent/
│
├── .streamlit/
│   └── config.toml            # Streamlit theme configuration
│
├── conftest.py                 # Makes `app/` importable both as a package
│                                # and via its internal bare imports (see Testing)
├── pytest.ini                  # Pytest configuration (pythonpath, testpaths)
│
├── tests/
│   ├── test_answer_agent.py    # AnswerAgent formatting logic (no API calls)
│   ├── test_config.py          # validate_config() behavior
│   ├── test_csv_loader.py      # CSV loading, missing/empty file handling
│   ├── test_duckdb.py          # DuckDB load + query
│   ├── test_sql_agent.py       # SQLAgent with a mocked Groq client
│   ├── test_sql_executor.py    # SQL execution against DuckDB
│   └── test_sql_validator.py   # Every forbidden keyword + edge cases
│
└── app/
    ├── main.py                 # CLI entry point
    ├── streamlit_app.py        # Streamlit web UI entry point
    ├── config.py                # Environment variable / config loader
    │
    ├── agent/
    │   ├── sql_agent.py          # Converts NL question → SQL
    │   ├── answer_agent.py       # Converts SQL result → NL answer
    │   ├── question_suggester.py # Suggests sample questions from schema
    │   └── prompts.py             # System prompts for SQL & Answer agents
    │
    ├── database/
    │   ├── csv_loader.py         # Loads CSV (file path or upload) into a DataFrame
    │   ├── duckdb_manager.py     # In-memory DuckDB connection manager
    │   ├── schema_reader.py      # Reads and formats table schema
    │   ├── sql_executor.py       # Executes validated SQL, returns DataFrame
    │   └── sql_validator.py      # Blocks unsafe SQL keywords/statements
    │
    ├── logger/
    │   └── qa_logger.py          # Logs Q&A history to outputs/qa_log.json
    │
    └── utils/
        └── question_generator.py # Rule-based fallback question generator
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd csv-data-qa-agent
```

### 2. Create a virtual environment

```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # macOS / Linux
```

### 3. Install dependencies

```bash
pip install pandas duckdb streamlit groq python-dotenv tabulate pytest
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
MODEL=openai/gpt-oss-120b
```

### 5. Run the app

**Streamlit Web UI:**

```bash
streamlit run app/streamlit_app.py
```

**Command Line Interface:**

```bash
python app/main.py
```

---

## 🖥️ Usage

1. Upload a CSV file (sidebar in the web UI, or file path prompt in the CLI).
2. Review the automatically detected schema and suggested questions.
3. Type a natural language question, e.g.:
   - *"What is the average sales per region?"*
   - *"Which product category has the highest revenue?"*
   - *"How many orders were placed each month?"*
4. View the generated SQL, the result table, and a plain-English answer.
5. Download the result as a CSV (web UI) or check `outputs/qa_log.json` for a full history of every question asked.

---

## 🧪 Testing

The core logic — validation, execution, loading, and both agents — is unit tested with **pytest**, including mocked-LLM tests so the suite runs without a live Groq API key.

```bash
pip install pytest
pytest -v
```

Run from the project root — `conftest.py` and `pytest.ini` handle the path setup automatically (this repo's internal modules use bare imports like `from config import ...`, which only resolve correctly with that setup in place).

**What's covered:**

| File | What it tests |
|---|---|
| `test_sql_validator.py` | Every forbidden SQL keyword, markdown-fence stripping, multi-statement rejection, false-positive guard |
| `test_csv_loader.py` | Valid CSV load, missing file, empty file, file-like objects |
| `test_duckdb.py` / `test_sql_executor.py` | DataFrame → DuckDB table → query round trip |
| `test_sql_agent.py` | SQL generation with a mocked Groq response (no network needed) |
| `test_answer_agent.py` | Deterministic answer formatting for empty / single-value / small-table results |
| `test_config.py` | `validate_config()` raises without an API key, passes with one |

---

## 🔒 SQL Safety Rules

**Allowed:** `SELECT`, `FROM`, `WHERE`, `GROUP BY`, `ORDER BY`, `LIMIT`, `HAVING`, `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`, `WITH`, `DISTINCT`

**Blocked:** `INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`, `CREATE`, `TRUNCATE`, `MERGE`, `CALL`, `COPY`, `ATTACH`, `DETACH`, `PRAGMA`

If any blocked keyword is detected, execution stops immediately and an error is shown.

---

## 📝 Logging

Every interaction is saved to `outputs/qa_log.json`, including:

- Timestamp
- Question asked
- Generated SQL
- Final answer
- Execution time (ms)

---

## 📊 Sample Questions & Answers

> Fill this in with real output from a run against your sample dataset before submitting —
> reviewers will check this against the actual repo, so it needs to reflect a genuine run
> rather than illustrative text.

| # | Question | Generated SQL | Answer |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |
| 6 | | | |
| 7 | | | |
| 8 | | | |

---

## ⚖️ Tradeoffs & Design Decisions

- **SQL generation over direct-answer generation:** the LLM never sees the raw data and never answers a question directly — it only writes SQL. This trades a small amount of flexibility (the model can't "eyeball" an answer for ambiguous questions) for a strong guarantee against hallucinated numbers.
- **DuckDB over pandas-only computation:** DuckDB lets the agent express arbitrary aggregations as SQL rather than hand-writing pandas logic per question, and scales better than pandas for larger CSVs.
- **Keyword-blocklist validation over a full SQL parser:** a regex-based blocklist (`SQLValidator`) is simple and fast but not as rigorous as parsing the SQL AST — a determined adversarial prompt could in principle craft SQL that evades a word-boundary check. For a single-user local tool this tradeoff is reasonable; a production multi-tenant version should use a proper SQL parser (e.g. `sqlglot`) to validate structure, not just keywords.
- **No conversation memory:** each question is answered independently with the schema, not prior Q&A context. This keeps prompts small and answers reproducible, at the cost of not supporting natural follow-up questions like "and last year?".
- **Small-result answers are template-formatted, not LLM-generated:** for empty, single-value, and ≤10-row results, `AnswerAgent` formats the answer directly in Python rather than calling the LLM. This is faster, cheaper, and removes any hallucination risk for the common case — the LLM is only used to summarize larger result sets in plain English.
- **What I'd improve with more time:** AST-based SQL validation, conversation memory for follow-up questions, and support for Excel/multi-table joins instead of a single flat CSV table.

---

## 📄 License

HARINI BHANDARI