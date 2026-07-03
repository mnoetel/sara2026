# =====================================================================
# SARA USA 2026 — helpers for the pre-registered report (report.Rmd)
# Reads the instrument spec (single source of truth) for labels/scales,
# parses the oTree wide export, derives the registered flags, and holds
# small statistical utilities. Keep analysis logic IN the report where a
# reviewer will read it; keep plumbing here.
# =====================================================================

suppressMessages({
  library(dplyr)
  library(tidyr)
  library(yaml)
})

# ── Instrument spec (labels come from sara_usa.md, never hardcoded) ───
load_instrument <- function(md_path) {
  txt <- paste(readLines(md_path, warn = FALSE, encoding = "UTF-8"),
               collapse = "\n")
  m <- regmatches(txt, regexpr("(?s)```ya?ml\\n.*?\\n```", txt, perl = TRUE))
  stopifnot(length(m) == 1)
  body <- sub("^```ya?ml\\n", "", m)
  body <- sub("\\n```$", "", body)
  yaml.load(body)
}

spec_items <- function(spec) {
  out <- list()
  for (p in spec$pages) for (it in p$items %||% list()) out[[it$id]] <- it
  out
}
`%||%` <- function(a, b) if (is.null(a)) b else a

# Labels for an item: its own options, or its scale's labels.
item_labels <- function(spec, items, id) {
  it <- items[[id]]
  if (!is.null(it$options)) return(unlist(it$options))
  unlist(spec$scales[[it$scale]]$labels)
}

# Map 1-based codes to labels; 0 (opt-out) and NA -> NA.
code_to_label <- function(x, labels) {
  x <- suppressWarnings(as.integer(x))
  ifelse(!is.na(x) & x >= 1 & x <= length(labels), labels[pmax(x, 1)], NA)
}

# ── oTree wide export ────────────────────────────────────────────────
read_wide <- function(path) {
  d <- read.csv(path, check.names = FALSE, colClasses = "character")
  names(d) <- sub("^sara\\.1\\.player\\.", "", names(d))
  names(d) <- sub("^sara\\.1\\.", "", names(d))
  d
}

# integer-ify a player field: "" -> NA, 0 (choice opt-out) / -1 (number
# opt-out) -> NA by default (keep_optout = TRUE keeps the sentinel).
num <- function(x, keep_optout = FALSE) {
  v <- suppressWarnings(as.integer(x))
  if (!keep_optout) v[v %in% c(0L, -1L)] <- NA
  v
}

# ── Berlin Numeracy quartile from the adaptive path (spec-driven) ─────
# Routing per Cokely et al. (2012): the spec's next_if_correct /
# next_if_incorrect targets end at quartile_1..quartile_4.
bnt_quartile <- function(d, items) {
  n <- nrow(d)
  out <- rep(NA_integer_, n)
  root <- "bnt_choir"
  for (i in seq_len(n)) {
    cur <- root
    for (step in 1:4) {
      it <- items[[cur]]
      ans <- num(d[[cur]][i], keep_optout = TRUE)
      if (is.na(ans)) break
      nxt <- if (!is.na(ans) && ans == it$correct_answer) it$next_if_correct
             else it$next_if_incorrect
      if (grepl("^quartile_", nxt)) {
        out[i] <- as.integer(sub("quartile_", "", nxt))
        break
      }
      cur <- nxt
    }
  }
  out
}

# ── Registered data-quality flags (PREREGISTRATION.md §3) ─────────────
add_flags <- function(d, blocks) {
  # §3.2 dominance: task 9 is the dominated pair; the dominated SIDE
  # alternates by block (odd: B dominated, even: A) — from the committed
  # design, not assumed: identify the dominated side per block.
  dom <- blocks %>%
    filter(task_type == "dominated") %>%
    mutate(a_is_best = a_risk_annual == "1 in 1,000,000") %>%
    select(block, a_is_best)
  d$dce_block_i <- num(d$dce_block, keep_optout = TRUE)
  d <- d %>% left_join(dom, by = c("dce_block_i" = "block"))
  d9 <- num(d$dce_9)
  d$flag_dominated <- !is.na(d9) & d9 %in% 1:2 &
    ((d$a_is_best & d9 == 2) | (!d$a_is_best & d9 == 1))
  # choosing the opt-out (3) is NOT a failure (registered rule)

  # §3.3 stability: task 10 exactly repeats task 2
  d2 <- num(d$dce_2); d10 <- num(d$dce_10)
  d$flag_unstable <- !is.na(d2) & !is.na(d10) & d2 %in% 1:3 & d10 %in% 1:3 &
    d2 != d10

  # §3.4 sanity anchor: AI less strict than Everest
  ev <- num(d$m3_sanity_everest)
  d$flag_everest <- !is.na(ev) & ev %in% c(4, 5)

  # §3.5 acquiescence: top-2-box BOTH the pro-ban and the anti-ban item
  sup <- num(d$muskan_support); anti <- num(d$muskan_support_anti)
  d$flag_acquiescer <- !is.na(sup) & !is.na(anti) &
    sup %in% 1:2 & anti %in% 1:2
  d
}

