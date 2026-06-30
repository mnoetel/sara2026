# CLAUDE.md — working in this repo

Orientation for AI assistants. Read this before editing.

## What this is
SARA USA 2026: a public-opinion survey measuring tolerable AI catastrophic risk, built
as a **single-source-of-truth pipeline**. See `README.md` for the overview.

## The golden rule: don't duplicate content
- **`survey/sara_usa.yaml` is the instrument.** All item text, scales, page order, and the
  `dumpster:` (cut items) live there. Edit the YAML; the oTree app and the review table
  follow. **Never hardcode item content in `survey/sara/__init__.py`.**
- **The protocol (`SARA USA — Survey Protocol v10.md`) is context only** — rationale,
  assumptions, criticisms, MRP plan. It must **not** restate items, the fielding list, or
  the dumpster (those are the YAML's job). When you change the instrument, update the
  protocol's *reasoning* if needed, but don't copy item text into it.

## How the survey is built (survey/sara/)
- `__init__.py` — reads the YAML and builds Player fields + one oTree Page per YAML page.
  It also wires what plain items can't express: **randomisation arms** (comparator,
  sanity activity, `info_arm` half, `dce_block`, Muskan stimulus) assigned in
  `creating_session`; the **consent gate** (declining → skip to end); the **DCE**
  (a `type: dce` page expands into one page per task, drawn from `dce_blocks.csv`);
  **Muskan's** assigned briefing + control-cell skip. Page conditions use the YAML
  `condition:` key (`info_arm`, `muskan_not_control`).
- `render.py` — builds each page's HTML body server-side (so text can be personalised:
  `{comparator}` / `{sanity}` tokens) and emits the UX layer (info-button tooltips from
  each item's `rationale`, card options). Inputs are `name=<item_id> value=<1-based index>`
  to match each item's `IntegerField(choices=...)`, so answers save normally.
- `Page.html` — the single template: `{{ body|safe }}` + `{{ next_button }}`, plus the
  progress bar / single-click-advance / tooltip JS.
- Data files: `dce_blocks.csv` (from `sara_dce_design.R`), `muskan_stimuli.json` (from
  Muskan's xlsx). Regenerate upstream, don't hand-edit.

## YAML schema (4 top-level keys)
`meta`, `scales`, `pages`, `dumpster`. A page may have `body:` (HTML), `note:`,
`condition:`, or `type: dce` + `n_tasks:`. An item has `id`, `text` (may contain
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
Trunk `master`; work on branches + PRs (repo `mnoetel/SARA-survey`, private). Commit only
when asked. Current feature branches: `ux-polish` (PR #1, the UX layer), `acs-mrp-alignment`
(the MRP frame + alignment).
