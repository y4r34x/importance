"""Data transformation utilities for contract features."""
import pandas as pd
from datetime import datetime


def calculate_term_length(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate contract term length from effective and expiration dates.

    Adds a 'term_length_days' column based on the difference between
    'Effective Date' and 'Expiration Date' columns.

    Args:
        df: DataFrame with 'Effective Date' and 'Expiration Date' columns

    Returns:
        DataFrame with additional 'term_length_days' column
    """
    df = df.copy()

    if 'Effective Date' not in df.columns or 'Expiration Date' not in df.columns:
        print("Warning: Missing date columns for term length calculation")
        return df

    def parse_date(date_str):
        """Try to parse various date formats."""
        if pd.isna(date_str) or date_str == '':
            return None

        formats = [
            '%m/%d/%Y',
            '%m/%d/%y',
            '%Y-%m-%d',
            '%d-%m-%Y',
            '%B %d, %Y',
        ]

        for fmt in formats:
            try:
                return datetime.strptime(str(date_str).strip(), fmt)
            except ValueError:
                continue

        return None

    def calc_days(row):
        """Calculate days between dates."""
        effective = parse_date(row.get('Effective Date'))
        expiration = parse_date(row.get('Expiration Date'))

        if effective and expiration:
            delta = expiration - effective
            return delta.days

        return None

    df['term_length_days'] = df.apply(calc_days, axis=1)

    return df


def normalize_party_names(df: pd.DataFrame, column: str = 'Parties') -> pd.DataFrame:
    """
    Normalize party names by removing common legal suffixes.

    Args:
        df: DataFrame with party name column
        column: Name of the column containing party names

    Returns:
        DataFrame with normalized party names
    """
    df = df.copy()

    if column not in df.columns:
        return df

    suffixes = [
        ', inc.', ', inc', ' inc.', ' inc',
        ', corp.', ', corp', ' corp.', ' corp',
        ', llc', ' llc',
        ', ltd.', ', ltd', ' ltd.', ' ltd',
        ', l.p.', ' l.p.',
        ', co.', ' co.',
    ]

    def normalize(name):
        if pd.isna(name):
            return name
        name = str(name).lower().strip()
        for suffix in suffixes:
            if name.endswith(suffix):
                name = name[:-len(suffix)]
        return name.strip()

    df[f'{column}_normalized'] = df[column].apply(normalize)

    return df


def encode_boolean_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert yes/no string columns to boolean integers.

    Converts columns containing 'yes'/'no' values to 1/0.

    Args:
        df: DataFrame with yes/no columns

    Returns:
        DataFrame with encoded boolean columns
    """
    df = df.copy()

    for col in df.columns:
        if df[col].dtype == 'object':
            unique_vals = df[col].dropna().str.lower().unique()
            if set(unique_vals).issubset({'yes', 'no', ''}):
                df[col] = df[col].apply(
                    lambda x: 1 if str(x).lower() == 'yes' else (0 if str(x).lower() == 'no' else None)
                )

    return df