# §3.6 speed flag: briefing-page dwell below the pilot 5th percentile.
briefing_dwell <- function(pagetimes_path) {
  pt <- read.csv(pagetimes_path, check.names = FALSE)
  pt <- pt %>%
    arrange(participant_code, page_index) %>%
    group_by(participant_code) %>%
    mutate(dwell = epoch_time_completed - lag(epoch_time_completed)) %>%
    ungroup()
  pt %>%
    filter(page_name == "SuperintelligenceBriefPage") %>%
    select(participant_code, session_code, brief_dwell = dwell)
}

# ── Brand theme (MIT FutureTech / AI Risk Initiative) ─────────────────
# Palette from the 2026 brand doc: Figtree, #A32035 primary, #666666 grey.
# Plot structure mirrors the SARA 2025 technical report (theme matched to
# the report CSS in report_theme.css).
SARA_RED      <- "#A32035"
SARA_RED_DARK <- "#5E1220"
SARA_INK      <- "#1F1F1F"
SARA_GREY     <- "#666666"
SARA_GRID     <- "#E2DDDC"

theme_sara <- function(base_size = 11) {
  ggplot2::theme_minimal(base_size = base_size) +
    ggplot2::theme(
      plot.title = ggplot2::element_text(colour = SARA_INK, face = "bold",
                                         size = ggplot2::rel(1.05)),
      plot.subtitle = ggplot2::element_text(colour = SARA_GREY,
                                            size = ggplot2::rel(0.85)),
      plot.title.position = "plot",
      axis.title = ggplot2::element_text(colour = SARA_GREY,
                                         size = ggplot2::rel(0.9)),
      axis.text = ggplot2::element_text(colour = SARA_INK),
      legend.title = ggplot2::element_text(colour = SARA_GREY),
      panel.grid.minor = ggplot2::element_blank(),
      panel.grid.major = ggplot2::element_line(colour = SARA_GRID),
      strip.text = ggplot2::element_text(colour = SARA_RED, face = "bold"))
}

# Sequential brand ramp (light tint -> brand red -> near-black) for ordinal
# scales, and a small discrete set for categorical ones.
sara_seq <- function(n) grDevices::colorRampPalette(
  c("#EFDCDF", SARA_RED, "#2E0A12"))(n)
SARA_DISCRETE <- c(SARA_RED, "#666666", "#2B2B2B", "#C98490", "#9E9E9E")

# ── Small utilities ──────────────────────────────────────────────────
fmt_1inN <- function(p) {
  # element-wise formatting (format() on a vector pads to a common width)
  vapply(p, function(x) {
    if (!is.finite(x) || x <= 0) return("-")
    if (x >= 1) return("any chance (>= 1)")
    paste0("1 in ", formatC(signif(1 / x, 2), format = "fg", big.mark = ","))
  }, character(1))
}

ordinal_median <- function(x) {           # median category, ties -> lower
  x <- x[!is.na(x)]
  if (!length(x)) return(NA_integer_)
  as.integer(quantile(x, 0.5, type = 1))
}

prop_ci <- function(k, n) {               # Wilson 95% CI
  if (n == 0) return(c(NA, NA, NA))
  z <- 1.96; p <- k / n
  den <- 1 + z^2 / n
  ctr <- (p + z^2 / (2 * n)) / den
  hw <- z * sqrt(p * (1 - p) / n + z^2 / (4 * n^2)) / den
  c(p, ctr - hw, ctr + hw)
}

pct <- function(x, digits = 1) sprintf(paste0("%.", digits, "f%%"), 100 * x)

# Raking (IPF) to the two Pew benchmark marginals (§7 sensitivity).
rake_two_margins <- function(x1, x2, target1, target2, iter = 50) {
  ok <- !is.na(x1) & !is.na(x2)
  w <- rep(1, length(x1)); w[!ok] <- NA
  for (k in seq_len(iter)) {
    for (m in 1:2) {
      x <- if (m == 1) x1 else x2
      tgt <- if (m == 1) target1 else target2
      cur <- tapply(w[ok], x[ok], sum) / sum(w[ok])
      adj <- tgt[as.character(sort(unique(x[ok])))] / cur
      w[ok] <- w[ok] * adj[as.character(x[ok])]
    }
  }
  w / mean(w, na.rm = TRUE)
}

weighted_share <- function(x, w, level) {
  ok <- !is.na(x) & !is.na(w)
  sum(w[ok] * (x[ok] %in% level)) / sum(w[ok])
}
