import polars as pl

from tyframe.dummy.other_model import OtherExampleModel
from tyframe.typed_df.polars import TypedLazyPolarsDataFrame


class OtherExampleModelLpl(TypedLazyPolarsDataFrame[OtherExampleModel]):
    model: type[OtherExampleModel] = OtherExampleModel
    name: str = 'name'

    @property
    def name_col(self) -> pl.Series:
        return self._df.select(self.name).collect().to_series()
