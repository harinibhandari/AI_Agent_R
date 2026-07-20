"""
csv_loader.py

Loads a CSV file into a Pandas DataFrame.
"""

from pathlib import Path
import pandas as pd


def load_csv(csv_path: str) -> pd.DataFrame:
    """
    Load a CSV file into a Pandas DataFrame.

    Args:
        csv_path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Loaded dataframe.

    Raises:
        FileNotFoundError: If the CSV file doesn't exist.
        ValueError: If the CSV is empty.
        Exception: For any other CSV reading errors.
    """

    file_path = Path(csv_path)

    # Check if file exists
    if not file_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    try:
        df = pd.read_csv(file_path)

        # Check if dataframe is empty
        if df.empty:
            raise ValueError("The CSV file is empty.")

        return df

    except pd.errors.EmptyDataError:
        raise ValueError("CSV contains no data.")

    except pd.errors.ParserError:
        raise ValueError("Invalid CSV format.")

    except Exception as e:
        raise Exception(f"Failed to load CSV: {e}")