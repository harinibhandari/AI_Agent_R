from unittest.mock import MagicMock

import pytest

from app.agent import sql_agent as sql_agent_module
from app.agent.sql_agent import SQLAgent


SCHEMA = """
Table: data

Columns:
- Age (BIGINT)
- City (VARCHAR)
"""


@pytest.fixture
def agent(monkeypatch):
    monkeypatch.setattr(sql_agent_module, "GROQ_API_KEY", "test-key")
    return SQLAgent()


def test_prompt_input_sanity_check():
    # Original sanity check kept as-is.
    question = "How many employees are there?"
    assert "Age" in SCHEMA
    assert question != ""


def test_generate_sql_returns_model_output(agent, monkeypatch):
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "SELECT COUNT(*) FROM data"

    monkeypatch.setattr(
        agent.client.chat.completions,
        "create",
        lambda **kwargs: mock_response,
    )

    sql = agent.generate_sql(schema=SCHEMA, question="How many employees are there?")

    assert sql == "SELECT COUNT(*) FROM data"


def test_generate_sql_strips_surrounding_whitespace(agent, monkeypatch):
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "  SELECT * FROM data  \n"

    monkeypatch.setattr(
        agent.client.chat.completions,
        "create",
        lambda **kwargs: mock_response,
    )

    sql = agent.generate_sql(schema=SCHEMA, question="Show everything")

    assert sql == "SELECT * FROM data"


def test_generate_sql_passes_schema_and_question_to_the_model(agent, monkeypatch):
    captured = {}

    def fake_create(**kwargs):
        captured["messages"] = kwargs["messages"]
        response = MagicMock()
        response.choices[0].message.content = "SELECT * FROM data"
        return response

    monkeypatch.setattr(agent.client.chat.completions, "create", fake_create)

    agent.generate_sql(schema=SCHEMA, question="How many employees are there?")

    user_message = captured["messages"][1]["content"]
    assert "Age" in user_message
    assert "How many employees are there?" in user_message