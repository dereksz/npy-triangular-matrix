import numpy as np
from triangular import TriangularMatrix

def test_simple():

    tri = TriangularMatrix(6, np.float16, np.nan)
    tri[2,1] = 3
    print(tri)


if __name__ == "__main__":
    test_simple()