# SARA USA 2026

**Survey Assessing Risks from AI — United States, 2026.** A survey that measures how
much catastrophic risk from AI the US public is willing to tolerate, designed to inform
policy. It triangulates risk tolerance four ways and recovers a population estimate via
multilevel regression and post-stratification (MRP).

## Single source of truth

The whole project is meant to be built and reviewed from **two files**:

- **`survey/sara_usa.yaml`** — the instrument: every item, response scale, page order,
  and the *dumpster* (items considered and cut). Editing this rebuilds both the live
  survey and the review table.
- **`SARA USA — Survey Protocol v10.md`** — the *context and assumptions* (methodology,
  rationale, criticisms, MRP plan). It deliberately **does not duplicate** the YAML.

Everything else is generated from, or supports, those two.

## Layout

```
survey/            oTree app — reads sara_usa.yaml, builds the Player model + pages
  sara_usa.yaml    THE instrument (items, scales, order, dumpster)
  sara/            engine (__init__.py), render.py, Page.html, data files
render/            review table generator (review.R / review_fallback.py → review.html)
SARA USA — Survey Protocol v10.md   design rationale & assumptions
sara_dce_design.R  DCE design → survey/sara/dce_blocks.csv (the choice tasks)
build_poststrat.py / acs_poststrat.R   MRP frame from ACS PUMS → poststrat_frame.csv
ACS_poststratification_manual.md   how to get ACS data + survey↔ACS alignment check
ethics consent form/   canonical Participant Information Sheet (v2.1)
Muskan's Expiermnet/   the 3×3 superintelligence-briefing sub-study
ARCHIVED/          superseded drafts, old prototypes
```

## The instrument (four methods + a final sub-study)

1. **Direct elicitation** — highest acceptable annual risk, by severity (a ladder from
   one death to ~800M).
2. **Discrete choice experiment (DCE)** — 10 tasks; severity × probability × utility ×
   competition × cost; design from `sara_dce_design.R`.
3. **Anchored to accepted standards** — compare AI to nuclear/aviation/etc. (+ 2 hidden
   attention checks).
4. **Judge the experts' numbers** — LeCun → Altman → Musk → Amodei.

Then costed tradeoffs, policy, demographics, and last, **Muskan's 3×3 ELM briefing
experiment** on superintelligence-ban support. Between-subjects arms (comparator,
sanity activity, information-provision half, DCE block, briefing) and a consent gate are
wired in the engine, not the YAML items.

## Run it

```bash
cd survey && otree devserver        # http://localhost:8000  (config: sara_usa)
make -C render                      # rebuild render/review.html (the review table)
```

Schema changes (adding/removing items) need a DB reset: `rm survey/db.sqlite3*`.

## Analysis

- **DCE:** `Rscript sara_dce_design.R` (needs `cbcTools`, `logitr`).
- **MRP frame:** `python3 build_poststrat.py` (needs a Census API key in `.Renviron`;
  see `ACS_poststratification_manual.md`). Builds `poststrat_frame.csv` — the joint
  population distribution by state × age × sex × education × income.

## Git

Repo: `github.com/mnoetel/SARA-survey` (private). Trunk is `main`; feature work goes on
branches with PRs. Secrets (`.Renviron`) and generated data (`db.sqlite3`,
`poststrat_frame.csv`, `*.otreezip`) are gitignored.
