"""Data loading utilities for contract datasets."""
import pandas as pd
from pathlib import Path

from negotiation.extraction.schemas import CUAD_COLUMNS, TSV_COLUMNS


def load_cuad_data(file_path: str | Path = 'data/training/cuad.tsv') -> pd.DataFrame:
    """
    Load CUAD training data from TSV file.

    The CUAD (Contract Understanding Atticus Dataset) contains 510 contracts
    with 22 labeled features from SEC filings.

    Args:
        file_path: Path to the CUAD TSV file

    Returns:
        DataFrame with contract data

    Example:
        >>> df = load_cuad_data()
        >>> print(df.columns.tolist())
        ['URL', 'Document Name', 'Parties', ...]
    """
    df = pd.read_csv(file_path, sep='\t')
    return df


def load_extracted_data(file_path: str | Path = 'data/extracted/raw.tsv') -> pd.DataFrame:
    """
    Load LLM-extracted contract data from TSV file.

    This data is produced by the extraction pipeline (html_parser + llm_extractor)
    and contains 68 features per contract.

    Args:
        file_path: Path to the extracted data TSV file

    Returns:
        DataFrame with extracted contract data

    Example:
        >>> df = load_extracted_data()
        >>> print(df.columns.tolist())
        ['idx', 'form', 'exhibit', ...]
    """
    df = pd.read_csv(file_path, sep='\t')
    return df


def validate_cuad_columns(df: pd.DataFrame) -> bool:
    """
    Validate that a DataFrame has the expected CUAD columns.

    Args:
        df: DataFrame to validate

    Returns:
        True if all expected columns are present
    """
    missing = set(CUAD_COLUMNS) - set(df.columns)
    if missing:
        print(f"Warning: Missing CUAD columns: {missing}")
        return False
    return True


def validate_extracted_columns(df: pd.DataFrame) -> bool:
    """
    Validate that a DataFrame has the expected extraction columns.

    Args:
        df: DataFrame to validate

    Returns:
        True if all expected columns are present
    """
    missing = set(TSV_COLUMNS) - set(df.columns)
    if missing:
        print(f"Warning: Missing extraction columns: {missing}")
        return False
    return True
