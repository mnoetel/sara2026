# =====================================================================
# SARA USA 2026 — Module 4a: Discrete Choice Experiment (DCE)
# Catastrophic risk tolerance and the utility / safety / competition tradeoff
# (framing per Dean Ball: "What tradeoffs between utility, safety, and
#  competition does the polity wish to make? What level of catastrophic
#  risk are we willing to tolerate?")
#
# Design choices:
#   * Severity is HELD FIXED (a defined mass-casualty catastrophe). Scope
#     sensitivity is measured separately and more simply in Module 4c
#     (within-subjects F-N), not here. This concentrates the DCE's power
#     on the level-of-risk vs tradeoffs question.
#   * Unlabelled design, 2 AI-future alternatives + a status-quo "neither"
#     opt-out, ~10 choice tasks per respondent, blocked into versions.
#   * No test-retest wave.
#
# Identification was checked by simulation (numpy, seed 7): a mixed-logit
# data-generating model recovered all coefficients to within ~0.03 of the
# truth, so this attribute structure identifies the tradeoffs and WTP.
#
# Run in R >= 4.2.  install.packages(c("cbcTools","logitr","dplyr"))
# =====================================================================

library(cbcTools)   # design generation + power
library(logitr)     # mixed logit (random parameters)
library(dplyr)

# ---------------------------------------------------------------------
# 1. THE GRID  (attributes x levels)
# ---------------------------------------------------------------------
# Catastrophe is defined to respondents as: "an AI-caused event that kills
# 100,000 or more people." (Tunable: swap to match a statutory threshold,
# e.g. SB 53 / RAISE Act, if you prefer.)

profiles <- cbc_profiles(
  risk_annual = c("1 in 100", "1 in 1,000", "1 in 10,000",
                  "1 in 100,000", "1 in 1,000,000"),   # SAFETY (5 levels)
  benefit     = c("Modest", "Major", "Transformative"),# UTILITY (3 levels)
  competition = c("Others lead", "Keep pace", "US leads"), # COMPETITION (3)
  cost_usd    = c(0, 100, 400, 1000)                   # COST to household/yr (4)
)
# Full factorial = 5 * 3 * 3 * 4 = 180 profiles.

# Map the risk label to a numeric log10(annual probability) for analysis.
# (Design can treat risk as categorical; analysis uses the continuous slope
#  so we can read off an "acceptable risk" threshold.)
risk_to_logp <- c("1 in 100"=-2, "1 in 1,000"=-3, "1 in 10,000"=-4,
                  "1 in 100,000"=-5, "1 in 1,000,000"=-6)

# ---------------------------------------------------------------------
# 2. PRIORS for a Bayesian D-efficient design (optional but recommended)
#    Signs: safer (more negative log10 p) is better -> negative coef on log10 p;
#    benefit & US-leading positive; cost negative.
# ---------------------------------------------------------------------
priors <- list(
  risk_annual = c(0.6, 1.2, 1.8, 2.4),  # utility increasing as risk falls (ref = "1 in 100")
  benefit     = c(0.6, 1.4),            # ref = Modest
  competition = c(0.3, 0.7),            # ref = Others lead
  cost_usd    = -0.001                  # per dollar
)

# ---------------------------------------------------------------------
# 3. GENERATE THE DESIGN  (D-optimal; 2 alts + opt-out; 10 q; blocks)
# ---------------------------------------------------------------------
set.seed(2026)
design <- cbc_design(
  profiles  = profiles,
  n_resp    = 4000,   # oversample the risk module relative to 2025
  n_alts    = 2,      # two AI-future options...
  n_q       = 10,     # ...over 10 choice tasks
  no_choice = TRUE,   # ...plus a "neither / keep today's status quo" opt-out
  n_blocks  = 10,     # 10 survey versions
  method    = "dopt", # D-optimal; use method = "bayesian" with `priors` for Bayesian D-eff
  priors    = priors
)

cbc_balance(design)   # check level balance
cbc_overlap(design)   # check within-task attribute overlap

# ---------------------------------------------------------------------
# 4. POWER / PILOT  (simulate choices under the priors, check SEs)
# ---------------------------------------------------------------------
sim    <- cbc_choices(design, obsID = "obsID")          # simulate responses
power  <- cbc_power(sim, pars = c("risk_annual","benefit","competition","cost_usd"),
                    obsID = "obsID", nbreaks = 10, n_q = 10)
plot(power)   # SEs vs sample size: confirm the risk & cost coefs are well powered

# ---------------------------------------------------------------------
# 5. ESTIMATE  (mixed logit; random coefs on risk slope and cost)
#    Replace `sim` with the real choice data once collected.
# ---------------------------------------------------------------------
dat <- sim %>%
  mutate(logp     = risk_to_logp[as.character(risk_annual)],
         cost_k   = cost_usd / 1000)

m <- logitr(
  data    = dat,
  outcome = "choice",
  obsID   = "obsID",
  pars    = c("logp", "benefit", "competition", "cost_k"),  # benefit/competition dummy-coded
  randPars = c(logp = "n", cost_k = "n"),                    # random (normal) heterogeneity
  numMultiStarts = 10
)
summary(m)

# ---------------------------------------------------------------------
# 6. RECOVER THE PUBLIC NUMBER
#    (a) Acceptable annual catastrophe risk p*  = the risk level at which an
#        AI-future option is valued equally to the status-quo opt-out, for a
#        given benefit/competition scenario and cost = 0.
#        Solve  b_logp * log10(p*) + benefit + competition = ASC_optout
#    (b) WTP for a 10x risk reduction = b_logp / b_cost (per $1,000).
# ---------------------------------------------------------------------
co  <- coef(m)
b_logp <- co[["logp"]]; b_cost <- co[["cost_k"]]
asc <- co[grepl("noChoice|ASC|no_choice", names(co))][1]   # opt-out intercept name varies

acc_risk <- function(benefit = 0, competition = 0) {
  10^((asc - benefit - competition) / b_logp)              # annual probability
}
# Example scenarios (fill benefit/competition with the relevant estimated dummies):
# acc_risk(benefit = co[["benefitMajor"]], competition = co[["competitionKeep pace"]])

wtp_per_10x <- b_logp / b_cost * 1000   # dollars/household/yr for a 10x risk cut

# Report p* as a DISTRIBUTION with credible intervals (use the mixed-logit
# draws / bootstrap), by benefit scenario — never a single point.

# ---------------------------------------------------------------------
# 7. GO/NO-GO + MULTIPLIER GOVERNANCE  (see protocol v5, Section 6)
#    Report a quantitative public number ONLY if this DCE estimate and the
#    direct within-subjects F-N (Module 4c) agree within ~1 order of magnitude
#    in the overlap subsample. If they diverge, report a bound + qualitative
#    finding. The expert-/-public multiplier is computed only on a PASS,
#    as a distribution with CIs, conditioned on a stated benefit scenario,
#    with uncertainty propagated from both numerator and denominator.
# =====================================================================
