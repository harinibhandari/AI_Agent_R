import pandas as pd


def test_dataframe_creation():

    df = pd.DataFrame({
        "Count": [10]
    })

    assert df.iloc[0]["Count"] == 10