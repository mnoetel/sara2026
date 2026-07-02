# 3×3 Superintelligence-Ban Study: Design and Stimulus Plan

Status: **plan, voice sample pending approval.** This documents what the study is and how I propose to generate the message stimuli and the Qualtrics import file.

### Decisions locked (2026-06-17)
1. **Build model:** pre-assemble all 9 cells, 3 versions each = **27 stimulus rows**. For/Against text is combined into a single passage per cell; no Qualtrics assembly logic needed.
2. **Workbook scope:** stimuli sheet + neutral definition / pure-control. (Comprehension item and social-desirability items excluded from this build.)
3. **Sources:** a16z added as the anti-ban anchor (file `05`). Fei-Fei Li sourcing not requested; will use only if you supply the original.

Next step before building the 27: a 3-version voice sample of one cell for your sign-off.

## 1. The research question

Does providing context about a proposed superintelligence ban change public support for it, and how durable is that shift? The framing is the Elaboration Likelihood Model (ELM): persuasion via the **peripheral route** (shallow processing, source cues) versus the **central route** (effortful processing of argument quality). Operationalisation:

- **Elite cue = peripheral route.** Persuasion carried by *who* endorses the position (celebrities, Nobel laureates, famous CEOs).
- **Substantive argument = central route.** Persuasion carried by *the argument itself*, with the prestige cue stripped out.

Hypothesis from the intro doc: substantive (central) messaging produces stronger and more certain attitudes than elite (peripheral) cues, because central-route attitudes are more durable.

## 2. The 3×3 design

Crossed factors are **Argument For the ban** and **Argument Against the ban**, each at three levels: Elite cue, Substantive, Nothing. A participant is randomised to one of the 9 cells and sees the corresponding For-message and/or Against-message.

|  For ↓ \ Against → | Elite cue | Substantive | Nothing |
| --- | :-: | :-: | :-: |
| **Elite cue** | pro-elite + anti-elite | pro-elite + anti-substantive | pro-elite only |
| **Substantive** | pro-substantive + anti-elite | pro-substantive + anti-substantive | pro-substantive only |
| **Nothing** | anti-elite only | anti-substantive only | pure control (neutral definition only) |

Planned contrasts (from the design doc):
- **Contrast 1** across {Elite, Substantive, Nothing} = `[+1, +1, -2]`: any argument vs none.
- **Contrast 2** across {Elite, Substantive} = `[+1, -1]`: peripheral vs central route.

Implication: **only 4 distinct passages are needed to populate the whole grid** (pro-ban elite, pro-ban substantive, anti-ban elite, anti-ban substantive). "Nothing" is the absence of a passage, not a passage to write. The 9 cells are assembled by Qualtrics display logic from those 4 building blocks.

## 3. Survey flow (for context; not part of this build)

1. Neutral definition of superintelligence (all participants).
2. Comprehension item: "Which of the following is closest to artificial superintelligence?" (4 options, from the design doc).
3. Randomise to one of 9 cells; show For and/or Against passage(s). Order of For vs Against randomised, so passages must read sensibly in either order.
4. DVs: ban support + attitude certainty.
5. Social desirability subset (Marlowe-Crowne items 16, 17, 26, 19, 22, per the design doc).

## 4. The four passages and their sources

Quality bar: each side must **pass the Ideological Turing Test (ITT) of that side** — written so the canonical advocate would accept it as a fair statement of their view, not a strawman. Canonical sides: **FLI (Future of Life Institute) for pro-ban**, **a16z (Andreessen Horowitz) for anti-ban**.

| Passage | Route | Canonical side | Source material (in `Materials for generating design/`) |
| --- | --- | --- | --- |
| **Pro-ban, elite** | Peripheral | FLI | TIME open letter: 700+ signatories, 5 Nobel laureates, two "Godfathers of AI", Wozniak, Harry & Meghan, faith leaders. Name the prestigious endorsers. |
| **Pro-ban, substantive** | Central | FLI / CAIS | CAIS extinction statement + FLI's "don't build until provably safe, controllable, with public buy-in"; loss-of-control and racing-dynamics reasoning. Argument only, endorsers anonymised. |
| **Anti-ban, elite** | Peripheral | a16z | Named opponents of development restrictions: Yann LeCun (Meta chief AI scientist, Turing Award), Andrew Ng (Coursera, Google Brain), Marc Andreessen and Ben Horowitz (a16z). Name them as the cue. NB: Fei-Fei Li removed after fact-check — she is not on record opposing a superintelligence ban (see flag 3). |
| **Anti-ban, substantive** | Central | a16z | Castro op-ed (freedom/innovation, enforceability, China competition, oversight-not-prohibition) + Ng/LeCun ("regulate products not research"). Argument only, names anonymised. |

Gaps to close before generation: (a) Castro op-ed body is now captured (you pasted the full WaPo text into file `02`). (b) Fei-Fei Li quotes in the design doc are not yet sourced to an original; if used in the anti-elite passage, point me at her open letter/op-ed. (c) For a stronger a16z anchor I would pull from Andreessen's "Techno-Optimist Manifesto" and the "Little Tech Agenda" — flag if you want me to add those to the materials.

## 5. Operationalising the ELM manipulation (the tricky part)

To make peripheral vs central a clean manipulation rather than a confound, I propose holding the *conclusion* constant within a side and varying only the *route*:

