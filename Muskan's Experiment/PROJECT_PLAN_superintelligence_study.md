# Superintelligence-Ban Study: Project Plan and Survey-Build Handoff

**Audience:** the agent (or person) building the full survey inside the SARA program in Qualtrics.
**Status:** stimuli built and fact-checked; mediators specified here for the first time (none existed in the folder). Items below are drafts for the supervisor to approve, not yet validated scales.
**Rev 2 (2026-06-17):** primary DV is now two 5-point Likert items (for top-2-box prevalence); mediators and manipulation checks are collected in the one-sided cells only; the contested (two-sided) cells are kept and their job is the considered-support estimate (Aim 2). The earlier separate durability probe is removed.
**Author of this handoff:** prepared 2026-06-17 from the project folder (presentation script, intro/theory-of-change docs, the 3×3 design table, and the source materials).
**Australian/US note:** stimuli and measures use plain English; the sample is US (US spelling fine in participant-facing text). Internal docs use Australian English.

---

## 0. How to use this document

1. The participant-facing **message stimuli already exist**: `Superintelligence_3x3_stimuli_v2.xlsx` (27 rows). Do not rewrite them; load them as described in §5.
2. The **measures and mediators** (§6–§7) are new. Build them in Qualtrics in the order in §6.
3. The **analysis plan** (§9) is written for R (the supervisor codes in R).
4. Anything marked **[DECISION]** needs a human call before launch (collected in §12).
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

## 4. Hypotheses

From the presentation (re-expressed for the 3×3), plus two new mediation hypotheses the mediators make testable.

- **H1 (route → certainty).** Substantive (central) conditions produce greater attitude **certainty** than elite (peripheral) conditions, regardless of framing direction. → C2 on the certainty DV.
- **H2 (route × framing).** The pro-vs-anti swing in **ban support** is larger under substantive than under elite messaging (people who engaged with content are more responsive to its direction). → For/Against direction × C2 interaction.
- **H3 (direction).** Pro-ban messaging raises support; anti-ban messaging lowers it, across both routes. → main effects of For and Against.
- **H4 (prior-attitude moderation).** Manipulation effects shrink for participants with extreme prior attitudes; the biggest movement is among the genuinely uncertain. → manipulation × prior-attitude-extremity interaction.
- **H5 (central-route mediation) [new].** The effect of substantive (vs elite) messaging on attitude certainty is **mediated by elaboration** (depth of processing). Substantive → more elaboration → more certain attitude.
- **H6 (peripheral-route mediation) [new].** The effect of elite (vs substantive) messaging on ban support is **mediated by perceived source credibility / reliance on source cues**. Elite → more cue reliance → attitude shift driven by the source rather than the argument.

H5 and H6 are the point of adding mediators: they let the study **demonstrate the ELM route directly** rather than infer it only from the certainty outcome (the limitation the presentation flags).

- **Aim 2 (descriptive, not a directional hypothesis).** Estimate the considered level of public support for the conditional ban — the top-2-box proportion who endorse it after balanced exposure to both sides (the contested cells) — bracketed by the naive (control) and one-sided estimates. Estimand and caveats in §9.0 and §11.

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

## 6. Survey flow (build in this order)

1. **Consent.**
2. **Demographics + context** (§7-J): age, gender, education, US region, political orientation, AI-use frequency, prior familiarity with the superintelligence-ban debate.
3. **Need for Cognition** short scale (§7-H) — optional moderator. *Place before the stimulus.*
4. **Prior attitude** (§7-A) — the two support items, measured BEFORE any message (safeguard 2).
5. **Neutral definition** of superintelligence (all participants).
6. **Knowledge check** (§7-B) — the 4-option ASI item (safeguard 1).
7. **Stimulus** — piped from the xlsx per §5. (Control cell 9: neutral definition only.)
8. **Branch on cell type (display logic):**
   - **One-sided cells (3, 6, 7, 8):** manipulation checks (§7-C) → mediators (§7-D) → attitude certainty/strength (§7-F). These are the Aim-1 / ELM-mechanism measures and need a single, unambiguous message.
   - **Two-sided cells (1, 2, 4, 5) and control (9):** skip C, D, F — go straight to the DV.
9. **Primary DV — ban support** (§7-A, post-exposure): the two 5-point items. **Shown in every cell** (this is the Aim-2 estimate in the contested cells, and the outcome everywhere else).
10. **Social desirability** — Strahan–Gerbasi M-C short form (safeguard 3, §7-I).
11. **Debrief** — explain the manipulation, note stimuli are composites of real positions, link to the FLI statement and an anti-ban source for balance.

**Why the branch.** The mediators ("how much did you think about *the* argument", "how credible was *the* source") only have a clean referent when one message was shown. In the contested cells two messages of possibly different routes appeared, so those items are uninterpretable there — and the contested cells do not need them, because their job is the Aim-2 support estimate, not the mechanism.

