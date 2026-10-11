from abc import ABCMeta, abstractmethod
from collections.abc import Iterable
from typing import Any, Protocol, Self, TypeGuard, TypeVar

from tyframe.base_df_model.base_df_model import BaseDfModel
from tyframe.validation.base_validator import BaseValidator
from tyframe.validation.config import TyframeValidationConfig


class TypedDfProtocol(Protocol):
    @classmethod
    def columns(cls) -> list[str]: ...

    def __init__(
        self,
        input_data: Any,  # pyright:ignore[reportAny, reportExplicitAny]
        validator: BaseValidator[Any],  # pyright:ignore[reportExplicitAny]
        validation_config: TyframeValidationConfig | None = None,
        *,
        skip_validation: bool = False,
    ) -> None: ...


DataFrameType = TypeVar('DataFrameType')
_T = TypeVar('_T', bound=TypedDfProtocol)


class BaseTypedDf[
    ModelType: BaseDfModel,
    DataFrameType,
](metaclass=ABCMeta):
    _df: DataFrameType
    validator: BaseValidator[DataFrameType]
    model: type[ModelType]
    validated: bool

    def __init__(
        self,
        input_data: DataFrameType | Iterable[ModelType],
        validator: BaseValidator[DataFrameType],
        validation_config: TyframeValidationConfig | None = None,
        *,
        skip_validation: bool = False,
    ):
        self.validator = validator
        if skip_validation:
            if self._is_dataframe_type(input_data):
                self._df = input_data
                self.validated = False
                return
            raise ValueError(
                'skip_validation can only be used when input_data is a DataFrameType instance.'
            )
        if self._is_dataframe_type(input_data):
            self._df = self.validator.validate(
                self.model,
                input_data,
                validation_config,
            )
        elif self._is_model_iterable(input_data):
            self._df = self.validator.create_dataframe(
                input_data,
                self.model,
            )
        else:
            raise TypeError(
                f'input_data must be either a {self.model.__name__} iterable or a {self.validator.df_type.__name__} instance.'
            )
        self.validated = True

    def _is_model_iterable(
        self,
        input_data: Any,  # pyright:ignore[reportAny, reportExplicitAny]
    ) -> TypeGuard[Iterable[ModelType]]:
        return isinstance(input_data, Iterable) and all(
            isinstance(el, self.model) for el in input_data
        )

    def _is_dataframe_type(
        self,
        input_data: Any,  # pyright:ignore[reportAny, reportExplicitAny]
    ) -> TypeGuard[DataFrameType]:
        return isinstance(input_data, self.validator.df_type)

    @property
    def df(self) -> DataFrameType:
        return self._df  # pragma: no cover

    @classmethod
    def columns(cls) -> list[str]:
        return list(cls.model.columns)

    def select(
        self,
        columns: list[str],
    ) -> DataFrameType:
        return self._select(columns)

    def select_to(
        self,
        to_type: type[_T],
    ) -> _T:
        return to_type(
            self.select(to_type.columns()),
            self.validator,
            skip_validation=True,
        )

    @abstractmethod
    def filter(self, *args: Any, **kwargs: Any) -> Self:  # pyright:ignore[reportExplicitAny]
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def _select(self, columns: list[str]) -> DataFrameType:
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def _head_record(self) -> dict[str, Any]:  # pyright:ignore[reportExplicitAny]
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def _records(self) -> Iterable[dict[str, Any]]:  # pyright:ignore[reportExplicitAny]
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def _count(self) -> int:
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def _distinct_df(self) -> DataFrameType:
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def _union_df(self, other: DataFrameType) -> DataFrameType:
        raise NotImplementedError  # pragma: no cover

    def first(self) -> ModelType:
        return self.model(**self._head_record())

    def collect(self) -> list[ModelType]:
        return [self.model(**row) for row in self._records()]

    def count(self) -> int:
        return self._count()

    ## SafeOps, which return a new instance of the same type,
    # with the same validator, and skip validation since the schema is guaranteed to be the same.

    def _pass_through(self, df: DataFrameType) -> Self:
        return type(self)(
            df,
            self.validator,
            skip_validation=True,
        )

    def distinct(self) -> Self:
        return self._pass_through(self._distinct_df())

    def union(self, other: Self) -> Self:
        return self._pass_through(self._union_df(other._df))
