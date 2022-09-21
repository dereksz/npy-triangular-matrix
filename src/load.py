from ttictoc import tic,toc
from zip_distances import ZipDistances

tic()
zip_distances = ZipDistances.from_csv(
    "zip-distances.csv.gz",
    # max_chunks=20,
)
print(toc("Loaded"))

tic()
zip_distances.to_npys()
print(toc("Saved to npys"))
# zip_distances._distances.to_txt("distances.txt.gz")

tic()
zip_distances2 = ZipDistances.from_npys()
print(toc("Reloaded"))
d = zip_distances2[83414,35004]

print(d)

a=0
