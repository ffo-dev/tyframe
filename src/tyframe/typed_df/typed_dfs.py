from abc import ABCMeta
from typing import Any, cast, override

import pandas as pd
import polars as pl

from tyframe.base_df_model.base_df_model import BaseDfModel
from tyframe.typed_df.base_typed_df import BaseTypedDf

type TypedPlDataframeInputData = pl.DataFrame | list[BaseDfModel]
type TypedPandasDataframeInputData = pd.DataFrame | list[BaseDfModel]


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
        return self._df.unique(keep="first")

    @override
    def _union_df(self, other: pl.DataFrame) -> pl.DataFrame:
        return pl.concat(
            [self._df, other],
            rechunk=False,
            how="vertical",
        )


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
        return self._df.unique(keep="first")

    @override
    def _union_df(self, other: pl.LazyFrame) -> pl.LazyFrame:
        return pl.concat(
            [self._df, other],
            rechunk=False,
            how="vertical",
        ).lazy()


class TypedPandasDataFrame[
    ModelType: BaseDfModel,
](BaseTypedDf[ModelType, pd.DataFrame], metaclass=ABCMeta):
    _df: pd.DataFrame
    model: type[ModelType]

    @override
    def _select(self, columns: list[str]) -> pd.DataFrame:
        return self._df.loc[:, columns]

    @override
    def _head_record(self) -> dict[str, Any]:  # pyright:ignore[reportExplicitAny]
        return cast(dict[str, Any], self._df.head(1).to_dict(orient="records")[0])  # pyright:ignore[reportExplicitAny]

    @override
    def _records(self) -> list[dict[str, Any]]:  # pyright:ignore[reportExplicitAny]
        return cast(list[dict[str, Any]], self._df.to_dict(orient="records"))  # pyright:ignore[reportExplicitAny]

    @override
    def _count(self) -> int:
        return len(self._df.index)

    @override
    def _distinct_df(self) -> pd.DataFrame:
        return self._df.drop_duplicates(keep="first")

    @override
    def _union_df(self, other: pd.DataFrame) -> pd.DataFrame:
        return pd.concat([self._df, other], ignore_index=True)
