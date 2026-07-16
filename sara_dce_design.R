# =====================================================================
# SARA USA 2026 — Module 4 (DCE): design generation + export for oTree
# Catastrophic-risk tolerance and the severity / probability / utility /
# competition tradeoff.
#
# v11 (29 Jun 2026): severity is now a VARIED attribute (the four-tier
# ladder), per protocol v10.
# v12 (01 Jul 2026): COST dropped (moved to the dumpster) — money is an
# implementation question, not the democratic tradeoff the DCE measures
# (Hadfield); WTP now comes from the stated item m5_wtp. Benefit levels
# reworded (Minor / Major / Transformational). Full factorial now
# 4 x 5 x 3 x 3 = 180.
# v13 (02 Jul 2026): internal-validity tasks added (ISPOR guidance). Each
# block is now 8 Bayesian D-efficient tasks + task 9 = a DOMINATED pair
# (one option strictly better on every attribute; dominant side alternates
# by block) + task 10 = an exact REPEAT of task 2 (within-person stability).
# Tasks 9-10 are excluded from estimation and analysed as quality checks
# (see protocol Appendix B and PREREGISTRATION.md).
# v14 (03 Jul 2026): severity extended with the FRI/XPT extinction tier
# (global population below 5,000), matching the new m4c_extinction ladder
# rung and the Method-4 forecaster anchors. Full factorial now
# 5 x 5 x 3 x 3 = 225. The registered model gains an extinction
# discontinuity indicator (`ext`) so the data can test whether extinction
# is dreaded beyond its log-death value (Schubert et al.) rather than
# assuming linearity in log deaths.
# This script (a) generates a Bayesian D-efficient design, (b) EXPORTS the
# 10 blocks x 10 tasks as a flat CSV that the oTree app consumes, and
# (c) keeps the simulate/estimate/recover sections for identification.
#
# Run in R >= 4.2.  install.packages(c("cbcTools","logitr","dplyr"))
# cbcTools >= 0.7 API.
# =====================================================================

library(cbcTools)
suppressMessages(library(dplyr))

# Write next to THIS script's checkout (works from any CWD / git worktree),
# with a sensible fallback when the script path can't be resolved.
.argv <- commandArgs(trailingOnly = FALSE)
.self <- sub("^--file=", "", .argv[grep("^--file=", .argv)])
.root <- if (length(.self)) dirname(normalizePath(.self)) else getwd()
OUT_CSV <- file.path(.root, "survey", "sara", "dce_blocks.csv")

# ---------------------------------------------------------------------
# 1. THE GRID  (attributes x levels)  — severity now varied
# ---------------------------------------------------------------------
# Wording shown to respondents is the level string itself, so the oTree
# DCE table can render these verbatim.
profiles <- cbc_profiles(
  severity    = c("A single death",
                  "100 deaths",
                  "1,000,000 deaths",
                  "~800,000,000 deaths (10% of humanity)",
                  "Human extinction (fewer than 5,000 people survive)"),  # SEVERITY (5)
  risk_annual = c("1 in 100", "1 in 1,000", "1 in 10,000",
                  "1 in 100,000", "1 in 1,000,000"),          # PROBABILITY (5)
  benefit     = c("Modest", "Major", "Transformative"),       # UTILITY (3)
  competition = c("Other countries are ahead", "The US keeps pace",
                  "The US is ahead")                          # COMPETITION (3)
)
# Full factorial = 5 * 5 * 3 * 3 = 225 profiles.
# Benefit levels are shown to respondents as short labels; render.py prints a
# one-line legend under each task with a plain-English gloss of each.

