"""PK-check benchmark: times primary-key uniqueness validation across row counts.

Compares `TyframeRowValidation(validate_pk_uniqueness=True)` against `False` so the
cost of the duplicate check is visible; it is expected to scale with the number of rows.
"""

from functools import partial

from benchmark.common import (
    DEFAULT_ROWS,
    BenchmarkResult,
    PandasDataFrameBuilder,
    PolarsDataFrameBuilder,
    build_raw_pandas_df,
    build_raw_polars_df,
    time_repeats,
)
from benchmark.generated.pandas import PkCheckPd
from benchmark.generated.polars import PkCheckPl
from tyframe.validation.config import TyframeRowValidation
from tyframe.validation.pandas import PandasValidator
from tyframe.validation.polars import PolarsValidator

ROW_CONFIGS = (
    TyframeRowValidation(validate_pk_uniqueness=True),
    TyframeRowValidation(validate_pk_uniqueness=False),
)


def benchmark_pandas(
    config: TyframeRowValidation,
    build_dataframe_method: PandasDataFrameBuilder,
    repeat: int,
) -> BenchmarkResult:
    """Benchmark pk validation of a pandas dataframe."""
    df = build_dataframe_method(PkCheckPd.model)
    validator = PandasValidator(row_config=config)
    mean_ms, std_ms = time_repeats(lambda: PkCheckPd(df, validator), repeat)

    return BenchmarkResult(
        library='pandas',
        n_col=len(df.columns),
        n_row=len(df),
        mean_ms=mean_ms,
        std_ms=std_ms,
        config=config,
    )


def benchmark_polars(
    config: TyframeRowValidation,
    build_dataframe_method: PolarsDataFrameBuilder,
    repeat: int,
) -> BenchmarkResult:
    """Benchmark pk validation of a polars dataframe."""
    df = build_dataframe_method(PkCheckPl.model)
    validator = PolarsValidator(row_config=config)
    mean_ms, std_ms = time_repeats(lambda: PkCheckPl(df, validator), repeat)

    return BenchmarkResult(
        library='polars',
        n_col=len(df.columns),
        n_row=len(df),
        mean_ms=mean_ms,
        std_ms=std_ms,
        config=config,
    )


def run_pk_check_benchmark(repeat: int) -> list[BenchmarkResult]:
    """Run the pk-check benchmark over both row configs, both libraries and all row counts."""
    results: list[BenchmarkResult] = []
    for config in ROW_CONFIGS:
        results.extend(
            benchmark_pandas(
                config,
                partial(build_raw_pandas_df, n_rows=n_rows),
                repeat,
            )
            for n_rows in DEFAULT_ROWS
        )
        results.extend(
            benchmark_polars(
                config,
                partial(build_raw_polars_df, n_rows=n_rows),
                repeat,
            )
            for n_rows in DEFAULT_ROWS
        )
    return results
