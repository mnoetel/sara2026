# analysis/ — the pre-registered report, built before the data exist

This directory holds the **entire registered analysis as executable code**,
developed and tested end-to-end on simulated data that is format-identical
to what the oTree server will export. When real data arrive, the same
`report.Rmd` pointed at the real export **is** the registered analysis —
nothing gets written after seeing the data.

```
make            # simulate 4 waves (N=4,000) -> render analysis/report.html
make check-schema   # prove simulator output == real oTree export format
make verify         # render + assert the pipeline recovers the ground truth
make real DATA=realdata   # run the identical report on a real export
```

## Pieces

| file | what it is |
|---|---|
| `simulate_data.py` | The simulation engine. Loads the instrument (`survey/sara_usa.md`), the Muskan stimuli, and the committed DCE design through the survey's own loaders; replicates the app's arm assignment (`creating_session`'s exact RNG stream), page sequence, display conditions, random_group shuffles, and adaptive BNT routing; draws answers from a documented data-generating process (DCE choices from the registered mixed logit, using the same truth vector as the archived identification sims); writes `all_apps_wide.csv`, `sara.csv`, `PageTimes.csv` in oTree's exact export format, plus `truth.json` (ground truth) and a **synthetic** post-stratification frame for pipeline testing. |
| `check_export_schema.py` | Runs the app's own bots (`otree test sara_usa 27 --export`) and asserts the simulator's headers and page count are identical. Run after any instrument or engine change. |
| `derive_orders.py` | Reconstructs each participant's randomised page orders (severity ladder, comparator block, …) from `participant.code` — the app seeds those shuffles deterministically, so the registered first-rung analysis needs no server-side logging. Works identically on real exports. |
| `report.Rmd` | The pre-registered report. Implements every analysis in `PREREGISTRATION.md`: §3 exclusions/flags, §4.1 F–N ladder (scope × numeracy, extinction discontinuity, first-rung check, WTP protest zeros), §4.2 DCE mixed logit + p\* distributions + sensitivities + wave robustness, §4.3 comparators, §4.4 named sources, §4.5 disclosure contrasts, §4.6 convergence go/no-go (+ gated multiplier), §4.7 superintelligence module (Aim 2, H2/H3 with the plan's planned contrasts, quasi-manipulation checks, exploratory mediation, sensitivities), §6 MRP (+ PPC, LOSO, state-map threshold), §7 Pew benchmarks (+ conditional raking), §8 negative-commitment checklist. Item text and scale labels are read from the instrument, never restated. |
| `report_utils.R` | Plumbing: instrument/YAML loading, export parsing, registered flags, small stats helpers. Model *specifications* stay in the report and `dce_model_utils.R`. |

## Running on real data

1. Export from the server: *Data* → all apps CSV + PageTimes CSV, into
   `analysis/realdata/` as `all_apps_wide.csv` and `PageTimes.csv`.
2. `python3 derive_orders.py realdata/all_apps_wide.csv realdata/orders.csv`
3. Build the real ACS frame (`python3 ../build_poststrat.py`) — the report
   uses `../poststrat_frame.csv` automatically when it exists.
4. `make real DATA=realdata`

Without `truth.json` the simulated-data banner and the recovery appendix
disappear automatically.

## Branding

`report_theme.css` styles the HTML report to the 2026 MIT FutureTech / AI
Risk Initiative brand (Figtree; primary `#A32035`; secondary grey `#666666`
— extracted from the brand's document styles), with the layout conventions
of the SARA 2025 technical report (banner title block, themed TOC/tables/
callouts, plot palette matched to the page). `theme_sara()` and the
`sara_seq()` ramp in `report_utils.R` carry the same palette into ggplot.
`fonts_figtree.css` embeds Figtree (latin, 400/600/700 + italic; OFL) as
base64 so the self-contained report needs no network; regenerate it by
re-running the snippet at the top of that file's git history or simply:

```python
# fetch css2 for Figtree ital,wght 0,400;0,600;0,700;1,400 with a browser
# User-Agent, download each latin woff2, and inline as
# src: url(data:font/woff2;base64,...) in @font-face blocks.
```

## Notes

- Expensive fits are cached in `<data>/cache/*.rds`, keyed on the input
  CSV's md5 — delete the cache directory to force refits.
- The MRP section uses `lme4` point estimates in this pipeline; the
  production analysis fits the same model in a fully Bayesian framework
  (`brms`) for interval estimates. The model specification is identical.
- Simulated outputs (`simdata/`, `*.html`) are gitignored: the *code* is
  the deliverable; artefacts regenerate with `make`.
