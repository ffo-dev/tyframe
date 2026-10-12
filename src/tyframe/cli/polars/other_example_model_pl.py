import polars as pl
from tyframe.typed_df.typed_dfs import TypedPolarsDataFrame

from tyframe.dummy.other_model import OtherExampleModel


class OtherExampleModelPl(TypedPolarsDataFrame[OtherExampleModel]):
    model: type[OtherExampleModel] = OtherExampleModel
    name: str = 'name'

    @property
    def name_col(self) -> pl.Series:
        return self._df[self.name]
