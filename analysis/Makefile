# SARA USA 2026 — reproducible pre-registered report pipeline
#
#   make            simulate data -> derive orders -> render the report
#   make simulate   regenerate analysis/simdata from the DGP (seeded)
#   make report     render report.html from whatever is in $(DATA)
#   make check-schema   prove the simulator's output is format-identical
#                       to a real `otree test --export` run (run after any
#                       instrument/engine change)
#   make real DATA=realdata   point the same pipeline at a real oTree
#                       export (put all_apps_wide.csv + PageTimes.csv in
#                       analysis/realdata/ first; no truth.json -> the
#                       recovery appendix is skipped automatically)
#
# Everything is deterministic given SEED (the DGP) and the registered
# fixed seeds inside report.Rmd (multistart estimation, bootstrap).

DATA  ?= simdata
SEED  ?= 1
WAVES ?= 500,1170,1170,1160

all: report

$(DATA)/all_apps_wide.csv:
	python3 simulate_data.py --seed $(SEED) --waves $(WAVES) --out $(DATA)

$(DATA)/orders.csv: $(DATA)/all_apps_wide.csv
	python3 derive_orders.py $(DATA)/all_apps_wide.csv $(DATA)/orders.csv

simulate:
	rm -rf $(DATA)
	python3 simulate_data.py --seed $(SEED) --waves $(WAVES) --out $(DATA)
	python3 derive_orders.py $(DATA)/all_apps_wide.csv $(DATA)/orders.csv

report: $(DATA)/all_apps_wide.csv $(DATA)/orders.csv
	Rscript -e 'rmarkdown::render("report.Rmd", params = list(data_dir = "$(DATA)"), output_file = "report.html", quiet = TRUE)'
	@echo "-> analysis/report.html"

# Render against a real export directory (e.g. make real DATA=realdata).
real: $(DATA)/orders.csv
	Rscript -e 'rmarkdown::render("report.Rmd", params = list(data_dir = "$(DATA)"), output_file = "report_$(DATA).html", quiet = TRUE)'

check-schema: $(DATA)/all_apps_wide.csv
	python3 check_export_schema.py $(DATA)

# End-to-end gate: simulate -> render -> assert parameter recovery passed.
verify: report
	@grep -q "RECOVERY OK" report.html \
	  && echo "VERIFY OK: pipeline recovers the simulated ground truth" \
	  || (echo "VERIFY FAILED: recovery warning in report.html" && exit 1)

clean:
	rm -rf simdata simdata_smoke report.html report_smoke.html

.PHONY: all simulate report real check-schema verify clean
