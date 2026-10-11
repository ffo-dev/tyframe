from tests.test_typed_df.simple_typed_df import (
    OneColModel,
    OneColModelPd,
    OneColModelPl,
    TwoColModel,
    TwoColModelPd,
    TwoColModelPl,
)
from tyframe.validation.pandas import PandasValidator
from tyframe.validation.polars import PolarsValidator


def test_typed_pl_df():

    df = TwoColModelPl(
        input_data=[
            TwoColModel(a=1, b='x'),
            TwoColModel(a=2, b='y'),
            TwoColModel(a=3, b='z'),
        ],
        validator=PolarsValidator(),
    )
    other_df = TwoColModelPl(
        input_data=[
            TwoColModel(a=4, b='w'),
            TwoColModel(a=5, b='v'),
        ],
        validator=PolarsValidator(),
    )
    assert df.validated
    assert df.a_col.to_list() == [1, 2, 3]
    assert df.b_col.to_list() == ['x', 'y', 'z']

    assert df.first() == TwoColModel(a=1, b='x')
    assert df.select([OneColModelPl.a]).to_dicts() == [{'a': 1}, {'a': 2}, {'a': 3}]
    one_col_model = df.select_to(OneColModelPl)
    assert isinstance(one_col_model, OneColModelPl)
    assert one_col_model.collect() == [
        OneColModel(a=1),
        OneColModel(a=2),
        OneColModel(a=3),
    ]
    assert one_col_model.count() == 3

    unioned = df.union(other_df)
    assert unioned.collect() == [
        TwoColModel(a=1, b='x'),
        TwoColModel(a=2, b='y'),
        TwoColModel(a=3, b='z'),
        TwoColModel(a=4, b='w'),
        TwoColModel(a=5, b='v'),
    ]
    assert unioned.count() == 5

    with_dups = TwoColModelPl(
        input_data=[
            TwoColModel(a=1, b='x'),
            TwoColModel(a=1, b='x'),
            TwoColModel(a=1, b='x'),
            TwoColModel(a=1, b='x'),
            TwoColModel(a=2, b='y'),
            TwoColModel(a=3, b='z'),
        ],
        validator=PolarsValidator(),
    )
    distinct = with_dups.distinct()
    assert distinct.count() == 3


def test_typed_pd_df():

    df = TwoColModelPd(
        input_data=[
            TwoColModel(a=1, b='x'),
            TwoColModel(a=2, b='y'),
            TwoColModel(a=3, b='z'),
        ],
        validator=PandasValidator(),
    )
    other_df = TwoColModelPd(
        input_data=[
            TwoColModel(a=4, b='w'),
            TwoColModel(a=5, b='v'),
        ],
        validator=PandasValidator(),
    )
    assert df.validated
    assert df.a_col.to_list() == [1, 2, 3]
    assert df.b_col.to_list() == ['x', 'y', 'z']

    assert df.first() == TwoColModel(a=1, b='x')
    assert df.select([OneColModelPd.a]).to_dict(orient='records') == [
        {'a': 1},
        {'a': 2},
        {'a': 3},
    ]
    one_col_model = df.select_to(OneColModelPd)
    assert isinstance(one_col_model, OneColModelPd)
    assert one_col_model.collect() == [
        OneColModel(a=1),
        OneColModel(a=2),
        OneColModel(a=3),
    ]
    assert one_col_model.count() == 3

    unioned = df.union(other_df)
    assert unioned.collect() == [
        TwoColModel(a=1, b='x'),
        TwoColModel(a=2, b='y'),
        TwoColModel(a=3, b='z'),
        TwoColModel(a=4, b='w'),
        TwoColModel(a=5, b='v'),
    ]
    assert unioned.count() == 5

    with_dups = TwoColModelPl(
        input_data=[
            TwoColModel(a=1, b='x'),
            TwoColModel(a=1, b='x'),
            TwoColModel(a=1, b='x'),
            TwoColModel(a=1, b='x'),
            TwoColModel(a=2, b='y'),
            TwoColModel(a=3, b='z'),
        ],
        validator=PolarsValidator(),
    )
    distinct = with_dups.distinct()
    assert distinct.count() == 3