Attention checks: at least one instructed-response item in a long block, plus a minimum-time gate on the stimulus page.

---

## 7. Measure and mediator item bank

Scales: the **two support items (A) use a 5-point** Likert (Strongly disagree … Strongly agree) so responses collapse to top-2-box prevalence ("% who agree"). All other multi-item constructs use **1 = Strongly disagree … 7 = Strongly agree** (more variance helps the continuous mediation models). Items marked (R) are reverse-scored. Compute each multi-item construct as the mean after reverse-scoring; report Cronbach's α / McDonald's ω.

### A. Ban support — primary DV (two 5-point items; also the prior-attitude measure)
Both on a **5-point** scale: Strongly disagree / Disagree / Neither / Agree / Strongly agree. Framing is the **conditional** ban (the actual FLI *Statement on Superintelligence* policy), held constant across both items.

- **SUPPORT item (pro-ban):** "The development of superintelligence should be prohibited until there is broad scientific agreement that it can be done safely and controllably, and strong public support."
- **OPPOSE item (anti-ban):** "Companies should be free to keep developing superintelligence without any government ban or pause."

Reporting: collapse the top two boxes of the SUPPORT item → "**X% agree** superintelligence should be paused until proven safe"; same for the OPPOSE item. Keeping them as two separate items (not one reverse-scored composite) lets you report both prevalences and catch acquiescence — anyone who top-2-boxes *both* is responding carelessly (use as a data-quality flag).
- **Continuous score** for the models: `support = SUPPORT − OPPOSE` (−4…+4), or treat the SUPPORT item as ordinal.
- **Prior attitude:** the same two items pre-exposure. **Prior extremity** = |prior continuous score| (distance from 0).
- *(Note: any "% of Americans" claim is a population estimate — see the sampling/weighting caveat in §9.0 and §11.)*

### B. Knowledge check (safeguard 1)
"Which of the following is closest to artificial superintelligence?" (single choice)
- a) A computer program that does some things more intelligently than humans
- b) A computer program that can write so well you cannot tell if it's a human or an AI
- c) **A computer program that is much smarter than people at almost everything** ✅ (correct)
- d) A computer program that is about as clever as a smart adult at most things

### C. Manipulation checks (one-sided cells only; the validity test of the ELM operationalisation)
- **MC1 — source-cue salience (peripheral):** "The information I just read pointed to well-known or respected people who hold this position." → should be higher in **elite** cells.
- **MC2 — argument salience (central):** "The information I just read gave detailed reasons and evidence for its position." → should be higher in **substantive** cells.
- **MC3 — direction check:** "The message I read was mostly…" 1 = strongly against a ban … 4 = neutral … 7 = strongly for a ban. → validates pro/anti framing.
- (Control cell: MC1/MC2 skipped or framed as "no message," used as a floor.)

### D. Mediators (mechanism; one-sided cells only — see §6 branch)

**D1. Elaboration / depth of processing** (central-route mediator; H5)
1. I thought carefully about the arguments in the message.
2. I tried to evaluate the reasons given, not just who was giving them.
3. While reading, I weighed points for and against the position.
4. (R) I skimmed the message without thinking much about it.

**D2. Reliance on source cues** (peripheral-route mediator; H6)
1. My reaction was shaped by who supported the position more than by the reasons given.
2. I was influenced by how prominent or credible the people involved seemed.
3. Who held this view mattered more to me than the details of the argument.

**D3. Perceived source credibility / prestige** (peripheral mediator; only where a source is present)
1. The people or sources behind this position are credible.
2. The people or sources behind this position are knowledgeable about this issue.
3. The people or sources behind this position are highly respected.

**D4. Perceived argument quality** (central mediator)
1. The argument I read was strong.
2. The argument I read was convincing on its merits.
3. The argument I read was well supported by evidence.

**D5. Thought-listing (optional, gold-standard cognitive-response measure).** Open text: "In the box below, list the thoughts that went through your mind while reading the message — one per line." Code each thought for (i) valence (pro-ban / anti-ban / neutral) and (ii) relevance (about the argument content vs about the source/other). Mediators derived: number of message-relevant thoughts (elaboration proxy), proportion favourable. *Labour-intensive to code; include only if a coder is available.* **[DECISION]**

### E. (Primary DV — see A, administered post-exposure.)

### F. Attitude strength / certainty — DV2 (H1; one-sided cells only)
1. **Certainty:** "How certain are you of your opinion about banning superintelligence?" 1 = not at all certain … 7 = extremely certain.
2. **Importance:** "How personally important is this issue to you?" 1 … 7.
3. **Perceived knowledge:** "How well-informed do you feel about this issue?" 1 … 7.
- Strength composite = mean of the three (report separately too).

