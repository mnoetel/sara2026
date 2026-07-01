# render/Makefile
# Regenerate the review table from sara_usa.md (the single source of truth).
#
# If R and reactable are available:
#   make review-r
# Otherwise, the Python fallback produces the same table:
#   make review-py
# Default target tries R first, falls back to Python.
#
# `make` also refreshes the protocol doc's auto-blocks from the instrument
# (sync-protocol); `make check-protocol` is a read-only CI guard that fails on drift.

SPEC   := ../survey/sara_usa.md
LOADER := ../survey/spec_loader.py
APP    := ../survey/sara/__init__.py
OUT    := review.html

.PHONY: all review-r review-py sync-protocol check-protocol clean

all: $(OUT) sync-protocol

# Refresh the protocol doc's auto-blocks from the instrument (the volatile
# facts that would otherwise drift — expert anchors, scales, live/cut split).
sync-protocol: $(SPEC) $(LOADER) $(APP) sync_protocol.py
	python3 sync_protocol.py

# CI guard: fail if the protocol's auto-blocks have drifted from the instrument.
check-protocol: $(SPEC) $(LOADER) $(APP) sync_protocol.py
	python3 sync_protocol.py --check

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
