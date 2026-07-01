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
                  "100 deaths or $1B damage",
                  "1,000,000 deaths or $100B damage",
                  "~800,000,000 deaths (10% of humanity)"),   # SEVERITY (4)
  risk_annual = c("1 in 100", "1 in 1,000", "1 in 10,000",
                  "1 in 100,000", "1 in 1,000,000"),          # PROBABILITY (5)
  benefit     = c("Modest", "Major", "Transformative"),       # UTILITY (3)
  competition = c("Other countries are ahead", "The US keeps pace",
                  "The US is ahead")                          # COMPETITION (3)
)
# Full factorial = 4 * 5 * 3 * 3 = 180 profiles.
# Benefit levels are shown to respondents as short labels; render.py prints a
# one-line legend under each task with a plain-English gloss of each.

# ---------------------------------------------------------------------
# 2. PRIORS for a Bayesian D-efficient design
#    Signs: safer (lower severity / lower prob) better; benefit & US-leading
#    positive. Ordered attributes get increasing part-worths.
# ---------------------------------------------------------------------
priors <- cbc_priors(
  profiles    = profiles,
  severity    = c(-0.8, -1.6, -2.4),   # vs ref "A single death" (worse = lower)
  risk_annual = c(0.6, 1.2, 1.8, 2.4), # vs ref "1 in 100" (safer = higher)
  benefit     = c(0.6, 1.4),           # vs ref "Minor"
  competition = c(0.3, 0.7),           # vs ref "Other countries are ahead"
  no_choice   = -0.2
)

# ---------------------------------------------------------------------
# 3. GENERATE THE DESIGN  (Bayesian D-efficient; 2 alts + opt-out; 10 q; 10 blocks)
# ---------------------------------------------------------------------
set.seed(2026)
design <- cbc_design(
  profiles  = profiles,
  priors    = priors,
  method    = "stochastic",  # Bayesian D-efficient
  n_alts    = 2,
  n_q       = 10,
  n_blocks  = 10,
  n_resp    = 4000,
  no_choice = TRUE,
  max_iter  = 50
)

cat("\n--- design columns ---\n"); print(names(design))
cat("\n--- design head ---\n"); print(utils::head(design, 8))

# ---------------------------------------------------------------------
# 3b. EXPORT the 10 unique blocks x 10 tasks for oTree (one row per task)
# ---------------------------------------------------------------------
# Keep one representative respondent per block, drop the no-choice alt, and
# pivot the two AI alternatives wide so each row is a full choice task.
attrs <- c("severity","risk_annual","benefit","competition")

# Identify the per-block question set (blocks repeat across respondents).
blk <- design %>%
  group_by(blockID) %>%
  filter(respID == min(respID)) %>%   # first respondent carrying each block
  ungroup() %>%
  filter(altID %in% c(1, 2)) %>%
  select(blockID, qID, altID, all_of(attrs))

a <- blk %>% filter(altID == 1) %>% select(-altID)
b <- blk %>% filter(altID == 2) %>% select(-altID)
names(a)[match(attrs, names(a))] <- paste0("a_", attrs)
names(b)[match(attrs, names(b))] <- paste0("b_", attrs)

tasks <- a %>%
  inner_join(b, by = c("blockID","qID")) %>%
  arrange(blockID, qID) %>%
  rename(block = blockID, task = qID)

dir.create(dirname(OUT_CSV), showWarnings = FALSE, recursive = TRUE)
write.csv(tasks, OUT_CSV, row.names = FALSE)
cat("\nWROTE", nrow(tasks), "tasks across",
    length(unique(tasks$block)), "blocks ->", OUT_CSV, "\n")

# ---------------------------------------------------------------------
# 4-7. Identification (simulate -> estimate -> recover p*) — unchanged logic,
#      now with severity in the model. Wrapped so export never blocks on it.
# ---------------------------------------------------------------------
try({
  library(logitr)
  risk_to_logp <- c("1 in 100"=-2, "1 in 1,000"=-3, "1 in 10,000"=-4,
                    "1 in 100,000"=-5, "1 in 1,000,000"=-6)
  sev_to_logn  <- c("A single death"=0,
                    "100 deaths or $1B damage"=2,
                    "1,000,000 deaths or $100B damage"=6,
                    "~800,000,000 deaths (10% of humanity)"=8.9)  # log10(deaths)

  sim <- cbc_choices(design, priors = priors)
  dat <- sim %>%
    mutate(logp  = risk_to_logp[as.character(risk_annual)],
           logn  = sev_to_logn[as.character(severity)])

  m <- logitr(
    data    = dat,
    outcome = "choice",
    obsID   = "obsID",
    pars    = c("logp","logn","benefit","competition"),
    randPars = c(logp = "n"),
    numMultiStarts = 5
  )
  print(summary(m))
}, silent = FALSE)

# Report p* as a DISTRIBUTION with credible intervals by severity tier and
# benefit scenario — never a single point (see protocol v10 §3.2 / Appendix B).
# =====================================================================
