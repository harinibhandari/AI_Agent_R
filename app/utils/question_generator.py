import pandas as pd


class QuestionGenerator:

    @staticmethod
    def generate(df: pd.DataFrame):

        questions = []

        columns = list(df.columns)

        numeric_cols = list(df.select_dtypes(include="number").columns)

        text_cols = list(df.select_dtypes(include="object").columns)

        # Generic
        questions.append("How many records are there?")

        # Numeric columns
        for col in numeric_cols:

            questions.append(f"What is the average {col}?")

            questions.append(f"What is the maximum {col}?")

            questions.append(f"What is the minimum {col}?")

        # Text columns
        for col in text_cols:

            questions.append(f"How many records are there for each {col}?")

            questions.append(f"Which {col} appears the most?")

        return questions[:10]