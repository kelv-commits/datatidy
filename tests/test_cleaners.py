import math

import pandas as pd

from kelvtidy import (
    clean,
    clean_columns,
    clean_currency,
    drop_duplicate_rows,
    parse_dates,
    strip_whitespace,
)


def test_clean_columns():
    df = pd.DataFrame(columns=[" Order Date ", "Total $", "Total $", "ID"])
    assert list(clean_columns(df).columns) == ["order_date", "total", "total_1", "id"]


def test_strip_whitespace():
    df = pd.DataFrame({"name": ["  Ada   Obi ", "Tunde"]})
    assert list(strip_whitespace(df)["name"]) == ["Ada Obi", "Tunde"]


def test_drop_duplicates():
    df = pd.DataFrame({"a": [1, 1, 2], "b": ["x", "x", "y"]})
    assert len(drop_duplicate_rows(df)) == 2


def test_parse_dates():
    df = pd.DataFrame({"d": ["2026-01-05", "not a date"]})
    out = parse_dates(df, ["d"])
    assert out["d"].iloc[0] == pd.Timestamp("2026-01-05")
    assert pd.isna(out["d"].iloc[1])


def test_clean_currency():
    df = pd.DataFrame({"p": ["$1,200.50", "₦ 3,000", "(45.10)", "1.234,56", "", None, "abc"]})
    vals = list(clean_currency(df, ["p"])["p"])
    assert vals[0] == 1200.50
    assert vals[1] == 3000.0
    assert vals[2] == -45.10
    assert vals[3] == 1234.56
    assert all(math.isnan(v) for v in vals[4:])


def test_clean_pipeline():
    df = pd.DataFrame(
        {
            " Customer Name ": ["  Ada ", "Ada", "Ada"],
            "Order Date": ["2026-01-05", "2026-01-05", "2026-01-05"],
            "Amount": ["$10.00", "$10.00", "$10.00"],
        }
    )
    out = clean(df, date_columns=["order_date"], currency_columns=["amount"])
    assert list(out.columns) == ["customer_name", "order_date", "amount"]
    assert len(out) == 1
    assert out["amount"].iloc[0] == 10.0
