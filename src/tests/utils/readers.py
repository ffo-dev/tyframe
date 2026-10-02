from pathlib import Path

import pandas as pd
import polars as pl


def read_pandas(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)


def read_polars(path: Path) -> pl.DataFrame:
    return pl.read_csv(path)


def read_lazy_polars(path: Path) -> pl.LazyFrame:
    return pl.scan_csv(path)
