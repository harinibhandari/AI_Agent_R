"""
csv_loader.py

Loads a CSV file into a Pandas DataFrame.
Supports:
1. Local file path (CLI)
2. Streamlit UploadedFile
"""

from pathlib import Path
import pandas as pd


def load_csv(csv_source) -> pd.DataFrame:
    """
    Load a CSV file into a Pandas DataFrame.

    Args:
        csv_source:
            - str or Path (CLI)
            - Streamlit UploadedFile (Web UI)

    Returns:
        pd.DataFrame

    Raises:
        FileNotFoundError
        ValueError
        Exception
    """

    try:
        # -----------------------------
        # Streamlit UploadedFile
        # -----------------------------
        if hasattr(csv_source, "read"):
            df = pd.read_csv(csv_source)

        # -----------------------------
        # Local File Path
        # -----------------------------
        else:
            file_path = Path(csv_source)

            if not file_path.exists():
                raise FileNotFoundError(
                    f"CSV file not found: {csv_source}"
                )

            df = pd.read_csv(file_path)

        # -----------------------------
        # Empty DataFrame
        # -----------------------------
        if df.empty:
            raise ValueError("The CSV file is empty.")

        return df

    except FileNotFoundError:
        raise

    except pd.errors.EmptyDataError:
        raise ValueError("CSV contains no data.")

    except pd.errors.ParserError:
        raise ValueError("Invalid CSV format.")

    except Exception as e:
        raise Exception(f"Failed to load CSV: {e}")