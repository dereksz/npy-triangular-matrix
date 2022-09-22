library(pacman)

p_load(dplyr, magrittr, data.table)
p_load(purrr, furrr)
p_load(tictoc)
p_load(zipcodeR)

zip_code_db %$%
  zipcode[!is.na(lat)] %>%
  sort() %>%
  as.factor() ->
  # head(10000) ->
  real_codes

n_codes <- length(real_codes)

tic("Build axies")
aa <- head(real_codes, n=-1)
aa <- rep.int(aa, seq(from=n_codes-1, to=1, by=-1))
bb <- unlist(map(seq(2,n_codes), ~real_codes[.x:n_codes]))
df <- data.table(aa=aa, bb=bb)
toc()

workers=11L
chunks = workers * 1000L
chunk_size <- ((length(aa) - 1L) %/% chunks)+1L
message("Running ", workers, " processes with ", chunks, " chunks of ", chunk_size, " each.")

lowers <- seq(1, length(aa), by=chunk_size)
uppers <- lowers + chunk_size - 1
uppers[workers] = length(aa)

plan(multisession, workers=workers)

tic("\nDistance Chunks")
map2(lowers, uppers, ~df[.x:.y,1:2]) %>%
  future_map(
    ~zip_distance(.x[[1]], .x[[2]])[[3]],
    .options = furrr_options(scheduling = Inf),
    .progress = TRUE
  ) ->
  chunks
toc()
tic("Consolidate")
df$distance <- unlist(chunks)
toc()

p_load(arrow)
write_feather(df, "distances.arrow", compression="lz4")

