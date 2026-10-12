from abc import ABCMeta
from collections.abc import Iterable
from typing import Any, Self, override

import polars as pl
from polars._typing import IntoExpr, IntoExprColumn

from tyframe.base_df_model.base_df_model import BaseDfModel
from tyframe.typed_df.base_typed_df import BaseTypedDf
from tyframe.typed_df.polars.common import flip_bool

type TypedPlDataframeInputData = pl.DataFrame | list[BaseDfModel]


class TypedPolarsDataFrame[
    ModelType: BaseDfModel,
](BaseTypedDf[ModelType, pl.DataFrame], metaclass=ABCMeta):
    _df: pl.DataFrame
    model: type[ModelType]

    @override
    def _select(self, columns: list[str]) -> pl.DataFrame:
        return self._df.select(columns)

    @override
    def _head_record(self) -> dict[str, Any]:  # pyright:ignore[reportExplicitAny]
        return self._df.head(n=1).to_dicts()[0]

    @override
    def _records(self) -> list[dict[str, Any]]:  # pyright:ignore[reportExplicitAny]
        return self._df.to_dicts()

    @override
    def _count(self) -> int:
        return self._df.height

    @override
    def _distinct_df(self) -> pl.DataFrame:
        return self._df.unique(keep='first')

    @override
    def _union_df(self, other: pl.DataFrame) -> pl.DataFrame:
        return pl.concat(
            [self._df, other],
            rechunk=False,
            how='vertical',
        )

    @override
    def filter(
        self,
        predicate_col: IntoExprColumn | Iterable[IntoExprColumn],
    ) -> Self:
        return self._pass_through(self._df.filter(predicate_col))

    def sort(
        self,
        by: IntoExpr | Iterable[IntoExpr],
        *,
        ascending: bool | list[bool] = True,
    ) -> Self:
        descending = flip_bool(ascending)
        return self._pass_through(
            self._df.sort(
                by,
                descending=descending,
            )
        )
