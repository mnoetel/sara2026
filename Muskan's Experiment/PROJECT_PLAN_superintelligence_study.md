# Superintelligence-Ban Study: Project Plan (as fielded in SARA)

**Audience:** anyone analysing or extending the superintelligence module of SARA USA 2026.
**Status:** **fielded design.** The module runs as the final block of the SARA oTree survey, not as a standalone Qualtrics study. Item text lives in the instrument (`survey/sara_usa.md`); passages live in `survey/muskan_stimuli.md`. This plan states the design, hypotheses, and analysis for what is actually fielded.
**Rev 3 (2026-07-02): reconciled to the fielded SARA module.** SARA's length budget cut the standalone battery. Fielded measures are: the **two 5-point support items** (pro-ban + anti-ban), the **two single-item route self-reports** (elaboration / cue-reliance, one-sided cells only, doubling as quasi-manipulation-checks), and the **comprehension check** (control cell only). Cut relative to Rev 2: pre-exposure prior attitude, attitude certainty/strength (F), MC1–MC3 as separate items, D3/D4, thought-listing, Need for Cognition, and social desirability. Hypotheses that depended on cut measures (old H1 certainty, H4 prior-extremity) are out of scope for this wave — see §4. SARA's demographics, political orientation, AI-use, and numeracy items are available as moderators instead. Debrief is delivered as links on the survey's end page.
**Rev 2 (2026-06-17):** primary DV became two 5-point Likert items (top-2-box); mediators/manipulation checks limited to one-sided cells; durability probe removed.
**Australian/US note:** stimuli and measures use plain English; the sample is US (US spelling fine in participant-facing text). Internal docs use Australian English.

---

## 0. How to use this document

1. The participant-facing **message stimuli** are the single source of truth in `survey/muskan_stimuli.md` (27 passages; the xlsx is kept for provenance only). Do not rewrite them.
2. The **fielded measures** are in `survey/sara_usa.md` (pages `superintelligence_def` → `superintelligence_check`); §7 below describes them and maps them to the original item bank.
3. The **analysis plan** (§9) is written for R (the supervisor codes in R).
4. Decisions previously marked **[DECISION]** are recorded in §12 with their outcomes.
5. Source provenance for every stimulus is in `Materials for generating design/` (files 01–05 and the README index).

---

## 1. Study overview

**Research aims.** **(Aim 1 — mechanism)** Does the *type* of contextual information people receive about a proposed superintelligence ban change how much they support it and how certain that attitude is, and does the ELM route (peripheral vs central) explain why? **(Aim 2 — estimate)** What is the *considered* level of public support for the ban: the estimate that survives exposure to the strongest arguments on *both* sides? Aim 1 lives in the one-sided cells; Aim 2 is the reason the two-sided ("contested") cells exist.

**Where it sits.** This is a sub-study within **SARA**, a survey program running since 2024 on public perceptions of AI risk and governance. The parent program has mostly sampled Australian adults; **this study runs on a US sample** and focuses on tolerance for, and persuadability around, a superintelligence ban.

**Real-world backdrop (for framing and debrief).**
- Oct 2025: the Future of Life Institute's *Statement on Superintelligence* called for a prohibition on developing superintelligence until safety is assured; it has 130k+ signatories.
- Mar 2026: the *Pro-Human Declaration* argued AI should serve humanity, keep humans in control, and prevent concentration of AI power.
These moved superintelligence governance from niche to mainstream, while public knowledge of the actual arguments remains low.

---

## 2. Theoretical framework

Three mechanisms, unified by the Elaboration Likelihood Model (ELM; Petty & Cacioppo, 1986):

- **Framing effects.** The same ban can be framed as protective (safety) or as ceding ground to competitors (innovation). Same policy, different gut reaction.
- **Elite cues.** People defer to trusted/prominent sources on topics they don't know well. A high-prestige magazine or famous signatory acts as an authority signal independent of argument content. → **peripheral route**.
- **Substantive argument.** Detailed reasons and evidence that the participant must evaluate. → **central route**.
- **Social desirability.** People may endorse the ban because it sounds responsible, not because the message moved them. Treated as a control/covariate, not a mechanism.

**ELM core claim used here:** central-route (effortful) processing produces attitudes that are stronger, more certain, more durable, and more predictive of behaviour than peripheral-route (cue-based) attitudes.

---

## 3. Design

**Current design: 3×3 between-subjects factorial.** Two crossed factors, each with three levels:

