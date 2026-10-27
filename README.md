# datatidy

Quick, dependable cleaning for messy CSV and Excel data, in one line of Python or one command.

## Why

Real-world spreadsheets are full of inconsistent column names, stray spaces, duplicate rows,
mixed date formats, and currency strings like `$1,200.50` or `(45.10)`. `datatidy` fixes these
so you can get to the analysis.

## Install

```bash
pip install git+https://github.com/kelv-commits/datatidy.git
```

## Use in Python

```python
import pandas as pd
from datatidy import clean

df = pd.read_csv("sales.csv")
tidy = clean(df, date_columns=["order_date"], currency_columns=["amount"])
```

Before:

| ` Customer Name ` | Order Date | Amount |
|---|---|---|
| `  Ada   Obi ` | 2026-01-05 | $1,200.50 |
| `Ada Obi` | 2026-01-05 | $1,200.50 |

After:

| customer_name | order_date | amount |
|---|---|---|
| Ada Obi | 2026-01-05 | 1200.5 |

## Use from the command line

```bash
datatidy sales.csv -o cleaned.csv --dates order_date --currency amount
```

## What it does

- `clean_columns`: lowercase snake_case column names (handles duplicates)
- `strip_whitespace`: trims and collapses spaces in text cells
- `drop_duplicate_rows`: removes exact duplicates
- `parse_dates`: mixed date formats to real datetimes (bad values become `NaT`)
- `clean_currency`: `$1,200.50`, `₦ 3,000`, `(45.10)`, `1.234,56` to floats
- `clean`: runs everything in order

Column names are normalized first, so pass date/currency columns by their cleaned names.

## Development

```bash
pip install -e ".[dev]"
pytest
```

## Roadmap

- Missing-value strategies
- Phone number and email normalization
- Excel report export

## License

MIT
