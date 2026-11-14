"""Benchmark CLI for tyframe dataframe validation.

Builds a raw polars dataframe that matches a model's schema (so it passes the
validator) and times how long validation takes, reported as mean and stddev
in milliseconds.

Run from the repo root:

    poe benchmark
    uv run python -m benchmark --rows 100 --rows 1000000 --cols 100 --repeat 5
"""

import statistics
import time
from typing import Annotated

import polars as pl
import typer

from benchmark.generated import C1Pl, C10Pl, C100Pl
from tyframe.base_df_model.base_df_model import BaseDfModel
from tyframe.validation.config import TyframeValidationConfig
from tyframe.validation.polars import PolarsValidator

app = typer.Typer(help='Benchmark tyframe validation of raw polars dataframes.')

WRAPPERS = {1: C1Pl, 10: C10Pl, 100: C100Pl}
DEFAULT_ROWS = [100, 10_000, 1_000_000]


def build_raw_df(
    model: type[BaseDfModel],
    n_rows: int,
) -> pl.DataFrame:
    """Build a raw polars dataframe with the model's columns and a valid dtype."""
    return pl.select(pl.int_range(0, n_rows, dtype=pl.Int32).alias(col) for col in model.columns)


def measure_validation(
    model: type[BaseDfModel],
    n_rows: int,
    validator: PolarsValidator,
    repeat: int,
) -> list[float]:
    """Return the validation times in seconds for ``repeat`` runs."""
    df = build_raw_df(model, n_rows)
    times: list[float] = []
    for _ in range(repeat):
        start = time.perf_counter()
        validator.validate(model, df)
        times.append(time.perf_counter() - start)
    return times


@app.command()
def main(
    rows: Annotated[list[int] | None, typer.Option(help='Row counts to benchmark.')] = None,
    cols: Annotated[list[int] | None, typer.Option(help='Column counts to benchmark (subset of 1, 10, 100).')] = None,
    repeat: Annotated[int, typer.Option(help='Runs per case; mean and stddev in ms are reported.')] = 1000,
) -> None:
    row_counts = rows or DEFAULT_ROWS
    cases = {n_cols: wrapper_cls for n_cols, wrapper_cls in WRAPPERS.items() if cols is None or n_cols in cols}
    validator = PolarsValidator(config=TyframeValidationConfig(validate_dtypes=True))

    typer.echo(f'{"cols":>6} | {"rows":>9} | {"mean (ms)":>10} | {"std (ms)":>10}')
    for n_cols, wrapper_cls in cases.items():
        for n_rows in row_counts:
            times = measure_validation(wrapper_cls.model, n_rows, validator, repeat)
            mean_ms = statistics.fmean(times) * 1000
            std_ms = statistics.pstdev(times) * 1000
            typer.echo(f'{n_cols:>6} | {n_rows:>9} | {mean_ms:>10.3f} | {std_ms:>10.3f}')


if __name__ == '__main__':
    app()
