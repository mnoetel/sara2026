# Muskan's 3x3 superintelligence-briefing experiment — stimulus source

This file **is** the source for the Muskan module's briefing passages — the
same pattern as `sara_usa.md`. The full text every participant might read
lives in the fenced ```yaml``` block below; `survey/sara/muskan.py` parses it
directly at runtime via `spec_loader.load_spec()`. There is no separate JSON
or xlsx copy of this content — edit it here and nothing else needs to change.

(`Muskan's Expiermnet/Superintelligence_3x3_stimuli_v2.xlsx` is the original
design workbook the passages were drafted in; it's kept for provenance/audit
but is no longer read by the pipeline.)

**For reviewers:** review changes in the GitHub pull request and comment inline
on the diff, same as `sara_usa.md`.

**For editors:** the fenced ```yaml block below is parsed as-is. Do not add
prose inside the fence; keep commentary outside it (in this preamble, or as PR
review comments).

Referenced from the `superintelligence_brief` page in `survey/sara_usa.md`,
which only describes this module in prose and does not restate the passages.

## The 3x3 design

Crossed factors are the **For-ban argument** and the **Against-ban
argument**, each at three levels: Elite cue (peripheral route — named
prestigious endorsers), Substantive (central route — the argument itself,
no endorsers named), or Nothing (that side is not shown).

|  For (ban) v \ Against (ban) > | Elite cue | Substantive | Nothing |
| --- | :-: | :-: | :-: |
| **Elite cue** | Cell 1 | Cell 2 | Cell 3 |
| **Substantive** | Cell 4 | Cell 5 | Cell 6 |
| **Nothing** | Cell 7 | Cell 8 | Cell 9 (pure control) |

Runs as the final module of the survey, after all other items, so the
briefing cannot contaminate responses to the rest of the survey. Each
participant is randomly assigned one of the 27 rows below (9 cells x 3
wording versions each; cell 9 is the neutral control, no argument shown)
and then answers the two ban-support DV items in `sara_usa.md`.

Each cell has 3 wording versions (27 rows total) so no single stimulus
drives the result; one version is served at random. For the four two-sided
cells (1, 2, 4, 5), the for/against reading order is rotated across the
three versions so neither side is always read first (see `order` per row
below). `neutral_definition` is shown to every participant before the
briefing, and is the *entire* passage shown in the control cell (cell 9).

---

```yaml
neutral_definition: |-
  "Superintelligence" refers to a hypothetical AI system that could reason, plan, and solve problems far better than any human across almost all tasks. Such systems do not exist today, and experts disagree about whether or when they might be built.

