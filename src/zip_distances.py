import numpy as np
import pandas as pd

from dense_lookup import DenseFromSemiDense
from triangular import TriangularMatrix


class ZipDistances:

    __slots__ = ("_dense_lookup", "_distances")


    @staticmethod
    def from_csv(filename="zip-distances.csv.gz", chunksize = 1e7, verbose=True, max_chunks=None):
        result = DynamicZipDistances()
        result.from_csv(filename=filename, chunksize = chunksize, verbose=verbose, max_chunks=max_chunks)
        return result


    def to_npys(self, folder=".") -> None:
        self._dense_lookup.to_npy(f"{folder}/index.npy")
        self._distances.to_npy(f"{folder}/distances.npy")


    @staticmethod
    def from_npys(folder=".") -> None:
        self = ZipDistances()
        self._dense_lookup = DenseFromSemiDense.from_npy(f"{folder}/index.npy")
        self._distances = TriangularMatrix.from_npy(f"{folder}/distances.npy")
        return self

    def __getitem__(self, pair):
        aa = self._dense_lookup.lookup_items(pair[0])
        bb = self._dense_lookup.lookup_items(pair[1])
        need_swaps = np.where(aa < bb)[0]
        if need_swaps.size > 0:
            aa[need_swaps], bb[need_swaps] = bb[need_swaps], aa[need_swaps]
        return self._distances[aa,bb]



class DynamicZipDistances(ZipDistances):

    def __init__(self, max_items=33104):
        self._dense_lookup = DenseFromSemiDense.empty(99999)
        self._distances = TriangularMatrix.empty(max_items, np.float32, np.nan)


    def set_distances_from_frame(self, frame: pd.DataFrame) -> None:
        aa = self._dense_lookup.add_or_lookup_items(frame.iloc[:,0].values)
        bb = self._dense_lookup.add_or_lookup_items(frame.iloc[:,1].values)
        need_swaps = np.where(aa < bb)[0]
        if need_swaps.size > 0:
            aa[need_swaps], bb[need_swaps] = bb[need_swaps], aa[need_swaps]
        self._distances[aa,bb] = frame.iloc[:,2].values


    def from_csv(self, filename="zip-distances.csv.gz", chunksize = 1e7, verbose=True, max_chunks=None) -> "ZipDistances":
        nan_distances = 0
        i = 0
        with pd.read_csv(
            filename,
            chunksize=chunksize, compression="gzip",
            names = ["aa", "bb", "distance"],
            dtype={"aa": np.uint32, "bb": np.uint32, "distance": np.float32}
        ) as reader:
            for chunk in reader:
                nan_distances += np.isnan(chunk.iloc[:,2]).sum()
                self.set_distances_from_frame(chunk)
                if verbose:
                    print(f"\rLoaded chunk {i}", end="")
                i += 1
                if max_chunks is not None and i >= max_chunks:
                    break
        if verbose:
            print()

        nan_in_mx = np.isnan(self._distances._ndarray).sum()
        assert nan_distances == nan_in_mx
