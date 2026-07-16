# =====================================================================
# SARA USA 2026 — shared DCE model utilities
# One place for the attribute coding, the registered estimation
# specification, choice simulation, block export, and the D-error metric.
# Used by sara_dce_design.R (one-shot design + identification sim) and
# dce_sequential.R (the pre-registered wave/checkpoint loop).
# =====================================================================

suppressMessages(library(dplyr))

# ── Level codings (must match the profiles in sara_dce_design.R) ──────
RISK_TO_LOGP <- c("1 in 100" = -2, "1 in 1,000" = -3, "1 in 10,000" = -4,
                  "1 in 100,000" = -5, "1 in 1,000,000" = -6)
# The extinction tier uses the FRI/XPT definition (global population falls
# below 5,000), matching the m4c_extinction ladder rung and the Method-4
# forecaster anchors.
EXT_LEVEL    <- "Human extinction (fewer than 5,000 people survive)"
SEV_TO_LOGN  <- c("A single death" = 0,
                  "100 deaths" = 2,
                  "1,000,000 deaths" = 6,
                  "~800,000,000 deaths (10% of humanity)" = 8.9,
                  "Human extinction (fewer than 5,000 people survive)" = 9.9)  # log10 deaths

# The registered estimation parameters (PREREGISTRATION.md §4.2):
# log annual probability (random normal), log severity, an extinction
# indicator (`ext` — the discontinuity beyond the log-death slope at the
# FRI/XPT extinction tier; Schubert et al.'s uniquely-bad test), benefit
# and competition dummies, opt-out constant.
MAIN_PARS <- c("logp", "logn", "ext", "ben_major", "ben_transf",
               "comp_pace", "comp_lead", "no_choice")

# ── Coding ────────────────────────────────────────────────────────────
# Turn a long design/choice frame with categorical columns (severity,
# risk_annual, benefit, competition; NA on the opt-out row) into the model
# matrix columns. Opt-out rows get all-zero attributes + no_choice = 1.
dce_code_rows <- function(df) {
  no_choice <- if ("no_choice" %in% names(df)) {
    as.integer(df$no_choice != 0)
  } else {
    as.integer(is.na(df$severity) | !(df$altID %in% c(1, 2)))
  }
  df$no_choice  <- no_choice
  df$logp       <- ifelse(no_choice == 1, 0, unname(RISK_TO_LOGP[as.character(df$risk_annual)]))
  df$logn       <- ifelse(no_choice == 1, 0, unname(SEV_TO_LOGN[as.character(df$severity)]))
  df$ext        <- ifelse(no_choice == 1, 0, as.integer(df$severity == EXT_LEVEL))
  df$ben_major  <- ifelse(no_choice == 1, 0, as.integer(df$benefit == "Major"))
  df$ben_transf <- ifelse(no_choice == 1, 0, as.integer(df$benefit == "Transformative"))
  df$comp_pace  <- ifelse(no_choice == 1, 0, as.integer(df$competition == "The US keeps pace"))
  df$comp_lead  <- ifelse(no_choice == 1, 0, as.integer(df$competition == "The US is ahead"))
  bad <- is.na(df$logp) | is.na(df$logn)
  if (any(bad)) stop("dce_code_rows: unmapped attribute levels in rows ",
                     paste(head(which(bad)), collapse = ", "))
  df
}

# Code a cbcTools design (adds obsID if absent).
dce_code_design <- function(design) {
  df <- as.data.frame(design)
  if (!"obsID" %in% names(df)) {
    df$obsID <- as.integer(factor(paste(df$respID, df$qID)))
  }
  dce_code_rows(df)
}

# ── Choice simulation from a known mixed logit ────────────────────────
# b: named vector over MAIN_PARS; sd_logp: SD of the respondent-normal
# risk slope. Adds a `choice` column (1 = chosen row within each obsID).
dce_simulate_choices <- function(dat, b, sd_logp = 0) {
  stopifnot(all(MAIN_PARS %in% names(b)), all(MAIN_PARS %in% names(dat)))
  resp <- unique(dat$respID)
  logp_i <- stats::setNames(stats::rnorm(length(resp), b[["logp"]], sd_logp), resp)
  X <- as.matrix(dat[, setdiff(MAIN_PARS, "logp")])
  V <- X %*% b[setdiff(MAIN_PARS, "logp")] +
    dat$logp * logp_i[as.character(dat$respID)]
  eps <- -log(-log(stats::runif(nrow(dat))))            # Gumbel
  dat$U <- as.numeric(V) + eps
  dat %>%
    group_by(obsID) %>%
    mutate(choice = as.integer(U == max(U))) %>%
    ungroup() %>%
    select(-U) %>%
    as.data.frame()
}

