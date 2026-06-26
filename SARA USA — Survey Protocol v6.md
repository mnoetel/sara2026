# SARA USA 2026 — Survey Protocol & Instrument (v6, markdown)

**Michael Noetel (UQ) & Alor Sahoo (MIT). Version date: 17 June 2026.**

This is the editable markdown master. It supersedes the v2–v5 Word docs (which stay archived in this folder) and folds in the live edits made while prototyping: the environment experiment moved first, matched-language frame item, two-orders-of-magnitude scope rows, a log willingness-to-pay scale, and the DCE-based quantitative core. The clickable prototype `SARA USA — full survey prototype.html` mirrors this document; the DCE design and analysis live in `sara_dce_design.R`.

---

## 1. Purpose and scope

The survey answers two questions about US public opinion on AI risk, **without** asking the public to produce probability estimates or to know which mitigations to apply:

1. **Is the current level of AI risk tolerable to the US public?** (status-quo judgement)
2. **What level of safety does the public expect AI to reach?** (expected-standard judgement)

Both are values questions voters are entitled to answer. The public's job is to *judge*, not to *calculate*.

**Two clusters, matched to their evidentiary weight (per Gradient Institute):**

- **Cluster A — Attitudes and policy preferences.** Concerns, trust, perceived regulatory adequacy, prioritised risks, mitigations, and concrete policy levers. Robust, descriptive, reported directly.
- **Cluster B — Risk tolerance and tradeoffs.** How much risk the public will tolerate, what standard they expect, what they will pay. We do **not** assume a precise latent quantitative risk preference exists to be read off. Consistency checks and cross-mode convergence test that assumption; where it fails, Cluster B is reported as ordinal attitudes, never a single precise number.

---

## 2. Design principles

- **Judgement over generation.** People are poor at producing "1 in 1,000,000" but reasonable at judging a figure handed to them. Recognition beats free recall.
- **Triangulation.** Each underlying question is asked several ways (status-quo recognition, relative-standard anchoring, DCE, direct elicitation). A conclusion that survives all of them survives whichever method a given critic distrusts.
- **Scope sensitivity, measured within subjects.** Probability and severity vary within person, so we can estimate each respondent's scope slope and test whether risk literacy predicts it (Benjamin Reid's thesis). Order is randomised with a between-subjects cross-check to guard against demand-driven consistency.
- **Neutral framing.** No wording that primes acceptance or reads as advocacy; every cited source is named.
- **Unprimed where it matters.** The reverse-halo (AI-label) experiment runs **first**, before anything reveals the survey is about AI; the intro is topic-neutral.
- **The output is the gap, not a point estimate.** AI risk estimates sit orders of magnitude above tolerated engineering standards; we report the robust gap, not a single tolerated probability.

---

## 3. Response to reviewer feedback

### Round 1 — Barnett & Delaney (v1 → v2)