stimuli:
  - stimulus_id: cell1_v1
    cell: 1
    for_arg: elite
    against_arg: elite
    version: 1
    order: for_first
    word_count: 132
    body_text: |-
      More than 700 well-known figures have signed a public statement calling for a ban on developing superintelligence — AI that can outperform humans at almost everything — until there is broad scientific agreement it can be done safely and clear public support. The signatories include five Nobel laureates, two pioneers often called the "Godfathers of AI," Apple co-founder Steve Wozniak, and figures from Prince Harry to a senior adviser to the Pope.

      On the other side, some of the most prominent researchers and investors in AI argue that such a ban would be a mistake — among them Meta's chief AI scientist Yann LeCun, a Turing Award winner; the deep-learning pioneer Andrew Ng, who founded Coursera and Google Brain; and Marc Andreessen and Ben Horowitz, co-founders of the venture-capital firm Andreessen Horowitz.

  - stimulus_id: cell1_v2
    cell: 1
    for_arg: elite
    against_arg: elite
    version: 2
    order: against_first
    word_count: 116
    body_text: |-
      A number of the most prominent scientists and investors in AI argue against banning superintelligence. They include Yann LeCun, Meta's chief AI scientist and a Turing Award winner; Andrew Ng, a founder of the modern deep-learning field and of Coursera; and Marc Andreessen and Ben Horowitz, co-founders of the venture-capital firm Andreessen Horowitz. In their view a prohibition on advanced AI would be a serious mistake.

      Set against them, more than 700 public figures have signed a statement urging that superintelligence not be built until it is provably safe and the public agrees — among them five Nobel laureates, two "Godfathers of AI," Apple's Steve Wozniak, and names from Prince Harry to advisers to the Pope.

  - stimulus_id: cell1_v3
    cell: 1
    for_arg: elite
    against_arg: elite
    version: 3
    order: for_first
    word_count: 117
    body_text: |-
      A public letter signed by over 700 notable people calls for prohibiting the development of superintelligence — systems that surpass people at nearly every task — until experts broadly agree it is safe and the public clearly supports it. Signatories include five Nobel laureates, two researchers regarded as founders of modern AI, Apple co-founder Steve Wozniak, and figures from Prince Harry and Meghan to the author Yuval Noah Harari.

      Against them stand some of the best-known names in AI — Meta's Yann LeCun, a Turing Award winner; the deep-learning pioneer Andrew Ng; and the venture capitalists Marc Andreessen and Ben Horowitz, co-founders of Andreessen Horowitz — who argue that outlawing advanced AI would be the wrong path.

  - stimulus_id: cell2_v1
    cell: 2
    for_arg: elite
    against_arg: substantive
    version: 1
    order: for_first
    word_count: 131
    body_text: |-
      More than 700 well-known figures have signed a statement calling for a ban on developing superintelligence — AI that can outperform humans at almost everything — until it can be shown safe and the public clearly supports it. They include five Nobel laureates, two pioneers called the "Godfathers of AI," Apple co-founder Steve Wozniak, and figures from Prince Harry to a senior adviser to the Pope.

      Others argue such a ban would be a mistake. They say it rests on speculation rather than evidence, and that prohibiting advanced AI would make a country weaker, not safer. A ban could not be enforced, because intelligence is open-ended knowledge rather than a single device, so the work would move abroad. The real risk, they argue, is misuse, better met with oversight than prohibition.

  - stimulus_id: cell2_v2
    cell: 2
    for_arg: elite
    against_arg: substantive
    version: 2
    order: against_first
    word_count: 132
    body_text: |-
      One camp argues that banning superintelligence would be a serious error. In their view the case relies on fear rather than proof, and outlawing advanced AI would sacrifice economic and strategic strength while making no one safer. A ban is close to unenforceable, since you cannot really outlaw knowledge, and it would push the most capable research abroad. Harm comes from misuse, they say, best met with accountability.

      On the other side, more than 700 prominent people have signed a statement urging a halt to developing superintelligence — AI smarter than humans at nearly every task — until it is shown safe and the public is on board. Among them are five Nobel laureates, two "Godfathers of AI," Apple co-founder Steve Wozniak, and figures from Prince Harry to advisers to the Pope.

  - stimulus_id: cell2_v3
    cell: 2
    for_arg: elite
    against_arg: substantive
    version: 3
    order: for_first
    word_count: 128
    body_text: |-
      A public letter signed by over 700 notable figures calls for prohibiting the development of superintelligence — systems that surpass people at almost everything — until experts broadly agree it is safe and the public clearly supports it. Signatories span five Nobel laureates, two researchers regarded as founders of modern AI, Apple's Steve Wozniak, and names from Prince Harry to advisers within the Vatican.

      Critics counter that a prohibition would be the wrong move. They contend it is driven by unproven fears, and that blocking advanced AI would erode competitiveness without delivering safety. Because capability is accumulated knowledge rather than a discrete product, a ban cannot be policed and would hand the lead to rivals. The sensible response to misuse, in their view, is oversight, not a ban.

  - stimulus_id: cell3_v1
    cell: 3
    for_arg: elite
    against_arg: none
    version: 1
    order: for_only
    word_count: 80
    body_text: |-
      More than 700 well-known figures have signed a public statement calling for a ban on developing superintelligence — AI that can outperform humans at almost everything — until there is broad scientific agreement it can be done safely and clear public support. The signatories include five Nobel laureates, two pioneers often called the "Godfathers of AI," Apple co-founder Steve Wozniak, faith leaders advising the Pope, and public figures ranging from Prince Harry and Meghan to the author Yuval Noah Harari.

  - stimulus_id: cell3_v2
    cell: 3
    for_arg: elite
    against_arg: none
    version: 2
    order: for_only
    word_count: 74
    body_text: |-
      A public letter signed by over 700 notable people calls for prohibiting the development of superintelligence — systems that surpass people at nearly every task — until experts broadly agree it is safe and controllable and the public clearly supports it. Among the signatories are five Nobel laureates, two researchers widely regarded as founders of modern AI, Apple's co-founder Steve Wozniak, the actor and writer Stephen Fry, and a senior adviser to the Pope.

  - stimulus_id: cell3_v3
    cell: 3
    for_arg: elite
    against_arg: none
    version: 3
    order: for_only
    word_count: 74
    body_text: |-
      More than 700 prominent figures have put their names to a statement urging that superintelligence not be developed until experts broadly agree it can be done safely and the public is on board. The list includes five Nobel laureates, two researchers so-called the "Godfathers of AI," Apple co-founder Steve Wozniak, former US national security adviser Susan Rice, the author Yuval Noah Harari, and public figures from Prince Harry and Meghan to the musician will.i.am.

  - stimulus_id: cell4_v1
    cell: 4
    for_arg: substantive
    against_arg: elite
    version: 1
    order: for_first
    word_count: 138
    body_text: |-
      There are calls to ban the development of superintelligence — AI that surpasses people at almost every task — until it can be shown safe and controllable. The argument is that no one knows how to keep a system far smarter than its creators under control, and that once such a system exists the step cannot be reversed; with companies racing to be first, supporters say, the safer course is to require clear proof of safety before crossing that threshold.

      On the other side, some of the most prominent figures in AI argue that such a ban would be a mistake — among them Meta's chief AI scientist Yann LeCun, a Turing Award winner; the deep-learning pioneer Andrew Ng, who founded Coursera and Google Brain; and Marc Andreessen and Ben Horowitz, co-founders of the venture-capital firm Andreessen Horowitz.

  - stimulus_id: cell4_v2
    cell: 4
    for_arg: substantive
    against_arg: elite
    version: 2
    order: against_first
    word_count: 117
    body_text: |-
      Several of the most prominent figures in artificial intelligence oppose a ban on superintelligence. Among them are Meta's chief AI scientist Yann LeCun, a Turing Award winner; the deep-learning pioneer Andrew Ng, who founded Coursera; and the venture capitalists Marc Andreessen and Ben Horowitz, co-founders of Andreessen Horowitz. They argue that prohibiting the technology would do more harm than good.

      Supporters of a ban respond that the real danger is loss of control: no one has shown how to keep a system far smarter than people aligned with human aims, and once it exists the decision cannot be taken back. Because firms are racing, they argue, development should pause at the threshold until safety can be demonstrated.

  - stimulus_id: cell4_v3
    cell: 4
    for_arg: substantive
    against_arg: elite
    version: 3
    order: for_first
    word_count: 110
    body_text: |-
      Advocates of a ban say superintelligence should not be developed until there is solid evidence it can be controlled. Their reasoning is that a system more capable than any human across the board would be hard or impossible to oversee, that the consequences of error could be irreversible and society-wide, and that commercial competition pushes developers toward speed over safety.

      Against this, some of the best-known names in AI — Yann LeCun of Meta, a Turing Award winner; the deep-learning pioneer Andrew Ng; and the venture capitalists Marc Andreessen and Ben Horowitz, co-founders of Andreessen Horowitz — argue that outlawing the development of advanced AI would be the wrong path.

  - stimulus_id: cell5_v1
    cell: 5
    for_arg: substantive
    against_arg: substantive
    version: 1
    order: for_first
    word_count: 134
    body_text: |-
      There are calls to ban the development of superintelligence — AI that surpasses people at almost every task — until it can be shown safe and controllable. Supporters argue that no one knows how to keep a system far smarter than its creators under control, that once it exists the step cannot be reversed, and that a commercial race rewards speed over caution, so safety should be proven before the threshold is crossed.

      Others argue the opposite: that the case rests on unproven fears, that a ban could not be enforced because advanced capability is open-ended knowledge rather than a single device, and that prohibition would push research abroad while surrendering economic and strategic ground. The real risk, they say, is misuse, which is better met with oversight and accountability than an outright ban.

  - stimulus_id: cell5_v2
    cell: 5
    for_arg: substantive
    against_arg: substantive
    version: 2
    order: against_first
    word_count: 128
    body_text: |-
      Some argue that banning superintelligence would be a mistake. They say it would outlaw something that does not yet exist, that a prohibition could not be enforced because you cannot really outlaw knowledge, and that the work would simply move to other countries. The genuine risk, in their view, is how people misuse technology, which is better handled through monitoring and accountability than a ban.

      Supporters of a ban respond that the central problem is loss of control: no one has shown how to keep a system far smarter than people aligned with human aims, and once such a system exists the decision cannot be undone. With firms racing to be first, they argue, the prudent step is to halt at the threshold until safety can be demonstrated.

  - stimulus_id: cell5_v3
    cell: 5
    for_arg: substantive
    against_arg: substantive
    version: 3
    order: for_first
    word_count: 114
    body_text: |-
      Advocates of a ban say superintelligence should not be built until there is solid evidence it can be controlled, because a system more capable than any human could be impossible to oversee and the consequences of error could be irreversible and widely shared. The commercial race, they argue, pushes developers toward speed rather than safety.

      Opponents counter that advanced AI already delivers real benefits — earlier cancer detection, new antibiotics, faster scientific work — and that halting development would forfeit those gains while failing to prevent misuse. A prohibition on "too much" intelligence, they add, could neither be defined nor enforced, and would be better replaced by sensible rules on how AI is used.

  - stimulus_id: cell6_v1
    cell: 6
    for_arg: substantive
    against_arg: none
    version: 1
    order: for_only
    word_count: 96
    body_text: |-
      Some are calling for a ban on developing superintelligence — AI that surpasses people at almost every task — until it can be shown safe and controllable. The core argument is that no one knows how to keep a system far smarter than its creators reliably under human control, and that once such a system exists the step cannot be reversed. Because competing companies face pressure to move quickly, the safer course is to stop at the threshold and require clear proof of safety before crossing it, much as society treats risks that could affect everyone.

  - stimulus_id: cell6_v2
    cell: 6
    for_arg: substantive
    against_arg: none
    version: 2
    order: for_only
    word_count: 75
    body_text: |-
      There is a push to prohibit building superintelligence until experts can demonstrate it is safe. Proponents argue that intelligence beyond the human level brings a loss of control: a system that can out-think people could pursue its goals in ways we cannot anticipate or correct, and the decision to build it cannot be undone. With firms racing to be first, they say, caution should come before capability, and development should pause until safety is proven.

  - stimulus_id: cell6_v3
    cell: 6
    for_arg: substantive
    against_arg: none
    version: 3
    order: for_only
    word_count: 75
    body_text: |-
      Advocates of a ban say superintelligence should not be developed until there is solid evidence it can be controlled. Their reasoning is that a system more capable than any human across the board would be difficult or impossible to oversee, and that the consequences of getting it wrong could be irreversible and society-wide. The commercial race, they argue, pushes developers toward speed rather than safety, so a halt at the threshold is the prudent response.

  - stimulus_id: cell7_v1
    cell: 7
    for_arg: none
    against_arg: elite
    version: 1
    order: against_only
    word_count: 79
    body_text: |-
      A number of the most prominent scientists and investors in artificial intelligence argue against banning superintelligence. They include Yann LeCun, Meta's chief AI scientist and a Turing Award winner; Andrew Ng, a founder of the modern deep-learning field who also started Coursera and Google Brain; and Marc Andreessen and Ben Horowitz, co-founders of the influential Silicon Valley venture-capital firm Andreessen Horowitz. In their view, a government prohibition on advanced AI would be a serious mistake rather than a safeguard.

  - stimulus_id: cell7_v2
    cell: 7
    for_arg: none
    against_arg: elite
    version: 2
    order: against_only
    word_count: 66
    body_text: |-
      Several of the most prominent figures in artificial intelligence oppose a ban on superintelligence. Among them are Meta's chief AI scientist Yann LeCun, a Turing Award laureate; the deep-learning pioneer Andrew Ng, who founded Coursera; and the investors Marc Andreessen and Ben Horowitz, whose firm backs many of the world's leading AI start-ups. They argue that prohibiting the technology would do far more harm than good.

  - stimulus_id: cell7_v3
    cell: 7
    for_arg: none
    against_arg: elite
    version: 3
    order: against_only
    word_count: 64
    body_text: |-
      Some of the best-known names in AI reject calls for a ban. Yann LeCun, Meta's chief AI scientist and a Turing Award winner; Andrew Ng, a founder of the modern deep-learning field and of Coursera; and the venture capitalists Marc Andreessen and Ben Horowitz have all argued that outlawing the development of advanced AI would be the wrong path for a country to take.

  - stimulus_id: cell8_v1
    cell: 8
    for_arg: none
    against_arg: substantive
    version: 1
    order: against_only
    word_count: 90
    body_text: |-
      Others argue that banning superintelligence would be a mistake. They say the case rests on unproven fears rather than evidence, and that a prohibition could not really be enforced, because advanced capability is open-ended knowledge rather than a single device. In practice, they argue, a ban would push the most capable research into other countries and surrender a nation's economic and strategic lead, while doing little to make anyone safer. The real risk, in their view, lies in how people misuse technology, which is better handled through oversight and accountability.

  - stimulus_id: cell8_v2
    cell: 8
    for_arg: none
    against_arg: substantive
    version: 2
    order: against_only
    word_count: 79
    body_text: |-
      Critics of a ban argue that it would outlaw something that does not yet exist and may never take the form people fear. Today's systems perform narrow tasks well but do not think or act on their own. Rather than prohibit a hypothetical, they say, governments should focus on real misuse: monitoring serious incidents, auditing high-risk systems, and holding people accountable. Oversight of this kind, they argue, manages the danger without halting the research that also produces enormous benefits.

  - stimulus_id: cell8_v3
    cell: 8
    for_arg: none
    against_arg: substantive
    version: 3
    order: against_only
    word_count: 88
    body_text: |-
      Opponents of a ban point to what advanced AI already delivers: earlier cancer detection, the discovery of new antibiotics, and faster scientific work across many fields. Halting development, they argue, would forfeit these gains and the ones still to come, while a prohibition on "too much" intelligence could not be defined or enforced in any case. The danger, they say, comes from misuse rather than from the technology itself, and is better met with sensible regulation of how AI is used than with a ban on building it.

  - stimulus_id: cell9_v1
    cell: 9
    for_arg: none
    against_arg: none
    version: 1
    order: control
    word_count: 40
    body_text: |-
      "Superintelligence" refers to a hypothetical artificial-intelligence system that could reason, plan, and solve problems far better than any human across almost all tasks. Such systems do not exist today, and researchers disagree about whether or when they might be built.

  - stimulus_id: cell9_v2
    cell: 9
    for_arg: none
    against_arg: none
    version: 2
    order: control
    word_count: 39
    body_text: |-
      Artificial superintelligence describes a possible future AI system that would outperform people at nearly everything, from scientific research to strategic planning. Nothing like it exists yet, and experts differ on how likely or how near such a system is.

  - stimulus_id: cell9_v3
    cell: 9
    for_arg: none
    against_arg: none
    version: 3
    order: control
    word_count: 39
    body_text: |-
      The term "superintelligence" is used for a hypothetical AI that would exceed human ability across almost all cognitive tasks. It remains theoretical: today's systems are far narrower, and there is no consensus on if or when superintelligence could arrive.
```