# ---------------------------------------------------------------------
# 2. PRIORS for a Bayesian D-efficient design
#    Signs: safer (lower severity / lower prob) better; benefit & US-leading
#    positive. Ordered attributes get increasing part-worths.
# ---------------------------------------------------------------------
priors <- cbc_priors(
  profiles    = profiles,
  severity    = c(-0.8, -1.6, -2.4, -3.4), # vs ref "A single death" (worse = lower);
                                           # extinction = the log-death trend (~-2.7)
                                           # plus a guessed dread premium (~-0.7)
  risk_annual = c(0.6, 1.2, 1.8, 2.4), # vs ref "1 in 100" (safer = higher)
  benefit     = c(0.6, 1.4),           # vs ref "Minor"
  competition = c(0.3, 0.7),           # vs ref "Other countries are ahead"
  no_choice   = -0.2
)

# ---------------------------------------------------------------------
# 3. GENERATE THE DESIGN  (Bayesian D-efficient; 2 alts + opt-out;
#    8 q per block — tasks 9-10 are appended quality checks, see 3c)
# ---------------------------------------------------------------------
# NOTE (verified 02 Jul 2026): cbc_design's stochastic search is NOT
# seed-reproducible — two runs differ even single-core with set.seed.
# Reproducibility is therefore ARCHIVAL: the committed dce_blocks.csv is
# the canonical design. Never regenerate casually once fielding has
# started; each wave's fielded design is archived by dce_sequential.R.
set.seed(2026)
design <- cbc_design(
  profiles  = profiles,
  priors    = priors,
  method    = "stochastic",  # Bayesian D-efficient
  n_alts    = 2,
  n_q       = 8,
  n_blocks  = 10,
  n_resp    = 4000,
  no_choice = TRUE,
  max_iter  = 50
)

cat("\n--- design columns ---\n"); print(names(design))
cat("\n--- design head ---\n"); print(utils::head(design, 8))

# ---------------------------------------------------------------------
# 3b/3c. EXPORT the 10 blocks x 10 tasks for oTree (one row per task):
# 8 D-efficient tasks + task 9 dominated pair + task 10 repeat of task 2.
# The export (incl. the quality tasks) is shared with the sequential loop
# via dce_export_blocks() in dce_model_utils.R, so the two scripts cannot
# drift apart.
# ---------------------------------------------------------------------
source(file.path(.root, "dce_model_utils.R"))
tasks <- dce_export_blocks(design, OUT_CSV)
cat("\nWROTE", nrow(tasks), "tasks across",
    length(unique(tasks$block)), "blocks ->", OUT_CSV, "\n")

# ---------------------------------------------------------------------
# 4-7. Identification: simulate from a KNOWN mixed logit -> estimate with
#      the registered specification -> compare. (v13 repair: the old
#      cbc_choices() path broke on cbcTools' automatic dummy re-coding;
#      choices are now simulated directly from the utility model we
#      estimate, which is also the honest recovery test — the DGP and the
#      estimator share a specification.) Wrapped so export never blocks.
#      The SEQUENTIAL procedure's recovery test lives in dce_sequential.R
#      (--simulate); this block validates the one-shot wave-1 design.
# ---------------------------------------------------------------------
try({
  library(logitr)
  dat <- dce_code_design(design)      # logp/logn/dummies/no_choice rows

  set.seed(7)
  b_true <- c(logp = -0.9, logn = -0.35, ext = -0.7, ben_major = 0.6,
              ben_transf = 1.4, comp_pace = 0.3, comp_lead = 0.7,
              no_choice = -0.2)
  sd_logp_true <- 0.4                 # respondent heterogeneity on the risk slope
  dat <- dce_simulate_choices(dat, b_true, sd_logp = sd_logp_true)

  m <- dce_estimate(dat, numMultiStarts = 5)
  print(summary(m))

  est <- coef(m)
  cat("\n--- recovery (estimate - truth) ---\n")
  print(round(est[names(b_true)] - b_true, 3))
  cat("sd_logp: est", round(est[["sd_logp"]], 3), "truth", sd_logp_true, "\n")
}, silent = FALSE)

# Report p* as a DISTRIBUTION with credible intervals by severity tier and
# benefit scenario — never a single point (see protocol v10 §3.2 / Appendix B).
# =====================================================================
