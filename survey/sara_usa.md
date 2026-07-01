# SARA USA 2026 — Survey instrument (single source of truth)

This document **is** the survey. Every item, response scale, page order, design
rationale, and the dumpster (cut items) live in the YAML block below. Editing it
here and syncing back to the repo rebuilds both the live oTree survey and the
generated review table — nothing else needs to change.

**For reviewers:** leave comments anywhere in this doc (HackMD / Google Docs
style). Structural edits should stay valid YAML inside the fenced block — ask
if you're not sure a change is safe.

**For editors:** the fenced ```yaml block below is parsed as-is. Do not add
prose inside the fence; keep commentary outside it (in this preamble, or in
HackMD comment threads).

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
  tolerability4:
    type: likert
    labels:
      - Acceptable
      - Tolerable
      - Intolerable
      - "Unacceptable / should be illegal"

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

  support_delay5:
    type: likert
    labels:
      - Strongly support
      - Support
      - Neither
      - Oppose
      - Strongly oppose

  politics7:
    type: likert
    labels:
      - Very liberal
      - Liberal
      - Slightly liberal
      - Moderate
      - Slightly conservative
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
      - "1 in 1,000,000,000"
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
    # canonical document at ethics consent form/…v2.1. This page is the consent
    # gate; the engine should present that sheet in full on this screen at fielding.
    body: |
      <p>This study runs under University of Queensland ethics approval <b>2023/HE002257</b>.</p>
      <p><b>The Participant Information Sheet (v2.1)</b> — purpose, what's involved, risks, data
      handling and your rights — is the canonical consent document. It is <b>not duplicated
      here</b>; the full sheet is in
      <code>ethics consent form/Participant Information Sheet and Consent Form Version 2.1.md</code>
      and is to be presented in full on this screen before fielding.</p>
      <p>By selecting "I consent" you confirm you have read the Information Sheet, are 18 or
      older, and freely agree to take part.</p>
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
      ~10 tasks a mixed-logit model recovers acceptable catastrophe risk and
      willingness-to-pay. Attributes match Ball's tradeoff: severity (4-tier
      ladder), probability, utility, competition, cost. Severity is varied so
      the DCE traces a full frequency–severity (F–N) surface. Tasks are assigned
      by Bayesian D-efficient block (cbcTools); the YAML does not enumerate them
      because the design is generated programmatically.
    triangulates: [m4c_single, m4c_100, m4c_1m, m4c_800m, m5_wtp]
    items: []

  # ── Page 6: Anchor to accepted safety (Method 3, §3.3) ───────────
  - id: safety_comparators
    title: "Compared with existing safety standards"
    items:
      - id: m3a_i_standards
        text: >
          Compared with the safety regulations on {comparator}, regulation of
          advanced AI should be:
        scale: strictness5_cantcompare
        widget: radio
        required: true
        rationale: >
          Relative anchoring (Method 3). Instead of asking for a number, we
          ask how AI should compare with a technology people already live with.
          The named comparator carries a known risk level so the answer implies
          a band. Comparator randomised across respondents.
        triangulates: [m3_sanity]

      - id: m3_sanity
        text: >
          {sanity}. Compared with how safe that is, advanced AI systems
          should be:
        scale: safety5_cantcompare
        widget: radio
        required: true
        rationale: >
          A deliberately easy, high-risk sanity anchor. Almost everyone should
          say AI must be far safer than a 1-in-100-death activity. Anyone
          choosing "as safe" or "less safe" is probably not engaging.
          Comparator randomised across high-risk voluntary activities (bungee
          jumping, BASE jumping, Everest). Death rates are approximate; verify
          before fielding.
        triangulates: [m3a_i_standards]

      - id: m3_att_elevator
        text: >
          Compared with the safety regulations on elevators, this is an
          attention check, so you must select "Somewhat stricter":
        scale: strictness5_cantcompare
        widget: radio
        required: true
        rationale: >
          Attention check disguised as a comparator item — same stem and scale
          as the real items, buried among them so a careless pattern-clicker is
          caught. One of two with the same required answer ("Somewhat
          stricter"); the other (playground) sits later so they are not adjacent.
        triangulates: [m3_att_playground]

      - id: m3_att_playground
        text: >
          Compared with the safety regulations on playground equipment, this is
          an attention check, so you must select "Somewhat stricter":
        scale: strictness5_cantcompare
        widget: radio
        required: true
        rationale: >
          Second attention check, same disguised-comparator format and required
          answer. See m3_att_elevator.
        triangulates: [m3_att_elevator]

  # ── Page 7: Judge the experts' numbers (Method 4, §3.4) ─────────
  - id: expert_judgement
    title: "Judging expert estimates"
    items:
      - id: m2_experts_lecun
        text: >
          Yann LeCun (Meta) has estimated the chance of an AI catastrophe
          killing a large fraction of humanity at less than 1 in 10,000.
          Accepting a risk at that level would be:
        scale: tolerability4
        widget: radio
        required: true
        rationale: >
          Recognition not generation (Method 4). People judge a named,
          real figure rather than producing one. Shown within-person
          alongside other expert estimates to dampen anchoring from any
          single source. Reported by source, never as a single average.
          Figures are illustrative; replace with exact, citable quotations
          before fielding.
        triangulates:
          - m2_experts_altman
          - m2_experts_musk
          - m2_experts_amodei

      - id: m2_experts_altman
        text: >
          Sam Altman (OpenAI) has estimated the chance of an AI catastrophe
          killing a large fraction of humanity at about 1 in 50. Accepting
          a risk at that level would be:
        scale: tolerability4
        widget: radio
        required: true
        rationale: >
          See m2_experts_lecun rationale. Figures illustrative; verify before
          fielding.
        triangulates:
          - m2_experts_lecun
          - m2_experts_musk
          - m2_experts_amodei

      - id: m2_experts_musk
        text: >
          Elon Musk (xAI / Tesla) has estimated the chance of an AI
          catastrophe killing a large fraction of humanity at about 1 in 5.
          Accepting a risk at that level would be:
        scale: tolerability4
        widget: radio
        required: true
        rationale: >
          See m2_experts_lecun rationale. Figures illustrative; verify before
          fielding.
        triangulates:
          - m2_experts_lecun
          - m2_experts_altman
          - m2_experts_amodei

      - id: m2_experts_amodei
        text: >
          Dario Amodei (Anthropic) has estimated the chance of an AI
          catastrophe killing a large fraction of humanity at about 1 in 4.
          Accepting a risk at that level would be:
        scale: tolerability4
        widget: radio
        required: true
        rationale: >
          See m2_experts_lecun rationale. Figures illustrative; verify before
          fielding.
        triangulates:
          - m2_experts_lecun
          - m2_experts_altman
          - m2_experts_musk

  # ── Page 8: Costed tradeoffs ────────────────────────────────────
  - id: tradeoffs
    title: "Costs and tradeoffs"
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
          last because willingness-to-pay is roughly log-normal. The
          continuous WTP estimate comes from the DCE cost coefficient; this
          is the cross-check.
        triangulates: [dce_choice, m5b_delay_cond, m5_race]

      - id: m5b_delay_uncond
        text: >
          Putting risk to one side, would you support or oppose delaying the
          deployment of advanced AI by several years?
        scale: support_delay5
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
          catastrophe from 5% to 1%, that delay would be:
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
          the chance of a catastrophe from 5% to 1%, that slowdown would be:
        scale: worthwhile5
        widget: radio
        required: true
        rationale: >
          The competition tradeoff as a direct item. Mirrors the "global
          position" attribute in the DCE and Ball's question about utility,
          safety, and competition.
        triangulates: [m5b_delay_uncond, m5b_delay_cond, dce_choice]

  # ── Page 9: Policy ───────────────────────────────────────────────
  - id: policy
    title: "Policy preferences"
    items:
      - id: m6_faa
        text: >
          Some have proposed regulating frontier AI like the FAA regulates
          aircraft: models would have to pass independent safety testing
          before release, and the government could block or reverse a release
          that fails to meet safety standards. Do you support or oppose this?
        scale: null
        widget: radio
        required: true
        options:
          - "Strongly support"
          - "Somewhat support"
          - "Somewhat oppose"
          - "Strongly oppose"
          - "Unsure"
        rationale: >
          The FAA model: binding pre-release testing. This is Anthropic's
          stated proposal, presented neutrally as "some have proposed". It
          goes beyond the June 2026 White House executive order, which is
          security-focused and explicitly voluntary. Tests the single most
          consequential mitigation directly.
        triangulates: [m6_liability, m6_killswitch]

      - id: m6_fedstate
        text: >
          Should the US have one national AI policy, or let each state set
          its own rules?
        scale: null
        widget: radio
        required: true
        options:
          - "Strongly prefer one federal policy"
          - "Somewhat prefer federal"
          - "Somewhat prefer state-by-state"
          - "Strongly prefer state-by-state"
        rationale: >
          Federal pre-emption vs a state patchwork. Central to whether the
          RAISE Act can model federal law. Four-point forced choice with no
          midpoint to avoid fence-sitting on a binary policy question.
        triangulates: [m6_faa]

      - id: m6_killswitch
        text: >
          Should advanced AI be legally required to have an emergency "kill
          switch" to shut it down if it behaves dangerously?
        scale: null
        widget: radio
        required: true
        options:
          - "Yes, for all AI systems"
          - "Yes, but only for high-risk systems"
          - "No, voluntary guidelines are enough"
          - "Unsure"
        rationale: >
          Fills a gap in current bills. Neither the RAISE Act nor SB 53
          addresses post-deployment intervention.
        triangulates: [m6_faa, m6_liability]

      - id: m6_liability
        text: >
          If an AI system causes a catastrophe, under what conditions should
          the company that built it be financially liable?
        scale: null
        widget: radio
        required: true
        options:
          - "Fully liable, even if it followed every rule (strict liability)"
          - "Liable only if it failed to take reasonable care (negligence / duty of care)"
          - "Liable only if it broke a specific written rule"
          - "Not liable if it followed all safety standards"
          - "Unsure"
        rationale: >
          Liability rules, with a real middle option. Tests appetite for
          proposals like the RAISE Act and SB 53. The negligence /
          duty-of-care middle was added so support for strict liability
          is not overstated (Ball's point).
        triangulates: [m6_faa, m6_killswitch]

  # (The old Stem-A/B superintelligence wording item and the accel/safety
  #  counter-message arm were retired 29 Jun 2026 — superseded by Muskan's 3x3
  #  superintelligence-briefing experiment, the final module below.)

  # ── Page 10: Numeracy check — Berlin Numeracy Test, adaptive ─────
  # type: adaptive — like the DCE's `type: dce`, this page shows one item
  # at a time; which item comes next depends on whether the previous one was
  # answered correctly (see each item's next_if_correct / next_if_incorrect).
  # NOT YET WIRED UP in the oTree engine (survey/sara/__init__.py today only
  # special-cases `type: dce`); this fully specifies the branching so that
  # engine support can be added. Item wording is verbatim from Cokely,
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
  - id: demographics
    title: "About you"
    items:
      - id: m9_politics
        text: >
          In general, how would you describe your political views?
        scale: politics7
        widget: radio
        required: true
        rationale: >
          Standard covariate (Jost, 2006). Lets us report across the
          political spectrum, which matters for a US sample and for
          federal-vs-state questions.
        triangulates: [m6_fedstate]

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

      - id: demo_age
        text: "What is your age?"
        scale: null
        widget: select
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

      - id: demo_income
        text: "What was your total household income last year, before taxes?"
        scale: null
        widget: select
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
          How much do you agree with the following? "The development of
          superintelligence should be prohibited until there is broad
          scientific agreement that it can be done safely and controllably,
          and strong public support."
        scale: agree5_asc
        widget: radio
        required: true
        rationale: >
          Muskan's primary DV — ban support (the FLI conditional-ban statement),
          reported as top-2-box prevalence. In the two-sided "contested" cells
          this is the considered-support estimate (support after hearing both
          sides). Shown in every cell.
        triangulates: [muskan_oppose]

      - id: muskan_oppose
        text: >
          And how much do you agree? "Companies should be free to keep
          developing superintelligence without any government ban or pause."
        scale: agree5_asc
        widget: radio
        required: true
        rationale: >
          The anti-ban DV item, kept separate (not reverse-scored) so both
          prevalences are reportable and acquiescence is detectable. Continuous
          score for models = support − oppose (−4…+4). Attitude certainty and the
          ELM mediators (one-sided cells only) are part of the full design but
          omitted from this prototype build.
        triangulates: [muskan_support]

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
  - name: m6_certify (before deployment, who should certify that an AI system is safe?)
    reason: >
      Cut 1 Jul 2026: the certifier question is subsumed by m6_faa (binding
      pre-release testing, which implies government/independent certification)
      and m6_liability (who bears the consequences if certification fails);
      a separate certifier item wasn't adding decision-relevant information.
  - name: m3a_ii_safety (compared with how safe {comparator} is in practice, AI systems should be)
    reason: >
      Cut 1 Jul 2026: page 9 now asks only about standards (m3a_i_standards),
      not about outcomes/practice. Splitting standards from safety-in-practice
      fixed a category error (Gradient Figure 11), but the outcomes half isn't
      needed for the headline number. Recoverable if the standards-vs-outcomes
      gap becomes a finding worth probing directly.
  - name: m2_frame_applicable (can you put a number on AI's risk, or is it too uncertain?)
    reason: >
      Cut 1 Jul 2026: the frame-applicability check was judged not important
      enough to keep in the live instrument.
  - name: free_estimate / m4b_reasonable (highest annual chance of an AI disaster killing 100,000 people you'd find reasonable)
    reason: >
      Cut 1 Jul 2026: redundant with the severity-ladder rung m4c_1m (1,000,000
      deaths), which asks essentially the same thing but is anchored to a
      published source (MIT AI Risk Repository "catastrophic" rung); the
      100,000 figure here wasn't anchored to any prior work.
  - name: Environment / data-centre module (env_label, env_reversal, env_forgo, env_attitude)
    reason: >
      Reverse-halo framing experiment, fielded first in v10. Cut 29 Jun 2026:
      decision relevance unclear; none of its justifications (predictive
      covariate, halo control, standalone framing study) earned its place
      against the length budget. Recoverable as a standalone study.
  - name: Module 1 descriptive-attitudes battery (m1_goodharm, m1_worry_control, m1_trust_companies, m1_extinction_priority, m1_reg_toofar, m1_treaty_ban)
    reason: >
      Cluster A descriptive attitudes, not risk tolerance — they don't feed the
      public number. Cut 29 Jun 2026; trend value recoverable from prior SARA
      waves; ban-appetite survives via Muskan's superintelligence module.
  - name: m2_pace (tolerability of the current pace of AI disruption)
    reason: "Non-catastrophic disruption is off-aim for a risk-tolerance survey. Cut 29 Jun 2026."
  - name: Stem-A/B superintelligence wording experiment + accel/safety counter-message arm
    reason: >
      The simple 2-cell wording experiment and the one-sided briefing arm.
      Retired 29 Jun 2026 — superseded by Muskan's 3x3 ELM briefing experiment
      (the final module), which is the rigorous version of the same idea.
  - name: Mitigations battery ("I'd trust AI more if…") and priority-risks battery
    reason: "Removed from the live instrument (17 Jun 2026); the FAA-style item (m6_faa) carries the single most important mitigation."
  - name: Cognitive Reflection Test (CRT) battery
    reason: "Overlaps the numeracy item we keep (r ≈ 0.3–0.5), classic items are leaked in online panels, likely-small moderation. Recoverable if a hypothesis emerges that numeracy cannot test."
  - name: Need-for-cognition short form
    reason: "A disposition, not an ability; its plausible effect is already captured by numeracy; rationale too weak to justify the items."
  - name: Icon arrays
    reason: "Bias judgements upward; kept only as a randomised arm to measure that bias, not as the default presentation."
  - name: Verbal societal-risk anchors ("1 in 100 = a pandemic")
    reason: "Confused 2024 Australian respondents; replaced by familiar-technology comparators (Method 3)."
  - name: Micromorts
    reason: "Not clearly validated or intuitive for a general US sample."
  - name: "\"All technologies carry residual risk\" preamble"
    reason: "Primes acceptance; imports a wrong 'last order of magnitude' frame for AI."
  - name: Off-the-shelf scales (AIAS-4, GAAIS, GRIPS, DOSPERT)
    reason: "Measure general attitudes / trait risk, not AI-specific tolerance; cannot build an F–N curve."
  - name: "\"4000x safer\" multiplier from a qualitative item"
    reason: "Conflates a qualitative answer with expert estimates (Gradient #16)."
  - name: Direct "do you support SB 53 / the RAISE Act"
    reason: "Reads as advocacy; we ask the underlying values question instead."
  - name: Test–retest recontact wave
    reason: "Dropped on cost; consistency handled within-survey."
  - name: "\"I'd pay whatever it takes\" WTP option"
    reason: "Strategic and unbounded; breaks the WTP scale."
```