### G. (Removed.) The contested cells now serve the "support even when given arguments both ways" function via simultaneous both-sides exposure (Aim 2, §9.0), so a separate counter-message probe is redundant.

### H. Need for Cognition — optional moderator (Cacioppo, Petty & Kao 1984 short form, 6 items, 1–7)
e.g., "I would prefer complex to simple problems"; "I really enjoy a task that involves coming up with new solutions"; (R) "Thinking is not my idea of fun." High NfC → central route dominates regardless of condition; low NfC → cue-driven. Tests ELM moderation.

### I. Social desirability (safeguard 3)
Strahan–Gerbasi short form of the Marlowe-Crowne scale (10 items, true/false). The design doc pre-selected five it wants included (Marlowe-Crowne items 16, 17, 26, 19, 22) — confirm whether to use the full 10-item short form or that 5-item subset. **[DECISION]** Use as a covariate.

### J. Demographics & exposure
Age; gender; education; US region; **political orientation** (1 = very liberal … 7 = very conservative — important, ban attitudes are politically loaded); AI-use frequency; prior familiarity with the superintelligence-ban debate (1–7).

---

## 8. Which measure tests which hypothesis

| Aim / Hypothesis | Test | Key variables |
| --- | --- | --- |
| **Aim 2 — considered support** | top-2-box % in contested cells (headline = cell 5), with CIs; bracketed by control & one-sided | SUPPORT item (A) |
| H1 route → certainty | C2 contrast on certainty (one-sided cells) | route, certainty (F) |
| H2 route × framing | direction × C2 interaction on support | For/Against direction, route, support (A) |
| H3 direction | main effects of For, Against on support | support (A) |
| H4 prior moderation | manipulation × prior extremity | prior extremity (A-pre) |
| H5 central mediation | route → elaboration (D1) → certainty (F); one-sided cells | indirect a×b |
| H6 peripheral mediation | route → source credibility (D3)/cue reliance (D2) → support; one-sided cells | indirect a×b |
| Manipulation valid + materials balanced? | MC1 higher in elite; MC2 higher in substantive; MC2 matched across pro vs anti substantive cells (6 vs 8) | MC1, MC2 |

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
**Weighting.** A "% of Americans" claim needs a representative/quota sample or post-stratification weights (age × sex × region × political affiliation to US margins, `survey` package). Report weighted and unweighted. This is the biggest threat to Aim 2 (see §11).
**Material balance.** The estimate is only as balanced as the stimuli. Check that pro and anti substantive arguments were perceived as equally strong by comparing MC2 across the one-sided substantive cells (6 vs 8); if they differ, the contested estimate is biased toward the stronger side — report this alongside the number.

**Factorial model with planned contrasts.**
```r
df$For     <- factor(df$for_arg,     levels = c("none","elite","substantive"))
df$Against <- factor(df$against_arg, levels = c("none","elite","substantive"))

# rows = none, elite, substantive
cmat <- cbind(any_vs_none = c(-2, 1, 1),   # C1
              route_elite_vs_sub = c(0, 1, -1)) # C2
contrasts(df$For)     <- cmat
contrasts(df$Against) <- cmat

# Primary DV: ban support
m_support <- lm(support ~ For * Against + prior_support + soc_desirability, data = df)

# DV2: attitude certainty (H1 via C2)
m_certain <- lm(certainty ~ For * Against + prior_support + soc_desirability, data = df)
```
Report the C2 (route) terms for H1; the direction × C2 interaction for H2; For/Against main effects for H3.

**Prior-attitude moderation (H4).**
```r
df$prior_extremity <- abs(df$prior_support - mid)  # mid = scale midpoint
m_mod <- lm(support ~ For * Against * prior_extremity + soc_desirability, data = df)
```

**Mediation (H5, H6), lavaan, bootstrapped.** Restrict to the **one-sided cells (3, 6, 7, 8)** — the only cells where mediators were collected and route is unambiguous — and code `route_sub` = +1 substantive / −1 elite (the C2 contrast).
```r
library(lavaan)
# H5: central route
med_h5 <- '
  elaboration ~ a*route_sub
  certainty   ~ b*elaboration + cp*route_sub
  indirect := a*b
  total    := cp + a*b
'
fit_h5 <- sem(med_h5, data = subset(df, cell %in% c(3,6,7,8)), se = "bootstrap", bootstrap = 5000)

# H6: peripheral route (source credibility as mediator of support)
med_h6 <- '
  source_cred ~ a*route_elite      # route_elite = -route_sub
  support     ~ b*source_cred + cp*route_elite
  indirect := a*b
'
```
Report indirect effects with 95% bootstrap CIs. Optionally run both mediators in parallel (competing central vs peripheral paths) in one model.

**Moderated mediation (optional):** add NfC as moderator of the a-path (route → elaboration); test index of moderated mediation.

