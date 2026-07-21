# 🤖 AI CSV Data Q&A Agent

Ask natural language questions about any CSV dataset and get accurate, computation-backed answers — powered by **Groq Llama 3.3 70B** and **DuckDB**.

No hallucinated numbers. Every answer is derived from a real SQL query executed against your actual data.

---

## ✨ Features

- 📂 Upload any CSV file (via CLI or Streamlit web UI)
- 🧠 Automatic schema detection
- 💡 AI-generated sample questions based on your dataset
- 🗣️ Natural language → SQL translation using Groq Llama 3.3
- 🔒 Strict SQL validation — only safe, read-only `SELECT` queries are allowed
- ⚡ Fast in-memory query execution with DuckDB
- 📝 Business-friendly natural language answers generated from real query results
- 📊 Interactive result tables with CSV export (Streamlit UI)
- 🗂️ Automatic JSON logging of every question, SQL, answer, and execution time

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
        Groq Llama 3.3 Generates SQL
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
    Groq Llama Generates Final Explanation
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
             Groq Llama 3.3 (SQL Agent)
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
           Groq Llama (Answer Agent)
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
5. The final response is generated strictly from that computed data.

This guarantees every numerical answer is derived from the dataset, not guessed by the model.

---

## ⚙️ Technology Stack

| Component             | Technology                   |
|------------------------|------------------------------|
| Programming Language   | Python                       |
| LLM                     | Groq Llama 3.3 70B           |
| Data Processing         | Pandas                       |
| SQL Engine              | DuckDB                       |
| Frontend                | Streamlit                    |
| Logging                 | JSON                         |
| Environment              | Python Virtual Environment   |

---

## 📁 Project Structure

```text
csv-data-qa-agent/
│
├── .streamlit/
│   └── config.toml            # Streamlit theme configuration
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
pip install pandas duckdb streamlit groq python-dotenv tabulate
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
MODEL=llama-3.3-70b-versatile
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

## 📄 License

This project is available for personal and educational use. Add your preferred license here (e.g., MIT).
