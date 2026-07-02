# -*- coding: utf-8 -*-
"""Load the R-generated Bayesian D-efficient DCE design (dce_blocks.csv).

Fails loudly if the design is missing or a task is out of range: silently
serving a fallback task would produce plausible-looking but worthless DCE
data. Regenerate the CSV with sara_dce_design.R; never hand-edit it.
"""
import csv
import os

_CSV = os.path.join(os.path.dirname(__file__), "dce_blocks.csv")


def _load():
    if not os.path.exists(_CSV):
        raise FileNotFoundError(
            "%s is missing — the DCE design is required to field the survey. "
            "Regenerate it with:  Rscript sara_dce_design.R" % _CSV)
    blocks = {}
    with open(_CSV, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            b = int(row["block"])
            blocks.setdefault(b, []).append(row)
    if not blocks:
        raise ValueError("%s has no rows — regenerate it with "
                         "sara_dce_design.R" % _CSV)
    for b in blocks:
        blocks[b].sort(key=lambda r: int(r["task"]))
    return blocks


BLOCKS = _load()
N_BLOCKS = len(BLOCKS)


def get_task(block, task_num):
    tasks = BLOCKS.get(block)
    if not tasks or task_num > len(tasks):
        raise ValueError(
            "DCE block %r has no task %r — the design (dce_blocks.csv) and "
            "the spec's n_tasks disagree." % (block, task_num))
    return tasks[task_num - 1]