**Covariates / robustness:** run all models with and without social desirability; report both. Include `version` as a random effect if using `lmer` (`(1|version)`), or confirm version is balanced and drop.

**Power / sample size [DECISION].** Nine cells; the interaction (H2) and indirect effects (H5/H6) are the power-limiting tests. Plan for ≥ ~60–70 completes per cell after exclusions → **target N ≈ 600–650** on US Prolific. Run a formal power analysis before launch: `pwr` for the ANOVA/contrasts, and a Monte Carlo simulation (e.g., `simsem` / custom lavaan simulation) for the indirect effects, since mediation power depends on assumed a and b paths. Pre-register the contrasts, the mediation models, and the exclusion rules.

---

## 10. Qualtrics build notes
- Evenly allocate `cell` (1–9) via a Randomizer with "evenly present elements"; nest a 3-way Randomizer for `version`.
- Store `cell, for_arg, against_arg, version, order` as embedded data set BEFORE the stimulus block so they export with the data.
- Pipe `body_text` from a lookup (loop & merge table or embedded data) keyed on `stimulus_id`.
- **Display logic for the branch (§6):** show the manipulation-check, mediator, and certainty blocks only when `for_arg = none` OR `against_arg = none` (the one-sided cells 3/6/7/8). Contested cells (1/2/4/5) and control (9) go straight from stimulus to the support DV.
- For the Aim-2 prevalence claim, recruit a **representative/quota US sample** (e.g., Prolific representative by age × sex × ethnicity × political affiliation) or capture quotas for post-stratification weighting.
- Force-response on the DV and mediator blocks; allow opt-out on demographics.
- Timing question on the stimulus page; flag completes below a minimum read time.

---

## 11. Known limitations and validity flags
- **Elite-cue asymmetry.** No anti-ban magazine source matches TIME's prestige; the anti-ban elite material leans on an opinion piece (WaPo/Dispatch) and named opponents (LeCun, Ng, Andreessen, Horowitz). This is inherent — there is simply less high-prestige anti-ban coverage. **Do not paper over it; measure it** via MC1 / source-credibility, and report perceived prestige by condition.
- **Prestige asymmetry across sides.** The pro-ban roster (Nobel laureates, "Godfathers of AI", Wozniak, royals) outweighs the anti-ban roster even after curation. A pro-vs-anti difference could partly reflect endorser prestige. The source-credibility mediator (D3) is the tool to detect and adjust for this.
- **Routes are not cleanly separable.** Elite passages still carry a little argument; substantive passages still reference "experts." The manipulation is cue *density*, not on/off. State this in the method.
- **ITT is approximated, not certified.** Stimuli are grounded in FLI/CAIS (pro) and a16z/Castro/Ng-LeCun (anti) actual positions, but no FLI or a16z reviewer has signed off.
- **Fei-Fei Li excluded** from the anti-ban cue after fact-check: she has not opposed a superintelligence ban (criticised SB-1047 but co-authored Newsom's report calling for more guardrails). See `README_3x3_design_and_stimulus_plan.md`, §9.
- **Balanced-information support, not persistence.** Exposure in the contested cells is simultaneous and measured once, so Aim 2 estimates considered support under balanced information — not resistance over time. A delayed re-test (true persistence) is out of scope for the honours timeline; flag as future work.
- **The Aim-2 estimate is only as balanced as the materials.** If the pro arguments read as stronger than the anti (see elite asymmetry), the contested estimate tilts pro by construction. Check via the per-side MC2 comparison (cells 6 vs 8) and report.
- **Prevalence claims need a representative/weighted sample.** "% of Americans" requires a representative panel or post-stratification weights, not a convenience sample. This is the single biggest threat to Aim 2.

---

## 12. Open decisions for the supervisor
1. **Mediators to include:** full battery (D1–D4) vs subset; include the thought-listing task (D5)?
Answer: No D5, just D1 and D2. D3 and D4 repeat d1 and 2.
2. **Social desirability:** full 10-item Strahan–Gerbasi short form vs the 5 items the design doc pre-selected?
Answer: the 5 pre-selected items, to keep the survey shorter.
3. **Need for Cognition:** include as a moderator, or drop to keep the survey short?
Answer: include, it's a core ELM variable and the short form is only 6 items.
4. **Headline Aim-2 estimate:** anchor on cell 5 (substantive both sides, recommended) or the average across all four contested cells?
5. **Sampling for Aim 2:** representative panel vs quotas + post-stratification weighting; confirm the weighting margins.
6. **Sample size:** confirm target N (≈600–650) and run the power simulation — the Aim-1 interaction (H2) and the indirect effects (H5/H6) are the binding constraints.
7. **Order:** keep order randomised within the 27 rows (recommended), or pre-write both orders (39 rows)? Only matters if a primacy/recency check is wanted.
