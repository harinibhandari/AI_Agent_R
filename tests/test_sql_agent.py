def test_prompt_input():

    schema = """
    Table: data

    Columns:
    Age BIGINT
    City VARCHAR
    """

    question = "How many employees are there?"

    assert "Age" in schema
    assert question != ""