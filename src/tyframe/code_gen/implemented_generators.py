from collections.abc import Mapping

from tyframe.code_gen.based_typed_df_generator import BasedTypedDfGenerator
from tyframe.code_gen.pandas import PandasTypedDfGenerator
from tyframe.code_gen.polars import LazyPolarsTypedDfGenerator, PolarsTypedDfGenerator
from tyframe.constants import IMPLEMENTED_DF_TYPES

IMPLEMENTED_GENERATORS: Mapping[IMPLEMENTED_DF_TYPES, type[BasedTypedDfGenerator]] = {
    'polars': PolarsTypedDfGenerator,
    'lazy_polars': LazyPolarsTypedDfGenerator,
    'pandas': PandasTypedDfGenerator,
}
