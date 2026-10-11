from typing import override

from tyframe.code_gen.based_typed_df_generator import (
    BasedTypedDfGenerator,
    TypedDfGeneratorConfig,
)
from tyframe.typed_df.typed_dfs import TypedLazyPolarsDataFrame, TypedPolarsDataFrame


class PolarsTypedDfGenerator(BasedTypedDfGenerator):
    """
    Configuration for the PolarsTypedDfGenerator.
    """

    def __init__(
        self,
        config: TypedDfGeneratorConfig,
        generated_class_suffix: str = 'Pl',
    ):
        super().__init__(config, generated_class_suffix)

    @override
    def _df_library_import(self):
        return 'import polars as pl'

    @override
    def _typed_df_base_class_import(self):
        return f'from {TypedPolarsDataFrame.__module__} import {TypedPolarsDataFrame.__name__}'

    @override
    def _typed_df_name(self):
        return TypedPolarsDataFrame.__name__

    @override
    def _col_return_type(self):
        return 'pl.Series'


class LazyPolarsTypedDfGenerator(BasedTypedDfGenerator):
    """
    Configuration for the PolarsTypedDfGenerator.
    """

    def __init__(
        self,
        config: TypedDfGeneratorConfig,
        generated_class_suffix: str = 'Lpl',
    ):
        super().__init__(config, generated_class_suffix)

    @override
    def _df_library_import(self):
        return 'import polars as pl'

    @override
    def _typed_df_base_class_import(self):
        return f'from {TypedLazyPolarsDataFrame.__module__} import {TypedLazyPolarsDataFrame.__name__}'

    @override
    def _typed_df_name(self):
        return TypedLazyPolarsDataFrame.__name__

    @override
    def _col_return_type(self):
        return 'pl.Series'

    @override
    def _get_df_column(self, col_name: str) -> str:
        return f'return self._df.select(self.{col_name}).collect().to_series()'
