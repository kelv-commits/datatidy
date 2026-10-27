"""Command line interface: kelvtidy input.csv -o cleaned.csv"""

from __future__ import annotations

import argparse
import sys

import pandas as pd

from .cleaners import clean


def _read(path: str) -> pd.DataFrame:
    if path.lower().endswith((".xlsx", ".xls")):
        return pd.read_excel(path)
    return pd.read_csv(path)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="kelvtidy", description="Clean messy CSV/Excel files.")
    parser.add_argument("input", help="Path to a .csv, .xlsx or .xls file")
    parser.add_argument("-o", "--output", default="cleaned.csv", help="Output CSV path")
    parser.add_argument("--dates", nargs="*", default=[], help="Date columns (cleaned names)")
    parser.add_argument("--currency", nargs="*", default=[], help="Currency columns (cleaned names)")
    parser.add_argument("--keep-duplicates", action="store_true", help="Do not drop duplicate rows")
    args = parser.parse_args(argv)

    try:
        df = _read(args.input)
    except Exception as exc:  # noqa: BLE001
        print(f"Could not read {args.input}: {exc}", file=sys.stderr)
        return 1

    before = len(df)
    result = clean(
        df,
        date_columns=args.dates,
        currency_columns=args.currency,
        drop_duplicates=not args.keep_duplicates,
    )
    result.to_csv(args.output, index=False)
    print(f"Cleaned {before} rows -> {len(result)} rows. Saved to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
