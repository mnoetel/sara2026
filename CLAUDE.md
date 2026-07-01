# CLAUDE.md — working in this repo

Orientation for AI assistants. Read this before editing.

## What this is
SARA USA 2026: a public-opinion survey measuring tolerable AI catastrophic risk, built
as a **single-source-of-truth pipeline**. See `README.md` for the overview.

## The golden rule: don't duplicate content
- **`survey/sara_usa.md` is the instrument.** A Markdown doc with the YAML spec inside one
  fenced ` ```yaml ` block. All item text, scales, page order, and the `dumpster:` (cut
  items) live there. Edit it there; the oTree app and the review table follow.
  **Never hardcode item content in `survey/sara/__init__.py`.**
- **`survey/muskan_stimuli.md` is the Muskan module's instrument**, same pattern: a fenced
  ` ```yaml ` block holding the `neutral_definition` and all 27 briefing passages (9 cells x
  3 versions). There is no separate JSON or xlsx copy — `survey/sara/muskan.py` parses this
  file directly via `spec_loader.load_spec()`. Edit it there.
  `Muskan's Expiermnet/Superintelligence_3x3_stimuli_v2.xlsx` is kept only as the original
  design workbook for provenance; the pipeline no longer reads it.
- **It's Markdown on purpose** — collaborators can co-edit and comment on it in HackMD or
  Google Docs without touching YAML directly. Content outside the fence is prose/commentary
  and is ignored by the parser; only the fenced block is read. Keep the fence's contents
  valid YAML.
- **The protocol (`SARA USA — Survey Protocol v10.md`) is context only** — rationale,
  assumptions, criticisms, MRP plan. It must **not** restate items, the fielding list, or
  the dumpster (those are the instrument's job). When you change the instrument, update the
  protocol's *reasoning* if needed, but don't copy item text into it.

## How the survey is built
- `survey/spec_loader.py` — extracts the fenced ` ```yaml ` block from `sara_usa.md` and
  parses it. The **only** place that knows the file format; both the oTree app and the
  review-table renderers import it. If you change the wrapper format, change it here once.
- `survey/sara/__init__.py` — loads the spec via `spec_loader`, builds Player fields + one
  oTree Page per page in the spec. It also wires what plain items can't express:
  **randomisation arms** (comparator, sanity activity, `info_arm` half, `dce_block`, Muskan
  stimulus) assigned in `creating_session`; the **consent gate** (declining → skip to end);
  the **DCE** (a `type: dce` page expands into one page per task, drawn from
  `dce_blocks.csv`); a **`type: random_group`** page expands into one page per item, shown
  in a per-participant randomised order (seeded on `participant.code`) — every participant
  sees every item exactly once; **Muskan's** assigned briefing + control-cell skip. Page conditions use
  the `condition:` key (`info_arm`, `muskan_not_control`).
- `survey/sara/render.py` — builds each page's HTML body server-side (so text can be
  personalised: `{comparator}` / `{sanity}` tokens) and emits the UX layer (info-button
  tooltips from each item's `rationale`, card options). Inputs are
  `name=<item_id> value=<1-based index>` to match each item's `IntegerField(choices=...)`,
  so answers save normally.
- `survey/sara/Page.html` — the single template: `{{ body|safe }}` + `{{ next_button }}`,
  plus the progress bar / single-click-advance / tooltip JS.
- Data files: `dce_blocks.csv` (from `sara_dce_design.R`). Regenerate upstream, don't
  hand-edit. (Muskan's stimuli are hand-edited directly in `survey/muskan_stimuli.md` —
  see above, not a generated data file.)

## Spec schema (4 top-level keys, inside the fenced block)
`meta`, `scales`, `pages`, `dumpster`. A page may have `body:` (HTML), `note:`,
`condition:`, `type: dce` + `n_tasks:`, or `type: random_group` (its `items:` are shown
one-per-page in randomised order). An item has `id`, `text` (may contain
`{comparator}`/`{sanity}`), `scale` or `options`, `widget` (radio/select/number),
`required`, `rationale`, `triangulates`.

## oTree / template gotchas
- oTree 6 (tested 6.0.15). Templates: `{{ block content }}`/`{{ endblock }}`, `{{ var }}`,
  **`{% if %}` / `{% endif %}`** for control flow, `{{ body|safe }}` for raw HTML.
- Page methods take `player` as the first arg (the user's `self` is actually the player).
- Adding/removing items changes the DB schema → `rm survey/db.sqlite3*` then restart.
- Session config name is **`sara_usa`** (not `sara`).

## Testing
- Run: `cd survey && otree devserver`. Walk a participant via a session's `/join/<room>`
  link; POST does **not** need a CSRF token on devserver.
- Review table: `make -C render` (R path) or `python3 render/review_fallback.py`.

## Analysis & data
- `sara_dce_design.R` → `survey/sara/dce_blocks.csv` (varied-severity 720-grid, Bayesian
  D-efficient).
- `build_poststrat.py` (stdlib, Census API) / `acs_poststrat.R` (tidycensus) →
  `poststrat_frame.csv` for MRP. **Verified survey↔ACS alignment:** age/education/income/
  state align (no survey change needed); **gender is the only mismatch** (ACS = M/F only)
  — keep the inclusive question, decide poststrat handling. Details in
  `ACS_poststratification_manual.md`.

## Secrets / don't commit
`.Renviron` holds the Census API key — gitignored, never commit it. Generated artifacts
(`db.sqlite3*`, `poststrat_frame.csv`, `*.otreezip`, `__pycache__`) are gitignored.

## Git
Trunk `main`; work on branches + PRs (repo `mnoetel/SARA-survey`, private). Commit only
when asked.
