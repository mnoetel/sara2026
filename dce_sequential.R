# =====================================================================
# SARA USA 2026 — the pre-registered DCE wave/checkpoint loop
# (PREREGISTRATION.md §5; protocol v10 Appendix B)
#
# Runs OFF-PLATFORM between waves. Deterministic given the data: fixed
# model specification (dce_model_utils.R), fixed seeds, fixed checkpoint
# sizes, adopt-if-better D-error rule, hard lock after the final wave.
# Only the PRIORS update — never the model, criterion, or an individual
# respondent's instrument. The update uses the posterior MEANS as the new
# cbcTools prior means (the D-error criterion is evaluated at the
# posterior mean; cbcTools' stochastic search supplies the draws).
#
# Usage:
#   Rscript dce_sequential.R --checkpoint <next_wave: 2|3|4> <export1.csv> [...]
#       Re-estimates on all accumulated oTree exports, regenerates the
#       design, adopts it only if the D-error improves, writes
#       survey/sara/dce_blocks.csv (+ an archived copy per wave, + a log).
#       Wave sizes: pilot ~500, then ~1,170 per main wave; cap N = 4,000.
#       After wave 4 the design is permanently locked: --checkpoint 5+ is
#       refused.
#   Rscript dce_sequential.R --simulate
#       End-to-end recovery test of the SEQUENTIAL procedure: simulates
#       all four waves from a known mixed logit (respondents choose on
#       whichever design their wave fielded), runs every checkpoint
#       exactly as above, and reports estimate-vs-truth at each step.
#
# oTree export format: one row per participant with columns
# participant.code, player.dce_block, player.dce_1 .. player.dce_10
# (prefixes are stripped automatically; 1 = Option A, 2 = B, 3 = opt-out).
# =====================================================================

library(cbcTools)
library(logitr)
suppressMessages(library(dplyr))

.argv <- commandArgs(trailingOnly = FALSE)
.self <- sub("^--file=", "", .argv[grep("^--file=", .argv)])
.root <- if (length(.self)) dirname(normalizePath(.self)) else getwd()
source(file.path(.root, "dce_model_utils.R"))

BLOCKS_CSV <- file.path(.root, "survey", "sara", "dce_blocks.csv")
LOG_CSV    <- file.path(.root, "dce_sequential_log.csv")
FINAL_WAVE <- 4          # design locked permanently after this checkpoint
DESIGN_SEED_BASE <- 2026 # wave k design seed = DESIGN_SEED_BASE + (k - 1)
N_MULTISTARTS <- 5

# The same profile grid as sara_dce_design.R (order matters for cbc_priors).
profiles <- cbc_profiles(
  severity    = names(SEV_TO_LOGN),
  risk_annual = names(RISK_TO_LOGP),
  benefit     = c("Modest", "Major", "Transformative"),
  competition = c("Other countries are ahead", "The US keeps pace",
                  "The US is ahead")
)

# ── One checkpoint: estimate -> regenerate -> adopt-if-better ─────────
# dat: coded long-format choice data (all waves so far).
# wave: the wave the NEW design would field (2..FINAL_WAVE).
# incumbent_tasks: the design the LAST wave fielded (defaults to the
# committed dce_blocks.csv; the simulation passes its in-memory copy).
# Returns list(model, adopted, d_incumbent, d_candidate, tasks).
run_checkpoint <- function(dat, wave, incumbent_tasks = NULL,
                           write_files = TRUE) {
  if (wave > FINAL_WAVE) stop(
    "Design is permanently locked after wave ", FINAL_WAVE,
    " (pre-registered); refusing checkpoint for wave ", wave, ".")

  m <- dce_estimate(dat, numMultiStarts = N_MULTISTARTS)
  est <- coef(m)
  beta_mean <- est[MAIN_PARS]

  set.seed(DESIGN_SEED_BASE + (wave - 1))
  candidate <- cbc_design(
    profiles  = profiles,
    priors    = dce_coefs_to_priors(est, profiles),
    method    = "stochastic",
    n_alts    = 2, n_q = 8, n_blocks = 10, n_resp = 4000,
    no_choice = TRUE, max_iter = 50,
    n_cores   = 1   # parallel workers ignore set.seed -> non-reproducible runs
  )
  cand_tasks <- dce_export_blocks(candidate, tempfile(fileext = ".csv"))

  if (is.null(incumbent_tasks)) {
    incumbent_tasks <- read.csv(BLOCKS_CSV, check.names = FALSE)
  }
  d_inc  <- dce_d_error(dce_blocks_template(incumbent_tasks), beta_mean)
  d_cand <- dce_d_error(dce_blocks_template(cand_tasks), beta_mean)
  adopted <- d_cand < d_inc

  cat(sprintf(
    "\ncheckpoint -> wave %d | n_resp = %d | D-error incumbent %.5g vs candidate %.5g -> %s\n",
    wave, length(unique(dat$respID)), d_inc, d_cand,
    if (adopted) "ADOPT candidate" else "KEEP incumbent"))

  tasks <- if (adopted) cand_tasks else incumbent_tasks
  if (write_files) {
    archive <- file.path(.root, sprintf("dce_blocks_wave%d.csv", wave))
    write.csv(tasks, BLOCKS_CSV, row.names = FALSE)
    write.csv(tasks, archive, row.names = FALSE)
    log_row <- data.frame(
      timestamp = format(Sys.time(), tz = "UTC"), wave = wave,
      n_resp = length(unique(dat$respID)),
      d_incumbent = d_inc, d_candidate = d_cand, adopted = adopted,
      t(round(beta_mean, 4)), sd_logp = round(est[["sd_logp"]], 4))
    write.table(log_row, LOG_CSV, sep = ",", row.names = FALSE,
                col.names = !file.exists(LOG_CSV), append = file.exists(LOG_CSV))
    cat("wrote", BLOCKS_CSV, "and", archive, "; logged to", LOG_CSV, "\n")
    cat("REMINDER: restart the oTree app so it reloads the new blocks, and\n",
        "commit the archived design + log before fielding the next wave.\n")
  }
  invisible(list(model = m, adopted = adopted,
                 d_incumbent = d_inc, d_candidate = d_cand, tasks = tasks))
}

