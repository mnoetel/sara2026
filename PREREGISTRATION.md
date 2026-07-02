# SARA USA 2026 — Pre-registration (draft for OSF)

**Status: DRAFT — not yet registered.** This document is the analysis-plan
pre-registration for SARA USA 2026. It must be frozen and posted to OSF (or
AsPredicted) **before the pilot wave fields**; after registration, this file
records the registered content and the registration URL below, and any change
ships as a dated, labelled amendment.

- **Registration URL:** _(fill in at registration)_
- **Instrument (item text, scales, order):** `survey/sara_usa.md` at the
  registered git commit — the instrument is part of the registration.
  This document deliberately does not restate item text (repo golden rule).
- **Companion design documents:** `SARA USA — Survey Protocol v10.md`
  (rationale), `Muskan's Experiment/PROJECT_PLAN_superintelligence_study.md`
  (Rev 3, superintelligence module), `sara_dce_design.R` (DCE design
  algorithm), `build_poststrat.py` / `acs_poststrat.R` (MRP frame).

---

## 1. Study information

**Title.** Survey Assessing Risks from AI (SARA) USA 2026: how much
catastrophic risk from AI will the US public tolerate?

**Research questions.**
- **RQ1.** What is the highest annual probability of an AI catastrophe, by
  severity, that the US public will tolerate (stated F–N curve; Method 1)?
- **RQ2.** What tradeoffs between catastrophe severity, probability, societal
  benefit, and international competition is the public willing to make, and
  what acceptable-risk level p\* do those choices imply (DCE; Method 2)?
- **RQ3.** Relative to industries whose risk society already regulates, how
  strictly does the public want advanced AI regulated (Method 3)?
- **RQ4.** Are the risk levels named experts have publicly stated tolerable
  to the public (Method 4, reported by source)?
- **RQ5.** How much do the estimates move under a minimal balanced
  disclosure (the information-provision arm)?
- **RQ6 (superintelligence module).** Does the type of briefing context
  (elite cue vs substantive argument, for and against) shift support for a
  conditional superintelligence ban, and what is considered support after
  balanced exposure? (Hypotheses H2, H3, H5′, H6′ and Aim 2 in the Rev 3
  project plan — old H1/H4 are explicitly out of scope: their measures are
  not fielded.)

**This is primarily an estimation study.** Except for the superintelligence
module and the disclosure arm, the registered quantities are estimands with
uncertainty, not directional hypotheses.

---

## 2. Design and sampling

- **Platform/sample:** Prolific, US adults, target **N = 4,000** total
  (pilot ~500 + ~3 main waves of ~1,170), quota-balanced where Prolific
  allows. Opt-in panel: see §7 (panel-selection limitation and benchmarks).
- **Randomised arms (assigned balanced, in shuffled blocks seeded on the
  oTree session code):** balanced-disclosure half (`info_arm`), DCE block
  (1–10), superintelligence briefing (27 stimulus rows; 9 cells × 3
  versions).
- **Within-person randomisation (seeded on participant code):** severity-
  ladder page order; comparator-block item order (attention checks always
  last); option order on the comprehension check; on each Pew benchmark
  item, the two directional options are rotated with the neutral/"Not sure"
  option anchored last.
