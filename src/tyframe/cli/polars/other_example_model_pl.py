import polars as pl

from tyframe.dummy.other_model import OtherExampleModel
from tyframe.typed_df.typed_dfs import TypedPolarsDataFrame


class OtherExampleModelPl(TypedPolarsDataFrame[OtherExampleModel]):
    model: type[OtherExampleModel] = OtherExampleModel
    name: str = 'name'

    @property
    def name_col(self) -> pl.Series:
        return self._df[self.name]