- **Argument For the ban** ∈ {elite cue, substantive, none}
- **Argument Against the ban** ∈ {elite cue, substantive, none}

A participant is randomised to one of the 9 cells and reads the corresponding passage (both, one, or — in the control cell — neither, just the neutral definition).

| For ↓ \ Against → | Elite | Substantive | None |
| --- | --- | --- | --- |
| **Elite** | 1 | 2 | 3 |
| **Substantive** | 4 | 5 | 6 |
| **None** | 7 | 8 | 9 (control) |

**Planned contrasts (per factor):**
- **C1 — any argument vs none:** elite = +1, substantive = +1, none = −2.
- **C2 — route (peripheral vs central):** elite = +1, substantive = −1, none = 0.

**Relationship to the 2×2+control in the presentation.** Muskan's slides describe a 2×2 (information type × framing) plus a control. That maps exactly onto the *one-sided* cells of this 3×3:

- Cell 3 (pro-elite only) = Condition C (elite, pro-ban)
- Cell 6 (pro-substantive only) = Condition A (substantive, pro-ban)
- Cell 7 (anti-elite only) = Condition D (elite, anti-ban)
- Cell 8 (anti-substantive only) = Condition B (substantive, anti-ban)
- Cell 9 = Condition E (control)

The 3×3 **adds** the four *two-sided* ("contested") cells (1, 2, 4, 5), where the participant reads both a pro-ban and an anti-ban message **at once**. Their job is the **Aim-2 estimate**: support measured here is support *after hearing the strongest case for and against*, i.e. the framing-robust "considered support" number (§9.0). Exposure is simultaneous and support is measured once — this is balanced-information support, not a resistance-over-time test. **Division of labour:** the one-sided cells + control carry Aim 1 (the ELM mechanism, §4); the contested cells carry Aim 2. Mediators and manipulation checks are collected **only in the one-sided cells**, where a single message makes the route unambiguous; the contested cells collect only the support DV.

**Stimulus versions.** Each cell has 3 wording versions (27 rows total) to avoid any single stimulus driving results. Version is a nuisance variable (stimulus sampling), not a factor of interest — serve one at random and model it as a random effect or ignore if balanced (§9).

---

## 4. Hypotheses (as testable with the fielded measures)

Re-expressed for the fielded module. The DV throughout is **ban support**: the pro-ban item, the (reverse-scored) anti-ban item, and their difference (§7-A).

- **H2 (route × framing).** The pro-vs-anti swing in **ban support** is larger under substantive than under elite messaging (people who engaged with content are more responsive to its direction). → For/Against direction × C2 interaction. *This is now the primary Aim-1 test.*
- **H3 (direction).** Pro-ban messaging raises support; anti-ban messaging lowers it, across both routes. → main effects of For and Against.
- **H5′ (central-route engagement, exploratory).** In the one-sided cells, substantive (vs elite) messages produce higher self-reported elaboration (the central-route item), and elaboration mediates the message's effect on support. Single-item mediator → treat as exploratory.
- **H6′ (peripheral-route engagement, exploratory).** In the one-sided cells, elite (vs substantive) messages produce higher self-reported cue reliance (the peripheral-route item), and cue reliance mediates the effect on support. Same single-item caveat.

**Out of scope this wave (measures not fielded; candidates for a follow-up):**
- **H1 (route → certainty).** Requires the attitude-certainty/strength DV, cut for length. The strongest ELM claim (central-route attitudes are more certain/durable) is therefore *not tested here* — say so plainly when reporting.
- **H4 (prior-attitude moderation).** Requires a pre-exposure support measure; asking the DV before the stimulus inside SARA would prime the whole module. SARA's political orientation, AI-use, and numeracy items are available as *proxy* moderators (exploratory only).

- **Aim 2 (descriptive, not a directional hypothesis).** Estimate the considered level of public support for the conditional ban — the top-2-box proportion who endorse it after balanced exposure to both sides (the contested cells) — bracketed by the naive (control) and one-sided estimates. Estimand and caveats in §9.0 and §11. *Unchanged by the descope: the two support items carry it.*

---

## 5. The stimuli file (`Superintelligence_3x3_stimuli_v2.xlsx`)

**Sheet "Stimuli"** — 27 rows, one per cell-version. Columns:

| column | meaning |
| --- | --- |
| `stimulus_id` | unique key, e.g. `cell5_v2` |
| `cell` | 1–9 (see §3 grid) |
| `for_arg` / `against_arg` | `elite` / `substantive` / `none` |
| `version` | 1–3 |
| `order` | `for_first` / `against_first` / `for_only` / `against_only` / `control` (order is rotated across versions for two-sided cells) |
| `word_count` | for length-matching checks |
| `body_text` | the passage shown to the participant |
| `source_refs` | provenance (not shown to participant) |

