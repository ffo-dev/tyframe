import polars as pl

from tests.generated_models.lazy_polars.one_col_model_lpl import OneColModelLpl
from tests.generated_models.lazy_polars.two_col_model_lpl import TwoColModelLpl
from tests.test_classes.models import OneColModel, TwoColModel
from tyframe.validation.polars import LazyPolarsValidator


def test_typed_pl_df() -> None:

    df = TwoColModelLpl(
        input_data=[
            TwoColModel(a=1, b='x'),
            TwoColModel(a=2, b='y'),
            TwoColModel(a=3, b='z'),
        ],
        validator=LazyPolarsValidator(),
    )
    other_df = TwoColModelLpl(
        input_data=[
            TwoColModel(a=4, b='a'),
            TwoColModel(a=5, b='b'),
        ],
        validator=LazyPolarsValidator(),
    )
    assert df.validated
    assert df.a_col.to_list() == [1, 2, 3]
    assert df.b_col.to_list() == ['x', 'y', 'z']

    assert df.first() == TwoColModel(a=1, b='x')
    assert df.select([OneColModelLpl.a]).collect().to_dicts() == [{'a': 1}, {'a': 2}, {'a': 3}]
    one_col_model = df.select_to(OneColModelLpl)
    assert isinstance(one_col_model, OneColModelLpl)
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
        TwoColModel(a=4, b='a'),
        TwoColModel(a=5, b='b'),
    ]
    assert unioned.count() == 5

    condition = pl.col(TwoColModelLpl.a).is_between(lower_bound=2, upper_bound=4, closed='both')

    filtered_df = unioned.filter(condition)

    assert filtered_df.sort([TwoColModelLpl.b]).collect() == [
        TwoColModel(a=4, b='a'),
        TwoColModel(a=2, b='y'),
        TwoColModel(a=3, b='z'),

    ]

    with_dups = TwoColModelLpl(
        input_data=[
            TwoColModel(a=1, b='x'),
            TwoColModel(a=1, b='x'),
            TwoColModel(a=1, b='x'),
            TwoColModel(a=1, b='x'),
            TwoColModel(a=2, b='y'),
            TwoColModel(a=3, b='z'),
        ],
        validator=LazyPolarsValidator(),
    )
    distinct = with_dups.distinct()
    assert distinct.count() == 3