| # | By | Comment | Action |
|---|----|---------|--------|
| 1 | OD (+PB) | Don't trust public probabilities; relative comparisons more useful | Demoted direct elicitation to validation; status-quo recognition + relative anchoring are primary |
| 2 | PB | Scope insensitivity (treat 1/100k ≈ 1/10M) | **Measured, not designed away:** within-subjects probability/severity, scope slope × risk-literacy interaction (Ben's thesis), order randomised + between-subjects cross-check |
| 3 | PB | Tolerability Likert = affect, not threshold | Accepted; triangulate, consistency check, counter-message, numeracy moderation |
| 5 | PB | F–N overshoots; may be dismissed | Headline reframed to the robust gap, not a point threshold |
| 7 | OD | Test counter-messages (a16z talking points) | Added randomised message arm (accel / safety / none) before the tolerance block |
| 8 | PB | "All technologies carry risk" framing misleads | Removed from public-facing items |
| 9 | PB | "Negligent" weaker than "Intolerable" | Scale relabelled, monotonic: Acceptable < Tolerable < Intolerable < Unacceptable/illegal |
| 11 | PB | Depends what you call "experts" | Each source named and randomised (LeCun, Altman, Musk, Amodei; superforecasters; XPT) |
| 17 | PB | Ask about non-catastrophic harms too | Added "pace and disruption" tolerability item |

### Ball-style skeptical review (v2 → v3) — objections turned into pre-registered methods

| Objection | Commitment |
|-----------|------------|
| "Advocacy in a lab coat" | **Disconfirmation list pre-registered** (results that would cut against us) + **adversarial review**: a regulation-skeptic and an environment-skeptic review the instrument pre-launch; their critiques are published alongside results |
| Curated alarming anchors | Symmetric anchor pool, LeCun (~0%) to Amodei (25%), reported by anchor |
| ALARP/F–N assumes quantifiability | **Frame-applicability item**; primaries reported separately for those who reject the frame |
| Back-out = false precision | Banded with uncertainty, gated on the cognitive pre-test, multiverse analysis; **never an "N times safer" headline** |
| Opinion is shallow/unstable | Counter-message swing is a primary outcome; durable policy + environment modules publishable on their own |
| Liability options biased | Negligence / duty-of-care middle added |
| State maps over-claim | Minimum effective-sample-per-state rule; MRP validated by posterior predictive checks + leave-one-state-out CV |

### Round 2 — Gradient Institute: Carroll, Reid (Alistair), Caetano (v3 → v4)

| # | Point | Action |
|---|-------|--------|
| 1 | Open with a clear purpose; two question classes | §1 purpose-and-scope split (Cluster A vs B) |
| 2 | Don't assume a latent quantitative preference exists | Stated explicitly; consistency + convergence test it; ordinal reporting where it fails |
| 3 | Define risk precisely (prob × impact; whose risk; control vs application) | Standard definitions in the instrument preface; every Cluster B item labelled; application risks anchored to today's baseline |
| 4 | Define key terms for a lay sample | Plain definitions shown to all; **information-provision experiment** gives a random half the argument and a counter-consideration |
| 5 | Don't conflate conditional with unconditional ("80% support waiting 10 years") | **Strict conditional-reporting rule**; separate unconditional and conditional delay items |
| 6 | A citizens' assembly may beat a poll | **Deliberative mini-public recommended as Phase 2** (complement, not replacement); calibration/info elements brought into the poll |
| 7 | Drop "public want AI 4000× safer" | Removed; qualitative result reported on its own; back-out downgraded to illustration |
| 8 | Figure 11 category error ("systems should be stricter") | Split into stricter **standards** (3a-i) and safer **systems** (3a-ii) |

*(Note: Alistair Reid of Gradient is a different person from Benjamin Reid, whose covariate items appear in Module 9.)*

---

## 4. The instrument

Standard definitions (probability vs impact; personal vs societal; loss-of-control vs application risk, anchored to today's baseline) are shown before any Cluster B item. Order below reflects the **current** fielding order; brackets mark randomisation/logic; long batteries are matrix-sampled (a random 5–8 of each taxonomy per respondent).

### Intro — topic-neutral
Generic framing ("technology and your community"). **Does not mention AI**, so the AI label is not salient before the reverse-halo test.

### Module 8 (Environment) — administered FIRST, unprimed
- **env_label.** A company wants land/power/water for a large facility (few local jobs, serves elsewhere, ~$2,800/resident/yr in tax). Acceptable if it's an **[randomise: AI data centre / manufacturing plant / semiconductor factory / bottling plant]**? *Rationale:* the AI-minus-generic gap, facts held constant, is the AI-specific penalty (reverse halo). Moved to Q1 because by Q8 the survey was obviously about AI, contaminating the contrast.
- **env_reversal.** Masley status-quo reversal: would giving up the ~$2,800 to avoid the externalities be worth it? *Rationale:* same trade, default flipped; the gap vs env_label estimates status-quo bias. (Masley's offset claims are contested, so we test framing, not facts.)
- **env_forgo.** Most revenue/resident you'd give up to avoid such a facility. Compared to the real tax figure.
- **env_attitude.** Worry about AI's energy/water use *(after the label test, so 'AI' isn't primed earlier)*.

### Module 1 — Attitudes (Cluster A)
good/harm; worry about loss of control; trust in companies (safe AI); CAIS extinction-priority statement; too-far/not-far-enough regulating; treaty to ban smarter-than-human AI.

### Information-provision experiment
A random half see a short balanced explanation of loss of control (plus a counter-consideration) before the tolerance block. We report the informed estimate where informed and uninformed diverge.

### Module 2 — Status-quo tolerability (Cluster B, primary)
Tolerability scale: **Acceptable / Tolerable / Intolerable / Unacceptable (should be illegal).**
- **m2_tol_anchor.** Judge a risk level a named figure stated **[randomise anchor: LeCun ~0% … Altman 2% … Musk 10–20% … Amodei 25%; superforecasters; XPT]**. Recognition, not generation; reported by anchor.
- **m2_pace.** Tolerability of the current pace of disruption (non-catastrophic).
- **m2_frame_applicable.** *Some technologies (flying, nuclear) are held to a strict number for how risky they may be. Closer to your view about advanced AI?* → "You can put a number on its risk and hold it to a safety limit too" / "Its risk is too uncertain to put a useful number on" / "Unsure". **Both options matched for length and reading level; the example sits in the stem so neither is easier to pick.**

### Module 3 — Expected standard (Cluster B, primary)
- **3a-i (standards).** Compared with the *regulations* on [randomise comparator], AI regulation should be much stricter … much less strict.
- **3a-ii (safety).** Compared with how safe [comparator] is *in practice*, AI systems should be much safer … much less safe. *Splitting standards from safety fixes the Figure-11 category error.* Back-out to an implied F–N band is illustrative only, gated on the cognitive pre-test, never an "N times safer" headline.

### Module 4 — Quantitative core: the public number
- **DCE (primary).** Choose between two AI-future options + a "keep status quo" opt-out, ~10 tasks. Attributes = **safety** (annual chance of a catastrophe, 1 in 100 → 1 in 1,000,000), **utility** (modest/major/transformative), **competition** (others lead / keep pace / US leads), **cost** ($0/$100/$400/$1,000). Catastrophe = 100,000+ deaths, **severity fixed** (scope handled in the grid). Mixed logit recovers the acceptable risk by benefit scenario (with CIs) and WTP. *Grid + analysis in `sara_dce_design.R`; identification confirmed by simulation.*
- **m4b_reasonable.** Direct single-shot "highest reasonable annual chance of a 100,000-death disaster" — secondary cross-check (RAISE Act "unreasonable risk").
- **m4c (scope, within-person).** Tolerability of a fixed 100,000-death disaster at **1 in 1,000 / 1 in 100,000 / 1 in 10,000,000 per year** — rows **two orders of magnitude apart** so scope-insensitive respondents are clearly distinguishable. Natural frequencies, no percentages; order randomised; between-subjects cross-check. This is Ben's scope instrument and the DCE's convergence cross-check.

**Convergence go/no-go.** A quantitative public number is reported only if the DCE and m4c agree within ~1 order of magnitude in an overlap subsample. Otherwise: a bound + qualitative finding. Pre-registered.
**Multiplier governance.** Expert ÷ public is computed only on a pass, as a distribution with CIs, conditioned on a benefit scenario, uncertainty propagated both sides, never via the Module 3 back-out.

### Module 5 — Costed tradeoffs
- **m5_wtp.** Most you'd pay/yr to cut catastrophe risk 1-in-20 → 1-in-100. **Log scale** ($0 / $1–10 / $10–100 / $100–1,000 / $1,000–10,000 / >$10,000), because WTP is roughly log-normal; cross-check to the DCE cost coefficient (which is the primary WTP). Not a free-text box (protest zeros, outliers).
- **m5b_delay_uncond / m5b_delay_cond.** Unconditional support for delay, and the conditional version (5%→1%) reported separately with its condition stated.
- **m5_race.** Conditional slowdown that lets others catch up but cuts risk — the competition tradeoff as a direct item.

### Module 6 — Mitigations, priorities, policy (Cluster A)
- **Mitigations battery** ("I'd trust AI more if…"): AISI, pre-deployment testing, audits, 72-hr incident reporting, liability, emergency shutdown that *genuinely reduces risk*, content labelling. Random 5–8 shown.
- **Priority-risks battery** ("government should focus regulation on…"): scams/NCII, manipulation, cyber, bio/chem, loss of control, jobs, privacy (International AI Safety Report taxonomy, plain English). Random 5–8.
- **Policy items:** certification (companies/government/third-party/none); federal vs state; emergency kill switch; **liability** (strict / negligence–duty-of-care / broke-a-rule / none-if-compliant / unsure).

### Module 7 — Validation
Bidirectional attention checks; within-person consistency check; **superintelligence statement [randomise Stem A campaign wording vs Stem B permission framing → wording effect]**; authenticity check (free-text, no AI tools); the counter-message arm (accel / safety / none) precedes the tolerance block.

### Module 9 — Individual differences & demographics
CRT (Benjamin Reid's items, e.g. the pig problem); Berlin-style numeracy / risk literacy; 7-point political orientation (Jost 2006); AI familiarity (frequency of use; Gillespie et al. 2025); age, gender, education, **state** (for MRP), household income (covariate for WTP). Covariates moderate, never exclude.

---

## 5. Quality control, pre-registration & analysis

- **Cognitive pre-test** (8–10 interviews): comprehension of the tolerability scale and whether "stricter" reads as monotonic in risk (the back-out depends on it). Plus the 20-person timing pilot. **No test-retest wave.**
- **Comprehension scoring:** exclude attention-check failures; consistency flags; numeracy retained as a moderator.
- **Primary analysis:** Goal 1 = share judging the status quo intolerable+ by anchor; Goal 2 = expected-stringency distribution + illustrative F–N band; DCE acceptable risk by scenario with CIs.
- **DCE:** mixed logit / hierarchical Bayes; acceptable risk where deploy-utility = opt-out-utility; WTP from the cost coefficient; per-respondent posteriors feed the literacy interaction.
- **Scope sensitivity:** within-person tolerability slope across probability and severity; **risk-literacy × scope interaction** (Ben's thesis); within- vs between-subjects cross-check for demand effects.
- **Pre-registered robustness:** counter-message effect (primary); numeracy moderation; convergence across modes; multiverse / specification-curve for the back-out and thresholds.
- **Reporting rules:** conditional stays conditional (the condition stated verbatim); no manufactured multipliers; Cluster A and B reported separately; informed estimate is the headline where it diverges from uninformed.
- **Sampling/weighting:** power analysis for every contrast incl. the mixed-logit DCE (oversample the risk module); MRP validated by posterior predictive checks + leave-one-state-out CV; **no state map unless the effective per-state sample clears the pre-registered threshold.**
- **Open science:** instrument, raw data, weighting syntax, analysis code published; deviations logged.
- **Adversarial review** (the strongest credibility move): skeptics from both sides review pre-launch; their unedited critiques are published with the results.
- **Phase 2 (recommended):** a representative deliberative mini-public for considered tolerance judgements — complement, not replacement.

---

## 6. Dumpster — considered, not asking

| Item | Why cut |
|------|---------|
| Icon arrays | Bias judgements upward; kept only as a randomised arm to measure that bias |
| Societal-risk verbal anchors ("1 in 100 = a pandemic") | Confused Australian respondents; replaced by familiar-technology comparators |
| Micromorts | Not clearly validated/intuitive for a general US sample |
| "All technologies carry residual risk" preamble | Primes acceptance; imports a wrong "last order of magnitude" frame for AI |
| Off-the-shelf scales (AIAS-4, GAAIS, GRIPS, DOSPERT) | Measure general attitudes/trait risk, not AI-specific tolerance; can't build an F–N curve |
| "4000× safer" multiplier from a qualitative item | Conflates a qualitative answer with expert estimates (Gradient #7) |
| Direct "do you support SB 53 / the RAISE Act" | Reads as advocacy; we ask the underlying values question instead |
| Test–retest recontact wave | Dropped on cost; consistency handled within-survey |
| "I'd pay whatever it takes" WTP option | Strategic and unbounded; breaks the scale |

---

## 7. Provenance

- Supersedes v5/v4.1/v4/v3/v2 Word docs and the archived Nov-2025 draft (all retained in this folder).
- Round 1: Peter Barnett, Oscar Delaney (Dec 2025). Round 2: Gradient Institute — Liam Carroll, Alistair Reid, Tiberio Caetano (24 Nov 2025). The "skeptical reviewer" is a reconstruction of a Dean-Ball-style critique, not a quotation.
- Added measures from Benjamin Reid, *Additional Questions for SARA*.
- Environment module after Andy Masley, *A simple trick to fix the data center debate* (blog.andymasley.com, Jun 2026); offset claims contested, treated as framings to test.
- Companion files: `SARA USA — full survey prototype.html` (clickable instrument), `sara_dce_design.R` (DCE design + analysis).
