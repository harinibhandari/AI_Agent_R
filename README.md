# 🤖 AI CSV Data Q&A Agent

> Ask questions about any CSV file in plain English.
> The AI agent converts natural language into SQL, executes it using DuckDB, and returns accurate answers backed by real computation.

---

# 🚀 Overview

AI CSV Data Q&A Agent is an intelligent data analysis assistant that allows users to upload any CSV dataset and ask questions in natural language.

Instead of guessing answers, the agent:

- Understands the dataset schema
- Generates SQL using an LLM (Groq Llama 3.3 70B)
- Validates SQL for safety
- Executes the query using DuckDB
- Returns both the computed result and a human-readable explanation

This prevents hallucinations because every answer comes directly from executing SQL on the uploaded dataset.

---

# ✨ Features

✅ Upload any CSV file

✅ Automatic schema detection

✅ AI-generated SQL queries

✅ SQL safety validation

✅ DuckDB in-memory execution

✅ Natural language answers

✅ Suggested dataset questions

✅ Query execution time

✅ QA logging

✅ Interactive CLI

✅ Streamlit Web UI

---

# 🏗 Project Architecture

```
                User

                  │

                  ▼

          Upload CSV File

                  │

                  ▼

           Pandas DataFrame

                  │

                  ▼

        DuckDB In-Memory Database

                  │

                  ▼

          Database Schema Reader

                  │

                  ▼

          Natural Language Question

                  │

                  ▼

            Groq LLM (SQL Agent)

                  │

                  ▼

          Generated SQL Query

                  │

                  ▼

           SQL Validator

                  │

                  ▼

          DuckDB Execution

                  │

                  ▼

            Result Table

                  │

                  ▼

          Groq LLM (Answer Agent)

                  │

                  ▼

     Final Answer + Supporting Data
```

---

# 📂 Project Structure

```
csv-data-qa-agent

│

├── app
│
├── agent
│     answer_agent.py
│     sql_agent.py
│     prompt.py
│     question_suggester.py
│
├── database
│     csv_loader.py
│     duckdb_manager.py
│     schema_reader.py
│     sql_executor.py
│     sql_validator.py
│
├── logger
│     qa_logger.py
│
├── outputs
│     qa_log.json
│
├── sample_data
│     Employee.csv
│
├── streamlit_app.py
├── main.py
├── requirements.txt
├── README.md
```

---

# 🧠 AI Workflow

```
Load CSV

↓

Read Schema

↓

Suggest Sample Questions

↓

User Question

↓

Generate SQL using LLM

↓

Validate SQL

↓

Execute in DuckDB

↓

Generate Final Answer

↓

Save QA Log
```

---

# 🔒 SQL Validation

Allowed

- SELECT
- FROM
- WHERE
- GROUP BY
- ORDER BY
- LIMIT
- HAVING
- COUNT
- SUM
- AVG
- MIN
- MAX

Blocked

- DROP
- DELETE
- UPDATE
- ALTER
- CREATE
- INSERT
- TRUNCATE
- MERGE
- CALL

This prevents malicious SQL execution.

---

# 🧠 Prompt Engineering

## SQL Agent

The SQL generation prompt instructs the LLM to:

- Use only provided schema
- Never invent columns
- Never invent tables
- Generate valid DuckDB SQL
- Return SQL only
- Generate only SELECT statements
- Return NOT_POSSIBLE if the question cannot be answered

---

## Answer Agent

The Answer Agent receives

- Original Question
- Executed SQL
- SQL Result

and generates

- concise
- factual
- human-readable answers

without changing computed values.

---

# 🛠 Technologies Used

| Technology | Purpose |
|------------|----------|
| Python | Backend |
| Groq API | LLM |
| Llama 3.3 70B | SQL Generation |
| DuckDB | SQL Execution |
| Pandas | CSV Processing |
| Streamlit | Web Interface |
| JSON | QA Logging |

---

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/harinibhandari/AI_Agent_R.git
```

Create virtual environment

```bash
python -m venv venv
```

Activate

Windows

```bash
venv\Scripts\activate
```

Install packages

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create

```
.env
```

Add

```
GROQ_API_KEY=YOUR_API_KEY
MODEL_NAME=llama-3.3-70b-versatile
```

---

# ▶ Run CLI

```bash
python app/main.py
```

---

# 🌐 Run Streamlit UI

```bash
streamlit run app/streamlit_app.py
```

---

# 📊 Sample Questions

- How many employees are from Bangalore?
- Show top 10 oldest employees.
- Average employee age.
- Which city has the highest employees?
- Count female employees.
- Employees with Payment Tier 3.
- Average experience by city.
- Show employees older than 30.
- Count employees who left.
- Which education level has the highest employees?

---

# 📋 Sample Output

Question

```
How many employees are from Bangalore?
```

Generated SQL

```sql
SELECT COUNT(*)
FROM data
WHERE City='Bangalore';
```

Result

```
2228
```

Answer

```
There are 2,228 employees from Bangalore.
```

---

# 📁 QA Log

Each interaction is stored as JSON.

Example

```json
{
  "question": "How many employees are from Bangalore?",
  "generated_sql": "SELECT COUNT(*) FROM data WHERE City='Bangalore';",
  "answer": "There are 2228 employees from Bangalore.",
  "execution_time_ms": 38
}
```

---

# 🧪 Testing

The agent has been tested with

- Count Queries

- Filtering

- Top N Queries

- Aggregations

- Sorting

- Average

- Group By

- Min/Max

- Invalid Questions

- SQL Validation

---

# 🚫 Hallucination Prevention

This project avoids hallucinations by

✔ Generating SQL only

✔ Executing SQL using DuckDB

✔ Returning actual computed values

✔ Never fabricating numbers

✔ Validating SQL before execution

---

# ⚖ Tradeoffs

Due to the 24-hour challenge:

- Single-table datasets are supported.
- Relational joins are not included.
- Visualization is minimal.
- SQL validation is rule-based.

Future Improvements

- Multi-table support
- Charts
- Download reports
- Voice queries
- Conversational memory
- Cached schema embeddings

---

# 📷 Screenshots

Add screenshots of

- CLI
- Streamlit UI
- Generated SQL
- Results

inside

```
screenshots/
```

---

# 👩‍💻 Author

**Harini Bhandari**

AI / ML Engineer

GenAI Engineer

Agentic AI Developer

GitHub

https://github.com/harinibhandari

LinkedIn

https://linkedin.com/in/harinibhandari24

---

# ⭐ Conclusion

AI CSV Data Q&A Agent demonstrates how Large Language Models can safely answer natural language questions over structured data using real computation instead of hallucination.

By combining Groq Llama, DuckDB, SQL validation, and natural-language explanation, the system provides trustworthy answers while remaining lightweight, modular, and easy to extend.