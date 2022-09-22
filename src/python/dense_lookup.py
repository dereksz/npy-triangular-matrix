import numpy as np



class DenseFromSemiDense:
    """ Lookup class for converting a semi-dense set of numbers into a dense set (unfilled-based) """

    __slots__ = ("_lookup")

    _lookup: np.ndarray


    @classmethod
    def empty(cls, max_items=99999, dtype=np.uint32):
        return DynamicDenseFromSemiDense(max_items=max_items, dtype=dtype)


    @classmethod
    def from_npy(cls, filename):
        self = cls()
        self._lookup = np.load(filename)
        return self


    def lookup_items(self, items: np.ndarray) -> int:
        return self._lookup[items]


    def to_npy(self, filename) -> None:
        np.save(filename, self._lookup)


class DynamicDenseFromSemiDense(DenseFromSemiDense):
    """ Lookup class for converting a semi-dense set of numbers into a dense set (unfilled-based) """

    __slots__ = ("_current_idx", "_unfilled")

    def __init__(self, max_items=99999, dtype=np.uint32):
        self._unfilled = ~dtype(0)
        self._lookup = np.full(max_items, self._unfilled, dtype)
        self._current_idx = 0


    def add_or_lookup_item(self, item) -> int:
        idx = self._lookup[item]
        if idx == self._unfilled:
            idx = self._current_idx
            self._lookup[item] = idx
            self._current_idx += 1
        return idx


    def add_or_lookup_items(self, items: np.ndarray) -> int:
        result = self._lookup[items]
        unfilled_count = (result == self._unfilled).sum()
        if unfilled_count > 0:
            unfilled_idxs = np.where(result == self._unfilled)
            unique_missing = np.unique(items[unfilled_idxs])
            new_indexes = range(self._current_idx, self._current_idx+unique_missing.size)
            self._current_idx += unique_missing.size
            self._lookup[unique_missing] = new_indexes
            result[unfilled_idxs] = self._lookup[items[unfilled_idxs]]
        return result
