# =====================================================================
# Superintelligence module — H2 power simulation (PREREGISTRATION.md §5c)
#
# H2: the pro-vs-anti swing in ban support is larger under substantive
# than under elite messaging. Test: the direction x route interaction on
# the continuous support score in the four ONE-SIDED cells (3, 6, 7, 8),
# where the route of the single message is unambiguous.
#
# Simulation: support ~ N(cell mean, sd = 1) — effects are therefore in
# SD units (Cohen's d). Direction main effect d = 0.30 throughout (a
# medium-small persuasion effect); the interaction delta (how much LARGER
# the substantive swing is than the elite swing, in SD units) varies over
# a grid. n per cell reflects ~4,000 SARA completes less ~10% screen-out/
# decline spread over 9 cells (~390/cell; 360 as a conservative floor).
#
# Run:  Rscript "Muskan's Experiment/power_sim_h2.R"
# =====================================================================

set.seed(2026)
N_REPS <- 4000
ALPHA  <- 0.05

power_h2 <- function(n_cell, delta, dir_main = 0.30) {
  # one-sided cells: direction (+1 pro / -1 anti) x route (elite/substantive)
  # swing under elite = 2*(dir_main - delta/4) ... parameterise so the
  # substantive-minus-elite difference of swings equals delta exactly:
  #   mean = direction * (dir_main + ifelse(substantive, delta/2, -delta/2)) / 1
  cells <- expand.grid(direction = c(1, -1), substantive = c(0, 1))
  hits <- 0L
  for (r in seq_len(N_REPS)) {
    df <- do.call(rbind, lapply(seq_len(nrow(cells)), function(i) {
      mu <- cells$direction[i] * (dir_main + (cells$substantive[i] - 0.5) * delta)
      data.frame(direction = cells$direction[i],
                 substantive = cells$substantive[i],
                 y = rnorm(n_cell, mu, 1))
    }))
    p <- coef(summary(lm(y ~ direction * substantive, df)))["direction:substantive", 4]
    hits <- hits + (p < ALPHA)
  }
  hits / N_REPS
}

grid <- expand.grid(n_cell = c(360, 390, 430),
                    delta  = c(0.10, 0.15, 0.20, 0.25, 0.30))
grid$power <- mapply(power_h2, grid$n_cell, grid$delta)
cat("H2 power (direction x route interaction, one-sided cells, alpha=.05,\n",
    "dir main effect d=0.30, ", N_REPS, " reps):\n\n", sep = "")
print(xtabs(power ~ n_cell + delta, grid))
cat("\nReading: delta is the substantive-minus-elite difference in the\n",
    "pro-vs-anti swing, in SD units of the support score.\n", sep = "")
