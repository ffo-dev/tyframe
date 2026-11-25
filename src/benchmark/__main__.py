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
from dataclasses import dataclass
from functools import partial
from pathlib import Path
from typing import Annotated

import pandas as pd
import polars as pl
import typer

from benchmark.generated.pandas import C1Pd, C10Pd, C100Pd
from benchmark.generated.polars import C1Pl, C10Pl, C100Pl
from tyframe.base_df_model.base_df_model import BaseDfModel
from tyframe.validation.config import TyframeColumnValidation
from tyframe.validation.pandas import PandasValidator
from tyframe.validation.polars import PolarsValidator

app = typer.Typer(help='Benchmark tyframe validation of raw pandas and polars dataframes.')

PANDAS_WRAPPERS = {1: C1Pd, 10: C10Pd, 100: C100Pd}
POLARS_WRAPPERS = {1: C1Pl, 10: C10Pl, 100: C100Pl}
DEFAULT_ROWS = [100, 10_000, 1_000_000]
EXTRA_COLUMNS = 10
DROP_COLUMNS = 5

type PandasDataFrameBuilder = Callable[[type[BaseDfModel]], pd.DataFrame]
type PolarsDataFrameBuilder = Callable[[type[BaseDfModel]], pl.DataFrame]
type PandasWrapperClass = type[C1Pd | C10Pd | C100Pd]
type PolarsWrapperClass = type[C1Pl | C10Pl | C100Pl]


def build_raw_polars_df(
    model: type[BaseDfModel],
    n_rows: int,
    add_extra_columns: int = 0,
    drop_columns: int = 0,
) -> pl.DataFrame:
    """Build a raw polars dataframe with valid model columns and extra columns."""
    remaining_model_columns = model.columns[: max(1, len(model.columns) - drop_columns)]
    df = pl.select(pl.int_range(0, n_rows, dtype=pl.Int32).alias(col) for col in remaining_model_columns)
    return df.with_columns(
        pl.int_range(0, n_rows, dtype=pl.Int32).alias(f'extra_{index + 1}') for index in range(add_extra_columns)
    )


def build_raw_pandas_df(
    model: type[BaseDfModel],
    n_rows: int,
    add_extra_columns: int = 0,
    drop_columns: int = 0,
) -> pd.DataFrame:
    """Build a raw pandas dataframe with valid model columns and extra columns."""
    remaining_model_columns = model.columns[: max(1, len(model.columns) - drop_columns)]
    columns = {col: range(n_rows) for col in remaining_model_columns}
    columns.update({f'extra_{index + 1}': range(n_rows) for index in range(add_extra_columns)})
    return pd.DataFrame(columns)


@dataclass(frozen=True, slots=True)
class BenchmarkResult:
    library: str
    n_col: int
    n_row: int
    mean_ms: float
    std_ms: float
    validation_config: TyframeColumnValidation


def show(results: list[BenchmarkResult], save: Path | None = None) -> None:
    """Print benchmark results and optionally save them to a file."""
    lines = [
        f'{"library":>7} | {"cols":>6} | {"rows":>9} | {"mean (ms)":>10} | {"std (ms)":>10} | config',
        *(
            f'{result.library:>7} | {result.n_col:>6} | {result.n_row:>9} | '
            f'{result.mean_ms:>10.3f} | {result.std_ms:>10.3f} | {result.validation_config}'
            for result in results
        ),
    ]
    output = '\n'.join(lines)
    typer.echo(output)
    if save is not None:
        save.write_text(f'{output}\n', encoding='utf-8')


def benchmark_pandas(
    config: TyframeColumnValidation,
    build_dataframe_method: PandasDataFrameBuilder,
    wrapper_cls: PandasWrapperClass,
    repeat: int,
) -> BenchmarkResult:
    """Benchmark validation of a pandas dataframe."""
    if repeat < 1:
        raise ValueError(repeat)

    df = build_dataframe_method(wrapper_cls.model)
    validator = PandasValidator(config=config)
    times: list[float] = []
    for _ in range(repeat):
        start = time.perf_counter()
        wrapper_cls(df, validator)
        times.append(time.perf_counter() - start)

    return BenchmarkResult(
        library='pandas',
        n_col=len(df.columns),
        n_row=len(df),
        mean_ms=statistics.fmean(times) * 1000,
        std_ms=statistics.pstdev(times) * 1000,
        validation_config=config,
    )


def benchmark_polars(
    config: TyframeColumnValidation,
    build_dataframe_method: PolarsDataFrameBuilder,
    wrapper_cls: PolarsWrapperClass,
    repeat: int,
) -> BenchmarkResult:
    """Benchmark validation of a polars dataframe."""
    if repeat < 1:
        raise ValueError(repeat)

    df = build_dataframe_method(wrapper_cls.model)
    validator = PolarsValidator(config=config)
    times: list[float] = []
    for _ in range(repeat):
        start = time.perf_counter()
        wrapper_cls(df, validator)
        times.append(time.perf_counter() - start)

    return BenchmarkResult(
        library='polars',
        n_col=len(df.columns),
        n_row=len(df),
        mean_ms=statistics.fmean(times) * 1000,
        std_ms=statistics.pstdev(times) * 1000,
        validation_config=config,
    )


@app.command()
def main(
    repeat: Annotated[
        int,
        typer.Option(help='Runs per case; mean and stddev in ms are reported.'),
    ] = 1000,
    save: Annotated[
        Path | None,
        typer.Option(help='Optional file path to save benchmark results.'),
    ] = None,
) -> None:
    results: list[BenchmarkResult] = []
    scenarios = (
        (TyframeColumnValidation(validate_dtypes=True), 0, 0),
        (TyframeColumnValidation(validate_dtypes=False), 0, 0),
        (TyframeColumnValidation(validate_dtypes=False, drop_extra_columns=True), EXTRA_COLUMNS, 0),
        (TyframeColumnValidation(validate_dtypes=False, fill_with_default=True), 0, DROP_COLUMNS),
        (
            TyframeColumnValidation(
                validate_dtypes=False,
                fill_with_default=True,
                drop_extra_columns=True,
            ),
            EXTRA_COLUMNS,
            DROP_COLUMNS,
        ),
    )
    for config, extra_columns, drop_columns in scenarios:
        results.extend(
            benchmark_pandas(
                config,
                partial(
                    build_raw_pandas_df,
                    n_rows=n_rows,
                    add_extra_columns=extra_columns,
                    drop_columns=drop_columns,
                ),
                wrapper_cls,
                repeat,
            )
            for wrapper_cls in PANDAS_WRAPPERS.values()
            for n_rows in DEFAULT_ROWS
        )
        results.extend(
            benchmark_polars(
                config,
                partial(
                    build_raw_polars_df,
                    n_rows=n_rows,
                    add_extra_columns=extra_columns,
                    drop_columns=drop_columns,
                ),
                wrapper_cls,
                repeat,
            )
            for wrapper_cls in POLARS_WRAPPERS.values()
            for n_rows in DEFAULT_ROWS
        )
    show(results, save)


if __name__ == '__main__':
    app()
