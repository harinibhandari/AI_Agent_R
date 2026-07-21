"""
answer_agent.py

Uses Groq to convert SQL results into a natural language answer.
"""

from groq import Groq

from config import GROQ_API_KEY, MODEL_NAME
from agent.prompts import ANSWER_SYSTEM_PROMPT


class AnswerAgent:

    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)

    def generate_answer(
        self,
        question: str,
        sql: str,
        result
    ) -> str:

        result_text = result.to_markdown(index=False)

        user_prompt = f"""
User Question:

{question}

Executed SQL:

{sql}

SQL Result:

{result_text}
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