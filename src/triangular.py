from io import StringIO
from math import log10
from sys import stdout
import numpy as np

class InvalidOperation(Exception):
    pass

def pair_to_linear(aa, bb):
    assert aa > bb
    return (aa)*(aa-1)//2 + bb

class TriangularMatrix:
    """ Triangular matrix """


    __slots__ = ("_size", "_linear_size", "_ndarray")


    def __init__(self, size: int, dtype, default=None):
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


    def pretty_print(self, out = stdout):
        s = self._size
        idx_width = 5 # int(log10(s-1))+2
        num_width = 5
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
