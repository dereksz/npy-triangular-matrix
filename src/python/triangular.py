from io import StringIO
from sys import stdout
from math import log10, sqrt
import gzip
import numpy as np
import pandas as pd



def pair_to_linear(aa, bb):
    if isinstance(aa, np.ndarray):
        assert (aa > bb).all()
        aa = aa
    else:
        assert aa > bb

    result = (aa)*(aa-1)//2 + bb

    return result


class TriangularMatrix:
    """ Triangular matrix """


    __slots__ = ("_size", "_linear_size", "_ndarray")

    @classmethod
    def empty(cls, size: int, dtype=np.float32, default=None) -> "DynamicTriangularMatrix":
        return DynamicTriangularMatrix(size=size, dtype=dtype, default=default)


    def to_npy(self, filename) -> None:
        np.save(filename, self._ndarray)


    def to_txt(self, filename: str) -> None:
        with (
            gzip.open
            if filename.endswith(".gz") else
            open
        )(filename, 'wt') as fh:
            self.pretty_print(fh)


    @classmethod
    def from_npy(cls, filename) -> "TriangularMatrix":
        self = cls()
        self._ndarray = np.lib.format.open_memmap(filename, mode="r")
        self._linear_size = self._ndarray.size
        self._size = (1 + sqrt(1 + 8*self._linear_size))/2
        return self

    def __getitem__(self, pair):
        linear = pair_to_linear(*pair)
        return self._ndarray[linear]


    def pretty_print(self, out = stdout):
        s = self._size
        idx_width = 8 # int(log10(s-1))+2
        num_width = 8
        nd_base = 0
        print("%*i | %*s" % (idx_width, 0, num_width, "x"), file=out)
        for aa in range(1,s):
            print("%*i | " % (idx_width, aa), file=out, end="")
            slice = self._ndarray[nd_base:(nd_base+aa)]
            for ff in slice:
                print("%*.1f" % (num_width, ff), file=out, end="")
            print("%*s" % (num_width, "x"), file=out)
            nd_base += aa
        print("(%*i) | " % (idx_width-2, self._linear_size), file=out, end="")
        for bb in range(0,s):
            print("%*i" % (idx_width, bb), file=out, end="")
        print(file=out)


    def __str__(self):
        string_buffer = StringIO()
        self.pretty_print(string_buffer)
        return string_buffer.getvalue()


class DynamicTriangularMatrix(TriangularMatrix):
    """ Triangular matrix """


    def __init__(self, size: int, dtype=np.float32, default=None):
        self._size = size
        self._linear_size = pair_to_linear(size,0)
        self._ndarray = (
            np.empty(self._linear_size, dtype)
            if default is None else
            np.full(self._linear_size, default, dtype)
        )


    def __setitem__(self, pair, value):
        linear = pair_to_linear(*pair)
        self._ndarray[linear] = value



