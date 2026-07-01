# -*- coding: utf-8 -*-
"""Muskan's 3x3 superintelligence-ban experiment — stimulus loader.

The final module of the SARA survey: each participant is randomly assigned one
of 27 pre-built briefings (9 ELM cells x 3 versions; cell 9 = neutral control),
reads it, then answers the ban-support DV. Passages are the single source of
truth in `survey/muskan_stimuli.md` (a fenced ```yaml``` block, same pattern
as `sara_usa.md`), parsed here via `spec_loader.load_spec()`.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from spec_loader import load_spec  # noqa: E402

_PATH = os.path.join(os.path.dirname(__file__), "..", "muskan_stimuli.md")

_DATA = load_spec(_PATH)

NEUTRAL_DEFINITION = _DATA["neutral_definition"]
STIMULI = _DATA["stimuli"]
STIM_IDS = [s["stimulus_id"] for s in STIMULI]
_BY_ID = {s["stimulus_id"]: s for s in STIMULI}


def get(stim_id):
    return _BY_ID.get(stim_id)


def is_control(stim_id):
    s = _BY_ID.get(stim_id)
    return bool(s) and s["cell"] == 9


def is_one_sided(stim_id):
    """True for cells that show exactly one side of the argument (for OR against,
    not both, and not the pure control) — cells 3, 6, 7, 8. The ELM mediators
    are asked only here, where a single message's route can be isolated."""
    s = _BY_ID.get(stim_id)
    if not s:
        return False
    shown = [a for a in (s["for_arg"], s["against_arg"]) if a != "none"]
    return len(shown) == 1
