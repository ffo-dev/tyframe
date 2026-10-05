from typing import override

from tyframe.base_df_model.base_df_model import BaseDfModel
from tyframe.code_gen.based_typed_df_generator import (
    BasedTypedDfGenerator,
    TypedDfGeneratorConfig,
)


class PolarsTypedDfGeneratorConfig(BasedTypedDfGenerator):
    """
    Configuration for the PolarsTypedDfGenerator.
    """

    @override
    def _df_library_import(self):
        return "import polars as pl"

    @override
    def _typed_df_base_class_import(self):
        return "from tyframe.typed_df.typed_dfs import TypedPolarsDataFrame"

    @override
    def _typed_df_name(self):
        return "TypedPolarsDataFrame"

    @override
    def _col_return_type(self):
        return "pl.Series"


class ExampleModel(BaseDfModel):
    name: int
    last_name: str
    result: float


if __name__ == "__main__":
    generator = PolarsTypedDfGeneratorConfig(TypedDfGeneratorConfig())
    generated_code = generator.generate_typed_df_class(ExampleModel)
    print(generated_code)
