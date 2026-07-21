import pandas as pd
import pytest

from app.agent import answer_agent as answer_agent_module
from app.agent.answer_agent import AnswerAgent


@pytest.fixture
def agent(monkeypatch):
    # AnswerAgent() builds a Groq client at construction time, which needs
    # *a* key even for tests that never actually call the API. Patch the
    # module-level constant so tests don't depend on a real GROQ_API_KEY.
    monkeypatch.setattr(answer_agent_module, "GROQ_API_KEY", "test-key")
    return AnswerAgent()


def test_empty_result_returns_no_data_message(agent):
    result = pd.DataFrame()

    answer = agent.generate_answer(
        question="How many rows are there?",
        sql="SELECT * FROM data WHERE 1=0",
        result=result,
    )

    assert answer == "No matching data was found in the dataset."


def test_single_value_result_formats_as_column_and_value(agent):
    result = pd.DataFrame({"total_orders": [42]})

    answer = agent.generate_answer(
        question="How many orders are there?",
        sql="SELECT COUNT(*) AS total_orders FROM data",
        result=result,
    )

    assert answer == "total_orders: 42"


def test_single_value_float_is_rounded_to_two_decimals(agent):
    result = pd.DataFrame({"avg_age": [30.4567]})

    answer = agent.generate_answer(
        question="What is the average age?",
        sql="SELECT AVG(Age) AS avg_age FROM data",
        result=result,
    )

    assert answer == "avg_age: 30.46"


def test_small_table_result_includes_every_row(agent):
    result = pd.DataFrame({
        "City": ["Delhi", "Mumbai", "Pune"],
        "Count": [5, 3, 2],
    })

    answer = agent.generate_answer(
        question="How many employees per city?",
        sql="SELECT City, COUNT(*) AS Count FROM data GROUP BY City",
        result=result,
    )

    assert "Delhi" in answer
    assert "Mumbai" in answer
    assert "Pune" in answer


def test_small_table_boundary_at_exactly_ten_rows_skips_llm_call(agent, monkeypatch):
    # Exactly 10 rows should take the deterministic table-formatting path,
    # not the LLM summarization path — calling the API here should fail
    # the test loudly instead of hanging on a network call.
    def fail_if_called(**kwargs):
        raise AssertionError("LLM should not be called for a 10-row result")

    monkeypatch.setattr(agent.client.chat.completions, "create", fail_if_called)

    result = pd.DataFrame({"n": list(range(10))})

    answer = agent.generate_answer(
        question="List the values",
        sql="SELECT n FROM data",
        result=result,
    )

    assert "9" in answer