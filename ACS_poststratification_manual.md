# Getting the ACS data for MRP post-stratification

**Goal.** Build the *post-stratification frame*: the joint distribution of US
adults (18+) across the variables the survey weights on — **state × age × sex ×
education × household income** — so the fitted MRP model can be re-weighted up to
the population (and to each state). See protocol §5 and Appendix A.

**Key point.** MRP needs the **joint** distribution (one row per cell), which
only the ACS **PUMS microdata** gives. The familiar summary tables (B01001 age/sex,
B15003 education, B19001 income) are one-way *margins* — fine for raking, not for
MRP cells. Use PUMS.

**Vintage.** Use the **2024 ACS 1-year PUMS** (released 16 Oct 2025 — the latest).
Switch to **5-year** (`acs5`) if you want more stable small-state cells at the cost
of a larger, older-averaged file. (2025 1-year lands ~Sept 2026.)

---

## Route A — tidycensus + Census API (recommended; matches `acs_poststrat.R`)

1. **Get a free Census API key** (instant): <https://api.census.gov/data/key_signup.html>
   — enter name + email, click the activation link they email you.
2. **Install the packages** (in R):
   ```r
   install.packages(c("tidycensus", "dplyr"))
   ```
3. **Register the key once:**
   ```r
   tidycensus::census_api_key("YOUR_KEY_HERE", install = TRUE)
   readRenviron("~/.Renviron")   # or restart R
   ```
4. **Run the script:**
   ```r
   source("acs_poststrat.R")
   ```
   It pulls all states' person records, recodes to the survey's exact bins,
   sums `PWGTP`, and writes `poststrat_frame.csv` (one row per cell with `n` =
   weighted adults). The national 1-year file is ~3.3M records — expect a few
   minutes and a few hundred MB of RAM.

That CSV is the post-stratification frame. The bottom of the script sketches the
MRP step (`posterior_epred` over the frame, then weighted means overall and by
state).

---

## Route B — IPUMS USA (more control over recodes / harmonised variables)

Use this if you want IPUMS's harmonised variables or a custom extract.

1. Make a free account: <https://usa.ipums.org/usa/>.
2. Create an extract: select **ACS 2024 1-year**; add variables **AGE, SEX,
   EDUCD, HHINCOME, STATEFIP, PERWT**; submit and download the `.dat.gz` + DDI
   `.xml` codebook.
3. In R:
   ```r
   install.packages("ipumsr")
   library(ipumsr)
   d <- read_ipums_micro(read_ipums_ddi("usa_0001.xml"))
   # recode AGE/EDUCD/HHINCOME/STATEFIP into the survey bins, then
   # group_by(state, age, sex, education, income) |> summarise(n = sum(PERWT))
   ```
   (Same bin logic as `acs_poststrat.R`; EDUCD/HHINCOME codes differ from PUMS
   SCHL/HINCP, so map per the IPUMS codebook.)

---

## Route C — marginal tables only (if you rake instead of full MRP)

If you decide to **rake/post-stratify on margins** rather than full joint cells,
pull the one-way tables from <https://data.census.gov> (or `tidycensus::get_acs`):

- **B01001** — sex by age
- **B15003** — educational attainment (25+)
- **B19001** — household income
- by **state** (`geography = "state"`).

```r
tidycensus::get_acs(geography = "state", table = "B15003", year = 2024, survey = "acs1")
```

This is lighter but loses cross-classification; MRP with the PUMS joint frame
(Route A) is the protocol's method.

---

## Bin mapping (already implemented in `acs_poststrat.R`)

| Survey variable | PUMS var | Recode |
|---|---|---|
| Age | `AGEP` | 18–24 / 25–34 / 35–44 / 45–54 / 55–64 / 65–74 / 75 or older |
| Sex | `SEX` | 1→Male, 2→Female |
| Education | `SCHL` | ≤15 <HS · 16–17 HS grad · 18–19 some college · 20 associate · 21 bachelor's · 22–24 grad/professional |
| Household income | `HINCP` | the nine B19001 brackets, Under $15,000 … $200,000 or more |
| State | `ST` | FIPS → state name (incl. DC) |

Notes:
- **Gender:** ACS records only Male/Female, so the survey's non-binary / prefer-not-to-say
  responses are allocated for weighting (protocol's stated approach).
- **Income** is household-level; each adult is assigned their household's income.
- **State reporting threshold:** only publish per-state estimates where the survey's
  effective n clears the pre-registered threshold (protocol §5 / Appendix A).
