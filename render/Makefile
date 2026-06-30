# render/Makefile
# Regenerate the review table from the YAML source of truth.
#
# If R and reactable are available:
#   make review-r
# Otherwise, the Python fallback produces the same table:
#   make review-py
# Default target tries R first, falls back to Python.

YAML := ../survey/sara_usa.yaml
OUT  := review.html

.PHONY: all review-r review-py clean

all: $(OUT)

$(OUT): $(YAML) review.R review_fallback.py
	@if command -v Rscript >/dev/null 2>&1 && Rscript -e 'library(reactable)' 2>/dev/null; then \
		echo "Building review table with R + reactable..."; \
		Rscript review.R; \
	else \
		echo "R/reactable not available; using Python fallback..."; \
		python3 review_fallback.py; \
	fi

review-r: $(YAML) review.R
	Rscript review.R

review-py: $(YAML) review_fallback.py
	python3 review_fallback.py

clean:
	rm -f $(OUT)
