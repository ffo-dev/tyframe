"""Tests for BasedTypedDfGenerator.generate_columns_with_tag_method and its imports."""

from typing import Any

import pytest

from tests.test_classes.models import CustomTagModel, OneColModel, TaggedModel
from tyframe.base_df_model.base_df_model import BaseDfModel
from tyframe.code_gen.based_typed_df_generator import TypedDfGeneratorConfig
from tyframe.code_gen.pandas import PandasTypedDfGenerator


@pytest.mark.parametrize(
    ('model', 'expected_tag_type'),
    [
        (TaggedModel, "Literal['map_key', 'unit_price', 'total_price', 'country']"),
        (OneColModel, 'TyframeTag'),
    ],
)
def test_generate_columns_with_tag_method(
    model: type[BaseDfModel[Any]],
    expected_tag_type: str,
) -> None:
    """The tag parameter is a Literal of the model's tags, or TyframeTag when tagless."""
    generator = PandasTypedDfGenerator(config=TypedDfGeneratorConfig())

    assert generator.generate_columns_with_tag_method(model) == [
        '    @classmethod',
        f'    def columns_with_tag(cls, tag: {expected_tag_type}) -> list[str]:',
        '        return cls.model.columns_with_tag(tag)',
    ]


def test_generate_columns_with_tag_method_respects_indentation_config() -> None:
    """The generated method uses the indentation size from the config."""
    generator = PandasTypedDfGenerator(config=TypedDfGeneratorConfig(indentation_size=2))

    assert generator.generate_columns_with_tag_method(TaggedModel) == [
        '  @classmethod',
        "  def columns_with_tag(cls, tag: Literal['map_key', 'unit_price', 'total_price', 'country']) -> list[str]:",
        '    return cls.model.columns_with_tag(tag)',
    ]


def test_generate_imports_with_tags_uses_literal() -> None:
    """Models with tags import Literal, and not TyframeTag."""
    generator = PandasTypedDfGenerator(config=TypedDfGeneratorConfig())

    imports = generator.generate_imports(CustomTagModel)

    assert 'from typing import Literal' in imports
    assert 'from tyframe.tagging import TyframeTag' not in imports


def test_generate_imports_without_tags_uses_tyframe_tag() -> None:
    """Models without tags import TyframeTag, and not Literal."""
    generator = PandasTypedDfGenerator(config=TypedDfGeneratorConfig())

    imports = generator.generate_imports(OneColModel)

    assert 'from tyframe.tagging import TyframeTag' in imports
    assert 'from typing import Literal' not in imports


def test_generate_columns_with_tag_method_full_output() -> None:
    """The whole output of the method matches exactly, including custom tags."""
    generator = PandasTypedDfGenerator(config=TypedDfGeneratorConfig())

    assert generator.generate_columns_with_tag_method(CustomTagModel) == [
        '    @classmethod',
        "    def columns_with_tag(cls, tag: Literal['custom', 'map_key']) -> list[str]:",
        '        return cls.model.columns_with_tag(tag)',
    ]
