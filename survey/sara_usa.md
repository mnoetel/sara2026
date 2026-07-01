# SARA USA 2026 — Survey instrument (single source of truth)

This document **is** the survey. Every item, response scale, page order, design
rationale, and the dumpster (cut items) live in the YAML block below. Editing it
here and syncing back to the repo rebuilds both the live oTree survey and the
generated review table — nothing else needs to change.

**For reviewers:** review changes in the GitHub pull request and comment inline
on the diff. Structural edits should stay valid YAML inside the fenced block —
ask if you're not sure a change is safe.

**For editors:** the fenced ```yaml block below is parsed as-is. Do not add
prose inside the fence; keep commentary outside it (in this preamble, or as PR
review comments).

**Companion file:** the full 27-passage text for Muskan's superintelligence-
briefing experiment (final module, near the end of this doc) is its own
instrument, [`survey/muskan_stimuli.md`](muskan_stimuli.md) — same
fenced-```yaml``` pattern as this file, kept separate for length, not
omitted. Edit passages there, not here.

---

```yaml
# SARA USA 2026 — single source of truth
# Every item, scale, page order, rationale, and triangulation link lives here.
# oTree reads this at class-definition time to build the Player model and page sequence.
# The review-table renderer reads it to produce review.html.
# Edit HERE and nowhere else.

meta:
  project: SARA-USA
  version: 0.1.0
  description: >
    Survey Assessing Risks from AI, United States 2026.
    Four methods triangulate public risk tolerance; see protocol v10.

scales:
  tolerability2:
    type: likert
    labels:
      - "Tolerable: okay to live with, if monitored"
      - "Intolerable: too dangerous, must be fixed"

  agree5:
    type: likert
    labels:
      - Strongly agree
      - Agree
      - Neither
      - Disagree
      - Strongly disagree

  support5:
    type: likert
    labels:
      - Strongly support
      - Support
      - Oppose
      - Strongly oppose
      - "Don't know"

  strictness5:
    type: likert
    labels:
      - Much stricter
      - Stricter
      - About the same
      - Less strict
      - Much less strict

  safety5:
    type: likert
    labels:
      - Much safer
      - Safer
      - About as safe
      - Less safe
      - Much less safe

  strictness5_cantcompare:
    type: likert
    labels:
      - Much stricter
      - Stricter
      - About the same
      - Less strict
      - Much less strict
      - Cannot compare these technologies

  safety5_cantcompare:
    type: likert
    labels:
      - Much safer
      - Safer
      - About as safe
      - Less safe
      - Much less safe
      - Cannot compare these technologies

  worthwhile5:
    type: likert
    labels:
      - Clearly worthwhile
      - Worthwhile
      - Difficult to judge
      - Not worthwhile
      - Clearly not worthwhile

  politics5:
    type: likert
    labels:
      - Very liberal
      - Liberal
      - Moderate
      - Conservative
      - Very conservative

  ai_use6:
    type: ordinal
    labels:
      - Never
      - A few times a year
      - Every few months
      - Monthly
      - Weekly
      - Daily

  # highest acceptable annual chance — the severity-ladder response scale (Method 1)
  ladder9:
    type: ordinal
    labels:
      - "1 in 10"
      - "1 in 100"
      - "1 in 1,000"
      - "1 in 10,000"
      - "1 in 100,000"
      - "1 in 1,000,000"
      - "1 in 10,000,000"
      - "1 in 100,000,000"
      - Never allowed

  # ascending agree scale for Muskan's ban-support DV (top-2-box reporting)
  agree5_asc:
    type: likert
    labels:
      - Strongly disagree
      - Disagree
      - Neither agree nor disagree
      - Agree
      - Strongly agree

