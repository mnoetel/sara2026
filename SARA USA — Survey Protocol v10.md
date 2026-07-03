# SARA USA 2026: Plan and Survey Protocol

**Survey Assessing Risks from AI 2026**

> "Hadfield argues that governance of any complex technology implicates two distinct types of question: first, democratic questions: what kinds of deception by AI developers count as unfair? **What tradeoffs between utility, safety, and competition does the polity wish to make? What level of catastrophic risk are we willing to tolerate?**"
> Dean W. Ball, *Leviathan Waking*, Hyperdimensional.[^ball]

This survey aims to fill what Hadfield and Clark call the *democratic deficit*: the values-based decisions that shape AI "must be made by democratically accountable public, not private, actors."[^clark] As is, it is not clear what level of risk the public is willing to tolerate. It does not aim to have the public estimate the actual risk or prescribe mitigations[^1], but to judge how much risk the public will tolerate (a values question the public is entitled to answer).

**Try the survey:** a live deployment of the current instrument is at <https://sara2026-1c79e9596779.herokuapp.com/room/sara_usa>.

---

## 1. How to read this document

| Section | What it covers |
|---|---|
| [§2](#2-the-problem-you-cannot-just-ask) | Why we need to triangulate: it's hard to ask "what risk is tolerable?" |
| [§3](#3-the-core-four-ways-to-triangulate-risk-tolerance) | Four ways we triangulate risk tolerance, each with its literature, strengths, limitations, our response, and a worked example item. |
| [§4](#4-moderators-who-we-measure-and-why) | Moderators to explore. |
| [§5](#5-estimating-the-population-view-mrp) | Estimating the *population* view using MRP. |
| [§6](#6-how-much-does-opinion-move-with-framing) | Testing how opinion moves with framing, including the superintelligence briefing experiment (does ban support get pushed around by talking points, and — via the ELM — is it the source cue or the argument content?). |
| [§7](#7-criticisms-and-our-responses) | Criticisms and tentative responses: one table for what we have resolved, one for what we have not. |
| Appendices | [A](#appendix-a-fielding-order--assumptions-and-rationale) fielding order, [B](#appendix-b-dce-design-and-analysis-summary-of-sara_dce_designr) Discrete choice experiment design, [C](#appendix-c-the-dumpster-considered-deliberately-not-asking) dumpster, [D](#appendix-d-provenance-and-sources) provenance. |

---

## 2. The problem: you cannot just ask

The obvious survey is one question: "What annual chance of an AI catastrophe is acceptable?" This would be unlikely to work for several reasons:

**People are unreliable with probabilities.** Asked the chance of getting two heads from two coin tosses, only 52% of UK MPs answered correctly.[^rss] If the people who write the laws cannot do two coin flips, a general-population sample will not respond meaningfully with "1 in 1,000" versus "1 in 1,000,000."

**People are scope insensitive.** Many respondents treat 1 in 1,000 and 1 in 1,000,000 as the same feeling of "small," so a single elicited number reflects affect, not a considered threshold.[^kk92][^slovic2007]

**People are framing sensitive.** The same question shifts with wording, anchors, and who is quoted.[^chong][^tk74] Because some framing is often necessary, this is an effect we want to quantify, rather than something we can eliminate (see §6).

**So we plan to triangulate rather than trusting any single method.** We plan to assess risk tolerance in four different ways. A conclusion that survives all four survives whichever method a given critic distrusts. Where the methods converge, we increase our confidence in the estimate. Where they diverge, we plan to report bounds and qualitative findings. Together, we hope the methods assess the gap between what experts estimate and what the public will tolerate.

---

## 3. The core: four ways to triangulate risk tolerance

The four methods run from least anchoring to most. We:
1. start by asking for the respondent's own number with nothing shown to them, then
2. infer a number from their choices, then
3. offer familiar comparators, and only at the end
4. reveal what named experts have said to see if they're tolerable.

Ordering them this way keeps the more suggestive figures from contaminating the unanchored estimate, both in this document and in the fielding sequence (Appendix A).

<details>
<summary>Background literature — the acceptable-risk tradition this builds on (click to expand)</summary>

Asking what risk society will tolerate is an old question with a serious literature. Starr's founding revealed-preference study concluded the public accepts voluntary risks roughly 1,000 times greater than involuntary ones, with acceptable risk "crudely proportional to the third power of the benefits."[^starr] The psychometric paradigm that followed showed expressed acceptability is structured by dread and unfamiliarity, not just expected fatalities — involuntary, poorly understood, catastrophic hazards (the AI case) are held to far lower probabilities.[^fischhoff][^slovicrisk] Recent AI surveys quantify attitudes and appetite for regulation — more than 8 in 10 Americans say AI requires careful management, and 70% globally believe regulation is needed — but none elicits a *tolerated probability* of catastrophe.[^zhang][^gillespie] To our knowledge no peer-reviewed study directly asks the public what probability of AI catastrophe is acceptable, so SARA has analogues, not precedents; that gap is the contribution.

</details>

Each subsection gives:
- the approach in plain English,
- some literature behind the approach
- its strengths and limitations,
- how we respond to those limitations, and
- a worked example with the real response scale.

### 3.1 Method 1: Ask directly, then test whether the answer is real

**The approach.** We ask people directly for the highest risk they will accept, but build in a test of whether the answer means anything. We ask it across a *severity ladder*, from a single death up to a global catastrophe (around one in ten people), and read off the highest annual chance the respondent will accept at each rung. The key test is *scope sensitivity*: a considered answer demands a lower acceptable chance as the outcome gets worse, so an answer that stays flat across the ladder is affect, not a threshold. This yields each person's stated frequency-number (F–N) curve. We also collect willingness-to-pay on a log scale.

**Why it is worth doing.** It is the most legible method ("the public's own number"), it provides the within-person scope slope that no other method gives, and it is the convergence cross-check for the discrete choice experiment. I have an honors student checking how scope sensitive people are, and who is more scope sensitive.

**Informing literature.** Scope-insensitivity and embedding effects (contingent-valuation literature, Kahneman & Knetsch).[^kk92] Willingness-to-pay is conventionally modelled as log-normal — a modelling convention that keeps WTP positive with finite moments, not an empirical law — which dictates a log response scale rather than a free-text box.[^trainweeks]

<details>
<summary>Background literature — scope insensitivity and embedding (click to expand)</summary>

The embedding effect is the founding result: stated WTP for the same public good can differ by more than an order of magnitude depending on whether it is valued alone or inside a more inclusive category.[^kk92] The textbook demonstration is Desvousges et al.: mean stated WTP to save 2,000, 20,000 or 200,000 migrating birds was essentially flat.[^desvousges] The mechanism is affective — valuation by feeling is insensitive to quantity while valuation by calculation is scope-sensitive[^hseerott] — and the same "psychic numbing" extends to human lives, where compassion can begin deteriorating at the second victim.[^slovic2007] At the top of our ladder the pattern persists: people do not spontaneously judge human extinction as uniquely worse than a catastrophe killing most-but-not-all of humanity, drawing that distinction only when prompted to consider the long-term future.[^schubert] This is why Method 1 measures the scope slope as an outcome rather than assuming a considered threshold exists — and why the ladder's top two rungs (the FRI/XPT catastrophe and extinction tiers) turn Schubert et al.'s finding into a measured within-person contrast rather than an assumption either way.

</details>

**Strengths.** Directly interpretable; yields the per-person scope slope; cheap; the natural convergence test for the DCE.

**Limitations, and how we respond.**
- **Scope insensitivity** ("1 in a million for everything").
  - We measure scope sensitivity instead of designing it away: severity varies *within person* across the ladder (a single death up to a global catastrophe) and the respondent sets the highest acceptable annual chance at each rung, so an insensitive respondent (flat across the ladder) is clearly distinguishable. We interact the per-person scope slope with risk literacy (Ben's thesis).
- **Protest zeros and outliers in WTP.**
  - WTP uses a bounded log scale (not free text) to tame outliers, and a follow-up probe on $0 answers separates protest zeros ("companies should pay", "the money would be wasted") from genuine zeros before the distribution is summarised; with cost dropped from the DCE (Appendix C), this stated item is now the *primary* willingness-to-pay estimate.
- **Demand effects** if the ladder rows are seen in an obvious order.
  - The rows are shown one per page in per-participant randomised order, and that randomisation doubles as the cross-check: **each participant's first-seen rung is a clean between-subjects experiment** (a random quarter of the sample answers each severity first), so the pre-registered sensitivity analysis compares first-response answers by severity against the full within-person curves, and reports the first-response estimates alongside if the two disagree.

**Worked example items.** The exact items are generated from the instrument below (folded so you can skim; expand to read them).

**(a) Highest acceptable risk, by severity (the public's stated F–N curve).** One item per outcome, from a single death up to a global catastrophe:

<!-- BEGIN:auto:ladder-items (generated by render/sync_protocol.py — edit the instrument, not here) -->

<details>
<summary>Method 1 — the severity-ladder items, as fielded — 5 items (click to expand)</summary>

- **`m4c_single`** — For an AI disaster that causes a single death, the highest annual chance you would find acceptable is:
  - _Scale:_ 1 in 10 / 1 in 100 / 1 in 1,000 / 1 in 10,000 / 1 in 100,000 / 1 in 1,000,000 / 1 in 10,000,000 / 1 in 100,000,000 / Never allowed / Prefer not to answer
- **`m4c_100`** — For an AI disaster causing 100 deaths or serious injuries, or $1 billion in damage, the highest annual chance you would find acceptable is:
  - _Scale:_ 1 in 10 / 1 in 100 / 1 in 1,000 / 1 in 10,000 / 1 in 100,000 / 1 in 1,000,000 / 1 in 10,000,000 / 1 in 100,000,000 / Never allowed / Prefer not to answer
- **`m4c_1m`** — For an AI disaster causing 1,000,000 deaths or $100 billion in damage, the highest annual chance you would find acceptable is:
  - _Scale:_ 1 in 10 / 1 in 100 / 1 in 1,000 / 1 in 10,000 / 1 in 100,000 / 1 in 1,000,000 / 1 in 10,000,000 / 1 in 100,000,000 / Never allowed / Prefer not to answer
- **`m4c_800m`** — For an AI disaster causing around 800,000,000 deaths (about 10% of humanity), the highest annual chance you would find acceptable is:
  - _Scale:_ 1 in 10 / 1 in 100 / 1 in 1,000 / 1 in 10,000 / 1 in 100,000 / 1 in 1,000,000 / 1 in 10,000,000 / 1 in 100,000,000 / Never allowed / Prefer not to answer
- **`m4c_extinction`** — For an AI disaster causing human extinction (fewer than 5,000 people survive anywhere on Earth), the highest annual chance you would find acceptable is:
  - _Scale:_ 1 in 10 / 1 in 100 / 1 in 1,000 / 1 in 10,000 / 1 in 100,000 / 1 in 1,000,000 / 1 in 10,000,000 / 1 in 100,000,000 / Never allowed / Prefer not to answer

</details>

<!-- END:auto:ladder-items -->

*(Respondents see only the plain outcome wording; the source anchors behind each rung — RAISE Act "critical harm", MIT AI Risk Repository "catastrophic", and FRI/XPT "catastrophe"[^catdef][^fri] — are internal and never shown. Severity rises down the ladder, so a considered respondent's acceptable chance should fall; one who picks the same chance regardless of severity is flagged scope-insensitive. Items shown one per page in randomised order. This traces each person's stated frequency-number, F–N, curve and is the stated-preference cross-check on the DCE's revealed surface, §3.2.)*

**(b) Willingness to pay (log scale).** A costed tradeoff on a roughly log-normal scale:

<!-- BEGIN:auto:wtp-item (generated by render/sync_protocol.py — edit the instrument, not here) -->

<details>
<summary>Method 1 — the willingness-to-pay item, as fielded — 1 item (click to expand)</summary>

- **`m5_wtp`** — What is the most you would pay each year, through taxes or higher prices, to cut the chance of an AI catastrophe from 1 in 20 to 1 in 100 over the next 30 years?
  - _Scale:_ $0 / $1-10 / $10-100 / $100-1,000 / $1,000-10,000 / More than $10,000 / Don't know / Prefer not to answer

</details>

<!-- END:auto:wtp-item -->

*(Fielded on the costed-tradeoffs page, not adjacent to (a); it is the primary willingness-to-pay estimate now that the DCE has dropped its cost attribute.)*

### 3.2 Method 2: Reveal preferences through choices (the discrete choice experiment)

**The approach.** Instead of asking what risk is tolerable, we show people pairs of realistic AI futures that differ on a few attributes and let them choose. From their choices we *infer* the tradeoffs they are actually willing to make, including the annual catastrophe risk at which they would rather keep today's status quo than accept a new AI future. This is the quantitative core, and it recovers a number without ever asking for one.

**Why it is worth doing.** It gives revealed preferences rather than stated ones. People reveal what they will trade off (safety against utility and global competitiveness) the way they reveal preferences when shopping, which is harder to game and less prone to "I'll just say one in a million for everything."

**Informing literature: the DCE methods canon.** Mike asked specifically that the established DCE desiderata sit here. The relevant guidance:

- **Lancsar & Louviere (2008)**, *Conducting Discrete Choice Experiments to Inform Healthcare Decision Making: A User's Guide*, PharmacoEconomics 26(8):661–677. The standard practitioner walkthrough.[^lancsar]
- **ISPOR good-research-practice trilogy.** Bridges et al. (2011), the **10-item conjoint-analysis checklist**, Value in Health 14(4):403–413;[^bridges] Reed Johnson et al. (2013) on **experimental design**, Value in Health 16(1):3–13;[^johnson] Hauber et al. (2016) on **statistical analysis** of DCEs, Value in Health 19(4):300–315.[^hauber]
- **Soekhai et al. (2019)**, *Discrete Choice Experiments in Health Economics: Past, Present and Future*, PharmacoEconomics 37:201–226. The comprehensive recent review.[^soekhai]

<details>
<summary>Background literature — design and estimation choices (click to expand)</summary>

The Bayesian D-efficient approach follows Sándor & Wedel, who introduced prior-informed efficient choice designs,[^sandorwedel] with Bliemer, Rose & Hess supplying the Bayesian-efficiency machinery behind modern implementations.[^bliemer] Log-normal coefficient specifications follow Train & Weeks's preference-space vs WTP-space treatment — a modelling convention, not an empirical law.[^trainweeks] The closest substantive precedents are DCEs valuing mortality-risk reductions,[^tsuge] and the road-safety value-of-statistical-life meta-analysis shows valuations depend strongly on the elicitation method[^deblaeij] — a further argument for triangulating across methods rather than trusting any one.

</details>

<details>
<summary>SARA's DCE against the ISPOR checklist</summary>

| Checklist step (Bridges et al. 2011) | What SARA does |
|---|---|
| 1. Well-defined research question, conjoint appropriate | Yes: acceptable annual catastrophe risk by severity, and the severity/probability/utility/competition tradeoff. |
| 2. Attributes and levels justified | 4 attributes: **severity** (the catastrophe ladder below, a single death → human extinction),[^catdef] **probability** (annual chance of that catastrophe, 1 in 100 → 1 in 1,000,000), **utility** (modest / major / transformative), **competition** (Other countries are ahead / The US keeps pace / The US is ahead). Cost was dropped to the dumpster (01 Jul 2026): money is an implementation question, not the democratic tradeoff the DCE measures (Hadfield), and acceptable risk is identified by the status-quo opt-out, not a price. Severity is varied, not fixed, so the design traces the full frequency-severity (F–N) surface rather than a single hard-coded 100,000-death point. |
| 3. Construction of choice tasks | Two unlabelled AI-future options plus a "keep today's status quo" opt-out, 10 tasks per respondent: 8 Bayesian D-efficient tasks + 2 internal-validity tasks (task 9 a dominated pair, task 10 an exact repeat of task 2). |
| 4. Experimental design (efficiency) | Bayesian D-efficient design, 10 blocks, 4,000 respondents; level balance and overlap checked. Fielded in waves with **population-level sequential re-optimisation**: priors are refreshed from accumulated data at fixed checkpoints (see "Population-level sequential design" below and Appendix B). |
| 5. Preference elicitation format | Forced choice among A / B / opt-out. |
| 6. Instrument design and data collection | Blocked versions; plain natural-frequency risk labels; oversample the risk module. |
| 7. Statistical analysis | Mixed logit / hierarchical Bayes; random coefficients on the risk slope; per-respondent posteriors feed the literacy interaction. |
| 8 & 9. Results, conclusions, reporting | Acceptable risk reported as a *distribution with credible intervals by benefit scenario*, never a point; WTP measured by the stated log-scale item (§3.1), not the DCE; identification confirmed by simulation (seed 7, coefficients recovered to within ~0.03). |

</details>

**Severity ladder (the varied catastrophe attribute).** Severity is one level of a ladder, never a single fixed definition; RAISE/SB 53 is the legal baseline.[^catdef]

| Severity level | Concrete wording shown to respondents | Why this level |
|---|---|---|
| A single death | A single death | Lower anchor for the F–N curve |
| Critical harm | 100 deaths or serious injuries, or $1 billion in damage | RAISE Act "critical harm" legal anchor[^catdef] |
| Catastrophic | 1,000,000 deaths or $100 billion in damage | MIT AI Risk Repository "catastrophic" threshold[^catdef] |
| Global catastrophe | ~800,000,000 deaths, about 10% of humanity | FRI/XPT "catastrophe"[^fri] |
| Human extinction | Fewer than 5,000 people survive anywhere on Earth | FRI/XPT "extinction"[^fri] — the severity the Method-4 forecaster anchors describe; added 03 Jul 2026 (pre-registration not yet frozen) so Methods 1–2 produce an own-stated public threshold at the tier the expert forecasts are about |

**Strengths.** Revealed not stated preferences; recovers a defensible number with intervals; lets us read off the utility and competition tradeoffs directly; resistant to scope-insensitivity gaming because risk trades against other attributes.

**Limitations, and how we respond.**
- **Combinatorial size.** Mike's worry: with several attributes at several levels the full factorial is sizeable (5 × 5 × 3 × 3 = 225 profiles once severity is varied), and pairwise comparisons multiply quickly. You cannot show one person everything.
  - We do **not** show every cell to every person. A Bayesian D-efficient design selects an efficient subset, split into 10 blocks, so each respondent sees ~10 well-chosen tasks while the *sample* identifies all tradeoffs. Severity is a varied attribute (the ladder above), so the DCE traces an F–N surface rather than a single point; varying severity spreads power across the grid, which the 4,000-respondent sample and an efficient design absorb (dropping cost shrank the grid from 720 to 180; the extinction tier brings it to 225). We confirmed by simulation that this attribute structure identifies the coefficients.
- **Cognitive load.** Ten multi-attribute choices is near the upper end of what a general sample handles well.
  - The blocked design keeps each respondent to about ten tasks — near, but not beyond, that upper end — rather than the full grid.
- **Hypotheticality.** Stated-choice futures are still hypothetical, even if the format is choice-based.
  - It stays a stated-choice format, so we lean on triangulation: the §3.1 severity-ladder elicitation (a stated F–N curve) is the cheaper stated-preference cross-check, and the DCE number must agree with the direct method (§3.1) within about one order of magnitude before we report any single public number (the convergence go/no-go, §5).

**Population-level sequential design (adaptive priors).** Varying severity enlarges the grid to 225 profiles, so a design built on *guessed* priors spreads its power thinly and may concentrate it in the wrong region — public AI-risk tolerance is close to unknown going in. We therefore field in waves and let the **population-level** priors adapt to the data, while holding each respondent's instrument fixed:

1. **Pilot wave** (~500 respondents) on a Bayesian D-efficient design built from diffuse priors (or the 2025 estimates where available).
2. At fixed sample checkpoints, re-estimate the population coefficients (mixed logit, `logitr`) and regenerate the Bayesian D-efficient design (`cbcTools`) using the posterior means as the new prior means (the adopt-if-better D-error criterion is evaluated at the posterior mean; implemented in `dce_sequential.R`).
3. **Main waves** (~3 waves of ~1,170) field the current design; the design is *locked within a wave*.
4. Lock the design permanently after the final checkpoint; cap the total at 4,000.

The adaptation is **between-respondent only**: it sharpens *which* tradeoffs the next wave sees, never *how* an individual is questioned mid-session. This buys the efficiency and prior-robustness of adaptivity while avoiding the costs of individual-level adaptation — no within-respondent endogeneity, no response-noise chasing, and a fixed, explainable instrument for any given person. Because task selection depends only on past *observed* choices, the adaptive sampling is ignorable for the mixed-logit/HB likelihood, so the pooled estimate stays consistent; we report design-wave as a robustness control. The whole loop is a **pre-registered, mechanical algorithm** — fixed model specification, fixed D-efficiency criterion, seeded estimation, fixed checkpoint sizes, with the design updated only if it improves the D-error — so no analyst discretion enters (full specification in Appendix B). One honesty note: the design-*search* step (cbcTools) is not bit-reproducible from a seed (verified 02 Jul 2026), so its reproducibility is **archival** — the exact design each wave fields is committed to the repo, and every downstream step is deterministic given those artifacts. **The §3.1 direct elicitation is held fully static**, preserving one fixed, non-adaptive instrument so the convergence cross-check (§5) rests on a clean comparison.

**Worked example choice task.**

> Here are two possible futures for advanced AI. Which do you prefer? (You may also choose to keep today's situation.)
>
> | | **Option A** | **Option B** | **Keep today's status quo** |
> |---|---|---|---|
> | Worst catastrophe it could cause | 100 deaths or $1B damage | 1,000,000 deaths | (as today) |
> | Annual chance of that catastrophe | 1 in 10,000 | 1 in 1,000,000 | (current trajectory) |
> | What AI delivers for society | **Transformative:** AI cures most major diseases and makes life's essentials cheap and plentiful, so almost everyone is far better off | **Modest:** AI stays roughly as capable as today, but more reliable, so it gets used more widely | (as today) |
> | America's position in AI development | The US is ahead | Other countries are ahead | (as today) |
>
> ◯ Option A  ◯ Option B  ◯ Keep today's status quo
> *(Repeated for ~10 tasks with different attribute levels.)*

### 3.3 Method 3: Anchor to the safety we already accept

**The approach.** Rather than ask for an absolute number, we ask the public to place AI *relative to industries whose risk we already tolerate*: nuclear power, commercial aviation, new pharmaceuticals, cars, dams. Should AI be held to a stricter standard, the same, or a looser one? This converts an impossible absolute judgement into a familiar comparison.

**Why it is worth doing.** It uses the public's lived intuitions about which activities society already keeps very safe (flying) and which it lets run hotter. It also lets us "back out" an implied risk band for AI from the band society tolerates for the comparator, as an illustration only.

**Informing literature.** The ALARP / "as low as reasonably practicable" and F–N (frequency–number) curve traditions in engineering safety (nuclear, rail, chemical).[^r2p2] These give the comparator standards. We treat them as benchmarks the public can react to, not as ground truth for AI. Comparative judgement is also psychologically easier than absolute judgement: hard-to-evaluate attributes become evaluable against a comparator.[^hsee96]

<details>
<summary>Background literature — tolerability frameworks and comparative judgement (click to expand)</summary>

UK engineering practice sets societal-risk tolerability inside a three-band framework — unacceptable / tolerable-if-ALARP / broadly acceptable — first developed for nuclear power and generalised in the HSE's *Reducing Risks, Protecting People*, whose societal anchor holds that an accident killing 50 or more people should be regarded as intolerable above a frequency of 1 in 5,000 per year.[^r2p2][^hse1992] Psychologically, the case for comparative rather than absolute elicitation is Hsee's evaluability work: attributes that are hard to evaluate in isolation become evaluable when a comparator is present, so joint evaluation yields more stable, scope-sensitive judgements than separate evaluation.[^hsee96][^hsee99] That is exactly the move Method 3 makes — replacing an impossible absolute number with a comparison to industries whose risk band society already lives with.

</details>

**Strengths.** Comparative judgements are far easier and more stable than absolute ones; the comparators are concrete and familiar; the result maps onto how regulators actually argue.

**Limitations, and how we respond.**
- **Category error.** "AI should be *stricter*" can mean stricter *rules* or safer *outcomes*.
  - We now focus exclusively on stricter standards rather than safer outcomes because policymakers set standards and we can't measure catastrophic AI outcomes.
- **The denominator problem (the big one).** "One death per what?" Expert AI risk figures are about the *whole technology*, the equivalent of every nuclear reactor or every flight worldwide, not a single unit. A naive comparison to "a plane crash" is apples to oranges.
  - We make it apples to apples by specifying each comparator at the *industry* level (all reactors, the whole aviation system), matching the scope of the AI estimate.
- **Quantifiability.** Some respondents reject the premise that AI risk can be put on a number at all. We must not force them onto a scale they reject.
  - The "reject the frame" escape survives as a **"Cannot compare these technologies"** option on the response scale, so no one is forced onto a scale they reject (this also carries the standalone frame-applicability item's function after that item was cut to the dumpster).

Beyond the three comparators, a single dangerous-activity sanity anchor at the risky end — climbing Mount Everest (restored 02 Jul 2026; one anchor, not the earlier three-activity pool), with its ~1-in-100 fatality record stated in the stem so the anchor doesn't assume the danger is known, fielded after the attention checks because its stem differs from the comparator stems — confirms people can place AI across the *full* range: the industry comparators only exercise the strict end, and nearly everyone should demand stricter rules for AI than for an activity whose risk falls on the climber. Any F–N back-out is illustrative, gated on the cognitive pre-test, and never published as an "N times safer" headline.

**Worked example items.** The live comparator items, their scales, and the randomisation pools, exactly as fielded:

<!-- BEGIN:auto:method3-live (generated by render/sync_protocol.py — edit the instrument, not here) -->

<details>
<summary>Method 3 — comparator items (incl. the embedded attention checks), as fielded — 6 items (click to expand)</summary>

- **`m3_std_nuclear`** — Compared with the safety regulations on nuclear power, regulation of advanced AI should be:
  - _Scale:_ Much stricter / Stricter / About the same / Less strict / Much less strict / Cannot compare these technologies / Prefer not to answer
- **`m3_std_aviation`** — Compared with the safety regulations on commercial aviation, regulation of advanced AI should be:
  - _Scale:_ Much stricter / Stricter / About the same / Less strict / Much less strict / Cannot compare these technologies / Prefer not to answer
- **`m3_std_dams`** — Compared with the safety regulations on large dams, regulation of advanced AI should be:
  - _Scale:_ Much stricter / Stricter / About the same / Less strict / Much less strict / Cannot compare these technologies / Prefer not to answer
- **`m3_att_bioweapons`** — Compared with the safety regulations on biological weapons, this is an attention check, so you must select much less strict:
  - _Scale:_ Much stricter / Stricter / About the same / Less strict / Much less strict / Cannot compare these technologies / Prefer not to answer
- **`m3_att_nuclear`** — Compared with the safety regulations on nuclear weapons, this is an attention check, so you must select much less strict:
  - _Scale:_ Much stricter / Stricter / About the same / Less strict / Much less strict / Cannot compare these technologies / Prefer not to answer
- **`m3_sanity_everest`** — Climbing Mount Everest is very dangerous: about 1 in every 100 people who have tried to climb it have died. Compared with the safety rules we accept for climbing Everest, regulation of advanced AI should be:
  - _Scale:_ Much stricter / Stricter / About the same / Less strict / Much less strict / Cannot compare these technologies / Prefer not to answer

</details>

<!-- END:auto:method3-live -->

*(Pedagogy: the "Cannot compare these technologies" option is the frame-rejection escape so no one is forced onto a scale they reject; the sanity anchor is a deliberately easy check — almost everyone should say AI needs far stricter rules, and anyone who does not is flagged. Its fatality figure is verified — about 1.3% of climbers above base camp died 1921-2006 (Firth et al., BMJ 2008), ~1% of first-time summit attempters 2006-2019 (Huey et al., PLOS ONE 2020), 0.7% for 2007-2024 (Moore et al., J Physiol 2026) — and is stated in the item stem so the anchor doesn't assume respondents know Everest is deadly. It fields after the attention checks (its stem differs from the disguised-comparator stems).)*

*(A pair of disguised attention checks — same stem and scale, on biological and nuclear weapons — is embedded among the live comparator items above; see §7.1 #9. The method's two cut items, and why they were retired, are covered under "How we respond" above; the dumpster itself lives in the instrument.)*

### 3.4 Method 4: Judge a named expert's number

**The approach.** We hand the respondent risk figures that named, real people have stated publicly, and we ask whether each level is acceptable. Because the numbers are recognised rather than generated, the respondent does the one thing they are good at: judging. We show **several** sources at once, spanning the full range of stated views, and read off the acceptability of each — a within-person tolerance curve rather than a single anchored reading.

**Why it is worth doing.** This is the method that speaks most directly to policy. It does not set the public's risk tolerance in the abstract; it tests whether the *current* expert estimates fall inside or outside that tolerance. If most of the public calls Amodei's stated figure "unacceptable, should be illegal," that is a finding lawmakers can act on without anyone first agreeing on the true probability.

**Informing literature.** Anchoring[^tk74] and constructed preference — people judge presented numbers better than they generate them de novo.[^constructed] The named-source design also answers Barnett's objection that "it depends what you call an expert": we never say "experts," we name the individual and report by source.

<details>
<summary>Background literature — anchoring and constructed preference (click to expand)</summary>

Numerical judgements are pulled toward presented values even when the anchor is transparently irrelevant,[^tk74] and a half-century of replication finds the effect robust across domains and stubbornly hard to debias.[^furnham] The constructed-preference literature holds that preferences over unfamiliar quantities are built at the moment of elicitation rather than retrieved, which favours structured judgement of presented figures over free numerical generation.[^constructed] We found no established result that presenting several anchors at once dampens the pull of any single one, so we treat that as a design hypothesis this method tests — the within-person spread across the four sources is itself informative — rather than a bias-removal claim.[^furnham]

</details>

**Strengths.** Recognition not generation; directly decision-relevant; robust to the "who counts as an expert" critique because every anchor is attributed.

**Limitations, and how we respond.**
- **Anchoring:** people may cluster around whatever number they are shown.
  - We show a set of figures within person that spans the credible range — from near-zero (LeCun's verbatim "below the chances of an asteroid hitting the Earth", glossed with the scientific asteroid base rate of ~1 in 1,000,000 per century, since LeCun himself declines to give a number) through careful forecasters (FRI/XPT superforecasters ~1 in 250, then FRI AI-domain experts ~1 in 30) to the top of the range (Amodei, between 1 in 10 and 1 in 4) — and we report results *by source* so the spread is visible rather than collapsed into one average. Whether showing several anchors at once dampens the pull of any single one is not established in the debiasing literature (which finds anchoring hard to remove),[^furnham] so we treat it as a design hypothesis, not an assumption: reporting by source keeps the result interpretable either way. (The earlier Altman/Musk anchors were replaced by the two FRI forecaster medians on 01 Jul 2026, so the set now spans named individuals *and* expert-forecaster groups.)
- **The figures must be real** and fairly quoted, or the whole item is indefensible.
  - Every figure is verified against a citable public statement before fielding (see the flag below).
- **A tolerability rating can still be affect** ("I dislike AI") rather than a considered threshold.
  - This method is only one of four; if affect were driving it, the choice-based method (§3.2) would not agree.

**Worked example item.** Public figures and expert-forecaster groups have estimated the chance that advanced AI leads to a catastrophe (for the two forecaster rows, human extinction this century). The exact items, generated from the instrument:

<!-- BEGIN:auto:experts (generated by render/sync_protocol.py — edit the instrument, not here) -->

<details>
<summary>Method 4 — the named-source items, as fielded — 4 items (click to expand)</summary>

- **`m2_experts_lecun`** — Yann LeCun (winner of the Turing Award, computer science's Nobel Prize) has said the chance that AI wipes out humanity is "below the chances of an asteroid hitting the Earth." Scientists put the chance of an extinction-level asteroid strike at about 1 in 1,000,000 per century. Accepting a risk at that level would be:
  - _Scale:_ Tolerable: okay to live with, if monitored / Intolerable: too dangerous, must be fixed / Prefer not to answer
- **`m2_experts_fri_super`** — Expert forecasters in a large forecasting tournament put the chance that AI causes human extinction this century at about 1 in 250. Accepting a risk at that level would be:
  - _Scale:_ Tolerable: okay to live with, if monitored / Intolerable: too dangerous, must be fixed / Prefer not to answer
- **`m2_experts_fri_domain`** — AI-domain experts in a large forecasting tournament put the chance that AI causes human extinction this century at about 1 in 30. Accepting a risk at that level would be:
  - _Scale:_ Tolerable: okay to live with, if monitored / Intolerable: too dangerous, must be fixed / Prefer not to answer
- **`m2_experts_amodei`** — Dario Amodei (CEO of Top AI Company, Anthropic) has estimated the chance that AI goes catastrophically wrong at between 1 in 10 and 1 in 4. Accepting a risk at that level would be:
  - _Scale:_ Tolerable: okay to live with, if monitored / Intolerable: too dangerous, must be fixed / Prefer not to answer

</details>

<!-- END:auto:experts -->

*(Each row's rationale in the instrument carries its verified citation — LeCun via the CBS Mornings interview (Dec 2023; the circulating "<0.01%" figure is a third party's inference, so no number is attributed to him); the two forecaster medians via Karger, Rosenberg, ... Tetlock 2023, FRI Existential Risk Persuasion Tournament, Table 9 (0.38% and 3% for AI-caused extinction by 2100); Amodei via The Logan Bartlett Show EP 82 (Oct 2023, "somewhere between 10 and 25%") with his more recent flat "25%" (Axios AI+ DC Summit, 17 Sep 2025) noted.)*

> **Field flag — resolved 02 Jul 2026.** Every figure was verified against an exact, citable statement (sources in each item's rationale). The check caught one misattribution: the "1 in 1,000,000" formerly attributed to LeCun is not his — he has never stated a numeric p(doom) — so the item now quotes his verbatim asteroid comparison and attributes the number to asteroid science. The rule stands for any future anchor: do not field a number we cannot source.

### A note on the tolerability scale

The named-expert items (§3.4) use one **two-point** tolerability scale: **Tolerable: okay to live with, if monitored** vs **Intolerable: too dangerous, must be fixed**.

Earlier drafts used a four-point monotonic scale (Acceptable < Tolerable < Intolerable < Unacceptable / should be illegal); it was collapsed to the two-point forced choice on 01 Jul 2026 for a cleaner, lower-effort judgement across the four within-person anchors. An even earlier draft labelled the middle points "negligent / grossly negligent"; Barnett pointed out that "negligent" reads as *weaker* than "intolerable," breaking monotonicity, so those labels were dropped. We keep the history because it is a case where reviewers' small wording points reshaped the instrument.

---

## 4. Moderators: who we measure, and why

These are variables to measure and control for, rather than for excluding participants. Covariates moderate the estimate and let us ask whether, for example, young people are less tolerant of low-probability futures that foreclose the long-term future. Default analysis enters them as controls or via MRP (§5) so the headline is a population estimate net of sample composition.

- **Demographics for weighting.** Age, gender, education, income, state, all aligned to US Census / ACS categories so they post-stratify to population controls (see Appendix A for the exact brackets).
- **AI familiarity.** Frequency of intentional AI use (Gillespie et al. 2025; item validated as a proxy for technology experience per Hargittai 2005).[^gillespie]
- **Political orientation.** 7-point Very Liberal to Very Conservative (Jost 2006).[^jost]
- **Risk literacy / numeracy.** Berlin Numeracy Test style items (Cokely et al. 2012; a fast, psychometrically sensitive measure of risk literacy and a robust predictor of decision quality).[^cokely] The key interaction for one of my honours students' projects: does higher risk literacy increase scope sensitivity?

---

## 5. Estimating the population view (MRP)

A convenience or panel sample is not the US public. We use **multilevel regression and post-stratification (MRP)**: model the outcome with demographic and geographic predictors, then re-weight model predictions to ACS population counts to recover the population-level risk tolerance (and, if the per-state effective sample is large enough, state-level estimates). MRP is validated by posterior predictive checks and leave-one-state-out cross-validation. **No state map is published unless the effective per-state sample clears a pre-registered threshold.**

**Panel-selection calibration.** MRP adjusts demographics, not the attitudinal self-selection of an opt-in panel — Prolific self-selects on tech engagement and AI familiarity, traits correlated with the outcome, and that residual selection is a named limitation in all reporting. Two verbatim Pew ATP benchmark items are fielded before any treatment (`bench_pew_cncexc`, `bench_pew_aireg`); the gap between our sample and Pew's probability-sample toplines is reported alongside every population claim.

**Convergence go/no-go (pre-registered).** A single quantitative public number is reported only if the DCE (§3.2) and the direct scope instrument (§3.1) agree within about one order of magnitude in an overlap subsample. If they diverge, we report a bound plus a qualitative finding. The expert assessment vs. public expectations multiplier (e.g., 4,000x safer) is reported, if at all, as researcher interpretations and never as public opinions.

---

## 6. How much does opinion move with framing?

Critics say poll answers are shallow and shift with messaging. Rather than pretend otherwise, we make the swing a primary outcome. We don't treat any of these as measuring "true" opinion; the question is how far opinion moves when the talking points change, and — where it moves — *why*.

<details>
<summary>Background literature — framing and information-provision experiments (click to expand)</summary>

That policy attitudes shift with how an issue is framed is one of the best-documented findings in political behaviour,[^chong] which is why briefing content is varied experimentally rather than treated as a neutral constant. The design template for §6.1 is the information-provision-experiment literature, which gives best practice on measuring prior beliefs, varying the information cleanly, measuring updating, and handling experimenter-demand confounds.[^haaland] The central-vs-peripheral decomposition in §6.2 and §6.3 comes from the Elaboration Likelihood Model: attitude change won by scrutiny of arguments (the central route) is more persistent and behaviour-predictive than change won by cues such as source prestige (the peripheral route).[^elm]

</details>

### 6.1 Balanced-disclosure experiment (information provision)

A random half see a short, balanced *disclosure* — a two-sentence statement of the loss-of-control worry plus the counter-consideration — *before* the tolerance block. "Disclosure" is the honest label: it is too brief to make anyone informed, and we don't claim it does; it tests whether even minimal balanced context moves the tolerance estimate. Where disclosed and undisclosed answers diverge, the *disclosed* estimate is the headline. This is the framing test that touches tolerance; everything else is kept off it.

### 6.2 The superintelligence briefing experiment (Muskan's 3×3 ELM)

This is a framing experiment, not a measure of superintelligence support in its own right: the question is whether support for *banning* the development of smarter-than-human AI gets pushed around by talking points, and — if it does — whether the movement comes from the *source cue* (who endorses the position, the peripheral route) or the *argument content* (the substance, the central route). We frame it with the **Elaboration Likelihood Model**[^elm] to separate those two routes.

The survey's final module, run last so its persuasive material cannot contaminate the tolerance core. After a neutral definition of superintelligence, each respondent is randomly assigned one pre-built briefing from a **3×3 design** — an argument *for* the ban crossed with an argument *against* it, each at three levels: an **elite source-cue** (peripheral route), a **substantive argument** (central route), or **none**. They then answer two 5-point ban-support items (a pro-ban and an anti-ban statement, reported by top-2-box prevalence and as their difference). The contested (two-sided) cells show how far a balanced brief moves support; the one-sided cells isolate the ELM mechanism — whether a source cue alone moves support (peripheral) as much as the argument does (central). Two self-report route items (`muskan_central_route`, `muskan_peripheral_route`) serve as mediators / quasi-manipulation-checks for which route did the work. (Supersedes the earlier accel/safety counter-message arm, the Stem-A/B wording experiment, and the descriptive twins — CAIS extinction-priority and a neutrally worded "treaty to ban" — all retired to the dumpster, 29 Jun 2026.)

The 27 briefing passages (9 cells × 3 versions) live in `survey/muskan_stimuli.md`; the full fielded design — aims, testable hypotheses, and the mediators-as-quasi-manipulation-checks — is in `Muskan's Experiment/` (Rev 3). Participants are debriefed on the end page: a note that the briefings were assembled from real published arguments, with links to full statements of both sides (FLI's statement; Andreessen's manifesto). The support DV and ELM route items, generated from the instrument:

<!-- BEGIN:auto:muskan-items (generated by render/sync_protocol.py — edit the instrument, not here) -->

<details>
<summary>Superintelligence module — ban-support DV and ELM route mediators, as fielded — 2 items (click to expand)</summary>

- **`muskan_support`** — Do you support or oppose a ban on the development of superintelligence, not lifted before there is (1) broad scientific consensus that it will be done safely and controllably, and (2) strong public buy-in?
  - _Scale:_ Strongly support / Support / Oppose / Strongly oppose / Don't know / Prefer not to answer
- **`muskan_central_route`** — I tried to judge the reasons given, not just who was giving them.
  - _Scale:_ Strongly disagree / Disagree / Neither agree nor disagree / Agree / Strongly agree / Prefer not to answer

</details>

<!-- END:auto:muskan-items -->

### 6.3 Argument vs social proof (considered, cut)

Mike's question, and the same central-vs-peripheral logic as §6.2 in miniature: when framing moves people, is it the *content* of the argument or the *social signal* (for example, "Prince Harry signed it")? The proposed design crossed the argument (present / absent) with a prestige-signatory cue (present / absent). **Cut to the dumpster 2 Jul 2026, never built:** Muskan's 3×3 (§6.2) already makes this decomposition — its one-sided cells separate the elite source-cue (peripheral route) from the substantive argument (central route) — so a standalone 2×2 would duplicate it. Recoverable if a prestige-signatory cue distinct from the elite-cue cells is later wanted (Appendix C).

A data-centre reverse-halo module was also considered as a framing experiment (does an "AI data centre" label draw more objection than an identical generic plant?) but was cut to the dumpster on 29 Jun 2026; see Appendix C.

---

## 7. Criticisms and our responses

### 7.1 Resolved or actioned

Each entry gives the reviewer's concern in fuller form and what we changed in response. The compact one-line version of this table lived in v9; reviewers asked for the concern *and* the fix spelled out, so both are expanded here.

**1. Oscar Delaney (Barnett agreeing) — don't trust public probabilities; relative comparisons are more useful.**

*Concern.* Delaney doesn't trust a general sample to understand or reason well about probabilities and severities, so a directly elicited number is "somewhat made up when forced" — it reflects affect, not a considered threshold — and politicians are unlikely to weight it. Comparative judgements ("should AI be held stricter than nuclear power?") are cognitively easier and more stable than absolute ones.

*Response.* We demoted the direct number (§3.1) from headline to a validation cross-check, and made the two methods that lean on *judgement rather than generation* primary: named-expert recognition (§3.4, where the respondent judges a real published figure rather than inventing one) and relative-standard anchoring (§3.3, comparison to industries whose risk we already tolerate). The direct number is only reported as a single public figure if it agrees with the revealed-preference DCE within about one order of magnitude (the convergence go/no-go, §5); otherwise we report a bound and a qualitative finding.

**2. Peter Barnett — scope insensitivity (treating 1 in 100,000 ≈ 1 in 10,000,000).**

*Concern.* Many respondents feel both very small probabilities as the same undifferentiated "small," so a single elicited threshold reflects that affect rather than a considered number, and a naive elicitation would report a spuriously precise figure.

*Response.* We *measure* scope sensitivity instead of designing it away. Severity varies within person across the ladder (a single death → human extinction) and the respondent sets the highest acceptable annual chance at each rung, with rows about two orders of magnitude apart and order randomised; anyone flat across the ladder is flagged scope-insensitive. The randomised one-per-page order gives the demand-effect cross-check for free: whichever rung a participant sees *first* is answered unanchored, so first-seen answers form a between-subjects comparison across severities, pre-registered as a sensitivity analysis against the within-person curves (§3.1). The per-person scope slope is interacted with risk literacy (an honours thesis) to ask *who* is insensitive rather than assuming everyone is.

**3. Peter Barnett — a tolerability Likert measures affect, not a threshold.**

*Concern.* A tolerability rating ("acceptable / intolerable") may capture nothing more than "I like or dislike AI," not a considered risk threshold the respondent would defend.

*Response.* Accepted — which is the whole reason we triangulate rather than trust any one method. The tolerability reading (§3.4) must agree with the revealed-preference DCE (§3.2) before we report a number; within-person consistency, the information-provision contrast (§6), and numeracy moderation all test whether the rating is stable or pure affect. If affect were driving it, the choice-based method would not converge.

**4. Peter Barnett — the F–N exercise overshoots and may be dismissed.**

*Concern.* Expert AI-risk estimates sit so far above any tolerated engineering standard that a precise frequency–number chart risks "overshooting the graph" and being discounted as absurd.

*Response.* The headline is reframed to the robust *gap* between what experts estimate and what the public will tolerate, not a point on an F–N curve.

**5. Peter Barnett — the "all technologies carry risk" framing misleads.**

*Concern.* A preamble that "every technology carries some residual risk" quietly imports a "we're only haggling over the last order of magnitude" frame, nudging respondents toward acceptance.

*Response.* Removed from all public-facing items and parked in the dumpster; the instrument does not tell respondents that residual risk is inevitable before asking what they will tolerate.

**6. Peter Barnett — "negligent" reads as weaker than "intolerable."**

*Concern.* An earlier scale used "negligent / grossly negligent" for the middle points; "negligent" reads as *milder* than "intolerable," breaking the monotonic ordering the scale depends on.

*Response.* Those labels were dropped for a strictly monotonic tolerability scale, later collapsed to the two-point **Tolerable / Intolerable** forced choice (01 Jul 2026) for the named-expert items, giving a cleaner low-effort judgement across the four within-person anchors (§3.4).

**7. Peter Barnett — it depends what you call "experts."**

*Concern.* A finding stated as "experts think X" hinges on the contested question of who counts as an expert, and is easy to wave away on that ground.

*Response.* We never say "experts." Every anchor is a named individual or a specified forecaster group — LeCun, the FRI/XPT superforecaster median, the FRI AI-domain-expert median, Amodei — shown within person and reported *by source*, so the reader sees the spread and its attribution rather than an undifferentiated average (§3.4).

**8. Oscar Delaney — test counter-messages (a16z / accelerationist talking points).**

*Concern.* Poll answers may be shallow and shift under industry counter-messaging; we should test whether accelerationist framing moves opinion rather than assume our numbers are stable.
*Response.* Folded into Muskan's 3×3 ELM briefing experiment (§6.2): each respondent gets one briefing crossing an argument *for* a ban × an argument *against*, each at three levels (elite source-cue / substantive argument / none). It runs last, off the tolerance core, so the persuasion test cannot contaminate the tolerance estimate.

**9. Peter Barnett — one attention check should point "more strict," one "less strict."**

*Concern.* Barnett suggested bidirectional attention checks (one demanding a high answer, one a low answer) to catch straightliners who pick the same option throughout.

*Response.* We embed two disguised checks among the comparator items (biological weapons, nuclear weapons) but made them *same-direction* on purpose: Prolific excludes a respondent only when they fail *both* checks, so a shared fail endpoint ("Much less strict") is more likely to catch someone straightlining across both than a split criterion would (instrument: `m3_att_bioweapons` / `m3_att_nuclear` + the `att_failed` screen-out).

**10. Barnett / Delaney — give people a neutral intuition for risk magnitudes by comparing to other fields.**

*Concern.* Absolute risk numbers are meaningless to most respondents without a reference point drawn from domains they already understand.
*Response.* The relative-standards method (§3.3) anchors AI against industries whose risk society already tolerates (nuclear power, commercial aviation, large dams), and the Mount Everest sanity anchor fixes the risky end of the range so we can confirm respondents can place AI across the full scale.

**11. Gradient (Carroll, A. Reid, Caetano) — open with a clear purpose; separate the two question classes.**

*Concern.* The instrument should state its purpose up front and not blur descriptive-attitude questions together with the values question about tolerance.

*Response.* §1–§2 were rewritten around the single purpose (how much catastrophic risk the public will tolerate).

**12. Gradient — don't assume a latent quantitative preference exists.**

*Concern.* Respondents may simply not hold a pre-formed numeric risk threshold, so eliciting one manufactures a preference that isn't there.

*Response.* Stated explicitly in the protocol; the convergence test (§5) is the check on whether a stable number exists at all, and where it fails we report ordinal findings and bounds rather than forcing a point estimate.

**13. Gradient — define risk precisely (probability × impact; whose risk; loss-of-control vs application).**

*Concern.* "Risk" is ambiguous across probability and severity, personal versus societal exposure, and loss-of-control versus ordinary application harms; leaving it undefined makes answers uninterpretable.

*Response.* Addressed structurally rather than with a definitions page: severity (impact) and annual probability are separate, concretely-labelled dimensions in both the severity ladder and the DCE, so probability and impact are not conflated, and the severity-ladder items are explicitly scoped to *societal* (not personal) risk. The loss-of-control-vs-application distinction is not drawn separately — the catastrophe framing deliberately spans both.

**14. Gradient — don't conflate conditional with unconditional support.**

*Concern.* "I'd support a pause *if* China also paused" is a different measurement from unconditional support, and merging them overstates agreement.

*Response.* A strict conditional-reporting rule, with separate unconditional and conditional delay items so the two are never collapsed in the headline.

**15. Gradient — a citizens' assembly may beat a poll.**

*Concern.* A deliberative mini-public might elicit more considered views than a one-shot survey, and could be the better instrument for a values question.

*Response.* Accepted as a complement, not a replacement: a deliberative Phase 2 is recommended, though not yet scoped or funded.

**16. Gradient — drop the "public want AI 4000× safer" claim.**

*Concern.* Headlining a precise multiplier backed out of an F–N comparison is indefensible and invites ridicule.

*Response.* Plan to avoid this framing; any multipliers will be clearly the researchers' interpretations not the public's beliefs.

**17. Gradient — the Figure-11 category error ("systems should be stricter").**
*Concern.* Asking whether AI "should be stricter" conflates stricter *rules* (standards) with safer *outcomes* (systems in practice) — two different judgements collapsed into one.

*Response.* All questions are now 'safety standards' not 'in practice' because standards are what policymakers have more control over, especially for catastrophic risks.

**18. Claude as Dean Ball skeptical review — avoiding advocacy.**

*Concern.* A hostile reader could see the exercise as advocacy, with design choices quietly tilted toward an alarming result.

*Response.* Removed attitude questions that looked like support for specific policies. Also, aim to seek adversarial pre-launch and post-report review, and publish their critiques alongside the results.

**19. Claude as Dean Ball skeptical review — curated alarming anchors.**

*Concern.* Original draft showed only high risk estimates that would bias respondents toward alarm.

*Response.* A full-range anchor set spanning the credible spread — LeCun (~1 in 1,000,000) up to Amodei (1 in 10 to 1 in 4), with the two FRI forecaster medians in between — every figure reported by anchor so the range is visible.

---

## Appendix A: Fielding order — assumptions and rationale

The authoritative item list, response scales, and exact page order **are the instrument** — `survey/sara_usa.md` (the single source of truth) and the generated review table `render/review.html`. This appendix gives only the design assumptions behind that order; it does not restate the items.

**Risk framing.** The severity-ladder items are explicitly scoped to *societal* risk (the chance somewhere in the population, not the respondent's personal risk), and severity and annual probability appear as separate, concretely-labelled dimensions throughout the tolerance block; there is no standalone definitions preamble.

**Least-to-most anchoring.** The four tolerance methods are fielded *free estimate → DCE → safety comparators → named-expert figures* (matching §3), so an earlier figure cannot anchor a later answer. They sit after the topic-neutral warm-up, so the harder quantitative items are not the respondent's first task. Fielding a gentler block first to cut early dropout is an open tradeoff (§8).

**Placement of the framing experiments.** Consent comes first (a non-consent ends the survey). The **balanced information-provision arm** (random half) sits *before* the tolerance block by design — the one framing test allowed to touch tolerance. The **persuasive** material (Muskan's 3×3 briefing experiment, §6.2) runs *last*, after demographics, so it cannot contaminate the tolerance core. The environment module, the descriptive-attitudes battery, and m2_pace are cut (the dumpster lives in the instrument).

**Demographics → MRP.** Age, gender, education, income and state are collected in Census/ACS-aligned categories (B01001 / B15003 / B19001) so they post-stratify cleanly; the exact brackets are in the instrument. ACS sex controls drive weighting (the extra gender category is allocated, not dropped). No state-level map is published unless the per-state effective sample clears the pre-registered threshold. Frame build: `acs_poststrat.R` + `ACS_poststratification_manual.md`.

---

## Appendix B: DCE design and analysis (summary of `sara_dce_design.R`)

- **Grid:** severity (5 levels: a single death, critical harm 100 deaths/$1B, catastrophic 1,000,000 deaths/$100B, global catastrophe ~800,000,000 deaths, human extinction — fewer than 5,000 survive),[^catdef] probability (5 levels, annual chance 1 in 100 → 1 in 1,000,000), utility (3), competition (3). Full factorial 5 × 5 × 3 × 3 = 225 profiles. Cost was dropped to the dumpster (01 Jul 2026) — money is an implementation question, not the democratic tradeoff the DCE measures (Hadfield), and p\* is anchored by the status-quo opt-out, not a price. Severity is varied across the five-tier ladder, not fixed; the RAISE Act "critical harm" tier is the legal baseline and the FRI/XPT extinction tier is the top (added 03 Jul 2026, pre-registration not yet frozen).
- **Design:** Bayesian D-efficient, 2 alternatives + opt-out, 10 blocks, 4,000 respondents (oversampling the risk module relative to 2025). Level balance and overlap checked (`cbcTools`). Each block fields 10 tasks: **tasks 1-8** are the D-efficient design; **task 9** is a dominated pair (one option strictly better on every attribute; the dominant side alternates by block to cancel position bias) and **task 10** is an exact repeat of task 2. Tasks 9-10 are **excluded from estimation**: choosing the dominated option (the opt-out is not a failure) and switching on the repeated task are reported as data-quality rates and drive a pre-registered sensitivity re-estimate excluding flagged respondents (ISPOR internal-validity guidance).
- **Population-level sequential re-optimisation (pre-registered algorithm):**
  - **Waves:** pilot ~500, then ~3 main waves of ~1,170 (≈4,010 total). Design locked within each wave.
  - **Checkpoints:** at each wave boundary, re-estimate the population coefficients on all data so far (mixed logit, `logitr`, fixed specification, seeded multistart — estimation IS seed-deterministic) and regenerate the Bayesian D-efficient design (`cbcTools`) using the posterior means as the new prior means; the adopt-if-better comparison is the local D-error at the posterior mean (`dce_sequential.R`). The search step is not seed-reproducible, so each wave's fielded design is archived (`dce_blocks_wave<k>.csv` + log) — reproducibility by artifact, not by seed.
  - **Update rule:** adopt the regenerated design only if it lowers the Bayesian D-error versus the incumbent; otherwise keep the incumbent. Design is locked permanently after the final checkpoint; hard cap 4,000.
  - **Why this is not p-hacking:** only the *priors* update — the model, the D-efficiency criterion, the checkpoint sizes, and the downstream analysis are all fixed in advance; estimation is seeded and the adopt rule is deterministic given the archived designs. No analyst discretion enters: the stochastic search proposes, the fixed rule disposes, and the artifacts are committed. Task selection depends only on past observed choices, so the adaptive sampling is ignorable for the likelihood and the pooled estimate is consistent; design-wave is reported as a robustness control. §3.1 is held static (non-adaptive).
- **Fielding pipeline:** the survey is the **oTree app generated from `survey/sara_usa.md`** (the single source of truth); it assigns each respondent a DCE block plus the randomisation arms and handles Prolific completion-code crediting. The population-level sequential loop runs *off-platform* in R between waves — `cbcTools` (design) + `logitr` (estimation) — regenerating `survey/sara/dce_blocks.csv` (the per-block design the app reads) for the next wave. No within-session compute is required.
- **Estimation:** mixed logit (`logitr`), random normal coefficients on the log-risk slope; multistart. Fixed specification: log annual probability, log severity (deaths), an **extinction indicator** (the discontinuity beyond the log-death slope at the extinction tier — without it, the linear-in-log-deaths model would *assume* extinction is just one more log unit; with it, the Schubert et al. uniquely-bad question is estimated, not assumed), benefit and competition dummies, opt-out constant.
- **Recovering the public number:** acceptable annual risk p\* is the level at which an AI-future option equals the status-quo opt-out for a given severity tier and benefit/competition scenario — the opt-out anchors p\*, so no cost attribute is needed. WTP is taken from the stated log-scale item (§3.1, `m5_wtp`), not backed out of a DCE cost coefficient. Report p\* as a distribution with credible intervals by scenario, never a point.
- **Identification:** confirmed by simulation (seed 7) on the 225-grid design; all coefficients — including the extinction discontinuity — recovered to within ~0.03 of truth (`dce_sequential_sim_2026-07-03.log`).
- **Go/no-go and multiplier governance:** see §5.
- **Status (03 Jul 2026):** `sara_dce_design.R` encodes the varied-severity 225-profile grid (extinction tier + the `ext` discontinuity term added 03 Jul 2026, before pre-registration), appends the two internal-validity tasks, exports the per-block CSV the app reads, and runs the repaired one-shot identification simulation (choices simulated directly from the registered mixed-logit specification). The wave/checkpoint sequential loop is implemented in `dce_sequential.R` (shared coding/estimator/export in `dce_model_utils.R`), with `--simulate` running the full four-wave sequential procedure against known coefficients. **Before the pilot fields:** freeze PREREGISTRATION.md (the clean `--simulate` recovery run on the 225-grid design is archived at `dce_sequential_sim_2026-07-03.log`).

---

## Appendix C: The dumpster (considered, deliberately not asking)

The full ledger of items and modules considered and cut — with the reason for each — lives in the instrument, `survey/sara_usa.md`, under the top-level **`dumpster:`** key, so the decision record sits beside the items themselves. It covers the icon arrays, verbal/micromort risk anchors, the "all technologies carry residual risk" preamble, off-the-shelf scales (AIAS-4/GAAIS/GRIPS/DOSPERT), the "4000× safer" multiplier, the direct "support SB 53/RAISE" item, the DCE cost attribute, the test–retest wave, the unbounded-WTP option, the mitigations and priority-risks batteries, CRT and need-for-cognition, the environment/data-centre module, the Module 1 descriptive-attitudes battery, m2_pace, the retired Stem-A/B wording experiment + counter-message arm (superseded by Muskan's 3×3), and the argument-vs-social-proof 2×2 (subsumed by the same 3×3, §6.3). The deeper rationale for the methodologically interesting cuts is in §2–§3 and §6.

---

## Appendix D: Provenance and sources

- Supersedes v6/v7/v8/v9 (markdown) and the v5/v4.1/v4/v3/v2 Word docs and the archived Nov-2025 draft (all retained in `ARCHIVED/`).
- Companion files (the instrument and its toolchain): `survey/sara_usa.md` (single source of truth — items, scales, order, dumpster), `render/review.html` (generated review table), `sara_dce_design.R` (DCE design), `acs_poststrat.R` + `ACS_poststratification_manual.md` (MRP frame), `ethics consent form/` (PIS v2.1), `Muskan's Experiment/` (3×3 study design).
- The FAA-model item and cars/airplanes/drugs framing follow Anthropic's public proposal; the contextual EO is the 2 June 2026 White House order *Promoting Advanced AI Innovation and Security* (security-focused, voluntary). **Verify the EO title and date before citing externally.**
- Round 1 reviewers: Peter Barnett, Oscar Delaney (Dec 2025). Round 2: Gradient Institute (Liam Carroll, Alistair Reid, Tiberio Caetano) (24 Nov 2025). The "skeptical reviewer" is a reconstruction of a Dean-Ball-style critique, not a quotation. (Alistair Reid of Gradient is a different person from Benjamin Reid, whose covariate items appear in §4.)
- Added measures from Benjamin Reid, *Additional Questions for SARA*.
- Environment module after Andy Masley, *A simple trick to fix the data center debate* (blog.andymasley.com, Jun 2026); offset claims are contested and treated as framings to test.

[^1]: Those are technical questions for experts

[^ball]: Dean W. Ball, "Leviathan Waking," *Hyperdimensional* (Substack), https://www.hyperdimensional.co/p/leviathan-waking. Ball attributes the framing to Gillian Hadfield's work on regulatory markets.

[^clark]: Gillian K. Hadfield & Jack Clark, "Regulatory Markets: The Future of AI Governance," arXiv:2304.04914 (submitted 11 Apr 2023, rev. 3 Feb 2026); published in *Jurimetrics: The Journal of Law, Science and Technology* 65:195–240 (2026), https://arxiv.org/abs/2304.04914. The paper frames AI governance as facing a "technical deficit" and a "democratic deficit," the latter being that "values-based decisions … must be made by democratically accountable public, not private, actors" (abstract).

[^rss]: Royal Statistical Society, "New RSS survey tests statistical skills of MPs" (2022), https://rss.org.uk/news-publication/news-publications/2022/general-news/new-rss-survey-tests-statistical-skills-of-mps/. Savanta ComRes poll of 101 MPs (fielded 17 Nov 2021–18 Jan 2022) asked the probability of two heads from two coin tosses: 52% answered 25% correctly, 33% said 50%, 10% didn't know. The predecessor survey was run by Ipsos MORI (97 MPs, fielded Nov–Dec 2011): ~40% correct. Reporting: NationalWorld, https://www.nationalworld.com/news/politics/mps-statistics-maths-problem-3564209.

[^lancsar]: Emily Lancsar & Jordan Louviere, "Conducting Discrete Choice Experiments to Inform Healthcare Decision Making: A User's Guide," *PharmacoEconomics* 26(8):661–677 (2008), https://pubmed.ncbi.nlm.nih.gov/18620460/.

[^bridges]: John F. P. Bridges et al., "Conjoint Analysis Applications in Health — a Checklist: A Report of the ISPOR Good Research Practices for Conjoint Analysis Task Force," *Value in Health* 14(4):403–413 (2011), https://pubmed.ncbi.nlm.nih.gov/21669364/. The 10-item checklist; verify the exact item labels against the paper before citing each.

[^johnson]: F. Reed Johnson et al., "Constructing Experimental Designs for Discrete-Choice Experiments: Report of the ISPOR Conjoint Analysis Experimental Design Good Research Practices Task Force," *Value in Health* 16(1):3–13 (2013), https://www.sciencedirect.com/science/article/pii/S1098301512041629.

[^hauber]: A. Brett Hauber et al., "Statistical Methods for the Analysis of Discrete Choice Experiments: A Report of the ISPOR Conjoint Analysis Good Research Practices Task Force," *Value in Health* 19(4):300–315 (2016), https://www.valueinhealthjournal.com/article/S1098-3015(16)30452-1/fulltext.

[^soekhai]: Vikas Soekhai, Esther W. de Bekker-Grob, Alan R. Ellis & Caroline M. Vass, "Discrete Choice Experiments in Health Economics: Past, Present and Future," *PharmacoEconomics* 37:201–226 (2019), https://link.springer.com/article/10.1007/s40273-018-0734-2.

[^jost]: John T. Jost, "The End of the End of Ideology," *American Psychologist* 61(7):651–670 (2006), https://doi.org/10.1037/0003-066X.61.7.651. Source for the 7-point orientation item per Benjamin Reid's notes.

[^gillespie]: Nicole Gillespie, Steven Lockey, T. Ward, A. Macdade & G. Hassed, "Trust, Attitudes and Use of Artificial Intelligence: A Global Study 2025," University of Melbourne (2025), https://doi.org/10.26188/28822919. Frequency-of-use item justified as a technology-experience proxy via Eszter Hargittai, "Survey Measures of Web-Oriented Digital Literacy," *Social Science Computer Review* 23(3):371–379 (2005).

[^catdef]: Definitions of catastrophic AI risk vary substantially across legal, expert-prioritisation, and existential-risk contexts. RAISE/SB 53-style statutory definitions use a relatively low legal threshold: "catastrophic risk" means a foreseeable and material risk that a frontier model will materially contribute to death or serious injury to 100 or more people, or at least $1 billion in property damage, from a single incident involving CBRN assistance, autonomous cyber/criminal conduct, or loss of control. The MIT AI Risk Repository prioritisation study uses a broader expert-severity frame: "catastrophic" harm includes, for example, more than 1 million human deaths, more than USD $100 billion in damage, or civilization-scale intangible harms such as collapse of democratic norms or privacy by 2030 under business as usual. The Existential Risk Persuasion Tournament focused on long-run risks to humanity from AI and other causes, distinguishing catastrophic and extinction outcomes across the century; public summaries report AI catastrophe and extinction probabilities separately, with large disagreement between experts and superforecasters. Because these definitions span ordinary legal catastrophes through existential outcomes, this survey does not assume a single threshold. It varies severity explicitly and reports risk tolerance conditional on the severity described.

[^fri]: Forecasting Research Institute, *Existential Risk Persuasion Tournament* (XPT, 2022). "Catastrophe" is defined as 10% or more of humans dying within a five-year period (about 800 million people at current population; pathogen risks use a 1% threshold). "Extinction" is defined as human extinction or the global population falling below 5,000. https://forecastingresearch.org/xpt

[^starr]: Chauncey Starr, "Social Benefit versus Technological Risk," *Science* 165(3899):1232–1238 (1969), https://doi.org/10.1126/science.165.3899.1232. Verbatim: "the public is willing to accept 'voluntary' risks roughly 1000 times greater than 'involuntary' risks," and "the acceptability of risk appears to be crudely proportional to the third power of the benefits."

[^fischhoff]: Baruch Fischhoff, Paul Slovic, Sarah Lichtenstein, Stephen Read & Barbara Combs, "How Safe Is Safe Enough? A Psychometric Study of Attitudes Towards Technological Risks and Benefits," *Policy Sciences* 9(2):127–152 (1978), https://doi.org/10.1007/BF00143739. Psychometric elicitation of perceived risk, acceptable risk and perceived benefit across 30 activities/technologies; acceptable risk correlates with benefit.

[^slovicrisk]: Paul Slovic, "Perception of Risk," *Science* 236(4799):280–285 (1987), https://doi.org/10.1126/science.3563507. The canonical psychometric-paradigm paper: dread and unknown-risk factors structure lay risk perception and acceptability.

[^zhang]: Baobao Zhang & Allan Dafoe, *Artificial Intelligence: American Attitudes and Trends* (Center for the Governance of AI, University of Oxford, 2019), https://doi.org/10.2139/ssrn.3312874. Nationally representative n=2,000 US adults; more than 8 in 10 agree AI and/or robots "require careful management." The closest large US precedent for AI-attitude measurement.

[^kk92]: Daniel Kahneman & Jack L. Knetsch, "Valuing Public Goods: The Purchase of Moral Satisfaction," *Journal of Environmental Economics and Management* 22(1):57–70 (1992), https://doi.org/10.1016/0095-0696(92)90019-S. The embedding effect: CVM estimates of the same good "may differ by more than an order of magnitude, all with an a priori equal claim to validity."

[^desvousges]: William H. Desvousges, F. Reed Johnson, Richard W. Dunford, Kevin J. Boyle, Sara P. Hudson & K. Nicole Wilson, *Measuring Nonuse Damages Using Contingent Valuation: An Experimental Evaluation of Accuracy* (Research Triangle Institute, 1992; reissued 2010), https://doi.org/10.3768/rtipress.2009.bk.0001.1009. Mean stated WTP to save 2,000 / 20,000 / 200,000 migrating birds was essentially flat — the textbook scope-insensitivity result. (Exact dollar figures circulate secondhand; verify against the RTI report before quoting them.)

[^slovic2007]: Paul Slovic, "'If I Look at the Mass I Will Never Act': Psychic Numbing and Genocide," *Judgment and Decision Making* 2(2):79–95 (2007). Feelings value individual lives strongly but are insensitive to large numbers; "the deterioration of compassion may appear in groups as small as two persons."

[^hseerott]: Christopher K. Hsee & Yuval Rottenstreich, "Music, Pandas, and Muggers: On the Affective Psychology of Value," *Journal of Experimental Psychology: General* 133(1):23–30 (2004), https://doi.org/10.1037/0096-3445.133.1.23. Affect-based valuation is scope-insensitive; calculation-based valuation is scope-sensitive. (Bibliographic details verified; spot-check the text before quoting directly.)

[^schubert]: Stefan Schubert, Lucius Caviola & Nadira S. Faber, "The Psychology of Existential Risk: Moral Judgments about Human Extinction," *Scientific Reports* 9:15100 (2019), https://doi.org/10.1038/s41598-019-50145-9. N=2,507 (UK/US public, UK students). Verbatim: respondents "do not think that an extinction catastrophe would be uniquely bad relative to near-extinction catastrophes, which allow for recovery"; the judgement reverses when prompted to consider long-term consequences.

[^trainweeks]: Kenneth Train & Melvyn Weeks, "Discrete Choice Models in Preference Space and Willingness-to-Pay Space," in R. Scarpa & A. Alberini (eds), *Applications of Simulation Methods in Environmental and Resource Economics* 1–16 (Springer, 2005), https://doi.org/10.1007/1-4020-3684-1_1. A log-normal cost coefficient yields right-skewed, approximately log-normal WTP — a modelling convention chosen to keep WTP positive with finite moments, not an established empirical law. Corroborating: Hole & Kolstad, *Empirical Economics* 42(2):445–469 (2012); Daly, Hess & Train, *Transportation* 39(1):19–31 (2012).

[^sandorwedel]: Zsolt Sándor & Michel Wedel, "Designing Conjoint Choice Experiments Using Managers' Prior Beliefs," *Journal of Marketing Research* 38(4):430–444 (2001), https://doi.org/10.1509/jmkr.38.4.430.18904. Seminal use of Bayesian priors to construct efficient choice designs.

[^bliemer]: Michiel C. J. Bliemer, John M. Rose & Stephane Hess, "Approximation of Bayesian Efficiency in Experimental Choice Designs," *Journal of Choice Modelling* 1(1):98–127 (2008), https://doi.org/10.1016/S1755-5345(13)70024-1. Underpins Bayesian D-efficient design as implemented in standard tools.

[^tsuge]: Takahiro Tsuge, Atsuo Kishimoto & Kenji Takeuchi, "A Choice Experiment Approach to the Valuation of Mortality," *Journal of Risk and Uncertainty* 31(1):73–95 (2005), https://doi.org/10.1007/s11166-005-2931-6. Explicit DCE valuing mortality-risk reductions; examines how subjective risk perception moves marginal WTP.

[^deblaeij]: Arianne de Blaeij, Raymond J. G. M. Florax, Piet Rietveld & Erik Verhoef, "The Value of Statistical Life in Road Safety: A Meta-Analysis," *Accident Analysis & Prevention* 35(6):973–986 (2003), https://doi.org/10.1016/S0001-4575(02)00105-7. VSL estimates depend strongly on valuation method (stated vs revealed preference) and elicitation format. Companion road-safety DCE: Rizzi & Ortúzar, *Accident Analysis & Prevention* 35(1):9–22 (2003).

[^r2p2]: Health and Safety Executive, *Reducing Risks, Protecting People: HSE's Decision-Making Process* (R2P2) (HSE Books, 2001), https://www.hse.gov.uk/enforce/expert/r2p2.htm. Establishes the three-band tolerability-of-risk framework and ALARP; para 136 gives the societal-risk anchor — an accident causing 50 or more deaths in a single event "should be regarded as intolerable if the frequency is estimated to be more than one in five thousand per annum" (used to construct F–N criterion lines, slope −1).

[^hse1992]: Health and Safety Executive, *The Tolerability of Risk from Nuclear Power Stations* (rev. ed., HMSO, 1992). Origin of the three-region tolerability framework later generalised in R2P2; proposes ~1 in 1,000 per year as the upper (worker) individual-risk tolerability bound. (Bibliographic details verified; spot-check pages before quoting directly.)

[^hsee96]: Christopher K. Hsee, "The Evaluability Hypothesis: An Explanation for Preference Reversals between Joint and Separate Evaluations of Alternatives," *Organizational Behavior and Human Decision Processes* 67(3):247–257 (1996), https://doi.org/10.1006/obhd.1996.0077. Hard-to-evaluate attributes receive more weight in joint than separate evaluation; comparison confers evaluability.

[^hsee99]: Christopher K. Hsee, George F. Loewenstein, Sally Blount & Max H. Bazerman, "Preference Reversals between Joint and Separate Evaluations of Options: A Review and Theoretical Analysis," *Psychological Bulletin* 125(5):576–590 (1999), https://doi.org/10.1037/0033-2909.125.5.576. The canonical review-level citation for "comparison is easier than absolute judgement." (Bibliographic details verified; spot-check before quoting directly.)

[^tk74]: Amos Tversky & Daniel Kahneman, "Judgment under Uncertainty: Heuristics and Biases," *Science* 185(4157):1124–1131 (1974), https://doi.org/10.1126/science.185.4157.1124. Introduces anchoring-and-adjustment: estimates are "biased toward the initially presented values," with insufficient adjustment.

[^furnham]: Adrian Furnham & Hua Chu Boo, "A Literature Review of the Anchoring Effect," *Journal of Socio-Economics* 40(1):35–42 (2011), https://doi.org/10.1016/j.socec.2010.10.008. Anchoring is robust across finance, appraisal, sentencing, negotiation and forecasting, and hard to debias (see also Jacowitz & Kahneman, *Personality and Social Psychology Bulletin* 21(11):1161–1166, 1995). We found no authoritative result that presenting multiple anchors dampens single-anchor pull — treated here as a design hypothesis, not an established finding.

[^constructed]: Sarah Lichtenstein & Paul Slovic (eds), *The Construction of Preference* (Cambridge University Press, 2006), https://doi.org/10.1017/CBO9780511618031. The foundational volume for the constructed-preference view: preferences over unfamiliar quantities are built at elicitation, favouring structured judgement over free generation. (Bibliographic details verified; spot-check before quoting directly.)

[^chong]: Dennis Chong & James N. Druckman, "Framing Theory," *Annual Review of Political Science* 10:103–126 (2007), https://doi.org/10.1146/annurev.polisci.10.072805.103054. The standard citation for framing effects on public opinion, with a psychological model of how frames operate.

[^haaland]: Ingar Haaland, Christopher Roth & Johannes Wohlfart, "Designing Information Provision Experiments," *Journal of Economic Literature* 61(1):3–40 (2023), https://doi.org/10.1257/jel.20211658. Best practice on measuring beliefs, designing the information intervention, measuring updating, and handling confounds such as experimenter demand.

[^elm]: Richard E. Petty & John T. Cacioppo, "The Elaboration Likelihood Model of Persuasion," *Advances in Experimental Social Psychology* 19:123–205 (1986), https://doi.org/10.1016/S0065-2601(08)60214-2. Central route (high elaboration, argument scrutiny) vs peripheral route (low elaboration, cue reliance); central-route change is more persistent and behaviour-predictive.

[^cokely]: Edward T. Cokely, Mirta Galesic, Eric Schulz, Saima Ghazal & Rocio Garcia-Retamero, "Measuring Risk Literacy: The Berlin Numeracy Test," *Judgment and Decision Making* 7(1):25–47 (2012). Introduces the 4-item test as a fast, psychometrically sensitive measure of statistical numeracy and risk literacy; a robust predictor of decision quality.