# ── The registered estimator ──────────────────────────────────────────
# numCores = 1: logitr's forked multistart workers crash on macOS at the
# full N=4,000 (fork + multithreaded BLAS); single-core is robust and the
# estimates are identical (starting points are drawn from R's RNG before
# the workers fork, so core count never changes the result).
dce_estimate <- function(dat, numMultiStarts = 5, numCores = 1) {
  logitr::logitr(
    data    = dat,
    outcome = "choice",
    obsID   = "obsID",
    panelID = "respID",
    pars    = MAIN_PARS,
    randPars = c(logp = "n"),
    numMultiStarts = numMultiStarts,
    numCores = numCores
  )
}

# ── D-error at a coefficient vector (design comparison metric) ────────
# Local D-error of the MNL information matrix evaluated at beta over ONE
# copy of each block's estimation tasks (the metric is invariant to
# replicating blocks across respondents). Lower is better. This is the
# deterministic adopt-if-better criterion in dce_sequential.R; it
# approximates the Bayesian D-error at the posterior mean.
dce_d_error <- function(coded_tasks, beta) {
  stopifnot(all(MAIN_PARS %in% names(coded_tasks)))
  X_all <- as.matrix(coded_tasks[, MAIN_PARS])
  K <- length(MAIN_PARS)
  info <- matrix(0, K, K)
  for (ob in split(seq_len(nrow(coded_tasks)), coded_tasks$obsID)) {
    X <- X_all[ob, , drop = FALSE]
    p <- exp(X %*% beta[MAIN_PARS]); p <- as.numeric(p / sum(p))
    xbar <- colSums(X * p)
    info <- info + t(X * p) %*% X - outer(xbar, xbar)
  }
  det(info)^(-1 / K)
}

# ── Export a cbcTools design as the oTree blocks CSV ──────────────────
# 8 D-efficient tasks per block + task 9 dominated pair (dominant side
# alternates by block) + task 10 = exact repeat of task 2. Mirrors
# sara_dce_design.R v13; see protocol Appendix B.
DOM_BEST  <- c(severity = "A single death",  risk_annual = "1 in 1,000,000",
               benefit  = "Transformative",  competition = "The US is ahead")
DOM_WORST <- c(severity = "Human extinction (fewer than 5,000 people survive)",
               risk_annual = "1 in 100",
               benefit  = "Modest",          competition = "Other countries are ahead")

dce_export_blocks <- function(design, out_csv) {
  attrs <- c("severity", "risk_annual", "benefit", "competition")
  blk <- as.data.frame(design) %>%
    group_by(blockID) %>%
    filter(respID == min(respID)) %>%
    ungroup() %>%
    filter(altID %in% c(1, 2)) %>%
    select(blockID, qID, altID, all_of(attrs))
  a <- blk %>% filter(altID == 1) %>% select(-altID)
  b <- blk %>% filter(altID == 2) %>% select(-altID)
  names(a)[match(attrs, names(a))] <- paste0("a_", attrs)
  names(b)[match(attrs, names(b))] <- paste0("b_", attrs)
  tasks <- a %>%
    inner_join(b, by = c("blockID", "qID")) %>%
    arrange(blockID, qID) %>%
    rename(block = blockID, task = qID) %>%
    mutate(task_type = "defficient")
  dominated <- lapply(sort(unique(tasks$block)), function(bk) {
    a_side <- if (bk %% 2 == 1) DOM_BEST else DOM_WORST
    b_side <- if (bk %% 2 == 1) DOM_WORST else DOM_BEST
    data.frame(block = bk, task = 9L,
               a_severity = a_side[["severity"]], a_risk_annual = a_side[["risk_annual"]],
               a_benefit = a_side[["benefit"]],   a_competition = a_side[["competition"]],
               b_severity = b_side[["severity"]], b_risk_annual = b_side[["risk_annual"]],
               b_benefit = b_side[["benefit"]],   b_competition = b_side[["competition"]],
               task_type = "dominated")
  }) %>% bind_rows()
  repeat2 <- tasks %>% filter(task == 2) %>% mutate(task = 10L, task_type = "repeat_of_2")
  tasks <- bind_rows(tasks, dominated, repeat2) %>% arrange(block, task)
  dir.create(dirname(out_csv), showWarnings = FALSE, recursive = TRUE)
  write.csv(tasks, out_csv, row.names = FALSE)
  tasks
}