**Sheet "Reference"** — neutral definition, ELM/ITT legend, cell map.

**How to randomise in Qualtrics.**
1. Use a randomiser / embedded-data field `cell` (1–9), evenly allocated.
2. Within the assigned cell, randomly pick `version` (1–3).
3. Pipe the matching `body_text` into the stimulus block. The control cell (9) shows only the neutral definition.
4. Store `cell`, `for_arg`, `against_arg`, `version`, `order` as embedded data for analysis.

**Order handling.** For/Against order is a nuisance variable. It is rotated across the three versions of each two-sided cell, so random version assignment randomises order. Optionally also enable Qualtrics "randomize element order" if the two halves are shown as separate blocks. Do **not** add order as a crossed factor unless the supervisor wants to estimate primacy/recency (would expand the two-sided cells to both orders = 39 rows; **[DECISION]**).

---

## 6. Survey flow (as fielded — the final block of SARA)

The module runs **last** in SARA (after the tolerance core and demographics), so its persuasion cannot contaminate SARA's risk-tolerance estimates. Sequence (pages in `survey/sara_usa.md`):

1. **Neutral definition** of superintelligence (`superintelligence_def`, all participants).
2. **Stimulus** (`superintelligence_brief`) — the assigned passage from `survey/muskan_stimuli.md`, balanced-assigned in the oTree engine (`creating_session`). Control cell 9 skips this page (neutral definition only).
3. **Primary DV — ban support** (`superintelligence_support`): the two 5-point items (§7-A), **shown in every cell**.
4. **Route self-reports** (`superintelligence_route`) — **one-sided cells (3, 6, 7, 8) only**: the elaboration item and the cue-reliance item (§7-D). These are the mediators and double as the quasi-manipulation-checks (§7-C).
5. **Comprehension check** (`superintelligence_check`) — **control cell only**: the 4-option ASI item. Non-control cells skip it (their briefing restates the concept).
6. **Debrief** — on SARA's end page: a note that the briefings were assembled from real published arguments, with links to the FLI statement (pro) and Andreessen's manifesto (anti) so participants can read both sides in full.

**Why the branch.** The route items ("the reasons given", "who backed the idea") only have a clean referent when one message was shown. In the contested cells two messages of possibly different routes appeared, so those items are uninterpretable there — and the contested cells do not need them, because their job is the Aim-2 support estimate, not the mechanism.

**Data quality** comes from SARA's shared machinery: two disguised attention checks earlier in the survey (failing both screens the respondent out before this module), and page-time paradata recorded by oTree (pre-register a minimum stimulus read-time flag rather than an exclusion).

**Order note.** The DV pages come before the route items so the support measure is never contaminated by self-reflection prompts. For/Against order within two-sided passages is rotated across the three stimulus versions (see §5).

---

## 7. Measures (fielded set, with the original item bank noted where cut)

Item text below is descriptive; **the instrument (`survey/sara_usa.md`) is authoritative**.

### A. Ban support — primary DV (two 5-point items, as fielded)

- **SUPPORT item (`muskan_support`, pro-ban):** "Do you support or oppose a ban on the development of superintelligence, not lifted before there is (1) broad scientific consensus that it will be done safely and controllably, and (2) strong public buy-in?" — Strongly support / Support / Oppose / Strongly oppose / Don't know.
- **OPPOSE item (`muskan_support_anti`, anti-ban):** "How much do you agree? 'Companies should be free to build machines smarter than humans, even without public support or guarantees of safety.'" — Strongly agree … Strongly disagree.

Reporting: top-2-box on each item separately, plus the **continuous difference** after reverse-scoring the OPPOSE item (map both to −2…+2 with "Don't know" set missing; `support = SUPPORT − reverse(OPPOSE)`). Keeping them as two separate items (not one composite) lets you report both prevalences and catch acquiescence — anyone who top-2-boxes *both* (supports the ban AND agrees companies should be free) is responding carelessly (data-quality flag, not an exclusion).
- **Not fielded (Rev 3):** the pre-exposure administration of these items (prior attitude / prior extremity) — see H4 in §4.
- *(Note: any "% of Americans" claim is a population estimate — see the sampling/weighting caveat in §9.0 and §11.)*