# ── Real-fielding entry point ─────────────────────────────────────────
read_exports <- function(paths) {
  resp <- bind_rows(lapply(paths, function(p) {
    df <- read.csv(p, check.names = FALSE)
    names(df) <- sub("^(player|participant)\\.", "", names(df))
    need <- c("code", "dce_block", paste0("dce_", 1:10))
    missing <- setdiff(need, names(df))
    if (length(missing)) stop(p, ": missing columns ", paste(missing, collapse = ", "))
    df[, need]
  }))
  resp[!is.na(resp$dce_block), ]
}

# ── Sequential recovery simulation ────────────────────────────────────
simulate_sequential <- function() {
  waves <- c(500, 1170, 1170, 1160)      # pre-registered sizes; sum = 4,000
  b_true <- c(logp = -0.9, logn = -0.35, ben_major = 0.6, ben_transf = 1.4,
              comp_pace = 0.3, comp_lead = 0.7, no_choice = -0.2)
  sd_logp_true <- 0.4

  # Wave-1 design = the committed guess-prior design (dce_blocks.csv as
  # generated by sara_dce_design.R).
  current_tasks <- read.csv(BLOCKS_CSV, check.names = FALSE)
  dat <- NULL
  offset <- 0
  set.seed(7)

  for (w in seq_along(waves)) {
    template <- dce_blocks_template(current_tasks)
    wave_dat <- dce_replicate_template(template, waves[w], resp_offset = offset)
    wave_dat <- dce_simulate_choices(wave_dat, b_true, sd_logp = sd_logp_true)
    offset <- offset + waves[w]
    wave_dat$obsID <- wave_dat$obsID + if (is.null(dat)) 0 else max(dat$obsID)
    dat <- bind_rows(dat, wave_dat)
    cat(sprintf("\n=== simulated wave %d fielded (n = %d, cumulative %d) ===\n",
                w, waves[w], length(unique(dat$respID))))

    if (w < length(waves)) {
      res <- run_checkpoint(dat, wave = w + 1,
                            incumbent_tasks = current_tasks, write_files = FALSE)
      est <- coef(res$model)
      cat("--- recovery so far (estimate - truth) ---\n")
      print(round(est[names(b_true)] - b_true, 3))
      current_tasks <- res$tasks
    }
  }

  m <- dce_estimate(dat, numMultiStarts = N_MULTISTARTS)
  est <- coef(m)
  cat("\n=== FINAL pooled estimate (all", length(unique(dat$respID)), "respondents) ===\n")
  print(summary(m))
  cat("\n--- FINAL recovery (estimate - truth) ---\n")
  dev <- est[names(b_true)] - b_true
  print(round(dev, 3))
  cat("sd_logp: est", round(est[["sd_logp"]], 3), "truth", sd_logp_true, "\n")
  # |sd_logp|: logitr's normal-SD parameter is sign-invariant
  ok <- all(abs(dev) < 0.1) && abs(abs(est[["sd_logp"]]) - sd_logp_true) < 0.1
  cat(if (ok) "\nRECOVERY OK: all deviations < 0.1\n"
      else "\nRECOVERY WARNING: some deviations >= 0.1 — inspect before fielding\n")
  invisible(ok)
}

# ── CLI ───────────────────────────────────────────────────────────────
args <- commandArgs(trailingOnly = TRUE)
if (length(args) >= 1 && args[1] == "--simulate") {
  simulate_sequential()
} else if (length(args) >= 3 && args[1] == "--checkpoint") {
  wave <- as.integer(args[2])
  resp <- read_exports(args[-(1:2)])
  dat <- dce_build_long(resp, BLOCKS_CSV)
  run_checkpoint(dat, wave)
} else if (length(args) == 0) {
  cat("usage:\n  Rscript dce_sequential.R --simulate\n",
      " Rscript dce_sequential.R --checkpoint <2|3|4> <export1.csv> [...]\n")
} else {
  stop("unrecognised arguments; run with no args for usage")
}
