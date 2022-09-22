library(pacman)

p_load(dplyr, magrittr, data.table)
p_load(purrr, furrr)
p_load(tictoc)
p_load(zipcodeR)

zip_code_db %>%
  select(zipcode, longitude=lng, latitude=lat) %>%
  filter(!is.na(latitude)) %>%
  arrange(zipcode) ->
  real_codes

writeLines(real_codes$zipcode, "nodes.txt")

p_load(geodist)
tic("Distances")
dists <- geodist(real_codes, measure="geodesic")
toc()

storage.mode(dists) <- "integer"

tic("Saving")
fh <- file("distances.sq.int32.bin", "wb")
writeBin(dists, fh)
close(fh)
toc()

tic("Saving triangular")
fh <- file("distances.tri.int32.bin", "wb")
for (aa in 2:nrow(dists)) {
  writeBin(dists[aa, 1:(aa-1)], fh)  
}
close(fh)
toc()
