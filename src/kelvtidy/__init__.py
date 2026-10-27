"""kelvtidy: quick, dependable cleaning for messy CSV/Excel data."""

from .cleaners import (
    clean,
    clean_columns,
    clean_currency,
    drop_duplicate_rows,
    parse_dates,
    strip_whitespace,
)

__version__ = "0.1.0"

__all__ = [
    "clean",
    "clean_columns",
    "clean_currency",
    "drop_duplicate_rows",
    "parse_dates",
    "strip_whitespace",
]
