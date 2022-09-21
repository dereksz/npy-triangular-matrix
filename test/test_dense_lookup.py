import numpy as np
from dense_lookup import DenseFromSemiDense

def test_simple():
    lookup = DenseFromSemiDense()
    idx = lookup.add_or_lookup_item(20)
    assert idx == 1
    idxs = lookup.add_or_lookup_items(np.array(range(100,200,10)))
    assert (idxs == np.array(range(2,12))).all()
    idxs = lookup.add_or_lookup_items(np.array(range(100,300,20)))
    assert (idxs == [2, 4, 6, 8, 10, 12, 13, 14, 15, 16]).all()


if __name__ == "__main__":
    test_simple()