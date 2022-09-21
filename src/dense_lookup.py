import math
import numpy as np

class DenseFromSemiDense:
    """ Lookup class for converting a semi-dense set of numbers into a dense set (zero-based) """

    __slots__ = ("_lookup", "_current_idx")

    _lookup: np.ndarray


    def __init__(self, max_items=33104):
        self._lookup = np.full(max_items, 0, np.uint16)
        self._current_idx = 1


    def add_or_lookup_item(self, item) -> int:
        idx = self._lookup[item]
        if idx == 0:
            idx = self._current_idx
            self._lookup[item] = idx
            self._current_idx += 1
        return idx


    def add_or_lookup_items(self, items) -> int:
        result = self._lookup[items]
        zero_count = (result == 0).sum()
        if zero_count > 0:
            new_indexes = range(self._current_idx, self._current_idx+zero_count)
            self._current_idx += zero_count
            zero_idxs = np.where(result == 0)
            self._lookup[items[zero_idxs]] = new_indexes
            result[zero_idxs] = new_indexes
        return result
