"""
answer_agent.py

Generate a natural language answer from SQL results.

Uses Python for simple results and the LLM only when needed.
"""

from groq import Groq

from config import GROQ_API_KEY, MODEL_NAME
from agent.prompts import ANSWER_SYSTEM_PROMPT


class AnswerAgent:

    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)

    def generate_answer(self, question: str, sql: str, result):

        # -------------------------
        # No rows
        # -------------------------
        if result.empty:
            return "No matching data was found in the dataset."

        # -------------------------
        # Single value (COUNT, AVG, SUM...)
        # -------------------------
        if result.shape == (1, 1):

            column = result.columns[0]
            value = result.iloc[0, 0]

            if isinstance(value, float):
                value = round(value, 2)

            return f"{column}: {value}"

        # -------------------------
        # Small table (<=10 rows)
        # -------------------------
        if len(result) <= 10:

            table = result.to_string(index=False)

            return (
                "The query returned the following results:\n\n"
                f"{table}"
            )

        # -------------------------
        # Large table
        # -------------------------
        preview = result.head(20).to_markdown(index=False)

        user_prompt = f"""
User Question:
{question}

Executed SQL:
{sql}

Result Preview:
{preview}

Total Rows:
{len(result)}

Summarize the results in 3-4 simple sentences.
Do not invent numbers.
Mention that only the first 20 rows are shown if appropriate.
"""

        response = self.client.chat.completions.create(
            model=MODEL_NAME,
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": ANSWER_SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
        )

        return response.choices[0].message.content.strip()