# ── Rebuild long-format choice data from oTree exports ────────────────
# `responses`: data.frame with one row per participant: dce_block (1-10)
# and dce_1..dce_10 (1 = Option A, 2 = Option B, 3 = opt-out), plus a
# participant identifier column `code`. `blocks_csv`: the dce_blocks.csv
# THAT WAVE was fielded with. Estimation tasks only (task_type ==
# "defficient"); tasks 9-10 are quality checks, never estimated.
dce_build_long <- function(responses, blocks_csv) {
  blocks <- read.csv(blocks_csv, check.names = FALSE)
  est <- blocks %>% filter(task_type == "defficient")
  rows <- list()
  for (i in seq_len(nrow(responses))) {
    r <- responses[i, ]
    bt <- est %>% filter(block == r$dce_block)
    for (j in seq_len(nrow(bt))) {
      t <- bt[j, ]
      ans <- r[[paste0("dce_", t$task)]]
      # 0 = "Prefer not to answer" (the survey's universal opt-out); an
      # opted-out task has no chosen alternative, so drop it here.
      if (is.na(ans) || !ans %in% 1:3) next
      obs <- paste(r$code, t$task, sep = "|")
      mk <- function(alt, prefix) data.frame(
        respID = r$code, obsID = obs, altID = alt,
        severity = t[[paste0(prefix, "_severity")]],
        risk_annual = t[[paste0(prefix, "_risk_annual")]],
        benefit = t[[paste0(prefix, "_benefit")]],
        competition = t[[paste0(prefix, "_competition")]],
        choice = as.integer(ans == alt))
      rows[[length(rows) + 1]] <- mk(1, "a")
      rows[[length(rows) + 1]] <- mk(2, "b")
      rows[[length(rows) + 1]] <- data.frame(
        respID = r$code, obsID = obs, altID = 3,
        severity = NA, risk_annual = NA, benefit = NA, competition = NA,
        choice = as.integer(ans == 3))
    }
  }
  dat <- bind_rows(rows)
  dat$obsID <- as.integer(factor(dat$obsID))
  dat <- dce_code_rows(dat)
  # logitr coerces panelID to numeric, and oTree participant codes are
  # strings — map them to integers for estimation, keeping the original
  # code in `code` for joins back to participant-level flags.
  dat$code <- dat$respID
  dat$respID <- as.integer(factor(dat$respID, levels = unique(dat$respID)))
  dat
}

# ── Coded long template from a wide blocks table ──────────────────────
# One coded row-set (A, B, opt-out) per estimation task of each block, one
# copy per block. Used for the D-error metric and to replicate tasks per
# synthetic respondent in simulations.
dce_blocks_template <- function(tasks_df) {
  est <- tasks_df %>% filter(task_type == "defficient")
  side <- function(alt, prefix) data.frame(
    block = est$block, task = est$task, altID = alt,
    severity = est[[paste0(prefix, "_severity")]],
    risk_annual = est[[paste0(prefix, "_risk_annual")]],
    benefit = est[[paste0(prefix, "_benefit")]],
    competition = est[[paste0(prefix, "_competition")]])
  optout <- data.frame(block = est$block, task = est$task, altID = 3,
                       severity = NA, risk_annual = NA,
                       benefit = NA, competition = NA)
  df <- bind_rows(side(1, "a"), side(2, "b"), optout) %>%
    arrange(block, task, altID)
  df$obsID <- as.integer(factor(paste(df$block, df$task)))
  dce_code_rows(df)
}

# Replicate a coded template for n synthetic respondents (blocks assigned
# round-robin), with unique respID/obsID — ready for dce_simulate_choices.
dce_replicate_template <- function(template, n_resp, resp_offset = 0) {
  blocks <- sort(unique(template$block))
  out <- lapply(seq_len(n_resp), function(i) {
    df <- template[template$block == blocks[((i - 1) %% length(blocks)) + 1], ]
    df$respID <- resp_offset + i
    df$obsID <- paste(df$respID, df$task, sep = "|")
    df
  })
  df <- bind_rows(out)
  df$obsID <- as.integer(factor(df$obsID))
  df
}

# ── Map estimated continuous coefficients back to cbc_priors form ─────
# The design generator wants per-level part-worths vs each reference
# level; the estimator is linear in logp/logn. Deterministic mapping.
dce_coefs_to_priors <- function(est, profiles) {
  # Per-level severity part-worths: the log-death slope, plus the extinction
  # discontinuity on the extinction tier only.
  sev <- est[["logn"]] * (SEV_TO_LOGN[-1] - SEV_TO_LOGN[1]) +
    est[["ext"]] * as.integer(names(SEV_TO_LOGN)[-1] == EXT_LEVEL)
  cbcTools::cbc_priors(
    profiles    = profiles,
    severity    = unname(sev),
    risk_annual = unname(est[["logp"]] * (RISK_TO_LOGP[-1] - RISK_TO_LOGP[1])),
    benefit     = c(est[["ben_major"]], est[["ben_transf"]]),
    competition = c(est[["comp_pace"]], est[["comp_lead"]]),
    no_choice   = est[["no_choice"]]
  )
}
