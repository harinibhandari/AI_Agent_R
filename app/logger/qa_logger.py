"""
qa_logger.py

Logs every question, generated SQL, answer,
and execution time to a JSON file.
"""

import json
import os
from datetime import datetime


class QALogger:

    def __init__(self, log_file="outputs/qa_log.json"):
        self.log_file = log_file

        # Create outputs directory if it doesn't exist
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

    def log(
        self,
        question,
        sql,
        answer,
        execution_time_ms
    ):
        """
        Save one QA interaction.
        """

        log_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "question": question,
            "generated_sql": sql,
            "answer": answer,
            "execution_time_ms": execution_time_ms
        }

        # Create file if it doesn't exist
        if not os.path.exists(self.log_file):
            with open(self.log_file, "w") as f:
                json.dump([], f, indent=4)

        with open(self.log_file, "r") as f:
            logs = json.load(f)

        logs.append(log_entry)

        with open(self.log_file, "w") as f:
            json.dump(logs, f, indent=4)