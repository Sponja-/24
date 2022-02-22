from expressions import Addition, Constant


def test_commutativity():
    assert hash(Addition(Constant(1), Constant(2))) == hash(Addition(Constant(2), Constant(1)))