### B. Comprehension check (fielded: control cell only)
`muskan_si_comprehension`: "Which of the following is closest to artificial superintelligence? A computer program that…" — 4 options, shuffled; correct = "does almost everything more intelligently than most humans." **Fielded only in the control cell** (non-control cells' briefings restate the concept). Used to flag/weight low-comprehension control responses, not as an exclusion.

### C. Manipulation checks → carried by the route items (quasi-checks)
The standalone MC battery (source-cue salience, argument salience, direction check) was cut for length. The **route self-reports in D double as quasi-manipulation-checks**, with a pre-registered expected pattern in the one-sided cells:
- the **cue-reliance item** should be higher in **elite** cells than substantive cells (MC1's job);
- the **elaboration item** should be higher in **substantive** cells than elite cells (MC2's job).

Honest limits of the quasi-check (state in the method): these measure the respondent's *self-perceived processing*, not the stimulus's properties, so they conflate manipulation success with individual differences; there is no direction check (MC3) — pro/anti direction is instead guaranteed by construction and provenance of the passages; and single items carry unknown reliability. A null on the quasi-check pattern therefore cannot cleanly separate "manipulation failed" from "self-report failed" — which is exactly why the original MC battery is the first thing to restore in any standalone follow-up.

### D. Mediators (fielded: one single item per route, one-sided cells only)
- **Elaboration / central route** (`muskan_central_route`, ≈ D1-2 of the original bank): "I tried to judge the reasons given, not just who was giving them." — 5-point agree.
- **Cue reliance / peripheral route** (`muskan_peripheral_route`, ≈ D2-1): "My reaction depended more on who backed the idea than on the reasons they gave." — 5-point agree.

Cut from the original bank: the remaining D1/D2 items (multi-item versions), D3 (source credibility), D4 (argument quality), D5 (thought-listing). Consequence: mediation tests (H5′/H6′) use single-item mediators on 5-point scales — exploratory, no internal-consistency estimate possible.

### E. (Primary DV — see A, administered post-exposure.)

### F. Attitude strength / certainty — NOT FIELDED
Cut for length; old H1 is out of scope this wave (§4). First priority for a standalone follow-up.

### G. (Removed at Rev 2.) The contested cells carry the both-sides function (Aim 2, §9.0).

### H. Need for Cognition — NOT FIELDED
Cut for length despite the §12 decision to include it; SARA's Berlin Numeracy quartile is available as a rough cognitive-engagement proxy (exploratory only — numeracy is not NfC).

### I. Social desirability — NOT FIELDED
Cut for length. Reporting consequence: the acquiescence flag in A (top-2-boxing both DV items) is the only careless-responding indicator inside the module; SARA's attention-check screen-out handles the rest upstream.

### J. Demographics & moderators (from the parent survey)
SARA collects age, gender, education, income, state, political orientation (7-point), AI-use frequency, and numeracy (Berlin Numeracy Test) before this module. Prior familiarity with the ban debate is not measured (cut with the prior-attitude block).

---

## 8. Which measure tests which hypothesis

| Aim / Hypothesis | Test | Key variables |
| --- | --- | --- |
| **Aim 2 — considered support** | top-2-box % in contested cells (headline = cell 5), with CIs; bracketed by control & one-sided | both DV items (A) |
| H2 route × framing | direction × C2 interaction on support | For/Against direction, route, support (A) |
| H3 direction | main effects of For, Against on support | support (A) |
| H5′ central engagement/mediation (exploratory) | route → elaboration item → support; one-sided cells | `muskan_central_route` (D) |
| H6′ peripheral engagement/mediation (exploratory) | route → cue-reliance item → support; one-sided cells | `muskan_peripheral_route` (D) |
| Quasi-manipulation-check | cue-reliance higher in elite cells; elaboration higher in substantive cells; elaboration matched across pro vs anti substantive cells (6 vs 8) | the two route items (C/D) |
| ~~H1 route → certainty~~ | not testable — certainty DV not fielded | — |
| ~~H4 prior moderation~~ | not testable — no pre-exposure measure | — |

---

## 9. Analysis plan (R)

### 9.0 Aim-2 estimand: considered public support (the headline number)
The Aim-2 quantity is the proportion endorsing the conditional ban **after balanced exposure to both sides** — top-2-box on the SUPPORT item in the contested cells.
- **Headline:** cell 5 (substantive for *and* against) = support after each side's strongest *reasoned* case. Report top-2-box % with a 95% CI.
- **Robustness:** average top-2-box % across all four contested cells (1, 2, 4, 5).
- **Bracket (how soft is the number):** control (9) = naive support; one-sided pro (3, 6) = upper push; one-sided anti (7, 8) = lower push. Report all so the reader sees the range the headline sits within.
```r
library(dplyr)
cell5 <- filter(df, cell == 5)
mean(cell5$support_item >= 4)                                  # 4–5 = Agree/Strongly agree
binom.test(sum(cell5$support_item >= 4), nrow(cell5))$conf.int # 95% CI
# population/weighted version: survey::svyciprop() on a post-stratified design
```
**Weighting.** A "% of Americans" claim rides on SARA's machinery: MRP / post-stratification to ACS margins (age × sex × education × income × state), plus the Pew benchmark items (`bench_pew_cncexc`, `bench_pew_aireg`) that quantify how far the Prolific panel sits from probability-sample toplines on AI attitudes. Report weighted and unweighted, and report the benchmark gap alongside any prevalence claim. This is the biggest threat to Aim 2 (see §11).
**Material balance.** The estimate is only as balanced as the stimuli. Check that pro and anti substantive arguments prompted equal engagement by comparing the elaboration item across the one-sided substantive cells (6 vs 8); if they differ, the contested estimate is biased toward the stronger side — report this alongside the number. (Weaker than the original MC2 argument-strength comparison — single self-report item; say so.)

**Factorial model with planned contrasts.**
```r
df$For     <- factor(df$for_arg,     levels = c("none","elite","substantive"))
df$Against <- factor(df$against_arg, levels = c("none","elite","substantive"))

# rows = none, elite, substantive
cmat <- cbind(any_vs_none = c(-2, 1, 1),   # C1
              route_elite_vs_sub = c(0, 1, -1)) # C2
contrasts(df$For)     <- cmat
contrasts(df$Against) <- cmat

# Primary DV: ban support (the continuous difference score; no prior_support
# or soc_desirability covariates — neither was fielded)
m_support <- lm(support ~ For * Against, data = df)
```
Report the direction × C2 interaction for H2; For/Against main effects for H3. (Old H1's certainty model and H4's prior-extremity model are dropped — measures not fielded.)

**Quasi-manipulation-check (pre-registered pattern, one-sided cells).**
```r
one_sided <- subset(df, cell %in% c(3, 6, 7, 8))
# cue-reliance higher under elite; elaboration higher under substantive
t.test(peripheral_item ~ route, data = one_sided)   # route = elite vs substantive
t.test(central_item    ~ route, data = one_sided)
```

**Mediation (H5′, H6′ — exploratory, single-item mediators), lavaan, bootstrapped.** Restrict to the **one-sided cells (3, 6, 7, 8)** and code `route_sub` = +1 substantive / −1 elite (the C2 contrast). The outcome in both models is **support** (there is no certainty DV).
```r
library(lavaan)
# H5': central route
med_h5 <- '
  central_item ~ a*route_sub
  support      ~ b*central_item + cp*route_sub
  indirect := a*b
  total    := cp + a*b
'
fit_h5 <- sem(med_h5, data = one_sided, se = "bootstrap", bootstrap = 5000)

# H6': peripheral route (cue reliance as mediator of support)
med_h6 <- '
  peripheral_item ~ a*route_elite      # route_elite = -route_sub
  support         ~ b*peripheral_item + cp*route_elite
  indirect := a*b
'
```
Report indirect effects with 95% bootstrap CIs, labelled exploratory (single-item mediators, unknown reliability — attenuation likely).

**Covariates / robustness:** include `version` as a random effect if using `lmer` (`(1|version)`), or confirm version is balanced (the oTree engine balance-assigns all 27 rows) and drop. SARA's political orientation and numeracy quartile enter only pre-registered exploratory moderation models.

**Power / sample size (resolved by embedding in SARA).** All ~4,000 SARA respondents pass through the module (less consent declines and attention-check screen-outs), giving roughly **~430+ per cell** — far beyond the standalone target of 60–70/cell. H2 (the interaction) is comfortably powered; the binding constraint is now the *exploratory mediation* (single-item mediators attenuate a and b paths), which no realistic n fully rescues — report those as effect estimates with CIs, not hypothesis tests. Run the pre-launch power simulation for H2 contrasts anyway (`pwr`) and record it in PREREGISTRATION.md.

---

## 10. Build notes (oTree, as implemented)
- Assignment: `creating_session` in `survey/sara/__init__.py` balance-assigns the 27 stimulus rows in shuffled blocks seeded on the session code, so cells and versions are near-exactly balanced; `muskan_stim, cell, for_arg, against_arg, version, order` are stored on the Player and export with the data.
- Passages are parsed from `survey/muskan_stimuli.md` by `survey/sara/muskan.py`; the briefing page injects the assigned `body_text`.
- **Branch display logic:** `condition: muskan_one_sided` shows the route items only in cells 3/6/7/8; `condition: muskan_control` shows the comprehension check only in cell 9; `condition: muskan_not_control` skips the briefing page for cell 9.
- Population claim: SARA's MRP + the Pew benchmark items (see §9.0), not Prolific quotas.
- All module items are force-response; oTree records page times (use for the minimum-read-time flag).

---

## 11. Known limitations and validity flags
- **Elite-cue asymmetry.** No anti-ban magazine source matches TIME's prestige; the anti-ban elite material leans on an opinion piece (WaPo/Dispatch) and named opponents (LeCun, Ng, Andreessen, Horowitz). This is inherent — there is simply less high-prestige anti-ban coverage. **Do not paper over it; measure it** via MC1 / source-credibility, and report perceived prestige by condition.
- **Prestige asymmetry across sides.** The pro-ban roster (Nobel laureates, "Godfathers of AI", Wozniak, royals) outweighs the anti-ban roster even after curation. A pro-vs-anti difference could partly reflect endorser prestige. The source-credibility mediator (D3) is the tool to detect and adjust for this.
- **Routes are not cleanly separable.** Elite passages still carry a little argument; substantive passages still reference "experts." The manipulation is cue *density*, not on/off. State this in the method.
- **ITT is approximated, not certified.** Stimuli are grounded in FLI/CAIS (pro) and a16z/Castro/Ng-LeCun (anti) actual positions, but no FLI or a16z reviewer has signed off.
- **Fei-Fei Li excluded** from the anti-ban cue after fact-check: she has not opposed a superintelligence ban (criticised SB-1047 but co-authored Newsom's report calling for more guardrails). See `README_3x3_design_and_stimulus_plan.md`, §9.
- **Balanced-information support, not persistence.** Exposure in the contested cells is simultaneous and measured once, so Aim 2 estimates considered support under balanced information — not resistance over time. A delayed re-test (true persistence) is out of scope for the honours timeline; flag as future work.
- **The Aim-2 estimate is only as balanced as the materials.** If the pro arguments read as stronger than the anti (see elite asymmetry), the contested estimate tilts pro by construction. Check via the per-side MC2 comparison (cells 6 vs 8) and report.
- **Prevalence claims need a representative/weighted sample.** "% of Americans" requires a representative panel or post-stratification weights, not a convenience sample. This is the single biggest threat to Aim 2. Fielded mitigation: SARA's MRP plus the verbatim Pew benchmark items, which measure (rather than assume away) the Prolific-vs-population gap on AI attitudes.
- **Rev-3 descope limitations (from embedding in SARA).** No certainty/strength DV → the flagship ELM durability claim (old H1) is untested here. Single-item mediators → H5′/H6′ are exploratory; reliability unknown, attenuation likely. No standalone manipulation checks → route validity rests on the quasi-check pattern in the route items (see §7-C for why a null there is ambiguous). No social-desirability covariate → the acquiescence flag on the DV pair is the only in-module careless-responding indicator. Debrief is delivered as links on the survey end page rather than a full explanatory debrief screen.

---

## 12. Decisions (resolved; history preserved)
1. **Mediators:** ~~full battery vs subset~~ → D1 and D2 only, and in the fielded module each was further cut to its single best item (`muskan_central_route`, `muskan_peripheral_route`). No D3/D4 (judged to overlap D1/D2), no D5.
2. **Social desirability:** ~~10-item vs 5-item~~ → superseded: not fielded at all (SARA length budget). The acquiescence flag on the DV pair is the in-module quality indicator.
3. **Need for Cognition:** the earlier "include" call was reversed by the SARA length budget → not fielded; numeracy quartile available as a rough exploratory proxy.
4. **Headline Aim-2 estimate:** cell 5 (substantive both sides), bracketed by the other contested cells, control, and one-sided cells — as in §9.0.
5. **Sampling for Aim 2:** resolved by embedding in SARA — MRP to ACS margins + the Pew benchmark items.
6. **Sample size:** resolved by embedding in SARA — ~4,000 through the module (~430+/cell); run the H2 power simulation pre-launch and record it in PREREGISTRATION.md.
7. **Order:** randomised within the 27 rows via version rotation (no 39-row expansion; no primacy/recency factor).
