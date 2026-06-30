# =====================================================================
# SARA USA 2026 — ACS post-stratification frame for MRP
# Builds the joint population distribution of US adults (18+) by
#   state x age x sex x education x household income,
# in the SAME bins the survey collects, so it can be joined to the
# fitted MRP model to produce population- and state-level estimates.
#
# Source: ACS 2024 1-year PUMS (person records), weighted by PWGTP.
# Needs a free Census API key — see ACS_poststratification_manual.md.
#
#   install.packages(c("tidycensus","dplyr"))
#   tidycensus::census_api_key("YOUR_KEY", install = TRUE)   # once
# =====================================================================

library(tidycensus)
library(dplyr)

YEAR    <- 2024          # latest ACS 1-year PUMS (released 2025-10-16)
SURVEY  <- "acs1"        # use "acs5" for more cells / small-state stability
OUT_CSV <- "/Users/michaelnoetel/git/sara2026/poststrat_frame.csv"

# ---------------------------------------------------------------------
# 1. Pull person-level PUMS for all states + DC.
#    get_pums() always also returns ST (FIPS), PWGTP, SERIALNO, SPORDER.
#    AGEP=age, SEX, SCHL=educational attainment, HINCP=household income.
# ---------------------------------------------------------------------
pums <- get_pums(
  variables = c("AGEP", "SEX", "SCHL", "HINCP"),
  state     = "all",
  survey    = SURVEY,
  year      = YEAR,
  recode    = FALSE
)

# ---------------------------------------------------------------------
# 2. Recode to the survey's exact categories.
# ---------------------------------------------------------------------
state_lookup <- tidycensus::fips_codes %>%
  distinct(state_code, state_name)

frame <- pums %>%
  mutate(AGEP = as.integer(AGEP), SCHL = as.integer(SCHL),
         HINCP = suppressWarnings(as.numeric(HINCP))) %>%
  filter(AGEP >= 18) %>%                                  # adults only
  mutate(
    age = cut(AGEP,
              breaks = c(18, 25, 35, 45, 55, 65, 75, Inf), right = FALSE,
              labels = c("18–24","25–34","35–44","45–54",
                         "55–64","65–74","75 or older")),
    sex = if_else(SEX == 1, "Male", "Female"),
    education = case_when(
      SCHL <= 15            ~ "Less than high school diploma",
      SCHL %in% c(16, 17)   ~ "High school graduate (or equivalent)",
      SCHL %in% c(18, 19)   ~ "Some college, no degree",
      SCHL == 20            ~ "Associate degree",
      SCHL == 21            ~ "Bachelor's degree",
      SCHL %in% c(22,23,24) ~ "Graduate or professional degree",
      TRUE                  ~ NA_character_),
    income = cut(HINCP,
              breaks = c(-Inf, 15000, 25000, 35000, 50000, 75000,
                         100000, 150000, 200000, Inf), right = FALSE,
              labels = c("Under $15,000","$15,000–$24,999","$25,000–$34,999",
                         "$35,000–$49,999","$50,000–$74,999","$75,000–$99,999",
                         "$100,000–$149,999","$150,000–$199,999","$200,000 or more"))
  ) %>%
  left_join(state_lookup, by = c("ST" = "state_code")) %>%
  rename(state = state_name) %>%
  filter(!is.na(age), !is.na(education), !is.na(income), !is.na(state))

# ---------------------------------------------------------------------
# 3. Collapse to post-stratification cells (sum of person weights = N).
# ---------------------------------------------------------------------
poststrat <- frame %>%
  group_by(state, age, sex, education, income) %>%
  summarise(n = sum(PWGTP), .groups = "drop") %>%
  arrange(state, age, sex, education, income)

write.csv(poststrat, OUT_CSV, row.names = FALSE)
cat("WROTE", nrow(poststrat), "poststrat cells covering",
    sum(poststrat$n), "weighted adults ->", OUT_CSV, "\n")

# ---------------------------------------------------------------------
# 4. MRP sketch (after fitting a multilevel model `fit` on survey data):
#    poststrat$pred <- posterior_epred(fit, newdata = poststrat) |> colMeans()
#    national  <- weighted.mean(poststrat$pred, poststrat$n)
#    by_state  <- poststrat |> group_by(state) |>
#                   summarise(est = weighted.mean(pred, n))
#    (Report state estimates only where the survey's effective n clears the
#     pre-registered threshold; see protocol Appendix A / §5.)
# =====================================================================
