"""
sql_agent.py

Uses the Groq LLM to convert natural language
questions into DuckDB SQL queries.
"""

from groq import Groq
try:
    from app.config import GROQ_API_KEY, MODEL_NAME
except ImportError:
    from config import GROQ_API_KEY, MODEL_NAME
try:
    from app.agent.prompts import SQL_SYSTEM_PROMPT
except ImportError:
    from agent.prompts import SQL_SYSTEM_PROMPT
class SQLAgent:
    """
    AI Agent that generates SQL from natural language.
    """

    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)

    def generate_sql(self, schema: str, question: str) -> str:
        """
        Generate SQL using the LLM.

        Args:
            schema: Database schema
            question: User question

        Returns:
            SQL query
        """

        user_prompt = f"""
Database Schema:

{schema}

User Question:

{question}

Generate ONLY valid DuckDB SQL.
"""

        response = self.client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": SQL_SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            temperature=0,
        )

        sql = response.choices[0].message.content.strip()

        return sql