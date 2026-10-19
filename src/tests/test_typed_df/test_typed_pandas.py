
from tests.generated_models.pandas.one_col_model_pd import OneColModelPd
from tests.generated_models.pandas.two_col_model_pd import TwoColModelPd
from tests.test_classes.models import OneColModel, TwoColModel
from tyframe.validation.pandas import PandasValidator


def test_typed_pl_df() -> None:

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
            TwoColModel(a=4, b='a'),
            TwoColModel(a=5, b='b'),
        ],
        validator=PandasValidator(),
    )
    assert df.validated
    assert df.a_col.to_list() == [1, 2, 3]
    assert df.b_col.to_list() == ['x', 'y', 'z']

    assert df.first() == TwoColModel(a=1, b='x')
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
        TwoColModel(a=4, b='a'),
        TwoColModel(a=5, b='b'),
    ]
    assert unioned.count() == 5

    condition = (unioned.a_col >= 2) & (unioned.a_col <=4)

    filtered_df = unioned.filter(condition)

    assert filtered_df.sort([TwoColModelPd.b]).collect() == [
        TwoColModel(a=4, b='a'),
        TwoColModel(a=2, b='y'),
        TwoColModel(a=3, b='z'),

    ]

    with_dups = TwoColModelPd(
        input_data=[
            TwoColModel(a=1, b='x'),
            TwoColModel(a=1, b='x'),
            TwoColModel(a=1, b='x'),
            TwoColModel(a=1, b='x'),
            TwoColModel(a=2, b='y'),
            TwoColModel(a=3, b='z'),
        ],
        validator=PandasValidator(),
    )
    distinct = with_dups.distinct()
    assert distinct.count() == 3