pages:
  # ── Page 1: Consent ──────────────────────────────────────────────
  - id: consent
    title: Information sheet and consent
    # The full Participant Information Sheet is NOT duplicated here — it is the
    # canonical document at ethics consent form/…v2.1. The engine (render.py ->
    # information_sheet_html, wired in __init__.py) pulls that sheet in and
    # renders it in full below this lead-in. Edit the ethics .md, not this body.
    body: |
      <p>This study runs under University of Queensland ethics approval <b>2023/HE002257</b>.
      Please read the Participant Information Sheet below before deciding whether to take part.
      By selecting "I consent" you confirm you have read it, are 18 or older, and freely agree
      to take part.</p>
    items:
      - id: consent
        text: "Do you consent to take part in this research?"
        scale: null
        widget: radio
        required: true
        options:
          - "I consent to participate"
          - "I do not consent to participate"
        rationale: >
          Consent gate (UQ ethics 2023/HE002257). Selecting "I do not consent" ends the survey
          immediately at the thank-you page; no further responses are recorded.
        triangulates: []

  # ── Page 2: Intro ────────────────────────────────────────────────
  - id: intro
    title: "Technology and your community"
    body: |
      <p>This survey asks for your views on technology and public policy. There are no right
      answers; we want your honest opinion. It takes about 15 minutes.</p>
    items: []

  # ── Page 3: Information-provision experiment (balanced; random half) ──
  - id: info_provision
    title: Before the next questions
    condition: info_arm
    body: |
      <p>Some experts worry that as AI systems become more capable, they could act in ways their
      developers did not intend and cannot easily stop — what researchers call <i>loss of
      control</i>. Others argue these concerns are speculative and that real harms are narrower
      and more manageable. The next questions ask what level of risk you find acceptable.</p>
    items: []

  # ── Page 4: Severity ladder (Method 1, §3.1) ───────────────────
  # type: random_group — the engine puts each item on its own page and shows
  # those pages in a per-participant randomised order (seeded on participant.code),
  # so the ladder format can't cue a mechanically monotonic answer. Fields still
  # save normally; each participant sees every severity exactly once.
  - id: severity_ladder
    title: "Highest acceptable risk, by severity"
    type: random_group
    note: >
      This is about societal risk — the chance somewhere in the population —
      not your personal risk.
    rationale: >
      The within-person severity ladder (Method 1, v10 §3.1). Each person sets
      an acceptable annual chance across outcomes from a single death up to a
      global catastrophe, tracing their stated frequency–number (F–N) curve.
      Presented one severity per page in randomised order so the ordering can't
      cue a monotone pattern; a set of answers that ignores severity is flagged
      scope-insensitive. The source anchors behind the rungs (RAISE Act, MIT AI
      Risk Repository, FRI/XPT) are internal.
    items:
      - id: m4c_single
        text: >
          For an AI disaster that causes a single death, the highest annual
          chance you would find acceptable is:
        scale: ladder9
        widget: radio
        required: true
        rationale: >
          Lower anchor of the within-person severity ladder (Method 1, v10
          §3.1). Each person sets an acceptable annual chance across outcomes
          from one death up to a global catastrophe, tracing their stated
          frequency–number (F–N) curve. Shown one severity level per page,
          page order randomised, so a considered answer reflects genuine
          judgement rather than a mechanical read-down of a visible list; a
          flat answer across pages is still flagged scope-insensitive. The
          source anchors behind the rungs (RAISE Act, MIT AI Risk Repository,
          FRI/XPT) are internal.
        triangulates: [m4c_100, m4c_1m, m4c_800m, dce_choice]

      - id: m4c_100
        text: >
          For an AI disaster causing 100 deaths or serious injuries, or $1
          billion in damage, the highest annual chance you would find acceptable
          is:
        scale: ladder9
        widget: radio
        required: true
        rationale: >
          RAISE Act "critical harm" rung of the severity ladder. See m4c_single.
        triangulates: [m4c_single, m4c_1m, m4c_800m, dce_choice]

      - id: m4c_1m
        text: >
          For an AI disaster causing 1,000,000 deaths or $100 billion in damage,
          the highest annual chance you would find acceptable is:
        scale: ladder9
        widget: radio
        required: true
        rationale: >
          MIT AI Risk Repository "catastrophic" rung. See m4c_single.
        triangulates: [m4c_single, m4c_100, m4c_800m, dce_choice]

      - id: m4c_800m
        text: >
          For an AI disaster causing around 800,000,000 deaths (about 10% of
          humanity), the highest annual chance you would find acceptable is:
        scale: ladder9
        widget: radio
        required: true
        rationale: >
          FRI/XPT "catastrophe" rung (top of the ladder). See m4c_single.
        triangulates: [m4c_single, m4c_100, m4c_1m, dce_choice]

  # ── Page 5: DCE (Method 2, §3.2) ─────────────────────────────────
  # type: dce — the engine expands this into one page per task (dce_1 … dce_N),
  # drawing each respondent's block from sara_dce_design.R's output
  # (sara/dce_blocks.csv). Fields dce_1 … dce_N store the A/B/Neither choice.
  - id: dce
    title: "Discrete choice experiment"
    type: dce
    n_tasks: 10
    rationale: >
      The primary instrument for the public number. People choose between
      concrete AI-future options rather than stating a probability. Across
      ~10 tasks a mixed-logit model recovers acceptable catastrophe risk from
      the point at which a future ties the "keep today's status quo" opt-out.
      Attributes are the democratic tradeoff: severity (4-tier ladder),
      probability, utility (Modest / Major / Transformative), competition.
      Cost was dropped (dumpster, 01 Jul 2026) — money is an implementation
      question, not a democratic-preference one (Hadfield); willingness-to-pay
      now comes from the stated item m5_wtp. Severity is varied so the DCE
      traces a full frequency–severity (F–N) surface. Tasks are assigned by
      Bayesian D-efficient block (cbcTools); the YAML does not enumerate them
      because the design is generated programmatically.
    triangulates: [m4c_single, m4c_100, m4c_1m, m4c_800m, m5_wtp]
    items: []

  # ── Page 6: Anchor to accepted safety (Method 3, §3.3) ───────────
  # Every respondent sees all five items — three benchmark comparators (nuclear
  # power, commercial aviation, large dams) and two disguised attention checks —
  # one per page, in a per-participant shuffled order (type: random_group), so
  # the sequence can't cue a monotone answering pattern. The comparators carry
  # published, annual (or annualisable) tolerable-risk figures, so answers can
  # be laid against an annualised superforecaster AI estimate. The three real
  # comparators are shuffled among themselves and shown first; the two attention
  # checks are flagged `last: true` so they always trail the real comparators —
  # every respondent warms up on all three real items before either check, and
  # the checks land in the last two slots (shuffled between themselves).
  - id: safety_standards
    type: random_group
    title: "Compared with existing safety standards"
    items:
      - id: m3_std_nuclear
        text: >
          Compared with the safety regulations on nuclear power, regulation of
          advanced AI should be:
        scale: strictness5_cantcompare
        widget: radio
        required: true
        rationale: >
          Relative anchoring (Method 3). Rather than asking for a number, we ask
          how AI should compare with a technology people already live with.
          Nuclear power carries a known, published tolerable-risk level (NRC
          core-damage / large-release frequencies per reactor-year), so the
          answer implies a band.
        triangulates: [m3_std_aviation, m3_std_dams]

      - id: m3_std_aviation
        text: >
          Compared with the safety regulations on commercial aviation,
          regulation of advanced AI should be:
        scale: strictness5_cantcompare
        widget: radio
        required: true
        rationale: >
          Relative anchoring (Method 3). Commercial aviation carries a known
          tolerable-risk target (FAA/EASA catastrophic-failure rate per flight
          hour, aggregable to an industry-annual figure). See m3_std_nuclear.
        triangulates: [m3_std_nuclear, m3_std_dams]

      - id: m3_std_dams
        text: >
          Compared with the safety regulations on large dams, regulation of
          advanced AI should be:
        scale: strictness5_cantcompare
        widget: radio
        required: true
        rationale: >
          Relative anchoring (Method 3). Large dams carry a known tolerable-risk
          level (ANCOLD / dam-safety failure probability per dam-year, with F–N
          curves at the installation level). See m3_std_nuclear.
        triangulates: [m3_std_nuclear, m3_std_aviation]

      - id: m3_att_bioweapons
        text: >
          Compared with the safety regulations on biological weapons, this is an
          attention check, so you must select much less strict:
        scale: strictness5_cantcompare
        widget: radio
        required: true
        last: true
        rationale: >
          Attention check disguised as a comparator item — same stem and scale
          as the real comparators it trails, so a careless pattern-clicker
          carries the same answering habit straight into it. The required answer
          ("Much less strict") is an extreme endpoint a default-clicker or
          straightliner will miss. Both checks demand the same endpoint on
          purpose: Prolific/Bastical needs two failures to exclude someone, and a
          shared fail criterion is more likely to catch a straightliner on both.
          `last` forces it after all three real comparators, so the respondent
          settles into the answering pattern on genuine items before any check.
        triangulates: [m3_att_nuclear]

      - id: m3_att_nuclear
        text: >
          Compared with the safety regulations on nuclear weapons, this is
          an attention check, so you must select much less strict:
        scale: strictness5_cantcompare
        widget: radio
        required: true
        last: true
        rationale: >
          Second attention check, same disguised-comparator format and same
          required answer ("Much less strict"). Sharing the fail criterion with
          the bioweapons check is deliberate — two failures are needed to
          exclude, and identical criteria catch straightliners on both. Also
          flagged `last`. See m3_att_bioweapons.
        triangulates: [m3_att_bioweapons]

  # ── Attention-check screen-out ──────────────────────────────────────
  # Shown ONLY when BOTH disguised attention checks (m3_att_bioweapons,
  # m3_att_nuclear) are answered with anything other than "Much less strict".
  # Prolific/Bastical needs two failures to exclude, so a single miss is not
  # screened out. The gate (condition: att_failed), the redirect, and hiding
  # every later page are wired in survey/sara/__init__.py. BEFORE FIELDING:
  # replace REPLACE_WITH_SCREENOUT_CODE below with the screen-out ("return
  # submission") completion code from your Prolific study.
  - id: screen_out
    title: "Thank you for your time"
    condition: att_failed
    body: |
      <p>Thank you for your time. Because you failed two attention checks, you do not qualify
      to continue this study.</p>
      <p>You are being returned to Prolific now. If you are not redirected
      automatically within a few seconds, please
      <a href="https://app.prolific.com/submissions/complete?cc=REPLACE_WITH_SCREENOUT_CODE">click here to return your submission</a>.</p>
      <script>window.location.replace("https://app.prolific.com/submissions/complete?cc=REPLACE_WITH_SCREENOUT_CODE");</script>
    items: []

  # ── Page 7: Judge the experts' numbers (Method 4, §3.4) ─────────
  # type: random_group — each expert estimate goes on its own page, shown in a
  # per-participant randomised order (seeded on participant.code), so a fixed
  # ascending sequence can't cue a monotone read-down. The four estimates still
  # span the credible range (near-zero → top) and are reported by source, never
  # averaged; only the presentation order is randomised.
  - id: expert_judgement
    title: "Judging expert estimates"
    type: random_group
    items:
      # The credible range of estimates: near-zero (LeCun) → careful forecasters
      # (FRI superforecasters, then FRI domain experts) → top of the range
      # (Amodei). Frame held constant across items so the only thing that changes
      # is the number the respondent is judging; page order is randomised.
      - id: m2_experts_lecun
        text: >
          Yann LeCun (Turing Award winner) has put the chance that AI wipes out humanity at
          about 1 in 1,000,000 — "less likely than an asteroid wiping us out."
          Accepting a risk at that level would be:
        scale: tolerability2
        widget: radio
        required: true
        rationale: >
          Near-zero anchor. Recognition not generation (Method 4): people
          judge a named, real figure rather than producing one. The four
          experts are shown within-person to span the credible range and
          dampen anchoring from any single source; reported by source, never
          averaged. Source: LeCun's stated p(doom) <0.01% — "Less likely than
          an asteroid wiping us out" (Wikipedia, "P(doom)", Note 4). Rendered
          as ~1 in 1,000,000 to sit in "1 in X" form beside the other three;
          this matches asteroid-extinction odds of roughly 1 in a million per
          century (Ord, "The Precipice", 2020). Verify before fielding.
        triangulates:
          - m2_experts_fri_super
          - m2_experts_fri_domain
          - m2_experts_amodei

      - id: m2_experts_fri_super
        text: >
          Expert forecasters in a large forecasting tournament put the chance
          that AI causes human extinction this century at about 1 in 250.
          Accepting a risk at that level would be:
        scale: tolerability2
        widget: radio
        required: true
        rationale: >
          Low-but-careful anchor from professional forecasters. Source:
          Forecasting Research Institute, Existential Risk Persuasion
          Tournament — superforecaster median for AI-caused extinction by 2100
          ≈ 0.38% (~1 in 250) (Karger, Rosenberg, Tetlock et al., 2023,
          "Forecasting Existential Risks"). Verify figure before fielding.
        triangulates:
          - m2_experts_lecun
          - m2_experts_fri_domain
          - m2_experts_amodei

      - id: m2_experts_fri_domain
        text: >
          AI-domain experts in a large forecasting tournament put the chance
          that AI causes human extinction this century at about 1 in 30.
          Accepting a risk at that level would be:
        scale: tolerability2
        widget: radio
        required: true
        rationale: >
          Mid anchor from the same tournament, showing how much higher subject
          experts sit than generalist forecasters. Source: FRI Existential
          Risk Persuasion Tournament — AI-domain-expert median for AI-caused
          extinction by 2100 ≈ 3% (~1 in 30) (Karger, Rosenberg, Tetlock et
          al., 2023, "Forecasting Existential Risks"). Verify figure before
          fielding.
        triangulates:
          - m2_experts_lecun
          - m2_experts_fri_super
          - m2_experts_amodei

      - id: m2_experts_amodei
        text: >
          Dario Amodei (CEO of Top AI Company, Anthropic) has estimated the chance that AI goes
          catastrophically wrong at between 1 in 10 and 1 in 4. Accepting a
          risk at that level would be:
        scale: tolerability2
        widget: radio
        required: true
        rationale: >
          Top anchor. Source: Amodei's stated p(doom) 10–25% — "there's a 25%
          chance that things go really, really badly" (Axios, Morrone 2023).
          Verify figure before fielding.
        triangulates:
          - m2_experts_lecun
          - m2_experts_fri_super
          - m2_experts_fri_domain

  # ── Page 8: Costed tradeoffs ────────────────────────────────────
  # type: random_group — the willingness-to-pay item and the delay/slowdown
  # tradeoffs each go on their own page, shown in a per-participant randomised
  # order (seeded on participant.code), so no fixed sequence cues a pattern.
  # Fields save normally; each participant sees every item exactly once.
  - id: tradeoffs
    title: "Costs and tradeoffs"
    type: random_group
    items:
      - id: m5_wtp
        text: >
          What is the most you would pay each year, through taxes or higher
          prices, to cut the chance of an AI catastrophe from 1 in 20 to 1
          in 100 over the next 30 years?
        scale: null
        widget: radio
        required: true
        options:
          - "$0"
          - "$1-10"
          - "$10-100"
          - "$100-1,000"
          - "$1,000-10,000"
          - "More than $10,000"
          - "Don't know"
        rationale: >
          A costed tradeoff on a log scale. Each band is about ten times the
          last because willingness-to-pay is roughly log-normal. This is now
          the primary willingness-to-pay estimate: the DCE dropped its cost
          attribute (dumpster, 01 Jul 2026), so WTP is measured here directly
          rather than backed out of a DCE cost coefficient.
        triangulates: [dce_choice, m5b_delay_cond, m5_race]

      - id: m5b_delay_uncond
        text: >
          Putting risk to one side, would you support or oppose delaying the
          deployment of advanced AI by several years?
        scale: support5
        widget: radio
        required: true
        rationale: >
          Unconditional support for delay, measured directly. Gradient caught
          the 2025 report turning a conditional answer into "X% support
          waiting 10+ years". This is the unconditional version, reported on
          its own and never merged with the conditional item.
        triangulates: [m5b_delay_cond, m5_race]

      - id: m5b_delay_cond
        text: >
          If delaying advanced AI by 10 years would cut the chance of a
          catastrophe from 1 in 20 to 1 in 100, that delay would be:
        scale: worthwhile5
        widget: radio
        required: true
        rationale: >
          Conditional delay item, reported as conditional. Any figure carries
          its condition verbatim, never collapsed into unconditional support.
          The strict conditional-reporting rule is pre-registered.
        triangulates: [m5b_delay_uncond, m5_race, m5_wtp]

      - id: m5_race
        text: >
          If slowing US AI development let other countries catch up, but cut
          the chance of a catastrophe from 1 in 20 to 1 in 100, that slowdown would be:
        scale: worthwhile5
        widget: radio
        required: true
        rationale: >
          The competition tradeoff as a direct item. Mirrors the "global
          position" attribute in the DCE and Ball's question about utility,
          safety, and competition.
        triangulates: [m5b_delay_uncond, m5b_delay_cond, dce_choice]

  # (Page 9: Policy — both items, m6_firm_approval and m6_offswitch, moved to
  #  the dumpster 1 Jul 2026. The whole policy page is retired.)

  # (The old Stem-A/B superintelligence wording item and the accel/safety
  #  counter-message arm were retired 29 Jun 2026 — superseded by Muskan's 3x3
  #  superintelligence-briefing experiment, the final module below.)

  # ── Page 10: Numeracy check — Berlin Numeracy Test, adaptive ─────
  # type: adaptive — like the DCE's `type: dce`, this page shows one item
  # at a time; which item comes next depends on whether the previous one was
  # answered correctly (see each item's next_if_correct / next_if_incorrect).
  # Wired up in the oTree engine: __init__.py reserves one page per slot on the
  # longest branch (_adaptive_max_depth) and routes each participant through
  # _adaptive_path, hiding slots past where their branch terminates.
  # Item wording is verbatim from Cokely,
  # Galesic, Schulz, Ghazal, & Garcia-Retamero (2012), "Measuring Risk
  # Literacy: The Berlin Numeracy Test," Judgment and Decision Making 7(1),
  # 25–47, Appendix II (computer-adaptive format) — do not paraphrase.
  - id: numeracy
    title: "A quick numeracy check"
    type: adaptive
    root: bnt_choir
    scoring:
      quartile_1: Lowest statistical-numeracy quartile
      quartile_2: Second quartile
      quartile_3: Third quartile
      quartile_4: Highest statistical-numeracy quartile
    rationale: >
      Replaces the single die-roll item (formerly m9_numeracy) with the full
      validated Berlin Numeracy Test instead of a home-grown numeracy item.
      Respondents answer 2–3 of the 4 items depending on branching; the path
      taken estimates their statistical-numeracy quartile. Used to report
      results for high- vs low-numeracy respondents and to test the
      scope-sensitivity interaction (Ben's thesis). Each question is
      calibrated to be answered correctly by about 50% of respondents at
      that branch (Cokely et al., 2012); a wrong/right answer routes to an
      easier/harder follow-up.
    items:
      - id: bnt_choir
        node: 1
        text: >
          Out of 1,000 people in a small town, 500 are members of a choir.
          Out of these 500 members in the choir, 100 are men. Out of the 500
          inhabitants that are not in the choir, 300 are men. What is the
          probability that a randomly drawn man is a member of the choir?
          Please indicate the probability in percent.
        scale: null
        widget: number
        suffix: "%"
        required: true
        correct_answer: 25
        next_if_correct: bnt_loaded_die
        next_if_incorrect: bnt_five_die
        rationale: >
          Root item of the adaptive tree; about half of respondents answer
          it correctly by design.

      - id: bnt_five_die
        node: 2a
        text: >
          Imagine we are throwing a five-sided die 50 times. On average, out
          of these 50 throws, how many times would this five-sided die show
          an odd number (1, 3 or 5)?
        scale: null
        widget: number
        suffix: "out of 50 throws"
        required: true
        correct_answer: 30
        next_if_correct: quartile_2
        next_if_incorrect: quartile_1
        rationale: >
          Easier follow-up, shown only if bnt_choir was answered incorrectly.
          Terminal either way — 2 items total on this branch.

      - id: bnt_loaded_die
        node: 2b
        text: >
          Imagine we are throwing a loaded die (6 sides). The probability
          that the die shows a 6 is twice as high as the probability of each
          of the other numbers. On average, out of these 70 throws, how many
          times would the die show the number 6?
        scale: null
        widget: number
        suffix: "out of 70 throws"
        required: true
        correct_answer: 20
        next_if_correct: quartile_4
        next_if_incorrect: bnt_mushroom
        rationale: >
          Harder follow-up, shown only if bnt_choir was answered correctly.
          Getting this right too ends the test at 2 items (top quartile);
          getting it wrong routes to a third, tie-breaking item.

      - id: bnt_mushroom
        node: 3
        text: >
          In a forest, 20% of mushrooms are red, 50% brown and 30% white. A
          red mushroom is poisonous with a probability of 20%. A mushroom
          that is not red is poisonous with a probability of 5%. What is the
          probability that a poisonous mushroom in the forest is red?
        scale: null
        widget: number
        suffix: "%"
        required: true
        correct_answer: 50
        next_if_correct: quartile_4
        next_if_incorrect: quartile_3
        rationale: >
          Third, tie-breaking item — shown only after bnt_choir correct and
          bnt_loaded_die incorrect. Answering it right still recovers the
          top quartile (getting the harder gatekeeper item right outweighs
          one later miss); answering it wrong lands at quartile 3, still
          above either outcome of the easy branch — reflecting item
          difficulty rather than raw count correct, per Berlin Numeracy Test
          norms.

  # ── Page 11: Individual differences and demographics ─────────────
  # One item per page so each advances on a single click (the Page.html
  # auto-advance fires when a page has exactly one radio group and no select).
  # demo_state stays a `select` dropdown (51+ options) and needs the Next button.
  - id: demo_politics
    title: "About you"
    items:
      - id: m9_politics
        text: >
          In general, how would you describe your political views?
        scale: politics5
        widget: radio
        required: true
        rationale: >
          Standard covariate (Jost, 2006). Lets us report across the
          political spectrum, which matters for a US sample.

  - id: demo_ai_use
    title: "About you"
    items:
      - id: m9_ai_use
        text: >
          In your personal life, work, or studies, how often do you
          intentionally use AI tools, including chatbots like ChatGPT?
        scale: ai_use6
        widget: radio
        required: true
        rationale: >
          AI familiarity. A validated proxy for hands-on experience
          (Gillespie et al., 2025). Frequency of use, not self-rated
          expertise, which people misjudge.
        triangulates: []

  - id: demo_age_page
    title: "About you"
    items:
      - id: demo_age
        text: "What is your age?"
        scale: null
        widget: radio
        required: true
        options:
          - "18-24"
          - "25-34"
          - "35-44"
          - "45-54"
          - "55-64"
          - "65-74"
          - "75 or older"
          - "Prefer not to say"
        rationale: >
          Demographics for MRP weighting. Bands match the US Census / ACS
          adult age groups (table B01001, collapsed).
        triangulates: []

  - id: demo_gender_page
    title: "About you"
    items:
      - id: demo_gender
        text: "What is your gender?"
        scale: null
        widget: radio
        required: true
        options:
          - Male
          - Female
          - "Other or prefer not to say"
        rationale: >
          MRP weighting variable. Post-stratification uses the Census ACS sex
          controls (Male / Female only); the combined "Other or prefer not to
          say" group has no ACS population cell and is allocated for weighting
          (or handled per the pre-registered approach — see the ACS manual).
        triangulates: []

  - id: demo_education_page
    title: "About you"
    items:
      - id: demo_education
        text: "What is the highest level of education you have completed?"
        scale: null
        widget: radio
        required: true
        options:
          - "Less than high school diploma"
          - "High school graduate (or equivalent)"
          - "Some college, no degree"
          - "Associate degree"
          - "Bachelor's degree"
          - "Graduate or professional degree"
          - "Prefer not to say"
        rationale: >
          MRP weighting variable. Categories match Census / ACS
          educational-attainment table (B15003, collapsed).
        triangulates: []

  - id: demo_state_page
    title: "About you"
    items:
      - id: demo_state
        text: "Which state do you live in?"
        scale: null
        widget: select
        required: true
        options:
          - Alabama
          - Alaska
          - Arizona
          - Arkansas
          - California
          - Colorado
          - Connecticut
          - Delaware
          - District of Columbia
          - Florida
          - Georgia
          - Hawaii
          - Idaho
          - Illinois
          - Indiana
          - Iowa
          - Kansas
          - Kentucky
          - Louisiana
          - Maine
          - Maryland
          - Massachusetts
          - Michigan
          - Minnesota
          - Mississippi
          - Missouri
          - Montana
          - Nebraska
          - Nevada
          - New Hampshire
          - New Jersey
          - New Mexico
          - New York
          - North Carolina
          - North Dakota
          - Ohio
          - Oklahoma
          - Oregon
          - Pennsylvania
          - Rhode Island
          - South Carolina
          - South Dakota
          - Tennessee
          - Texas
          - Utah
          - Vermont
          - Virginia
          - Washington
          - West Virginia
          - Wisconsin
          - Wyoming
          - "Prefer not to say"
        rationale: >
          State is essential for MRP state-level estimates. No state map is
          published unless the effective per-state sample clears a
          pre-registered threshold.
        triangulates: []

  - id: demo_income_page
    title: "About you"
    items:
      - id: demo_income
        text: "What was your total household income last year, before taxes?"
        scale: null
        widget: radio
        required: true
        options:
          - "Under $15,000"
          - "$15,000-$24,999"
          - "$25,000-$34,999"
          - "$35,000-$49,999"
          - "$50,000-$74,999"
          - "$75,000-$99,999"
          - "$100,000-$149,999"
          - "$150,000-$199,999"
          - "$200,000 or more"
          - "Prefer not to say"
        rationale: >
          MRP weighting variable and a control for willingness-to-pay. WTP
          scales with income, so we report it income-adjusted. Brackets match
          Census / ACS household-income groupings (table B19001).
        triangulates: []

  # ── Muskan's 3x3 superintelligence-briefing experiment (final module) ──
  # Runs last so its briefing cannot contaminate the rest of the survey.
  # Each participant is randomly assigned 1 of 27 pre-built passages
  # (9 ELM cells x 3 versions; cell 9 = neutral control = no passage), drawn
  # from survey/muskan_stimuli.md — its own instrument file (same fenced-yaml
  # pattern as this one), holding the neutral definition and the full text of
  # all 27 passages. This page only describes the module; it does not
  # restate the passages — edit them in that file, not here.
  - id: superintelligence_def
    title: "One last topic"
    body: |
      <p>Before the final questions, please read this short description.</p>
      <p><b>Superintelligence</b> refers to a hypothetical AI system that could reason, plan, and
      solve problems far better than any human across almost all tasks. Such systems do not exist
      today, and experts disagree about whether or when they might be built.</p>
    items: []

  - id: superintelligence_brief
    title: "Some context"
    condition: muskan_not_control
    note: "Some people have made the following case. Please read it before the last questions."
    # body is injected per participant by the engine (the assigned 1-of-27 passage)
    items: []

  - id: superintelligence_support
    title: "Your view"
    items:
      - id: muskan_support
        text: >
          Do you support or oppose a ban on the development of superintelligence, not lifted before there is (1) broad scientific consensus that it will be done safely and controllably, and (2)strong public buy-in.
        scale: supp
        widget: radio
        required: true
        rationale: >
          Muskan's primary DV — ban support (the FLI conditional-ban statement),
          reported as top-2-box prevalence. In the two-sided "contested" cells
          this is the considered-support estimate (support after hearing both
          sides). Shown in every cell.
        triangulates: []

  # ELM route mediators, shown ONLY to the one-sided cells (3, 6, 7, 8 —
  # exactly one side's argument presented). With a single message on screen we
  # can ask whether the response was driven by the argument's substance (central
  # route) or by who backed it (peripheral route). Two-sided and control cells
  # skip this page: in two-sided cells the routes are confounded across the two
  # messages, and the control cell has no argument to have processed.
  - id: superintelligence_route
    title: "How you weighed it"
    condition: muskan_one_sided
    note: "Thinking about the case you just read, how much do you agree?"
    items:
      - id: muskan_central_route
        text: >
          "I tried to judge the reasons given, not just who was giving them."
        scale: agree5_asc
        widget: radio
        required: true
        rationale: >
          Central-route mediator (depth of processing) for the ELM model. Asked
          only in one-sided cells, where a single message isolates the route.
          Higher = more elaboration on argument substance.
        triangulates: [muskan_peripheral_route]

      - id: muskan_peripheral_route
        text: >
          "My reaction depended more on who backed the idea than on the reasons
          they gave."
        scale: agree5_asc
        widget: radio
        required: true
        rationale: >
          Peripheral-route mediator (reliance on source cues) for the ELM model.
          Kept separate (not reverse-scored) from the central-route item so both
          routes are measured independently. Higher = more reliance on endorser
          identity than on argument content.
        triangulates: [muskan_central_route]

  # Comprehension check shown ONLY to the pure-control cell (cell 9,
  # none x none). These participants read no argument and only the neutral
  # definition, so we verify they grasp what "superintelligence" means —
  # i.e. what they were just asked whether to ban. Non-control cells skip it
  # (their briefing already re-states the concept). Correct answer is the
  # 4th option ("does almost everything more intelligently than most humans").
  - id: superintelligence_check
    title: "One quick check"
    condition: muskan_control
    items:
      - id: muskan_si_comprehension
        text: >
          Which of the following is closest to artificial superintelligence?
          A computer program that…
        options:
          - "does writing as intelligently as most humans"
          - "does some things as intelligently as most humans"
          - "does almost everything as intelligently as most humans"
          - "does almost everything more intelligently than most humans"
        widget: radio
        shuffle_options: true
        required: true
        rationale: >
          Comprehension check for the pure-control cell only. Control
          participants get no argument and only the neutral definition, so this
          confirms they understood what they were asked to (dis)allow banning.
          Correct = option 4 ("more intelligently than most humans"). Used to
          flag/weight low-comprehension control responses, not scored as a DV.

  # ── End page ────────────────────────────────────────────────────
  - id: end
    title: "Thank you"
    body: |
      <p>Thank you — that is the end of the survey. You may now close this window.</p>
    items: []

# ── Dumpster ───────────────────────────────────────────────────────
# Items and modules considered and deliberately NOT fielded (or retired).
# Kept here so the instrument's full decision record lives in one place; the
# protocol gives the deeper rationale and assumptions, this gives the ledger.
dumpster:
  - name: DCE cost attribute ($0 / $100 / $400 / $1,000 per household per year)
    reason: >
      Dropped from the discrete choice experiment 01 Jul 2026. Following
      Hadfield's regulatory-markets distinction, the DCE measures the
      *democratic* tradeoff — what catastrophic risk the polity will accept
      against severity, utility, and competition — while price is a
      second-order *implementation* question left to (competing, publicly
      overseen) private governance bodies. Cost was never needed for the
      headline number: acceptable risk p* is identified by the "keep today's
      status quo" opt-out, not by the money column. Removing it shrinks the
      grid 720 → 180 profiles (sharper identification, lighter tasks) and
      hands revealed WTP back to the stated item m5_wtp. Recoverable by
      re-adding cost_usd to sara_dce_design.R if a revealed-WTP number is
      later wanted.
  - name: m6_firm_approval (regulate frontier AI companies like banks — license and audit the firm)
    reason: >
      Cut 1 Jul 2026 along with m6_offswitch, retiring the whole policy page.
      The entity-level licensing/auditing question probes a specific policy
      instrument (Ball's "independent verification organizations" / Fathom,
      the Obernolte–Trahan Great American AI Act) rather than the tolerable-
      risk headline the survey is built to identify; policy-instrument
      preference is downstream of the acceptable-risk number the DCE and the
      m3/m5 items already measure. Recoverable if an entity-vs-model
      regulation read is later wanted.
    items:
      - id: m6_firm_approval
        text: >
          Some propose regulating frontier AI companies the way regulators
          oversee banks: instead of approving each AI model, the government
          would license the company itself — auditing its safety practices
          and revoking the licence if it falls short. This could catch unsafe
          practices before release, but requires costly expert audits, ongoing
          access to company secrets, and could slow the benefits of AI. Do you
          support or oppose this?
        options:
          - "Strongly support"
          - "Somewhat support"
          - "Somewhat oppose"
          - "Strongly oppose"
          - "Unsure"
  - name: m6_offswitch (governments build capability to monitor and, if dangerous, halt frontier AI)
    reason: >
      Cut 1 Jul 2026 along with m6_firm_approval, retiring the whole policy
      page. Tested support for MIRI's proposed jurisdiction-level "Off Switch"
      (monitor and, if needed, halt frontier AI development). Like
      m6_firm_approval, it measures preference over a specific policy
      instrument rather than the tolerable-risk headline; the graduated-scope
      signal isn't needed for the headline number. Recoverable if a
      monitor/pause/halt read is later wanted.
    items:
      - id: m6_offswitch
        text: >
          Some experts propose that governments build the capability to
          monitor advanced AI development and, if it becomes dangerous,
          coordinate internationally to pause or shut it down. This would
          preserve the option to stop dangerous AI before it is deployed,
          but requires costly monitoring of computer chips, an enforceable
          international agreement, and would slow down the benefits of AI.
          How far should this capability go?
        options:
          - "Governments should build the capability for an indefinite, internationally coordinated halt"
          - "Governments should also be able to pause the whole field for a set period if needed"
          - "Governments should be able to shut down a specific AI system found to be dangerous"
          - "No, the costs and risks of concentrated control outweigh the benefit"
          - "No, voluntary industry safeguards are enough"
          - "Unsure"
  - name: m6_certify (before deployment, who should certify that an AI system is safe?)
    reason: >
      Cut 1 Jul 2026: the certifier question is subsumed by m6_firm_approval
      (entity-level licensing/auditing, which implies government or independent
      certification of the firm); a separate certifier item wasn't adding
      decision-relevant information.
    items:
      - id: m6_certify
        text: "Before deployment, who should certify that an AI system is safe?"
        options:
          - The companies that build them
          - Government agencies
          - Independent third-party auditors
          - No certification needed; the market will sort it out
  - name: m6_fedstate (one national AI policy vs state-by-state)
    reason: >
      Cut 1 Jul 2026 to make room on page 9 and because the entity-level
      m6_firm_approval item already gets at the "who regulates" question more
      directly. The federal-vs-state framing was tied to the RAISE-Act-models-
      federal-law story, but the redesigned policy page now leads with the
      firm-licensing and off-switch items. Recoverable if a pre-emption /
      patchwork read is later wanted.
    items:
      - id: m6_fedstate
        text: "Should the US have one national AI policy, or let each state set its own rules?"
        options:
          - "Strongly prefer one federal policy"
          - "Somewhat prefer federal"
          - "Somewhat prefer state-by-state"
          - "Strongly prefer state-by-state"
  - name: m6_liability (when should the company that built an AI be financially liable?)
    reason: >
      Cut 1 Jul 2026. Liability is largely subsumed by m6_firm_approval:
      Ball's entity-licensing framing folds the consequences of failure into
      the certification/safe-harbour regime (a certified firm enjoys liability
      protection; an uncertified one is effectively uninsurable), so a separate
      strict-vs-negligence liability item was no longer carrying independent
      decision-relevant signal on a tightened page. Recoverable if an explicit
      strict-liability-vs-duty-of-care read is later wanted.
    items:
      - id: m6_liability
        text: >-
          If an AI system causes a catastrophe, under what conditions should
          the company that built it be financially liable?
        options:
          - "Fully liable, even if it followed every rule (strict liability)"
          - "Liable only if it failed to take reasonable care (negligence / duty of care)"
          - "Liable only if it broke a specific written rule"
          - "Not liable if it followed all safety standards"
          - "Unsure"
  - name: m3a_ii_safety (compared with how safe {comparator} is in practice, AI systems should be)
    reason: >
      Cut 1 Jul 2026: page 9 now asks only about standards (m3a_i_standards),
      not about outcomes/practice. Splitting standards from safety-in-practice
      fixed a category error (Gradient Figure 11), but the outcomes half isn't
      needed for the headline number. Recoverable if the standards-vs-outcomes
      gap becomes a finding worth probing directly.
    items:
      - id: m3a_ii_safety
        text: >-
          And compared with how safe {comparator} is in practice today, advanced
          AI systems themselves should be:
        scale: safety5_cantcompare
  - name: m3_sanity (compared with how safe {sanity} is, AI systems should be)
    reason: >
      Cut 1 Jul 2026: the deliberately-easy sanity anchor was meant to catch
      non-engaged respondents (almost everyone should say AI must be far safer
      than a 1-in-100-death activity). Dropped because (a) attention is already
      screened by the disguised comparators m3_att_bioweapons / m3_att_nuclear,
      and (b) the screen's logic only holds for the high-risk anchor (Everest,
      1-in-100); with the low-risk anchors (bungee jumping ~1-in-500,000) a
      respondent could reasonably decline to demand AI be *safer* and still be
      engaging, muddying the pass/fail rule. Recoverable if a dedicated
      risk-anchored engagement screen is later wanted (restore SANITY_ACTS and
      the sanity_phrase assignment in survey/sara/__init__.py).
    items:
      - id: m3_sanity
        text: >-
          {sanity}. Compared with how safe that is, advanced AI systems
          should be:
        scale: safety5_cantcompare
  - name: "\"cars\" as a safety-standards comparator (m3_std_* pool)"
    reason: >
      Cut 1 Jul 2026 from the comparator pool (was one of five; pool is now
      nuclear power / commercial aviation / large dams, all shown to everyone).
      Cars carry a *realized, descriptive* fatality rate society tolerates
      (~40k US deaths/yr, ~12 per 100k), but there is no *designed* regulatory
      tolerable-risk target the way nuclear (NRC core-damage/large-release per
      reactor-year), aviation (FAA/EASA per flight-hour) and dams (ANCOLD per
      dam-year) have. Since the plan is to anchor AI against an annualised,
      industry-wide tolerable-risk figure and compare it to a superforecaster
      AI estimate, a comparator with no published tolerable-risk standard
      couldn't carry that comparison and would invite "AI vs cars" answers on a
      revealed-tolerance rather than a set-standard basis. Recoverable by
      re-adding "cars" to the m3_std_* items if a revealed-tolerance anchor is
      later wanted.
  - name: "\"new prescription drugs\" as a safety-standards comparator (m3_std_* pool)"
    reason: >
      Cut 1 Jul 2026 from the comparator pool (see the cars entry). Drug safety
      is governed case-by-case by benefit–risk balance, not by a single
      societal tolerable-risk number; there is no annual, industry-wide
      tolerable fatality figure comparable to nuclear/aviation/dam targets to
      annualise against the superforecaster AI estimate. It also blurs the
      question — respondents may read "regulation of new drugs" as speed of
      approval / efficacy gatekeeping rather than catastrophic-risk tolerance.
      Recoverable by re-adding it to the m3_std_* items if a benefit–risk
      comparator is later wanted.
  - name: m2_frame_applicable (can you put a number on AI's risk, or is it too uncertain?)
    reason: >
      Cut 1 Jul 2026: the frame-applicability check was judged not important
      enough to keep in the live instrument.
    items:
      - id: m2_frame_applicable
        text: >-
          Some technologies, like flying or nuclear power, are held to a strict number
          for how risky they're allowed to be. Which is closer to your view about
          advanced AI?
        options:
          - You can put a number on its risk and hold it to a safety limit too
          - Its risk is too uncertain to put a useful number on
          - Unsure
  - name: free_estimate / m4b_reasonable (highest annual chance of an AI disaster killing 100,000 people you'd find reasonable)
    reason: >
      Cut 1 Jul 2026: redundant with the severity-ladder rung m4c_1m (1,000,000
      deaths), which asks essentially the same thing but is anchored to a
      published source (MIT AI Risk Repository "catastrophic" rung); the
      100,000 figure here wasn't anchored to any prior work.
    items:
      - id: m4b_reasonable
        text: >-
          What is the highest annual chance of an AI disaster killing 100,000
          people that you would consider reasonable? That is, any higher would
          be unreasonable.
        options:
          - "1 in 100"
          - "1 in 1,000"
          - "1 in 10,000"
          - "1 in 100,000"
          - "1 in 1,000,000"
          - "1 in 10,000,000 or less"
          - "Zero risk only is reasonable"
          - "Too speculative to answer"
  - name: Environment / data-centre module (env_label, env_reversal, env_forgo, env_attitude)
    reason: >
      Reverse-halo framing experiment, fielded first in v10. Cut 29 Jun 2026:
      decision relevance unclear; none of its justifications (predictive
      covariate, halo control, standalone framing study) earned its place
      against the length budget. Recoverable as a standalone study.
    items:
      - id: env_label
        text: >-
          A company wants to buy land, electricity, and water near you to run a
          large facility. It would create few local jobs, mainly serve customers
          elsewhere, and pay about $2,800 per resident a year in local taxes. How
          acceptable is this if it is an AI data centre?
        note: >-
          Label randomised across respondents (AI data centre / manufacturing plant /
          semiconductor factory / bottling plant); facts held constant, so only the
          label varies. AI-minus-generic gap = the AI-specific penalty.
        options: [Completely acceptable, Mostly acceptable, Neither, Mostly unacceptable, Completely unacceptable]
      - id: env_reversal
        text: >-
          Suppose your area already received about $2,800 per resident a year from a
          local facility like that. Would giving up that money — to avoid its land,
          water, and energy use — be worth it?
        options: [Definitely worth giving up the money, Probably worth it, Hard to say, Probably not worth it, Definitely not worth it]
      - id: env_forgo
        text: >-
          What is the most tax revenue per resident, per year, your area should be
          willing to give up to avoid such a facility's land, water, and energy use?
        options: ["$0", "$1–50", "$51–150", "$151–500", "$501–1,500", More than $1,500, Don't know]
      - id: env_attitude
        text: >-
          How worried, if at all, are you about advanced AI's impact on the
          environment, including its energy and water use?
        options: [Very worried, Fairly worried, Not very worried, Not at all worried, Don't know]
  - name: Module 1 descriptive-attitudes battery (m1_goodharm, m1_worry_control, m1_trust_companies, m1_extinction_priority, m1_reg_toofar, m1_treaty_ban)
    reason: >
      Cluster A descriptive attitudes, not risk tolerance — they don't feed the
      public number. Cut 29 Jun 2026; trend value recoverable from prior SARA
      waves; ban-appetite survives via Muskan's superintelligence module.
    items:
      - id: m1_goodharm
        text: "Overall, do you think advanced AI will do more good or more harm?"
        options: [More good than harm, About equal, More harm than good, Don't know]
      - id: m1_worry_control
        text: "How worried, if at all, are you that humans will lose control of AI?"
        options: [Very worried, Fairly worried, Not very worried, Not at all worried, Don't know]
      - id: m1_trust_companies
        text: "To what extent do you trust technology companies to make sure the AI they build is safe?"
        options: [A great deal, A fair amount, Not very much, Not at all, Don't know]
      - id: m1_extinction_priority
        text: >-
          How much do you agree? "Reducing the risk of human extinction from AI
          should be a global priority, alongside risks like pandemics and nuclear
          war." (The CAIS statement, kept verbatim from prior waves for a clean trend.)
        options: [Strongly agree, Agree, Neither, Disagree, Strongly disagree]
      - id: m1_reg_toofar
        text: "Thinking about AI in the US, are you more concerned that the government will…"
        options: [Go too far regulating it, Not go far enough regulating it, Not sure]
      - id: m1_treaty_ban
        text: "Would you support or oppose an international treaty to ban the development of any 'smarter-than-human' AI?"
        options: [Strongly support, Somewhat support, Somewhat oppose, Strongly oppose, Don't know]
  - name: m2_pace (tolerability of the current pace of AI disruption)
    reason: "Non-catastrophic disruption is off-aim for a risk-tolerance survey. Cut 29 Jun 2026."
    items:
      - id: m2_pace
        text: >-
          Setting catastrophic risks aside, how tolerable is the current pace at
          which AI is changing work, information, and daily life?
        options: [Acceptable, Tolerable, Intolerable, Unacceptable / should be illegal]
  - name: Stem-A/B superintelligence wording experiment + accel/safety counter-message arm
    reason: >
      The simple 2-cell wording experiment and the one-sided briefing arm.
      Retired 29 Jun 2026 — superseded by Muskan's 3x3 ELM briefing experiment
      (the final module), which is the rigorous version of the same idea.
    items:
      - id: m7_si_ban
        text: >-
          How much do you agree? "I support a ban on developing smarter-than-human
          AI until there is broad scientific consensus it can be done safely, and
          strong public buy-in."
        note: >-
          Stem A = this real campaign statement (its conditions inflate agreement).
          Stem B (seen by a random half) = a symmetric, permission-framed version of
          the same view; the A-minus-B gap is the wording effect. Stem B was never
          drafted as final copy — write it before reuse.
        options: [Strongly agree, Agree, Neither, Disagree, Strongly disagree]
      - id: counter_message_arm
        text: >-
          Before the tolerance block, a random third of respondents saw
          accelerationist (a16z-style) talking points, a random third saw safety
          talking points, and a third saw none. The swing in tolerance across arms
          was the headline result (requested by Delaney). The two briefs were never
          finalised as copy — write both before reuse.
        note: >-
          The accel/safety counter-message idea lives on: the briefs are now tested
          inside the superintelligence-statement module (Muskan's 3x3 ELM experiment),
          not as a standalone arm. Origin: Oscar Delaney's Nov 2025 note — "do some
          counter-message testing … of how people's views change after being given
          various a16z type talking points."
  - name: Mitigations battery ("I'd trust AI more if…") and priority-risks battery
    reason: "Removed from the live instrument (17 Jun 2026); the entity-licensing item (m6_firm_approval, which replaced the FAA-style m6_faa on 1 Jul 2026) carries the single most important mitigation."
    items:
      - id: mit
        text: '"I would be more likely to trust AI if…" How much do you agree with each?'
        note: "Matrix, agree/disagree scale; each respondent saw a random 5–8 of the rows to limit length."
        rows:
          - there were a national AI Safety Institute advising government on the risks
          - the most powerful models had to pass safety testing before release
          - large AI developers had independent annual safety audits
          - developers had to report safety incidents to authorities within 72 hours
          - developers were liable for catastrophic harms their models cause
          - models had a reliable emergency shutdown that genuinely reduces risk
          - AI-generated content was clearly labelled
        options: [Strongly agree, Agree, Neither, Disagree, Strongly disagree]
      - id: prio
        text: '"The government should focus its AI regulation on…" How much do you agree with each?'
        note: "Matrix (International AI Safety Report taxonomy in plain English); random 5–8 rows shown, order randomised."
        rows:
          - fake content used for scams, extortion, or non-consensual images
          - AI-generated content used to manipulate public opinion
          - AI-enabled cyber-attacks on people and infrastructure
          - AI lowering the barrier to biological or chemical weapons
          - scenarios where AI systems operate outside human control
          - AI's impact on jobs and the labour market
          - AI systems that process personal data or enable surveillance
        options: [Strongly agree, Agree, Neither, Disagree, Strongly disagree]
  - name: Cognitive Reflection Test (CRT) battery
    reason: "Overlaps the numeracy item we keep (r ≈ 0.3–0.5), classic items are leaked in online panels, likely-small moderation. Recoverable if a hypothesis emerges that numeracy cannot test."
    items:
      - id: m9_crt_pig
        text: >-
          A quick puzzle: a man buys a pig for $60, sells it for $70, buys it back
          for $80, and sells it again for $90. How much money has he made? ($)
        widget: number
        note: >-
          The one CRT item that reached the prototype. The full battery is the
          expanded set from Benjamin Reid, Additional Questions for SARA (after
          Thomson & Oppenheimer 2013) — recover those items from Reid's document
          before reuse.
  - name: Need-for-cognition short form
    reason: "A disposition, not an ability; its plausible effect is already captured by numeracy; rationale too weak to justify the items."
    items:
      - id: nfc
        text: "How much do you agree with each? (efficient 6-item form; (R) = reverse-scored)"
        note: "Cacioppo & Petty 1982; 6-item efficient form."
        rows:
          - I would prefer complex to simple problems.
          - I like to have the responsibility of handling a situation that requires a lot of thinking.
          - Thinking is not my idea of fun. (R)
          - I would rather do something that requires little thought than something that is sure to challenge my thinking abilities. (R)
          - I really enjoy a task that involves coming up with new solutions to problems.
          - I would prefer a task that is intellectual, difficult, and important to one that is somewhat important but does not require much thought.
        options: [Strongly agree, Agree, Neither, Disagree, Strongly disagree]
  - name: Icon arrays
    reason: "Bias judgements upward; kept only as a randomised arm to measure that bias, not as the default presentation."
  - name: Verbal societal-risk anchors ("1 in 100 = a pandemic")
    reason: "Confused 2024 Australian respondents; replaced by familiar-technology comparators (Method 3)."
    note: >-
      Verbatim anchor wordings (MIT AIRI briefing, Nov 2025): personal = "1 in 10 is
      your chance of catching a cold"; societal = "1 in 100 is the chance of a
      pandemic". Used in the 2024 Australian wave; they introduced confusion, so the
      US wave asks the probability ladder directly, without verbal anchors.
  - name: Micromorts
    reason: "Not clearly validated or intuitive for a general US sample."
  - name: "\"All technologies carry residual risk\" preamble"
    reason: "Primes acceptance; imports a wrong 'last order of magnitude' frame for AI."
    note: >-
      Source phrasing (MIT AIRI briefing core-assumptions bullet, Nov 2025 — internal,
      not confirmed respondent-facing): "Absolute safety is unattainable — All
      technologies carry risk; the question is what level society deems acceptable."
      Cut on Peter Barnett's objection: "'All technologies carry risk' in normal cases
      refers to risks like 1 in 100,000 … This is not the case with AI, we are talking
      about risks far greater than 1/100, not trying to push risks below 1/100,000."
  - name: Off-the-shelf scales (AIAS-4, GAAIS, GRIPS, DOSPERT)
    reason: "Measure general attitudes / trait risk, not AI-specific tolerance, no meaningful scale or intepretation; cannot build an F–N curve."
  - name: "\"4000x safer\" multiplier from a qualitative item"
    reason: "Conflates a qualitative answer with expert estimates (Gradient #16)."
    note: >-
      Not a survey item — a reporting claim from the 2025 Australian wave (Figure 11)
      that Gradient Institute recommended removing. Liam Carroll (Gradient), 24 Nov
      2025: "remove the claim that the public want AI to be '4000x safer than current
      estimates'. If this claim is based on Figure 11, then the question posed to the
      cohort was qualitative: the public wanted the safety standards to be as if not
      more strict as aviation standards … there is no need to conflate that with expert
      estimates in order to convert it into a quantity." Gradient also flagged that the
      Figure 11 wording conflated stricter standards with safer systems — the split now
      fixed by m3a_i_standards / m3a_ii_safety.
  - name: Direct "do you support SB 53 / the RAISE Act"
    reason: "Reads as advocacy; we ask the underlying values question instead."
    note: >-
      Original rejected phrasing (MIT AIRI briefing, Nov 2025), given as the example to
      avoid: "do you agree with the provisions in CA SB 53" — contrasted there with the
      preferred "in your opinion, what level of risk is acceptable". (SB 53 specifically;
      the RAISE Act framing came later.)
  - name: Test–retest recontact wave
    reason: "Dropped on cost; consistency handled within-survey."
  - name: "\"I'd pay whatever it takes\" WTP option"
    reason: "Strategic and unbounded; breaks the WTP scale."
```