- **Adaptive elements:** Berlin Numeracy Test branching (validated adaptive
  format); the DCE's *population-level* sequential re-optimisation between
  waves (see §5 — mechanical, pre-registered algorithm with archival
  design reproducibility; each respondent's instrument is fixed).

---

## 3. Data quality: exclusions and flags (registered rules)

1. **Screen-out (exclusion).** A respondent who answers BOTH disguised
   attention checks (`m3_att_bioweapons`, `m3_att_nuclear`) with anything
   other than the instructed endpoint is screened out mid-survey and
   replaced; their partial data are not analysed (Prolific two-fail
   standard).
2. **DCE dominated-option flag.** Task 9 is a dominated pair. Choosing the
   dominated option is a failure; choosing the opt-out is NOT. Failure rate
   is reported; flagged respondents are retained in the primary analysis and
   dropped in a sensitivity re-estimate.
3. **DCE stability flag.** Task 10 exactly repeats task 2. Switching
   (task 2 ≠ task 10 choice) is reported as a stability rate; same
   retain-primary / drop-sensitivity handling as the dominance flag.
   Tasks 9–10 never enter estimation.
4. **Sanity-anchor flag.** `m3_sanity_everest`: answering that AI should be
   regulated less strictly than Everest climbing ("Less strict"/"Much less
   strict") is flagged and reported descriptively; not an exclusion.
5. **Acquiescence flag (superintelligence module).** Top-2-boxing both the
   pro-ban and the anti-ban DV items is flagged; reported, and dropped in a
   sensitivity analysis of module results only.
6. **Speed flag.** Briefing-page dwell time below a floor set in the pilot
   (registered at wave 1 lock as the pilot 5th percentile) is flagged;
   sensitivity analysis only.
7. **Scope-insensitivity is NOT an exclusion.** Flat ladder curves are a
   measured outcome (who is scope-insensitive), never grounds for dropping.

No other exclusions. Any additional cleaning is labelled exploratory.

---

## 4. Primary estimands and analyses

### 4.1 Method 1 — stated F–N curve
- Per-severity distributions of highest acceptable annual chance (ordinal;
  "Never allowed" reported as its own category, not coerced to a number).
- **Scope-sensitivity slope** per respondent: ordinal position change across
  the ladder; % flat (scope-insensitive) reported overall and by numeracy
  quartile (registered interaction: slope × Berlin Numeracy quartile).
- **First-rung sensitivity analysis (anchoring/demand check).** The ladder
  is one-item-per-page in per-participant random order, so each
  respondent's *first-seen* rung is a between-subjects experiment (~25% of
  the sample per severity, unanchored). Registered comparison: first-seen
  answers by severity vs the full within-person curves. Divergence beyond
  sampling error is reported, and the first-response (between-subjects)
  estimates are published alongside the within-person headline.
- **WTP (`m5_wtp`).** Distribution over the log-scale bands; "Don't know"
  reported separately. **Protest-zero handling:** $0 respondents receive
  `m5_wtp_zero_reason`; "not worth money" and "cannot afford" are genuine
  zeros (retained); "companies/government should pay" and "money would be
  wasted" are protest zeros — primary estimate retains all zeros, registered
  sensitivity excludes protest zeros; "another reason" is retained and
  reported.

### 4.2 Method 2 — DCE
- **Model:** mixed logit (`logitr`), fixed specification: log annual
  probability (random normal coefficient), log severity (deaths), benefit
  and competition as categorical, opt-out constant. Multistart, fixed seed.
  Estimation on tasks 1–8 only.
- **Estimand:** p\*(severity, benefit, competition) — the annual probability
  at which an AI-future option is indifferent to the status-quo opt-out —
  reported as a posterior distribution with credible intervals by scenario,
  never a point.
- **Wave robustness:** design-wave enters as a robustness control
  (sequential design is ignorable for the likelihood; see protocol
  Appendix B).

### 4.3 Method 3 — relative standards
- Per-comparator distributions (nuclear, aviation, dams); "Cannot compare"
  reported as frame rejection, not missing. No "N× safer" back-out headline.

### 4.4 Method 4 — named-source tolerability
- % Intolerable per source, reported **by source only** (LeCun, FRI
  superforecasters, FRI AI-domain experts, Amodei); no pooling across
  sources (their events and horizons differ). Within-person response
  patterns reported descriptively.

### 4.5 Disclosure arm
- Registered contrast: each Method 1–4 headline in disclosed vs undisclosed
  halves. Where they diverge, the **disclosed** estimate is the headline and
  the swing is reported as a primary finding.

### 4.6 Convergence go/no-go (registered decision rule)
A single quantitative public number is published only if the Method 1
(stated) and Method 2 (DCE) estimates agree within **one order of
magnitude** in the overlap of severity tiers, on the disclosed-arm data.
Otherwise: report a bound and qualitative findings. Any expert-vs-public
multiplier (e.g. "4,000× safer") is computed only on a pass, as a
distribution conditioned on a stated benefit scenario, and is always
labelled as researcher interpretation — never presented as a public-opinion
finding (protocol §5, §7.1 #16).

### 4.7 Superintelligence module (Rev 3 plan, §9)
- **Aim 2 headline:** top-2-box ban support in cell 5, with CI; bracketed by
  the other contested cells, control, and one-sided cells. Both DV items (fielded on
  separate consecutive pages) reported; continuous score = pro-ban − reverse(anti-ban), "Don't know"
  missing.
- **H2:** For/Against direction × route (C2) interaction on support.
  **H3:** For/Against main effects. Planned contrasts C1/C2 as in the plan.
- **Quasi-manipulation-check (registered pattern):** in one-sided cells,
  cue-reliance higher in elite cells; elaboration higher in substantive
  cells; elaboration compared across cells 6 vs 8 for material balance.
- **H5′/H6′ mediation:** exploratory (single-item mediators); bootstrap CIs,
  labelled exploratory in all reporting.
- Stimulus `version` checked for balance; modelled as a random effect if
  imbalanced.

---

## 5. DCE sequential design algorithm (registered, deterministic)

As specified in protocol Appendix B: waves (pilot ~500; ~3 × ~1,170); at
each wave boundary re-estimate the fixed mixed-logit specification on all
data (seeded multistart — estimation is seed-deterministic) and regenerate
the Bayesian D-efficient design (`cbcTools`) with the posterior means as the
new prior means; adopt only if the local D-error at the posterior mean
improves; design locked within waves and permanently after the final
checkpoint; hard cap N=4,000. The quality tasks (9–10) are never
re-optimised. Method 1 is held fully static.

**Reproducibility is archival for the design-search step:** cbcTools'
stochastic search is not bit-reproducible from a seed (verified 02 Jul
2026, single- and multi-core), so the registered guarantee is that (i) the
exact design fielded at every wave is committed to the repository
(`dce_blocks.csv`, `dce_blocks_wave<k>.csv`, `dce_sequential_log.csv`) and
(ii) estimation and the adopt-if-better rule are deterministic given those
artifacts. Re-running the search would propose a different, equally valid
candidate; it could not change what was fielded or how it is analysed.

**Pre-freeze checklist (status, 02 Jul 2026):**
- (a) **DONE** — `dce_sequential.R`: the checkpoint loop (estimate →
  regenerate → adopt-if-better local D-error at the posterior mean →
  archive per-wave design + log), sharing its coding/estimator/export
  with `sara_dce_design.R` via `dce_model_utils.R`. Note: the update rule
  uses the **posterior means** as the new cbcTools prior means (the
  D-error criterion is evaluated at the posterior mean); the earlier
  "mean and covariance" phrasing in protocol Appendix B is amended
  accordingly.
- (b) **DONE** — identification simulation repaired (choices simulated
  directly from the registered mixed-logit specification) and extended to
  the full sequential procedure. Pre-freeze run archived
  (`dce_sequential_sim_2026-07-02.log`): all four waves simulated, every
  checkpoint executed (each regenerated design improved the D-error and
  was adopted: 0.0754→0.0745, 0.0760→0.0752, 0.0748→0.0732), and final
  pooled recovery on N=4,000 was within 0.033 of truth on every fixed
  coefficient, with the random risk-slope SD recovered at |−0.42| vs 0.4
  ("RECOVERY OK").
- (c) **DONE** — H2 power simulation (`Muskan's Experiment/
  power_sim_h2.R`, 4,000 reps): power for the direction × route
  interaction is 0.83 at δ=0.15 SD and 0.97 at δ=0.20 SD at a
  conservative 360/cell.
- (d) **DONE (02 Jul 2026)** — every Method-4 figure verified against a
  citable primary source (citations in each item's rationale). One
  misattribution caught and fixed: the "1 in 1,000,000" formerly
  attributed to LeCun is not his (he declines to give a number); the item
  now quotes his verbatim asteroid comparison and attributes the number
  to the asteroid base rate. FRI medians confirmed against the report's
  Table 9 (0.38% / 3%); Amodei's 10–25% confirmed (Logan Bartlett Show,
  Oct 2023; flat 25% at Axios AI+ Summit, Sep 2025). PI sign-off on the
  reworded LeCun item still required.
- (e) **DONE (02 Jul 2026)** — Everest figure verified and now stated in
  the item stem: ~1.3% of climbers above base camp died 1921–2006 (Firth
  et al., BMJ 2008); ~1.0% of first-time summit attempters 2006–2019
  (Huey et al., PLOS ONE 2020); 0.7% for 2007–2024 (Moore et al., J
  Physiol 2026). Fielded as "about 1 in every 100 people who have tried
  to climb it have died."

---

## 6. MRP (population estimates)

- Multilevel model per registered outcome with age × gender × education ×
  income × state; post-stratified to the ACS frame
  (`build_poststrat.py` / `acs_poststrat.R`; gender handling per
  `ACS_poststratification_manual.md` — the inclusive survey category is
  allocated, not dropped).
- Validation: posterior predictive checks; leave-one-state-out
  cross-validation.
- **State maps:** published only for outcomes where the effective per-state
  sample exceeds **300** (registered threshold).

---

## 7. Panel-selection limitation and benchmarks (registered reporting rule)

Prolific is an opt-in panel; MRP adjusts demographics only. Two verbatim
Pew ATP items are fielded before any treatment: `bench_pew_cncexc`
(excited vs concerned; Pew Jun 2025: 10/50/38) and `bench_pew_aireg`
(regulation won't go far enough; Pew Aug 2024: 21/58/21). On each item the
two directional options are rotated per respondent with the neutral/"Not
sure" option anchored last. **Every
population-level headline is published next to the sample-vs-Pew gap on
these two items**, with direction-of-bias reasoning. If our raw sample
differs from the Pew topline by more than 10 percentage points on either
item, all population claims carry an explicit calibration caveat, and a
raking-to-benchmark sensitivity estimate is reported.

---

## 8. What we will NOT do (registered negative commitments)

- No "N times safer than experts' estimates" multiplier headline from the
  Method 3 back-out; any multiplier reported anywhere is labelled as
  researcher interpretation, never as a public belief.
- No pooling of Method 4 sources into a single "experts say" figure.
- No point estimate of p\* — distributions with intervals only.
- No state map below the effective-sample threshold.
- No mid-wave design changes; no within-respondent adaptation of the DCE.
- No re-labelling of exploratory analyses (H5′/H6′, proxy moderators,
  benchmark raking) as confirmatory after the fact.
