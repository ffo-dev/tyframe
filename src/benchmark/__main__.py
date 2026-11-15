"""Benchmark CLI for tyframe dataframe validation.

Builds raw pandas and polars dataframes that match a model's schema (so they
pass the validator) and times validation, reported as mean and stddev in
milliseconds.

Run from the repo root:

    poe benchmark
    uv run python -m benchmark --repeat 5
"""

import statistics
import time
from collections.abc import Callable
from functools import partial
from typing import Annotated

import pandas as pd
import polars as pl
import typer

from benchmark.generated.pandas import C1Pd, C10Pd, C100Pd
from benchmark.generated.polars import C1Pl, C10Pl, C100Pl
from tyframe.base_df_model.base_df_model import BaseDfModel
from tyframe.validation.config import TyframeValidationConfig
from tyframe.validation.pandas import PandasValidator
from tyframe.validation.polars import PolarsValidator

app = typer.Typer(help='Benchmark tyframe validation of raw pandas and polars dataframes.')

PANDAS_WRAPPERS = {1: C1Pd, 10: C10Pd, 100: C100Pd}
POLARS_WRAPPERS = {1: C1Pl, 10: C10Pl, 100: C100Pl}
DEFAULT_ROWS = [100, 10_000, 1_000_000]


def build_raw_polars_df(
    model: type[BaseDfModel],
    n_rows: int,
) -> pl.DataFrame:
    """Build a raw polars dataframe with the model's columns and a valid dtype."""
    return pl.select(pl.int_range(0, n_rows, dtype=pl.Int32).alias(col) for col in model.columns)


def build_raw_pandas_df(
    model: type[BaseDfModel],
    n_rows: int,
) -> pd.DataFrame:
    """Build a raw pandas dataframe with the model's columns and a valid dtype."""
    return pd.DataFrame({col: range(n_rows) for col in model.columns})


def measure_validation(
    validate: Callable[[], object],
    repeat: int,
) -> list[float]:
    """Return the validation times in seconds for ``repeat`` runs."""
    times: list[float] = []
    for _ in range(repeat):
        start = time.perf_counter()
        validate()
        times.append(time.perf_counter() - start)
    return times


def report_validation(
    library: str,
    n_cols: int,
    n_rows: int,
    times: list[float],
) -> None:
    mean_ms = statistics.fmean(times) * 1000
    std_ms = statistics.pstdev(times) * 1000
    typer.echo(f'{library:>7} | {n_cols:>6} | {n_rows:>9} | {mean_ms:>10.3f} | {std_ms:>10.3f}')


class BenchmarkResult:
    library: str
    n_col: int
    n_row: int
    mean_ms: float
    std_ms: float
    validation_config: TyframeValidationConfig


@app.command()
def main(
    repeat: Annotated[
        int,
        typer.Option(help='Runs per case; mean and stddev in ms are reported.'),
    ] = 1000,
) -> None:
    pandas_validator = PandasValidator(config=TyframeValidationConfig(validate_dtypes=True))
    polars_validator = PolarsValidator(config=TyframeValidationConfig(validate_dtypes=True))

    typer.echo(f'{"library":>7} | {"cols":>6} | {"rows":>9} | {"mean (ms)":>10} | {"std (ms)":>10}')
    for n_cols, wrapper_cls in PANDAS_WRAPPERS.items():
        for n_rows in DEFAULT_ROWS:
            df = build_raw_pandas_df(wrapper_cls.model, n_rows)
            times = measure_validation(partial(wrapper_cls, df, pandas_validator), repeat)
            report_validation('pandas', n_cols, n_rows, times)

    for n_cols, wrapper_cls in POLARS_WRAPPERS.items():
        for n_rows in DEFAULT_ROWS:
            df = build_raw_polars_df(wrapper_cls.model, n_rows)
            times = measure_validation(partial(wrapper_cls, df, polars_validator), repeat)
            report_validation('polars', n_cols, n_rows, times)


if __name__ == '__main__':
    app()
