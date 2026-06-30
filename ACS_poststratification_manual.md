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

---

## Survey ↔ ACS alignment for MRP (verified against ACS 2024)

For MRP, **every survey demographic must map onto an ACS category** so a population
cell exists for it. Checked against the live ACS 2024 tables and PUMS codings:

| Survey variable | Survey categories | ACS source | Aligns? |
|---|---|---|---|
| **Age** | 7 bins, 18–24 … 75+ | PUMS `AGEP` (continuous); B01001 5-yr groups | ✅ exact |
| **Sex / gender** | Male / Female / non-binary / prefer-not-to-say | `SEX`, B01001: **Male / Female only** | ⚠️ partial |
| **Education** | 6 categories | `SCHL`; B15003 (**25+ only**) | ✅ via PUMS |
| **Household income** | 9 brackets | `HINCP`; B19001 | ✅ exact |
| **State** | 50 + DC | `ST` / state FIPS | ✅ exact |

**Age — ✅.** The survey's bins aggregate cleanly from B01001's 5-year groups
(18–24 = 18–19 + 20 + 21 + 22–24; 25–34 = 25–29 + 30–34; … 75+ = 75–79 + 80–84 + 85+),
and PUMS `AGEP` is continuous so it bins to the survey boundaries exactly. No change.

**Sex / gender — ⚠️ the one real mismatch.** ACS records **only Male and Female** —
there is no population count for "In another way / non-binary" or "Prefer not to say,"
so those responses cannot form a post-stratification cell. Keep the inclusive question
(good practice), but for the MRP *sex* variable you must decide how to handle the others.
Pre-register one of:
1. **Allocate** non-binary / PNS to Male/Female (e.g. proportional, or by another
   covariate) — the protocol's current stated approach;
2. **Drop** them from the sex margin, post-stratify the rest, and report the excluded
   group descriptively;
3. **Sensitivity analysis** comparing (1) and (2).
This is a values/measurement call, not a coding fix.

**Education — ✅ via PUMS, with a caveat.** The 6 survey categories collapse cleanly
from B15003's 25 detailed levels (<HS = everything below "Regular high school diploma";
HS grad = Regular diploma **+** GED; some college = <1 yr **+** 1+ yr no degree;
associate; bachelor; grad/professional = Master's **+** Professional **+** Doctorate).
**Caveat:** the *summary table* B15003 covers **age 25+ only** — it has no education for
18–24-year-olds. So if you rake on summary tables you cannot post-stratify education for
the 18–24 cell. **Use the PUMS frame** (`SCHL` is present for all ages), which the
scripts here do. No change needed.

**Household income — ✅.** The 9 survey brackets aggregate cleanly from B19001's 16
(Under $15,000 = <$10k + $10–15k; $15–25k = $15–20k + $20–25k; … $100–150k = $100–125k +
$125–150k; $150–200k and $200k+ map 1:1). B19001 is **household** income, matching the
survey wording. Group-quarters persons (PUMS `HINCP` sentinel **−60000**, ~4% of adults:
dorms, military, nursing homes) have no household income and are excluded from the
household-income frame. No change.

**State — ✅.** All 50 + DC, exact.

**Bottom line:** age, education, income and state were designed to ACS boundaries and
need **no survey changes**. The only open decision is **gender handling** for the
post-stratification step — pick an approach and pre-register it.

Notes:
- **Income** is household-level; each adult is assigned their household's income.
- **State reporting threshold:** only publish per-state estimates where the survey's
  effective n clears the pre-registered threshold (protocol §5 / Appendix A).
