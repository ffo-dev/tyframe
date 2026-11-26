from tests.generated_models.lazy_polars.custom_tag_model_lpl import CustomTagModelLpl
from tests.generated_models.lazy_polars.one_col_model_lpl import OneColModelLpl
from tests.generated_models.lazy_polars.tagged_model_lpl import TaggedModelLpl
from tests.generated_models.pandas.custom_tag_model_pd import CustomTagModelPd
from tests.generated_models.pandas.one_col_model_pd import OneColModelPd
from tests.generated_models.pandas.tagged_model_pd import TaggedModelPd
from tests.generated_models.polars.custom_tag_model_pl import CustomTagModelPl
from tests.generated_models.polars.one_col_model_pl import OneColModelPl
from tests.generated_models.polars.tagged_model_pl import TaggedModelPl
from tests.test_classes.models import TaggedModel
from tyframe.validation.pandas import PandasValidator


def test_columns_with_tag_tyframe_tag() -> None:
    assert TaggedModelPd.columns_with_tag('map_key') == ['id']
    assert TaggedModelPl.columns_with_tag('map_key') == ['id']
    assert TaggedModelLpl.columns_with_tag('map_key') == ['id']
    assert TaggedModelPd.columns_with_tag('unit_price') == ['price']
    assert TaggedModelPd.columns_with_tag('total_price') == ['price']
    assert TaggedModelPd.columns_with_tag('country') == ['country']
    assert TaggedModelPl.columns_with_tag('unit_price') == ['price']
    assert TaggedModelLpl.columns_with_tag('country') == ['country']


def test_columns_with_tag_custom_tag() -> None:
    assert CustomTagModelPd.columns_with_tag('custom') == ['a']
    assert CustomTagModelPl.columns_with_tag('custom') == ['a']
    assert CustomTagModelLpl.columns_with_tag('custom') == ['a']
    assert CustomTagModelPd.columns_with_tag('map_key') == ['b']
    assert CustomTagModelPl.columns_with_tag('map_key') == ['b']
    assert CustomTagModelLpl.columns_with_tag('map_key') == ['b']


def test_columns_with_tag_no_tags_returns_empty() -> None:
    assert OneColModelPd.columns_with_tag('map_key') == []
    assert OneColModelPl.columns_with_tag('join_key') == []
    assert OneColModelLpl.columns_with_tag('country') == []


def test_columns_with_tag_used_in_select() -> None:
    df = TaggedModelPd(
        input_data=[
            TaggedModel(id=1, price=9.5, country='it', name='x'),
            TaggedModel(id=2, price=3.0, country='fr', name='y'),
        ],
        validator=PandasValidator(),
    )
    selected = df.select(TaggedModelPd.columns_with_tag('map_key'))
    assert list(selected.columns) == ['id']
