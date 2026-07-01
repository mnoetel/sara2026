# SARA USA 2026 Survey

Single-source survey pipeline for the SARA USA 2026 project. All item text, response scales, page ordering, design rationale, and triangulation mappings live in one file, `sara_usa.md` — Markdown wrapping a YAML spec, so it can be co-edited/commented in HackMD or Google Docs. Both the live oTree survey and the peer-review table are generated from it.

## Project structure

```
survey/
├── settings.py            # oTree project settings
├── sara_usa.md            # Single source of truth: YAML spec in a fenced block
│                          #   (Markdown, so it's HackMD/Google-Docs-editable)
├── spec_loader.py         # Extracts + parses the fenced block; shared by the
│                          #   app and render/ — the only place that knows the format
├── sara/
│   ├── __init__.py        # oTree app: reads YAML, builds Player fields + Pages,
│   │                      #   randomisation arms, DCE expansion, consent gate, Muskan
│   ├── render.py          # server-side body rendering (per-participant substitution)
│   ├── dce.py             # loads the R-generated DCE design (dce_blocks.csv)
│   ├── muskan.py          # loads the 27 briefing stimuli (muskan_stimuli.json)
│   ├── Page.html          # the one template; renders each page's body + Next
│   ├── dce_blocks.csv     # 10 blocks × 10 tasks, from sara_dce_design.R
│   └── muskan_stimuli.json# 27 ELM briefings + neutral definition
├── _static/               # oTree static files
└── _templates/            # oTree template overrides

render/
├── Makefile               # One-step build: `make` (or `make review-py`)
├── review.R               # R renderer (reactable, self-contained HTML)
├── review_fallback.py     # Python fallback renderer (no R required)
└── review.html            # Generated review table (do not edit by hand)
```

## YAML schema

`sara_usa.md` has four top-level keys: `meta`, `scales`, `pages`, and `dumpster`.

```yaml
meta:
  project: SARA-USA
  version: "0.1.0"

scales:
  scale_id:
    type: likert | ordinal
    labels: ["Label 1", "Label 2", ...]

pages:
  - id: page_slug
    title: "Page title shown to participants"
    note: "Optional instruction text"       # shown in an alert box
    body: |                                  # optional HTML shown above items (consent, intro, briefings)
      <p>…</p>
    condition: info_arm | muskan_not_control # optional: show only to the matching arm
    type: dce                                # optional: expand into one page per task…
    n_tasks: 10                              # …drawing each respondent's block from dce_blocks.csv
    items:
      - id: variable_name                   # becomes the database column
        text: "Question text…"              # may contain {comparator} / {sanity} tokens
        scale: scale_id                     # references a key in `scales:`
        widget: radio | select | number
        required: true
        options: [...]                      # inline options (overrides scale)
        rationale: "Why this item is included"
        triangulates: [other_item_id, ...]  # cross-references for the review table

dumpster:                                    # items/modules considered and cut, with reasons
  - name: "…"
    reason: "…"
```

Items reference scales by ID; `options:` overrides `scale:`. **Beyond the items**, the engine (`sara/__init__.py`) wires the things the content needs: between-subjects randomisation arms (comparator, sanity activity, information-provision half, DCE block, Muskan stimulus), `{comparator}`/`{sanity}` substitution, the consent gate (a non-consent skips to the end), the `type: dce` expansion into per-task pages, and Muskan's per-participant briefing. Page bodies are rendered server-side via `render.py` into the single `Page.html` template. Edit the YAML; the engine and the review table follow.

## Running the survey locally

Requires Python 3.8+ and oTree 5+.

```bash
pip install otree pyyaml
cd survey
otree devserver 8000
```

Open `http://localhost:8000/demo/` and click "SARA USA 2026" to start a demo session.

**Note:** oTree uses SQLite, which cannot write to some network/FUSE-mounted filesystems (e.g. Google Drive). If you see a disk I/O error, copy the `survey/` folder to a local path first:

```bash
cp -r survey /tmp/sara_otree
cd /tmp/sara_otree
otree devserver 8000
```

## Building the review table

From the `render/` directory:

```bash
make            # tries R first, falls back to Python
make review-r   # force R + reactable
make review-py  # force Python fallback
```

Or without Make:

```bash
cd render
python3 review_fallback.py
# or
Rscript review.R
```

Both produce `render/review.html`, a self-contained HTML file with a searchable, sortable, grouped review table. Open it in any browser; no server required.

## Editing items

1. Edit `survey/sara_usa.md` (the only file you need to touch).
2. Rebuild the review table: `make -C render`
3. Restart the oTree devserver to pick up the changes.

A single-line YAML edit produces a minimal diff and updates both outputs.

## oTree version

Built for oTree v5+ (tested on v6.0.15). Player fields are created dynamically via `setattr(Player, field_name, field)` at class-definition time. Page classes are created dynamically via `type()`. The fixed-field constraint was not hit: all 33 fields attached successfully and oTree created the database tables without issue.

## Item provenance

All 33 items were migrated from the HTML prototype (`SARA USA — full survey prototype v2.html`) and cross-checked against the v10 protocol document. Items listed in Appendix C (dumpster) of the v10 protocol were excluded. No items were invented.