- **Peripheral / elite version:** leads with named prestigious endorsers, high cue density, minimal argumentation. "More than 700 public figures, including five Nobel laureates and two 'Godfathers of AI', have called for…"
- **Central / substantive version:** identical position, but endorsers replaced with generic attribution ("researchers argue…"), and the body carries the reasoning. This matches the design doc's note that names/titles were changed to "they" for the substantive cells.

Shared constraints for all four passages (from the design doc):
1. Real-quote stitching ("frankenquote") is allowed.
2. Lengths matched across cells (target ~90–130 words, within ±10% of each other).
3. Each passage states *what the ban is*, so For/Against order can be shuffled and still read coherently.
4. Elite passages must contain elite cues; substantive passages must contain a substantive argument and no prestige cue.

## 6. Generation method

For each of the 4 passages, generate **3 versions** (12 passages total) that differ in wording/structure but hold position, route, length, and core content constant. The point of multiple versions, per your meeting note, is to avoid any single stimulus being criticised as idiosyncratic; Qualtrics can randomly serve one of the 3 versions per participant.

ITT check: after drafting, I will adversarially review each side against the canonical advocate's actual published positions (FLI statement / a16z manifesto) and flag anything that reads as a strawman. I can approximate the ITT but cannot truly certify it without a reviewer from each side; treat my check as a first pass, not a guarantee.

## 7. The nine cells (27 rows)

Each row is one pre-assembled cell at one version. Cells 1–8 combine or show the building-block passages; cell 9 is the neutral definition only.

| # | For (pro-ban) | Against (anti-ban) | Passage shown |
| --- | --- | --- | --- |
| 1 | Elite | Elite | pro-elite + anti-elite |
| 2 | Elite | Substantive | pro-elite + anti-substantive |
| 3 | Elite | — | pro-elite only |
| 4 | Substantive | Elite | pro-substantive + anti-elite |
| 5 | Substantive | Substantive | pro-substantive + anti-substantive |
| 6 | Substantive | — | pro-substantive only |
| 7 | — | Elite | anti-elite only |
| 8 | — | Substantive | anti-substantive only |
| 9 | — | — | neutral definition (pure control) |

Each cell × 3 versions = 27 rows. Order counterbalancing: for the four two-sided cells (1, 2, 4, 5), the For/Against order is rotated across the three versions so neither side is always first.

Length: each building-block paragraph targets ~70–90 words, so the route contrast of interest (elite vs substantive, within a side) is length-matched. Two-sided cells therefore run ~140–180 words; one-sided cells ~70–90.

## 8. Proposed long-format xlsx schema

One row per cell-version. Columns:

| column | example | notes |
| --- | --- | --- |
| `stimulus_id` | `cell2_v1` | unique key |
| `cell` | `2` | 1–9 |
| `for_arg` | `elite` / `substantive` / `none` | |
| `against_arg` | `elite` / `substantive` / `none` | |
| `version` | `1` / `2` / `3` | |
| `order` | `for_first` / `against_first` / `na` | counterbalancing record |
| `word_count` | `162` | length-matching check |
| `body_text` | full assembled passage | the text shown to the participant |
| `source_refs` | provenance of the quotes used | audit trail, not shown |

Sheet 2 holds the neutral definition and the comprehension item's correct framing, for reference. Total: 27 stimulus rows.

## 9. Validity flags (worth deciding early)

- **Prestige asymmetry across sides.** The pro-ban elite roster (Nobel laureates, Hinton, Bengio, Wozniak, royals) is arguably more prestigious than the anti-ban roster (LeCun, Ng, Andreessen, Horowitz). If so, a pro-vs-anti difference could reflect endorser prestige rather than position. Consider deliberately matching the calibre of named endorsers across sides, or measuring perceived source prestige as a manipulation check.
- **Fei-Fei Li removed (fact-checked 2026-06-17).** She is not a signatory to the FLI superintelligence statement, but she has not opposed it either. Her record is centrist: she criticised SB-1047 as too blunt, yet co-authored Newsom's post-veto AI policy report recommending more guardrails (transparency, independent oversight, whistleblower protections) and regulation that anticipates "risks that have not yet been observed." Naming her as an anti-ban voice would misrepresent her, so she is out of the elite anti cue. Sources: [TechCrunch, 19 Mar 2025](https://techcrunch.com/2025/03/19/group-co-led-by-fei-fei-li-suggests-that-ai-safety-laws-should-anticipate-future-risks/); [TIME100 AI 2025](https://time.com/collections/time100-ai-2025/7305810/fei-fei-li/); [CNBC, 22 Oct 2025](https://www.cnbc.com/2025/10/22/800-petition-signatures-apple-steve-wozniak-and-virgin-richard-branson-superintelligence-race.html).
- **Elite passages still contain some argument; substantive passages still name a field ("experts").** Pure separation is impossible. The manipulation is cue *density*, not a clean on/off. Worth stating explicitly in the method.
- **ITT cannot be fully certified by me.** Calibrated claim: I can make each side non-strawman and grounded in real positions; I cannot guarantee FLI or a16z would sign off.

## 10. Remaining checks before generating all 27

1. **Voice/tone sign-off** on the sample cell (below / in chat). Once approved I generate the other 26 in the same register.
2. **Register for the anti side:** plain neutral prose (default), or retain more of a16z's combative tone? Default is plain.
3. **Source labels shown to participants:** for elite (peripheral) cells, do you want a visible attribution line (e.g. "Reported in TIME, 2025") as part of the cue, or names embedded in the body only?
