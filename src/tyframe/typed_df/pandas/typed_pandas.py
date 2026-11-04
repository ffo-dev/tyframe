from abc import ABCMeta
from collections.abc import Sequence
from typing import Any, Self, cast, override

import pandas as pd

from tyframe.base_df_model.base_df_model import BaseDfModel
from tyframe.typed_df.base_typed_df import BaseTypedDf

type TypedPandasDataframeInputData = pd.DataFrame | list[BaseDfModel]


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
        return cast('dict[str, Any]', self._df.head(1).to_dict(orient='records')[0])  # pyright:ignore[reportExplicitAny]

    @override
    def _records(self) -> list[dict[str, Any]]:  # pyright:ignore[reportExplicitAny]
        return cast('list[dict[str, Any]]', self._df.to_dict(orient='records'))  # pyright:ignore[reportExplicitAny]

    @override
    def _count(self) -> int:
        return len(self._df.index)

    @override
    def _distinct_df(self) -> pd.DataFrame:
        return self._df.drop_duplicates(keep='first')

    @override
    def _union_df(self, other: pd.DataFrame) -> pd.DataFrame:
        return pd.concat([self._df, other], ignore_index=True)

    @override
    def filter(
        self,
        predicate_col: pd.Series,
    ) -> Self:
        return self._pass_through(self._df[predicate_col])

    def sort(
        self,
        by: str | Sequence[str],
        *,
        ascending: bool | Sequence[bool] = True,
    ) -> Self:
        return self._pass_through(
            self._df.sort_values(
                by,
                ascending=ascending,
            ),
        )
