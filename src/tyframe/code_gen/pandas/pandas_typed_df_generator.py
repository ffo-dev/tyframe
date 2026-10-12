from typing import override

from tyframe.code_gen.based_typed_df_generator import (
    BasedTypedDfGenerator,
    TypedDfGeneratorConfig,
)
from tyframe.typed_df.pandas import TypedPandasDataFrame


class PandasTypedDfGenerator(BasedTypedDfGenerator):
    """Configuration for the PandasTypedDfGenerator.
    """

    def __init__(
        self,
        config: TypedDfGeneratorConfig,
        generated_class_suffix: str = 'Pd',
    ) -> None:
        super().__init__(config, generated_class_suffix)

    @override
    def _df_library_import(self) -> str:
        return 'import pandas as pd'

    @override
    def _typed_df_base_class_import(self) -> str:
        return f'from {TypedPandasDataFrame.__module__} import {TypedPandasDataFrame.__name__}'

    @override
    def _typed_df_name(self) -> str:
        return TypedPandasDataFrame.__name__

    @override
    def _col_return_type(self) -> str:
        return 'pd.Series'
