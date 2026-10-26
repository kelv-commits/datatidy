"""Core cleaning functions. Every function returns a new DataFrame."""

from __future__ import annotations

import re
from typing import Iterable

import pandas as pd

_CURRENCY_CHARS = re.compile(r"[^\d,.\-()]")


def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Make column names lowercase snake_case, e.g. ' Order Date ' -> 'order_date'."""
    out = df.copy()
    names = []
    seen: dict[str, int] = {}
    for col in out.columns:
        name = re.sub(r"[^0-9a-zA-Z]+", "_", str(col).strip()).strip("_").lower()
        name = name or "column"
        if name in seen:
            seen[name] += 1
            name = f"{name}_{seen[name]}"
        else:
            seen[name] = 0
        names.append(name)
    out.columns = names
    return out


def strip_whitespace(df: pd.DataFrame) -> pd.DataFrame:
    """Trim leading/trailing spaces and collapse repeated spaces in text cells."""
    out = df.copy()
    for col in out.columns:
        if pd.api.types.is_object_dtype(out[col]) or pd.api.types.is_string_dtype(out[col]):
            out[col] = out[col].map(
                lambda v: re.sub(r"\s+", " ", v).strip() if isinstance(v, str) else v
            )
    return out


def drop_duplicate_rows(df: pd.DataFrame, subset: Iterable[str] | None = None) -> pd.DataFrame:
    """Drop exact duplicate rows (or duplicates on `subset`), keeping the first."""
    cols = list(subset) if subset is not None else None
    return df.drop_duplicates(subset=cols, keep="first").reset_index(drop=True)


def parse_dates(df: pd.DataFrame, columns: Iterable[str]) -> pd.DataFrame:
    """Convert the given columns to datetimes. Unparseable values become NaT."""
    out = df.copy()
    for col in columns:
        out[col] = pd.to_datetime(out[col], errors="coerce", dayfirst=False, format="mixed")
    return out


def _to_number(value):
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return float("nan")
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip()
    if not text:
        return float("nan")
    negative = text.startswith("(") and text.endswith(")") or text.startswith("-")
    text = _CURRENCY_CHARS.sub("", text).replace("(", "").replace(")", "").replace("-", "")
    # Handle European style 1.234,56 vs US style 1,234.56
    if "," in text and "." in text:
        if text.rfind(",") > text.rfind("."):
            text = text.replace(".", "").replace(",", ".")
        else:
            text = text.replace(",", "")
    elif "," in text:
        head, _, tail = text.rpartition(",")
        text = head.replace(",", "") + "." + tail if len(tail) <= 2 else text.replace(",", "")
    try:
        number = float(text)
    except ValueError:
        return float("nan")
    return -number if negative else number


def clean_currency(df: pd.DataFrame, columns: Iterable[str]) -> pd.DataFrame:
    """Turn values like '$1,200.50', '₦ 3,000', '(45.10)' into floats."""
    out = df.copy()
    for col in columns:
        out[col] = out[col].map(_to_number).astype("float64")
    return out


def clean(
    df: pd.DataFrame,
    date_columns: Iterable[str] | None = None,
    currency_columns: Iterable[str] | None = None,
    drop_duplicates: bool = True,
) -> pd.DataFrame:
    """Run the full pipeline.

    Column names are normalized first, so pass date/currency columns using
    their cleaned (snake_case) names.
    """
    out = clean_columns(df)
    out = strip_whitespace(out)
    if date_columns:
        out = parse_dates(out, date_columns)
    if currency_columns:
        out = clean_currency(out, currency_columns)
    if drop_duplicates:
        out = drop_duplicate_rows(out)
    return out
