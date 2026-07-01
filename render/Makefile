# render/Makefile
# Regenerate the review table from sara_usa.md (the single source of truth).
#
# If R and reactable are available:
#   make review-r
# Otherwise, the Python fallback produces the same table:
#   make review-py
# Default target tries R first, falls back to Python.

SPEC   := ../survey/sara_usa.md
LOADER := ../survey/spec_loader.py
OUT    := review.html

.PHONY: all review-r review-py clean

all: $(OUT)

$(OUT): $(SPEC) $(LOADER) review.R review_fallback.py
	@if command -v Rscript >/dev/null 2>&1 && Rscript -e 'library(reactable)' 2>/dev/null; then \
		echo "Building review table with R + reactable..."; \
		Rscript review.R; \
	else \
		echo "R/reactable not available; using Python fallback..."; \
		python3 review_fallback.py; \
	fi

review-r: $(SPEC) review.R
	Rscript review.R

review-py: $(SPEC) $(LOADER) review_fallback.py
	python3 review_fallback.py

clean:
	rm -f $(OUT)
