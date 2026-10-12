from abc import ABCMeta
from collections.abc import Iterable
from typing import Any, Self, override

import polars as pl
from polars._typing import IntoExpr, IntoExprColumn

from tyframe.base_df_model.base_df_model import BaseDfModel
from tyframe.typed_df.base_typed_df import BaseTypedDf
from tyframe.typed_df.polars.common import flip_bool

type TypedPlDataframeInputData = pl.LazyFrame | list[BaseDfModel]


class TypedLazyPolarsDataFrame[
    ModelType: BaseDfModel,
](BaseTypedDf[ModelType, pl.LazyFrame], metaclass=ABCMeta):
    _df: pl.LazyFrame
    model: type[ModelType]

    @override
    def _select(self, columns: list[str]) -> pl.LazyFrame:
        return self._df.select(columns)

    @override
    def _head_record(self) -> dict[str, Any]:  # pyright:ignore[reportExplicitAny]
        return self._df.head(n=1).collect().to_dicts()[0]

    @override
    def _records(self) -> list[dict[str, Any]]:  # pyright:ignore[reportExplicitAny]
        return self._df.collect().to_dicts()

    @override
    def _count(self) -> int:
        return self._df.collect().height

    @override
    def _distinct_df(self) -> pl.LazyFrame:
        return self._df.unique(keep='first')

    @override
    def _union_df(self, other: pl.LazyFrame) -> pl.LazyFrame:
        return pl.concat(
            [self._df, other],
            rechunk=False,
            how='vertical',
        ).lazy()

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
        ascending: bool | list[bool] = False,
    ) -> Self:
        return self._pass_through(self._df.sort(by, descending=flip_bool(ascending)))
