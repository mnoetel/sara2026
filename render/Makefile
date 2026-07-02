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
# (sync-protocol) and re-renders the public protocol page (docs);
# `make check-protocol` / `make check-docs` are the read-only CI drift guards.

SPEC   := ../survey/sara_usa.md
LOADER := ../survey/spec_loader.py
OUT    := review.html

.PHONY: all review-r review-py sync-protocol check-protocol docs check-docs clean

all: $(OUT) sync-protocol docs

# Refresh the protocol doc's auto-blocks from the instrument (the volatile
# facts that would otherwise drift — expert anchors, scales, live/cut split).
sync-protocol: $(SPEC) $(LOADER) sync_protocol.py
	python3 sync_protocol.py

# CI guard: fail if the protocol's auto-blocks have drifted from the instrument.
check-protocol: $(SPEC) $(LOADER) sync_protocol.py
	python3 sync_protocol.py --check

# Publish the protocol as a pretty standalone page for non-GitHub readers
# (docs/index.html, served by GitHub Pages). Renders the protocol Markdown;
# needs the `markdown` package (pinned in ../requirements.txt). Runs after
# sync-protocol so the page reflects freshly synced auto-blocks.
# Also publishes the review table (docs/review.html) so reviewers can proof
# the item list + dumpster without cloning the repo.
docs: sync-protocol build_docs.py $(OUT)
	python3 build_docs.py
	cp $(OUT) ../docs/review.html

# CI guard: fail if docs/index.html has drifted from the protocol.
check-docs: build_docs.py
	python3 build_docs.py --check

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
