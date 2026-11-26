"""Tests for BasedTypedDfGenerator.generate_columns_with_tag_method and its imports."""

from typing import Any, Literal

import pytest

from tests.test_classes.models import CustomTagModel, OneColModel, TaggedModel
from tyframe.base_df_model.base_df_model import BaseDfModel
from tyframe.code_gen.based_typed_df_generator import TypedDfGeneratorConfig
from tyframe.code_gen.pandas import PandasTypedDfGenerator
from tyframe.tagging import TyframeTag


@pytest.mark.parametrize(
    'model',
    [
        TaggedModel,
        OneColModel,
    ],
)
def test_generate_columns_with_tag_method_defaults_to_tyframe_tag(
    model: type[BaseDfModel[Any]],
) -> None:
    """Plain BaseDfModel subclasses get TyframeTag as the tag parameter type."""
    generator = PandasTypedDfGenerator(config=TypedDfGeneratorConfig())

    assert generator.generate_columns_with_tag_method(model) == [
        '    @classmethod',
        '    def columns_with_tag(cls, tag: TyframeTag) -> list[str]:',
        '        return cls.model.columns_with_tag(tag)',
    ]


def test_generate_columns_with_tag_method_full_output() -> None:
    """A custom-tagged model gets its own tag alias; the whole output matches exactly."""
    generator = PandasTypedDfGenerator(config=TypedDfGeneratorConfig())

    assert generator.generate_columns_with_tag_method(CustomTagModel) == [
        '    @classmethod',
        '    def columns_with_tag(cls, tag: MyTag) -> list[str]:',
        '        return cls.model.columns_with_tag(tag)',
    ]


def test_generate_columns_with_tag_method_respects_indentation_config() -> None:
    """The generated method uses the indentation size from the config."""
    generator = PandasTypedDfGenerator(config=TypedDfGeneratorConfig(indentation_size=2))

    assert generator.generate_columns_with_tag_method(TaggedModel) == [
        '  @classmethod',
        '  def columns_with_tag(cls, tag: TyframeTag) -> list[str]:',
        '    return cls.model.columns_with_tag(tag)',
    ]


def test_generate_imports_default_model_uses_tyframe_tag() -> None:
    """Plain BaseDfModel subclasses import TyframeTag, and not Literal."""
    generator = PandasTypedDfGenerator(config=TypedDfGeneratorConfig())

    imports = generator.generate_imports(TaggedModel)

    assert 'from tyframe.tagging import TyframeTag' in imports
    assert 'from typing import Literal' not in imports


def test_generate_imports_custom_tag_model_imports_tag_alias() -> None:
    """A custom-tagged model imports its tag alias alongside the model."""
    generator = PandasTypedDfGenerator(config=TypedDfGeneratorConfig())

    imports = generator.generate_imports(CustomTagModel)

    assert 'from tests.test_classes.models import CustomTagModel, MyTag' in imports
    assert 'from tyframe.tagging import TyframeTag' not in imports
    assert 'from typing import Literal' not in imports


def test_resolve_tag_type_explicit_tyframe_tag() -> None:
    """A model parameterized with TyframeTag resolves to the tyframe.tagging alias."""

    class ExplicitModel(BaseDfModel[TyframeTag]):
        a: int

    generator = PandasTypedDfGenerator(config=TypedDfGeneratorConfig())

    assert generator.resolve_tag_type(ExplicitModel) == ('TyframeTag', [('tyframe.tagging', 'TyframeTag')])


def test_resolve_tag_type_inline_literal_falls_back_to_literal() -> None:
    """An unnamed inline tag type is flattened into a Literal of its values."""

    class InlineModel(BaseDfModel[Literal['x'] | Literal['y']]):  # noqa: PYI030
        a: int

    generator = PandasTypedDfGenerator(config=TypedDfGeneratorConfig())

    assert generator.resolve_tag_type(InlineModel) == ("Literal['x', 'y']", [('typing', 'Literal')])


def test_resolve_tag_type_non_literal_falls_back_to_str() -> None:
    """A non-literal tag type (e.g. plain str) falls back to str."""

    class StrModel(BaseDfModel[str]):
        a: int

    generator = PandasTypedDfGenerator(config=TypedDfGeneratorConfig())

    assert generator.resolve_tag_type(StrModel) == ('str', [])
