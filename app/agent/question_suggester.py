"""
question_suggester.py

Generates intelligent questions based on the database schema.
"""

from groq import Groq

from config import GROQ_API_KEY, MODEL_NAME


class QuestionSuggester:

    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)

    def suggest_questions(self, schema: str):

        prompt = f"""
You are an expert data analyst.

Below is a database schema.

{schema}

Suggest 10 useful business questions that can be answered using ONLY this dataset.

Rules:

- Use only the available columns.
- Do not invent columns.
- Questions should be short.
- Questions should be practical.
- Return ONLY the questions.
- Number them from 1 to 10.
"""

        response = self.client.chat.completions.create(
            model=MODEL_NAME,
            temperature=0.3,
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional data analyst."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content.strip()