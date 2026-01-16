"""Data transformation utilities for contract features."""
import pandas as pd
import numpy as np
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


def bucket_renewal_term(df: pd.DataFrame) -> pd.DataFrame:
    """
    Bucket 'Renewal Term (Days)' into ordinal categories.

    Categories:
        0 = none/unspecified (NaN or 0)
        1 = short (< 365 days)
        2 = standard (365 days / 1 year)
        3 = long (366-1095 days / 2-3 years)
        4 = very_long (> 1095 days / 3+ years)

    Args:
        df: DataFrame with 'Renewal Term (Days)' column

    Returns:
        DataFrame with additional 'Renewal Term Bucket' column
    """
    df = df.copy()

    col = 'Renewal Term (Days)'
    if col not in df.columns:
        return df

    def bucket(val):
        if pd.isna(val):
            return 0
        # Handle string values like "3 years" or "successive 1820"
        if isinstance(val, str):
            val = val.lower().strip()
            # Try to extract number
            import re
            nums = re.findall(r'\d+', val)
            if nums:
                val = int(nums[0])
                # If it mentions "years", multiply
                if 'year' in val if isinstance(val, str) else False:
                    val = val * 365
            else:
                return 0
        try:
            val = float(val)
        except (ValueError, TypeError):
            return 0

        if val <= 0:
            return 0
        elif val < 365:
            return 1  # short
        elif val == 365:
            return 2  # standard (1 year)
        elif val <= 1095:
            return 3  # long (2-3 years)
        else:
            return 4  # very_long (3+ years)

    df['Renewal Term Bucket'] = df[col].apply(bucket)

    return df


def bucket_notice_period(df: pd.DataFrame) -> pd.DataFrame:
    """
    Bucket 'Notice Period To Terminate Renewal' into ordinal categories.

    Categories:
        0 = none/unspecified (NaN)
        1 = short (≤ 30 days)
        2 = standard (31-90 days)
        3 = long (> 90 days)

    Args:
        df: DataFrame with 'Notice Period To Terminate Renewal' column

    Returns:
        DataFrame with additional 'Notice Period Bucket' column
    """
    df = df.copy()

    col = 'Notice Period To Terminate Renewal'
    if col not in df.columns:
        return df

    def bucket(val):
        if pd.isna(val):
            return 0
        try:
            val = float(val)
        except (ValueError, TypeError):
            return 0

        if val <= 0:
            return 0
        elif val <= 30:
            return 1  # short
        elif val <= 90:
            return 2  # standard
        else:
            return 3  # long

    df['Notice Period Bucket'] = df[col].apply(bucket)

    return df
