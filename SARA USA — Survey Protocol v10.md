# SARA USA 2026: Plan and Survey Protocol (v10)

**Survey Assessing Risks from AI 2026**
**v10, 26 June 2026**

> "Hadfield argues that governance of any complex technology implicates two distinct types of question: first, democratic questions: what kinds of deception by AI developers count as unfair? **What tradeoffs between utility, safety, and competition does the polity wish to make? What level of catastrophic risk are we willing to tolerate?**"
> Dean W. Ball, *Leviathan Waking*, Hyperdimensional.[^ball]

This survey aims to fill what Hadfield and Clark call the *democratic deficit*: the values-based decisions that shape AI "must be made by democratically accountable public, not private, actors."[^clark] As is, it not clear what level of risk the public is willing to tolerate. It does not aim to have the public estimate the actual risk or prescribe mitigiations[^1], but to judge how much risk the public will tolerate (a values question the public is entitled to answer).

---

## 1. How to read this document

| Section | What it covers |
|---|---|
| [§2](#2-the-problem-you-cannot-just-ask) | Why we need to triangulate: it's hard to ask "what risk is tolerable?" |
| [§3](#3-the-core-four-ways-to-triangulate-risk-tolerance) | Four ways we triangulate risk tolerance, each with its literature, strengths, limitations, our response, and a worked example item. |
| [§4](#4-moderators-who-we-measure-and-why) | Moderators to explore. |
| [§5](#5-estimating-the-population-view-mrp) | Estimating the *population* view using MRP. |
| [§6](#6-how-much-does-opinion-move-with-framing) | Testing how opinion moves with framing. |
| [§7](#7-secondary-modules-not-about-risk-tolerance) | Secondary modules not about risk tolerance: the superintelligence ban (the data-centre module was cut to the dumpster, Appendix C). |
| [§8](#8-criticisms-and-our-responses) | Criticisms and tentative responses: one table for what we have resolved, one for what we have not. |
| [§9](#9-open-questions-to-settle) | Open questions we still need to settle. |
| Appendices | [A](#appendix-a-full-fielding-order-and-demographics) fielding order, [B](#appendix-b-dce-design-and-analysis-summary-of-sara_dce_designr) DCE design, [C](#appendix-c-the-dumpster-considered-deliberately-not-asking) dumpster, [D](#appendix-d-provenance-and-sources) provenance. |

---

## 2. The problem: you cannot just ask

The obvious survey is one question: "What annual chance of an AI catastrophe is acceptable?" This would be unlikely to work for several reasons:

**People are unreliable with probabilities.** Asked the chance of getting two heads from two coin tosses, only 52% of UK MPs answered correctly.[^rss] If the people who write the laws cannot do two coin flips, a general-population sample will not respond meaningfully with "1 in 1,000" versus "1 in 1,000,000."

**People are scope insensitive.** Many respondents treat 1 in 1,000 and 1 in 1,000,000 as the same feeling of "small," so a single elicited number reflects affect, not a considered threshold.

**People are framing sensitive.** The same question shifts with wording, anchors, and who is quoted. Because some faming is often necessary, this is an effect we want to quantify, rather than something we can eliminate (see §6).

**So we plan to trianguate rather than trusting any single method.** We plan to assess risk tolerance in four different ways. A conclusion that survives all four survives whichever method a given critic distrusts. Where the methods converge, we increase our confidence in the estimate. Where they diverge, we plan to report bounds and qualitative findings. Together, we hope the methods assess the gap between what experts estimate and what the public will tolerate.

---

## 3. The core: four ways to triangulate risk tolerance

The four methods run from least anchoring to most. We start by asking for the respondent's own number with nothing shown to them, then infer a number from their choices, then offer familiar comparators, and only at the end reveal what named experts have said. Ordering them this way keeps the more suggestive figures from contaminating the unanchored estimate, both in this document and in the fielding sequence (Appendix A). Each subsection gives the approach in plain English, the literature behind it, its strengths and limitations, how we respond to those limitations, and a worked example with the real response scale.

### 3.1 Method 1: Ask directly, then test whether the answer is real

**The approach.** We ask people directly for the highest risk they will accept, but build in a test of whether the answer means anything. We ask it across a *severity ladder*, from a single death up to a global catastrophe (around one in ten people), and read off the highest annual chance the respondent will accept at each rung. The key test is *scope sensitivity*: a considered answer demands a lower acceptable chance as the outcome gets worse, so an answer that stays flat across the ladder is affect, not a threshold. This yields each person's stated frequency-number (F–N) curve. We also collect willingness-to-pay on a log scale.

**Why it is worth doing.** It is the most legible method ("the public's own number"), it provides the within-person scope slope that no other method gives, and it is the convergence cross-check for the discrete choice experiment. I have an honors student checking how scope sensitive people are, and who is more scope sensitive.

**Informing literature.** Scope-insensitivity and embedding effects (contingent-valuation literature, Kahneman & Knetsch). Willingness-to-pay is roughly log-normal, which dictates a log response scale rather than a free-text box.

**Strengths.** Directly interpretable; yields the per-person scope slope; cheap; the natural convergence test for the DCE.

**Limitations.** Most exposed to scope insensitivity ("1 in a million for everything"), to protest zeros and outliers in WTP, and to demand effects if the ladder rows are seen in an obvious order.

**How we respond.** We measure scope sensitivity instead of designing it away: severity varies *within person* across the ladder (a single death up to a global catastrophe) and the respondent sets the highest acceptable annual chance at each rung, so an insensitive respondent (flat across the ladder) is clearly distinguishable; row order is randomised, and a between-subjects arm cross-checks for demand effects. We interact the per-person scope slope with risk literacy (Ben's thesis). WTP uses a bounded log scale (not free text) to tame protest zeros and outliers, and the DCE cost coefficient is the *primary* WTP, with this item as the cross-check.

**Worked example items.**

> **(a) Highest acceptable risk, by outcome (the public's stated F–N curve).** For each outcome, what is the highest chance *per year* you would find acceptable for AI systems to cause it?
>
> | Outcome | Highest acceptable annual chance |
> |---|---|
> | A single death | _(select)_ |
> | 100+ deaths or serious injuries, or $1 billion in damage | _(select)_ |
> | 1,000,000+ deaths or $100 billion in damage | _(select)_ |
> | ~800,000,000 deaths, about 10% of humanity | _(select)_ |
>
> Every row uses the same scale: 1 in 10 / 1 in 100 / 1 in 1,000 / 1 in 10,000 / 1 in 100,000 / 1 in 1,000,000 / 1 in 10,000,000 / 1 in 1,000,000,000 / Should never be allowed.
> *(Respondents see only the plain outcome wording above; the source anchors behind each rung — RAISE Act "critical harm", MIT AI Risk Repository "catastrophic", and FRI/XPT "catastrophe"[^catdef][^fri] — are internal and never shown. Severity rises down the ladder, so a considered respondent's acceptable chance should fall; one who picks the same chance regardless of severity is flagged scope-insensitive. Row order randomised. This traces each person's stated frequency-number, F–N, curve and is the stated-preference cross-check on the DCE's revealed surface, §3.2.)*
>
> **(b) Willingness to pay (log scale).** What is the most you would be willing to pay each year, through higher prices and taxes, to cut the annual chance of an AI catastrophe from 1 in 20 to 1 in 100?
> ◯ $0  ◯ $1–10  ◯ $10–100  ◯ $100–1,000  ◯ $1,000–10,000  ◯ More than $10,000

### 3.2 Method 2: Reveal preferences through choices (the discrete choice experiment)

**The approach.** Instead of asking what risk is tolerable, we show people pairs of realistic AI futures that differ on a few attributes and let them choose. From their choices we *infer* the tradeoffs they are actually willing to make, including the annual catastrophe risk at which they would rather keep today's status quo than accept a new AI future. This is the quantitative core, and it recovers a number without ever asking for one.

**Why it is worth doing.** It gives revealed preferences rather than stated ones. People reveal what they will trade off (safety against utility, cost, and global competitiveness) the way they reveal preferences when shopping, which is harder to game and less prone to "I'll just say one in a million for everything."

**Informing literature: the DCE methods canon.** Mike asked specifically that the established DCE desiderata sit here. The relevant guidance:

- **Lancsar & Louviere (2008)**, *Conducting Discrete Choice Experiments to Inform Healthcare Decision Making: A User's Guide*, PharmacoEconomics 26(8):661–677. The standard practitioner walkthrough.[^lancsar]
- **ISPOR good-research-practice trilogy.** Bridges et al. (2011), the **10-item conjoint-analysis checklist**, Value in Health 14(4):403–413;[^bridges] Reed Johnson et al. (2013) on **experimental design**, Value in Health 16(1):3–13;[^johnson] Hauber et al. (2016) on **statistical analysis** of DCEs, Value in Health 19(4):300–315.[^hauber]
- **Soekhai et al. (2019)**, *Discrete Choice Experiments in Health Economics: Past, Present and Future*, PharmacoEconomics 37:201–226. The comprehensive recent review.[^soekhai]

**SARA's DCE against the ISPOR checklist:**

| Checklist step (Bridges et al. 2011) | What SARA does |
|---|---|
| 1. Well-defined research question, conjoint appropriate | Yes: acceptable annual catastrophe risk by severity, and the severity/probability/utility/competition/cost tradeoff. |
| 2. Attributes and levels justified | 5 attributes: **severity** (the catastrophe ladder below, a single death → ~800,000,000 deaths),[^catdef] **probability** (annual chance of that catastrophe, 1 in 100 → 1 in 1,000,000), **utility** (modest / major / transformative), **competition** (others lead / keep pace / US leads), **cost** ($0 / $100 / $400 / $1,000 per household per year). Severity is varied, not fixed, so the design traces the full frequency-severity (F–N) surface rather than a single hard-coded 100,000-death point. |
| 3. Construction of choice tasks | Two unlabelled AI-future options plus a "keep today's status quo" opt-out, ~10 tasks per respondent. |
| 4. Experimental design (efficiency) | Bayesian D-efficient design, 10 blocks, 4,000 respondents; level balance and overlap checked. Fielded in waves with **population-level sequential re-optimisation**: priors are refreshed from accumulated data at fixed checkpoints (see "Population-level sequential design" below and Appendix B). |
| 5. Preference elicitation format | Forced choice among A / B / opt-out. |
| 6. Instrument design and data collection | Blocked versions; plain natural-frequency risk labels; oversample the risk module. |
| 7. Statistical analysis | Mixed logit / hierarchical Bayes; random coefficients on the risk slope and cost; per-respondent posteriors feed the literacy interaction. |
| 8 & 9. Results, conclusions, reporting | Acceptable risk reported as a *distribution with credible intervals by benefit scenario*, never a point; WTP from the cost coefficient; identification confirmed by simulation (seed 7, coefficients recovered to within ~0.03). |

**Severity ladder (the varied catastrophe attribute).** Severity is one level of a ladder, never a single fixed definition; RAISE/SB 53 is the legal baseline.[^catdef]

| Severity level | Concrete wording shown to respondents | Why this level |
|---|---|---|
| A single death | A single death | Lower anchor for the F–N curve |
| Critical harm | 100+ deaths or serious injuries, or $1 billion in damage | RAISE Act "critical harm" legal anchor[^catdef] |
| Catastrophic | 1,000,000+ deaths or $100 billion in damage | MIT AI Risk Repository "catastrophic" threshold[^catdef] |
| Global catastrophe | ~800,000,000 deaths, about 10% of humanity | FRI/XPT "catastrophe"[^fri] |

**Strengths.** Revealed not stated preferences; recovers a defensible number with intervals; lets us read off willingness-to-pay and the competition tradeoff directly; resistant to scope-insensitivity gaming because risk trades against other attributes.

**Limitations.**
- **Combinatorial size.** Mike's worry: with several attributes at several levels the full factorial is large (now 4 × 5 × 3 × 3 × 4 = 720 profiles once severity is varied), and pairwise comparisons explode. You cannot show one person everything.
- **Cognitive load.** Ten multi-attribute choices is near the upper end of what a general sample handles well.
- **Hypotheticality.** Stated-choice futures are still hypothetical, even if the format is choice-based.

**How we respond.** We do **not** show every cell to every person. A Bayesian D-efficient design selects an efficient subset, split into 10 blocks, so each respondent sees ~10 well-chosen tasks while the *sample* identifies all tradeoffs. Severity is a varied attribute (the ladder above), so the DCE traces an F–N surface rather than a single point; the cost is power spread across the larger grid, which the 4,000-respondent sample and an efficient design must absorb. The §3.1 severity-ladder elicitation (a stated F–N curve) stays as the cheaper stated-preference cross-check. We confirmed by simulation that this attribute structure identifies the coefficients and WTP. And the DCE number must agree with the direct method (§3.1) within about one order of magnitude before we report any single public number (the convergence go/no-go, §5).

**Population-level sequential design (adaptive priors).** Adding severity enlarges the grid from 180 to 720 profiles, so a design built on *guessed* priors spreads its power thinly and may concentrate it in the wrong region — public AI-risk tolerance is close to unknown going in. We therefore field in waves and let the **population-level** priors adapt to the data, while holding each respondent's instrument fixed:

1. **Pilot wave** (~500 respondents) on a Bayesian D-efficient design built from diffuse priors (or the 2025 estimates where available).
2. At fixed sample checkpoints, re-estimate the population coefficients (mixed logit, `logitr`) and regenerate the Bayesian D-efficient design (`cbcTools`) using the posterior mean and covariance as the new priors.
3. **Main waves** (~3 waves of ~1,170) field the current design; the design is *locked within a wave*.
4. Lock the design permanently after the final checkpoint; cap the total at 4,000.

The adaptation is **between-respondent only**: it sharpens *which* tradeoffs the next wave sees, never *how* an individual is questioned mid-session. This buys the efficiency and prior-robustness of adaptivity while avoiding the costs of individual-level adaptation — no within-respondent endogeneity, no response-noise chasing, and a fixed, explainable instrument for any given person. Because task selection depends only on past *observed* choices, the adaptive sampling is ignorable for the mixed-logit/HB likelihood, so the pooled estimate stays consistent; we report design-wave as a robustness control. The whole loop is a **pre-registered, deterministic algorithm** — fixed model specification, fixed D-efficiency criterion, fixed seeds, fixed checkpoint sizes, with the design updated only if it improves the Bayesian D-error — so no analyst discretion enters (full specification in Appendix B). **The §3.1 direct elicitation is held fully static**, preserving one fixed, non-adaptive instrument so the convergence cross-check (§5) rests on a clean comparison.

**Worked example choice task.**

> Here are two possible futures for advanced AI. Which do you prefer? (You may also choose to keep today's situation.)
>
> | | **Option A** | **Option B** | **Keep today's status quo** |
> |---|---|---|---|
> | Worst catastrophe it could cause | 100+ deaths or $1B damage | 1,000,000+ deaths | (as today) |
> | Annual chance of that catastrophe | 1 in 10,000 | 1 in 1,000,000 | (current trajectory) |
> | What AI can do for society | Transformative | Modest | (as today) |
> | Global competition | US leads | Others lead | (as today) |
> | Cost to your household per year | $400 | $1,000 | $0 |
>
> ◯ Option A  ◯ Option B  ◯ Keep today's status quo
> *(Repeated for ~10 tasks with different attribute levels.)*

### 3.3 Method 3: Anchor to the safety we already accept

**The approach.** Rather than ask for an absolute number, we ask the public to place AI *relative to industries whose risk we already tolerate*: nuclear power, commercial aviation, new pharmaceuticals, cars, dams. Should AI be held to a stricter standard, the same, or a looser one? This converts an impossible absolute judgement into a familiar comparison.

**Why it is worth doing.** It uses the public's lived intuitions about which activities society already keeps very safe (flying) and which it lets run hotter. It also lets us "back out" an implied risk band for AI from the band society tolerates for the comparator, as an illustration only.

**Informing literature.** The ALARP / "as low as reasonably practicable" and F–N (frequency–number) curve traditions in engineering safety (nuclear, rail, chemical). These give the comparator standards. We treat them as benchmarks the public can react to, not as ground truth for AI.

**Strengths.** Comparative judgements are far easier and more stable than absolute ones; the comparators are concrete and familiar; the result maps onto how regulators actually argue.

**Limitations.**
- **Category error.** "AI should be *stricter*" can mean stricter *rules* or safer *outcomes*. v7 split these into two items (standards vs safety-in-practice) after Gradient flagged the Figure-11 conflation.
- **The denominator problem (the big one).** "One death per what?" Expert AI risk figures are about the *whole technology*, the equivalent of every nuclear reactor or every flight worldwide, not a single unit. A naive comparison to "a plane crash" is apples to oranges. We make it apples to apples by specifying the comparator at the *industry* level (all reactors, the whole aviation system), matching the scope of the AI estimate.
- **Quantifiability.** Some respondents reject the premise that AI risk can be put on a number at all. We must not force them onto a scale they reject.

**How we respond.** Two separate items (rules vs outcomes); comparators specified at industry scope to fix the denominator; a *frame-applicability* item that lets people say "AI's risk is too uncertain to put a number on," with primaries reported separately for those who reject the frame; and a dangerous-activity sanity anchor at the risky end (BASE jumping, Everest) so we can confirm people can place AI across the full range. Any F–N back-out is illustrative, gated on the cognitive pre-test, and never published as an "N times safer" headline.

**Worked example items.**

> **(a) Standards.** Compared with how strictly the US government regulates **[randomise: nuclear power / commercial aviation / new prescription drugs / cars / large dams]**, regulation of advanced AI should be:
> ◯ Much less strict  ◯ Somewhat less strict  ◯ About the same  ◯ Somewhat stricter  ◯ Much stricter
>
> **(b) Safety in practice.** Compared with how safe **[same comparator]** is *in practice today*, advanced AI systems should be:
> ◯ Much less safe  ◯ Somewhat less safe  ◯ About as safe  ◯ Somewhat safer  ◯ Much safer
>
> **(c) Frame-applicability.** Some technologies (flying, nuclear power) are held to a strict number for how risky they are allowed to be. Which is closer to your view about advanced AI?
> ◯ "You can put a number on its risk and hold it to a safety limit too"
> ◯ "Its risk is too uncertain to put a useful number on"
> ◯ Unsure
> *(Both options matched for length and reading level; the example sits in the stem so neither option is easier to pick.)*
>
> **(d) Sanity anchor.** Compared with a high-risk voluntary activity **[randomise: bungee jumping, BASE jumping, climbing Everest]**, how safe should advanced AI be? *(Almost everyone should say "much safer"; anyone who does not is flagged. Comparator death rates are approximate and must be verified before fielding.)*

### 3.4 Method 4: Judge a named expert's number

**The approach.** We hand the respondent a risk figure that a named, real person has stated publicly, and we ask whether that level is acceptable. Because the number is recognised rather than generated, the respondent does the one thing they are good at: judging. We randomise which source they see, across a pool spanning the full range of stated views.

**Why it is worth doing.** This is the method that speaks most directly to policy. It does not set the public's risk tolerance in the abstract; it tests whether the *current* expert estimates fall inside or outside that tolerance. If most of the public calls Amodei's stated figure "unacceptable, should be illegal," that is a finding lawmakers can act on without anyone first agreeing on the true probability.

**Informing literature.** Anchoring and recognition-over-recall (Kahneman & Tversky). The named-source design also answers Barnett's objection that "it depends what you call an expert": we never say "experts," we name the individual and report by source.

**Strengths.** Recognition not generation; directly decision-relevant; robust to the "who counts as an expert" critique because every anchor is attributed.

**Limitations.** (a) Anchoring: people may cluster around whatever number they are shown. (b) The figures must be real and fairly quoted, or the whole item is indefensible. (c) A tolerability rating can still be affect ("I dislike AI") rather than a considered threshold.

**How we respond.** We use a *symmetric* anchor pool, from roughly 0% (LeCun) to 25% (Amodei), plus superforecasters and the Existential Risk Persuasion Tournament (XPT), and we report results *by anchor* so any anchoring effect is visible rather than hidden. Every figure is verified against a citable public statement before fielding (see the flag below). And this method is only one of four; if affect were driving it, the choice-based method (§3.2) would not agree.

**Worked example item.**

> Dario Amodei, CEO of the AI company Anthropic, has said there is roughly a **1 in 4 (25%) chance** that advanced AI leads to a catastrophe killing a large fraction of humanity.
> In your view, accepting a 25% chance of that outcome would be:
> ◯ Acceptable  ◯ Tolerable  ◯ Intolerable  ◯ Unacceptable (should be illegal)
>
> *[Randomise the source and figure across: Yann LeCun (~0%), Sam Altman (~2%), Elon Musk (~10–20%), Dario Amodei (~25%), the median superforecaster, the XPT median. Report by anchor.]*

> **Field flag.** Every named figure above is illustrative and must be replaced with an exact, citable quotation (source, date, wording) before fielding. Do not field a number we cannot source. This is non-negotiable given the named-attribution design.

### A note on the tolerability scale

All Cluster B items use one monotonic four-point scale: **Acceptable < Tolerable < Intolerable < Unacceptable (should be illegal).** An earlier draft used "negligent / grossly negligent." Barnett pointed out that "negligent" reads as *weaker* than "intolerable," breaking monotonicity, so the scale was relabelled. We mention this because it is a case where a reviewer's small wording point changed the instrument.

---

## 4. Moderators: who we measure, and why

These are viables to measure and control for, rather than for exluding participats. Covariates moderate the estimate and let us ask whether, for example, young people are less tolerant of low-probability futures that foreclose the long-term future. Default analysis enters them as controls or via MRP (§5) so the headline is a population estimate net of sample composition.

- **Demographics for weighting.** Age, gender, education, income, state, all aligned to US Census / ACS categories so they post-stratify to population controls (see Appendix A for the exact brackets).
- **AI familiarity.** Frequency of intentional AI use (Gillespie et al. 2025; item validated as a proxy for technology experience per Hargittai 2005).[^gillespie]
- **Political orientation.** 7-point Very Liberal to Very Conservative (Jost 2006).[^jost]
- **Risk literacy / numeracy.** Berlin Numeracy Test style items. The key interaction for one of my honours students projects: does higher risk literacy reduce increase scope sensitivity?

---

## 5. Estimating the population view (MRP)

A convenience or panel sample is not the US public. We use **multilevel regression and post-stratification (MRP)**: model the outcome with demographic and geographic predictors, then re-weight model predictions to ACS population counts to recover the population-level risk tolerance (and, if the per-state effective sample is large enough, state-level estimates). MRP is validated by posterior predictive checks and leave-one-state-out cross-validation. **No state map is published unless the effective per-state sample clears a pre-registered threshold.**

**Convergence go/no-go (pre-registered).** A single quantitative public number is reported only if the DCE (§3.2) and the direct scope instrument (§3.1) agree within about one order of magnitude in an overlap subsample. If they diverge, we report a bound plus a qualitative finding. The expert-to-public multiplier, if reported at all, is computed only on a pass, as a distribution with credible intervals, conditioned on a stated benefit scenario, with uncertainty propagated on both sides. We never manufacture an "N times safer" headline from the §3.3 back-out.

---

## 6. How much does opinion move with framing?

Critics say poll answers are shallow and shift with messaging. Rather than pretend otherwise, we make the swing a primary outcome.

- **Counter-message arm.** Before the tolerance block, a random third see accelerationist talking points (a16z style), a random third see safety talking points, and a third see none. The swing in tolerance is a headline result. (Requested by Delaney.)
- **Information-provision experiment.** A random half see a short, balanced explanation of loss-of-control risk plus a counter-consideration. Where informed and uninformed answers diverge, the *informed* estimate is the headline.
- **Superintelligence-statement wording experiment (Muskan's).** The same statement is shown in two framings (Stem A: campaign / petition wording; Stem B: a neutral permission framing), randomised, to isolate the wording effect on agreement.
- **Argument vs social proof (proposed decomposition).** Mike's question: when framing moves people, is it the *content* of the argument or the *social signal* (for example, "Prince Harry signed it")? Proposed design: cross the argument (present / absent) with a prestige-signatory cue (present / absent) so we can attribute any movement to the substance or to the social proof. **This is a proposed addition; flag for sign-off (§9).**

---

## 7. Secondary modules (not about risk tolerance)

These two modules are deliberately kept separate from the triangulation core because they answer different questions.

### 7.1 The superintelligence ban / treaty

At least one item captures support for halting or banning development of smarter-than-human AI. We field the CAIS-style extinction-priority statement and a "treaty to ban smarter-than-human AI" item, with the wording experiment in §6 applied to the superintelligence statement. Reported descriptively (Cluster A), with the framing sensitivity reported alongside.

### 7.2 Data centres and the environment (reverse-halo) — moved to the dumpster (29 Jun 2026)

Cut from the live instrument and parked in Appendix C. The module measured an AI-specific affective penalty (a reverse halo) by randomly describing an identical facility as an AI data centre or a generic plant, with status-quo-framing (after Masley) and revenue-forgone follow-ups, fielded first so the AI label was not primed. It was dropped against the survey's length budget: none of its three candidate justifications — a predictive covariate for risk tolerance, a halo control, or a standalone framing experiment — clearly earned its place, and Mike's own note was that the items' decision relevance was unclear. The first-fielding / un-priming rationale lapses with the cut. Recoverable as a standalone study (see Appendix C).

---

## 8. Criticisms and our responses

### 8.1 Resolved or actioned

| # | Reviewer | Criticism | Our response |
|---|---|---|---|
| 1 | Oscar Delaney (+Barnett) | Don't trust public probabilities; relative comparisons are more useful | Direct elicitation demoted to a validation cross-check; named-expert recognition (§3.4) and relative-standard anchoring (§3.3) are primary |
| 2 | Peter Barnett | Scope insensitivity (treat 1/100k ≈ 1/10M) | **Measured, not designed away:** within-person probability/severity, scope-slope × risk-literacy interaction, rows two OOMs apart, order randomised + between-subjects cross-check (§3.1) |
| 3 | Peter Barnett | Tolerability Likert = affect, not a threshold | Accepted; triangulated across four methods, consistency-checked, counter-messaged, numeracy-moderated |
| 4 | Peter Barnett | F–N overshoots and may be dismissed | Headline reframed to the robust *gap*, not a point threshold; back-out is illustrative only |
| 5 | Peter Barnett | "All technologies carry risk" framing misleads | Removed from public-facing items (it imports a wrong "last order of magnitude" frame) |
| 6 | Peter Barnett | "Negligent" is weaker than "Intolerable" | Scale relabelled to a monotonic Acceptable < Tolerable < Intolerable < Unacceptable |
| 7 | Peter Barnett | Depends what you call "experts" | Every source named and randomised (LeCun, Altman, Musk, Amodei; superforecasters; XPT); reported by anchor (§3.4) |
| 8 | Oscar Delaney | Test counter-messages (a16z talking points) | Added a randomised message arm (accel / safety / none) before the tolerance block (§6) |
| 9 | Peter Barnett | One attention check should be "more strict," one "less strict" | Bidirectional attention-check pair, embedded next to the comparative-standard items so it blends in |
| 10 | Barnett / Delaney | Give people a neutral intuition for risk levels by comparing to other fields | Relative-standards method (§3.3) plus the dangerous-activity sanity anchor |
| 11 | Gradient (Carroll, A. Reid, Caetano) | Open with a clear purpose; two question classes | §1–§2 rewrite; Cluster A (attitudes) vs Cluster B (tolerance) split |
| 12 | Gradient | Don't assume a latent quantitative preference exists | Stated explicitly; convergence test (§5); ordinal reporting where it fails |
| 13 | Gradient | Define risk precisely (prob × impact; whose risk; control vs application) | Standard definitions in the instrument preface; every Cluster B item labelled; application risks anchored to today's baseline |
| 14 | Gradient | Don't conflate conditional with unconditional support | Strict conditional-reporting rule; separate unconditional and conditional delay items |
| 15 | Gradient | A citizens' assembly may beat a poll | Deliberative mini-public recommended as Phase 2 (complement, not replacement) |
| 16 | Gradient | Drop "public want AI 4000× safer" | Removed; back-out downgraded to illustration |
| 17 | Gradient | Figure 11 category error ("systems should be stricter") | Split into stricter *standards* (§3.3a) and safer *systems* (§3.3b) |
| 18 | Ball-style skeptical review (reconstructed) | "Advocacy in a lab coat" | Pre-registered disconfirmation list + adversarial review: a regulation-skeptic and an environment-skeptic review the instrument pre-launch; their unedited critiques are published with the results |
| 19 | Ball-style review | Curated alarming anchors | Symmetric anchor pool (LeCun ~0% to Amodei 25%), reported by anchor |
| 20 | Ball-style review | Liability options biased | Negligence / duty-of-care middle option added |

### 8.2 Open, not yet resolved

| # | Raised by | The criticism (paraphrased, with the live quote in the footnote) | Where we stand |
|---|---|---|---|
| A | Delaney; Barnett agreed | It may not matter what the public thinks here: these are not deeply held beliefs, just numbers people invent when forced, politicians won't weight them, and unless AI becomes personally salient the public won't act on them.[^open1] | **Partially mitigated, not resolved.** We measure stability (counter-message swing, consistency, information effects) and recommend a deliberative Phase 2. But the deeper theory-of-change challenge (does this move decisions?) is unsettled. See §9. |
| B | Barnett | The whole F–N exercise may overshoot: AI risk estimates sit 3–12 orders of magnitude above any tolerated engineering standard, so a precise risk-management chart may "overshoot the graph" and be discounted as absurd.[^open2] | **Partially mitigated.** Headline is now the *gap*, not a point on an F–N curve; the back-out is illustrative only. The residual worry (that the framing invites dismissal) remains. |
| C | Barnett | The method relies on people accurately assessing risks, which they will do badly or with wild optimism (off by OOMs).[^open3] | **Partially mitigated** via recognition-over-generation, the information-provision arm, and numeracy moderation. Not fully closed. |
| D | Liam Carroll (Gradient) | Latent-preference and conditional-vs-unconditional points (mostly actioned in §8.1) plus the standing recommendation that a deliberative process may be the better instrument. | Phase 2 deliberative mini-public recommended; not yet scoped or funded. |

---

## 9. Open questions to settle

1. **Theory of change.** What is the strongest version of "this changes a real decision"? If the honest answer is "it shifts the Overton window and arms regulators with a public number," say so, and design the dissemination around that. (Open item A.)
2. **The overshoot problem.** If the gap is 3–12 OOMs, is the F–N machinery the right vehicle, or does the simpler "the public finds the current trajectory unacceptable" framing land better and dodge the "absurd precision" dismissal? (Open item B.)
3. **Data-centre module.** *Decided (29 Jun 2026): cut to the dumpster (Appendix C); none of the three justifications earned its place against the length budget.*
4. **Cognitive measures (CRT and need for cognition).** Tentatively dropped to the dumpster (Appendix C) on space and weak rationale; revisit only if a collaborator brings a hypothesis the numeracy item cannot test.
5. **Argument vs social-proof decomposition (§6).** Approve, modify, or drop the proposed 2×2.
6. **Convergence failure.** Pre-commit now to exactly what we publish if the DCE and direct methods disagree by more than one OOM (a bound and qualitative finding, with what wording).
7. **Australia replication.** What changes for an AU run: comparators (Australian regulators), the income/ACS analogues (ABS categories), and whether the data-centre module is more relevant there.
8. **Verification before fielding.** (a) Every named-expert figure in §3.4 needs an exact citable quote. (b) The dangerous-activity death rates in §3.3d need checking. (c) Confirm reviewer names: the project documents record **Oscar Delaney** (not "Mollonez"); confirm this is the person Mike meant.
9. **Fielding order vs dropout.** v9 fields the tolerance blocks least-to-most anchoring (§3, Appendix A); confirm this is worth front-loading the harder quantitative items, or move a gentler block first.

---

## Appendix A: Full fielding order and demographics

Order reflects current fielding. Brackets mark randomisation/logic; long batteries are matrix-sampled (a random 5–8 per respondent). Standard definitions (probability vs impact; personal vs societal; loss-of-control vs application risk, anchored to today's baseline) are shown before any Cluster B item.

1. **Information sheet & consent.** UQ Participant Information Sheet (v2.1, ethics 2023/HE002257) and consent ("I consent" / "I do not consent"); a non-consent ends the survey. *(Files: `ethics consent form/`.)*
2. **Intro (topic-neutral).** "Technology and your community." Does **not** mention AI.
3. **Module 1: Attitudes (Cluster A).** Good/harm; loss-of-control worry; trust in companies; CAIS extinction-priority statement; too-far / not-far-enough regulating; treaty to ban smarter-than-human AI.
4. **Information-provision experiment** (random half; §6).
5. **Free number estimation (§3.1).** Fielded first among the tolerance blocks so no figure we show can anchor the respondent's own number: m4b_reasonable (highest reasonable annual risk); m4c severity ladder (within person).
6. **Discrete choice experiment (§3.2).** The DCE, ~10 choice tasks.
7. **Anchor to accepted safety (§3.3).** 3a-i standards; 3a-ii safety-in-practice; m3_sanity dangerous-activity anchor; m3_attention (bidirectional quality check embedded here).
8. **Judge a named expert's number (§3.4).** Fielded last because named figures are the strongest anchors: m2_tol_anchor; m2_pace (tolerability of the current pace of disruption); m2_frame_applicable.
9. **Costed tradeoffs.** m5_wtp (log scale); m5b_delay_uncond and m5b_delay_cond (reported separately); m5_race (conditional slowdown).
10. **Policy (Cluster A).** m6_certify; **m6_faa** (FAA-style mandatory independent pre-release safety testing with government power to block; Anthropic's stated proposal, presented neutrally as "some have proposed"); m6_fedstate (federal pre-emption vs state patchwork); m6_killswitch; m6_liability.
11. **Validation.** Within-person consistency; superintelligence-statement wording experiment (§6); free-text authenticity check (no AI tools); the counter-message arm precedes the tolerance block.
12. **Individual differences and demographics** (§4).

*(The environment / data-centre module was fielded first in v10; cut to the dumpster on 29 Jun 2026 — see Appendix C.)*

**Anchoring note (changed in v9).** The four tolerance blocks are now fielded from least to most anchoring (free estimate, then DCE, then safety comparators, then named-expert figures), matching §3, so an earlier figure cannot anchor a later answer. They sit after the topic-neutral warm-up and the attitude items, so the harder quantitative items are not the respondent's very first task. If you would rather field a gentler block first to cut early dropout, that tradeoff is open (see §9).

**Demographics (US Census / ACS categories; verify against the exact ACS pull before fielding):**
- **Age:** 18–24 / 25–34 / 35–44 / 45–54 / 55–64 / 65–74 / 75+ (ACS B01001, collapsed).
- **Gender:** Male / Female / In another way–non-binary / prefer not to say. Weighting uses ACS sex controls; the extra category is kept descriptively and allocated, not dropped.
- **Education:** < high school / high-school grad / some college, no degree / associate / bachelor's / graduate or professional (ACS B15003, collapsed).
- **Income:** Census/ACS household brackets, < $15k to $200k+ (B19001).
- **State:** all 50 + DC. No state map unless the per-state effective sample clears the pre-registered threshold.

---

## Appendix B: DCE design and analysis (summary of `sara_dce_design.R`)

- **Grid:** severity (4 levels: a single death, critical harm 100+ deaths/$1B, catastrophic 1,000,000+ deaths/$100B, global catastrophe ~800,000,000 deaths),[^catdef] probability (5 levels, annual chance 1 in 100 → 1 in 1,000,000), utility (3), competition (3), cost (4). Full factorial 4 × 5 × 3 × 3 × 4 = 720 profiles. Severity is varied across the four-tier ladder, not fixed; the RAISE Act "critical harm" tier is the legal baseline.
- **Design:** Bayesian D-efficient, 2 alternatives + opt-out, 10 tasks, 10 blocks, 4,000 respondents (oversampling the risk module relative to 2025). Level balance and overlap checked (`cbcTools`).
- **Population-level sequential re-optimisation (pre-registered algorithm):**
  - **Waves:** pilot ~500, then ~3 main waves of ~1,170 (≈4,010 total). Design locked within each wave.
  - **Checkpoints:** at each wave boundary, re-estimate the population coefficients on all data so far (mixed logit, `logitr`, fixed specification, multistart, fixed seed) and regenerate the Bayesian D-efficient design (`cbcTools`, fixed prior-draw count and seed) using the posterior mean and covariance as priors.
  - **Update rule:** adopt the regenerated design only if it lowers the Bayesian D-error versus the incumbent; otherwise keep the incumbent. Design is locked permanently after the final checkpoint; hard cap 4,000.
  - **Why this is not p-hacking:** only the *priors* update — the model, the D-efficiency criterion, the seeds, the checkpoint sizes, and the downstream analysis are all fixed in advance. The algorithm is deterministic given the data; no analyst discretion enters. Task selection depends only on past observed choices, so the adaptive sampling is ignorable for the likelihood and the pooled estimate is consistent; design-wave is reported as a robustness control. §3.1 is held static (non-adaptive).
- **Fielding pipeline:** survey scripted in **GuidedTrack** (code-based; handles block assignment, task-order randomisation, and Prolific completion-code crediting). The adaptive loop runs *off-platform* in R on the droplet — `cbcTools` (design) + `logitr` (estimation) — with the regenerated block design pasted into the GT program between waves. No within-session compute is required (see chat rationale, 29 Jun 2026).
- **Estimation:** mixed logit (`logitr`), random normal coefficients on the log-risk slope and cost; multistart.
- **Recovering the public number:** acceptable annual risk p\* is the level at which an AI-future option equals the status-quo opt-out for a given severity tier, benefit/competition scenario at cost 0; WTP for a 10× risk reduction is the risk coefficient over the cost coefficient. Report p\* as a distribution with credible intervals by scenario, never a point.
- **Identification:** confirmed by simulation (seed 7); coefficients recovered to within ~0.03 of truth.
- **Go/no-go and multiplier governance:** see §5.
- **To update before fielding (26 Jun 2026):** `sara_dce_design.R` still encodes the old single-severity design (catastrophe fixed at 100,000). Add severity as a varied attribute (the four-tier ladder), regenerate the design for the larger 720-profile grid, and re-run the identification simulation. **Also implement the sequential loop (29 Jun 2026):** wrap design generation + `logitr` estimation into the wave/checkpoint procedure above, and extend the identification simulation to confirm the *sequential* procedure recovers the coefficients (not just a one-shot static design).

---

## Appendix C: The dumpster (considered, deliberately not asking)

| Item | Why cut |
|---|---|
| Icon arrays | Bias judgements upward; kept only as a randomised arm to measure that bias |
| Verbal societal-risk anchors ("1 in 100 = a pandemic") | Confused 2024 Australian respondents; replaced by familiar-technology comparators |
| Micromorts | Not clearly validated/intuitive for a general US sample |
| "All technologies carry residual risk" preamble | Primes acceptance; imports a wrong "last order of magnitude" frame for AI |
| Off-the-shelf scales (AIAS-4, GAAIS, GRIPS, DOSPERT) | Measure general attitudes / trait risk, not AI-specific tolerance; can't build an F–N curve |
| "4000× safer" multiplier from a qualitative item | Conflates a qualitative answer with expert estimates (Gradient #16) |
| Direct "do you support SB 53 / the RAISE Act" | Reads as advocacy; we ask the underlying values question instead |
| Test–retest recontact wave | Dropped on cost; consistency handled within-survey |
| "I'd pay whatever it takes" WTP option | Strategic and unbounded; breaks the scale |
| Mitigations battery ("I'd trust AI more if…") | Removed from the live instrument (MN, 17 Jun 2026); the FAA-style item carries the single most important mitigation; the rest are recoverable here |
| Priority-risks battery ("government should focus regulation on…") | Removed from the live instrument (MN, 17 Jun 2026) |
| Cognitive reflection (CRT) battery | Dropped (MN, 26 Jun 2026): too little space and the rationale is too weak to be essential. Overlaps with the numeracy item we keep (same reflective-ability construct, correlations typically r ≈ 0.3–0.5), the classic items are leaked in online panels, and any moderation is likely small. Recoverable if a hypothesis emerges that numeracy cannot test.[^crt] |
| Need-for-cognition short form | Dropped (MN, 26 Jun 2026): a disposition, not an ability; its plausible effect (engaged respondents answer more steadily) is already captured by numeracy; likely small and the rationale is too weak to justify the items.[^nfc] |
| Environment / data-centre module (reverse-halo: env_label, env_reversal, env_forgo, env_attitude) | Dropped (MN, 29 Jun 2026): decision relevance unclear; none of the three justifications (predictive covariate, halo control, or standalone framing experiment) earned its place against the length budget. Fielded-first/un-priming rationale lapses with the cut. Recoverable as a standalone framing study (after Masley, *A simple trick to fix the data center debate*). |

---

## Appendix D: Provenance and sources

- Supersedes v6/v7/v8/v9 (markdown) and the v5/v4.1/v4/v3/v2 Word docs and the archived Nov-2025 draft (all retained in this folder).
- Companion files: `SARA USA — full survey prototype v2.html` (clickable instrument), `sara_dce_design.R` (DCE design + analysis).
- The FAA-model item and cars/airplanes/drugs framing follow Anthropic's public proposal; the contextual EO is the 2 June 2026 White House order *Promoting Advanced AI Innovation and Security* (security-focused, voluntary). **Verify the EO title and date before citing externally.**
- Round 1 reviewers: Peter Barnett, Oscar Delaney (Dec 2025). Round 2: Gradient Institute (Liam Carroll, Alistair Reid, Tiberio Caetano) (24 Nov 2025). The "skeptical reviewer" is a reconstruction of a Dean-Ball-style critique, not a quotation. (Alistair Reid of Gradient is a different person from Benjamin Reid, whose covariate items appear in §4.)
- Added measures from Benjamin Reid, *Additional Questions for SARA*.
- Environment module after Andy Masley, *A simple trick to fix the data center debate* (blog.andymasley.com, Jun 2026); offset claims are contested and treated as framings to test.

[^1]: Those are technical questions for experts

[^ball]: Dean W. Ball, "Leviathan Waking," *Hyperdimensional* (Substack), https://www.hyperdimensional.co/p/leviathan-waking. Ball attributes the framing to Gillian Hadfield's work on regulatory markets.

[^clark]: Gillian K. Hadfield & Jack Clark, "Regulatory Markets: The Future of AI Governance," arXiv:2304.04914 (submitted 11 Apr 2023, rev. 3 Feb 2026); published in *Jurimetrics: The Journal of Law, Science and Technology* 65:195–240 (2026), https://arxiv.org/abs/2304.04914. The paper frames AI governance as facing a "technical deficit" and a "democratic deficit," the latter being that "values-based decisions … must be made by democratically accountable public, not private, actors" (abstract).

[^rss]: Royal Statistical Society, "New RSS survey tests statistical skills of MPs" (2022), https://rss.org.uk/news-publication/news-publications/2022/general-news/new-rss-survey-tests-statistical-skills-of-mps/. Of 101 MPs asked the probability of two heads from two coin tosses, 52% answered 25% correctly, 33% said 50%, 10% didn't know; a 2012 RSS survey found ~40% correct. Reporting: NationalWorld, https://www.nationalworld.com/news/politics/mps-statistics-maths-problem-3564209.

[^lancsar]: Emily Lancsar & Jordan Louviere, "Conducting Discrete Choice Experiments to Inform Healthcare Decision Making: A User's Guide," *PharmacoEconomics* 26(8):661–677 (2008), https://pubmed.ncbi.nlm.nih.gov/18620460/.

[^bridges]: John F. P. Bridges et al., "Conjoint Analysis Applications in Health — a Checklist: A Report of the ISPOR Good Research Practices for Conjoint Analysis Task Force," *Value in Health* 14(4):403–413 (2011), https://pubmed.ncbi.nlm.nih.gov/21669364/. The 10-item checklist; verify the exact item labels against the paper before citing each.

[^johnson]: F. Reed Johnson et al., "Constructing Experimental Designs for Discrete-Choice Experiments: Report of the ISPOR Conjoint Analysis Experimental Design Good Research Practices Task Force," *Value in Health* 16(1):3–13 (2013), https://www.sciencedirect.com/science/article/pii/S1098301512041629.

[^hauber]: A. Brett Hauber et al., "Statistical Methods for the Analysis of Discrete Choice Experiments: A Report of the ISPOR Conjoint Analysis Good Research Practices Task Force," *Value in Health* 19(4):300–315 (2016), https://www.valueinhealthjournal.com/article/S1098-3015(16)30452-1/fulltext.

[^soekhai]: Vikas Soekhai, Esther W. de Bekker-Grob, Alan R. Ellis & Caroline M. Vass, "Discrete Choice Experiments in Health Economics: Past, Present and Future," *PharmacoEconomics* 37:201–226 (2019), https://link.springer.com/article/10.1007/s40273-018-0734-2.

[^crt]: Expanded CRT items per Benjamin Reid, *Additional Questions for SARA*, drawing on "Assessing Miserly Information Processing: An Expansion of the Cognitive Reflection Test," *Thinking & Reasoning* (2013), https://www.tandfonline.com/doi/abs/10.1080/13546783.2013.844729.

[^nfc]: Need-for-cognition: original John T. Cacioppo & Richard E. Petty, "The Need for Cognition," *J. Personality and Social Psychology* 42:116–131 (1982); efficient 6-item form, https://pmc.ncbi.nlm.nih.gov/articles/PMC7545655/: I would prefer complex to simple problems. I like to have the responsibility of handling a situation that requires a lot of thinking. Thinking is not my idea of fun. (R)
I would rather do something that requires little thought than something that is sure to challenge my thinking abilities. (R) I really enjoy a task that involves coming up with new solutions to problems. I would prefer a task that is intellectual, difficult, and important to one that is somewhat important but does not require much thought.

[^jost]: John T. Jost, "The End of the End of Ideology," *American Psychologist* 61(7):651–670 (2006), https://doi.org/10.1037/0003-066X.61.7.651. Source for the 7-point orientation item per Benjamin Reid's notes.

[^gillespie]: Nicole Gillespie, Steven Lockey, T. Ward, A. Macdade & G. Hassed, "Trust, Attitudes and Use of Artificial Intelligence: A Global Study 2025," University of Melbourne (2025), https://doi.org/10.26188/28822919. Frequency-of-use item justified as a technology-experience proxy via Eszter Hargittai, "Survey Measures of Web-Oriented Digital Literacy," *Social Science Computer Review* 23(3):371–379 (2005).

[^open1]: Oscar Delaney (review comment, Dec 2025): "I don't really trust people to understand and think well about probabilities and severities, so I don't think I would care much what people say here. And plausibly politicians won't care much either, since these aren't deeply held beliefs in the electorate but just somewhat made up numbers people give when forced." And on policy items: "people probably won't be engaging with tradeoffs. And unless this becomes a salient issue to people it probably doesn't matter what people think." Peter Barnett reacted in agreement.

[^open2]: Peter Barnett (review comment, Dec 2025): "the current estimates about AI risk are just so so far from anything remotely acceptable by current standards … I somewhat expect the results to be something like 'Current estimates of AI risk are 3-12 Orders of magnitude too high by the normal standards.' And this is such a crazy thing to say that it might just get discounted … I worry that because the risk situation is so unreasonable by any current risk management standard that trying to use precise risk management tools … won't really work." (Self-described as possibly "too doomy.")

[^open3]: Peter Barnett (review comment, Dec 2025): "I think this relies on being able to accurately assess risks, which I think people will either be bad at, or wildly optimistic (off by multiple OOMs)."

[^catdef]: Definitions of catastrophic AI risk vary substantially across legal, expert-prioritisation, and existential-risk contexts. RAISE/SB 53-style statutory definitions use a relatively low legal threshold: "catastrophic risk" means a foreseeable and material risk that a frontier model will materially contribute to death or serious injury to 100 or more people, or at least $1 billion in property damage, from a single incident involving CBRN assistance, autonomous cyber/criminal conduct, or loss of control. The MIT AI Risk Repository prioritisation study uses a broader expert-severity frame: "catastrophic" harm includes, for example, more than 1 million human deaths, more than USD $100 billion in damage, or civilization-scale intangible harms such as collapse of democratic norms or privacy by 2030 under business as usual. The Existential Risk Persuasion Tournament focused on long-run risks to humanity from AI and other causes, distinguishing catastrophic and extinction outcomes across the century; public summaries report AI catastrophe and extinction probabilities separately, with large disagreement between experts and superforecasters. Because these definitions span ordinary legal catastrophes through existential outcomes, this survey does not assume a single threshold. It varies severity explicitly and reports risk tolerance conditional on the severity described.

[^fri]: Forecasting Research Institute, *Existential Risk Persuasion Tournament* (XPT, 2022). "Catastrophe" is defined as 10% or more of humans dying within a five-year period (about 800 million people at current population; pathogen risks use a 1% threshold). https://forecastingresearch.org/xpt
