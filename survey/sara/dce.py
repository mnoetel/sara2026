# -*- coding: utf-8 -*-
"""Load the R-generated Bayesian D-efficient DCE design (dce_blocks.csv)."""
import csv
import os

_CSV = os.path.join(os.path.dirname(__file__), "dce_blocks.csv")


def _cost_label(v):
    try:
        return f"${int(round(float(v))):,}"
    except (TypeError, ValueError):
        return str(v)


def _load():
    blocks = {}
    if not os.path.exists(_CSV):
        return blocks
    with open(_CSV, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            b = int(row["block"])
            row["a_cost_label"] = _cost_label(row.get("a_cost_usd"))
            row["b_cost_label"] = _cost_label(row.get("b_cost_usd"))
            blocks.setdefault(b, []).append(row)
    for b in blocks:
        blocks[b].sort(key=lambda r: int(r["task"]))
    return blocks


BLOCKS = _load()
N_BLOCKS = max(len(BLOCKS), 1)

# Fallback so the app still runs if the CSV is absent.
_FALLBACK_TASK = {
    "a_severity": "100 deaths or $1B damage", "a_risk_annual": "1 in 10,000",
    "a_benefit": "Transformative", "a_competition": "US leads", "a_cost_label": "$400",
    "b_severity": "1,000,000 deaths or $100B damage", "b_risk_annual": "1 in 1,000,000",
    "b_benefit": "Modest", "b_competition": "Others lead", "b_cost_label": "$0",
}


def get_task(block, task_num):
    tasks = BLOCKS.get(block)
    if not tasks or task_num > len(tasks):
        return dict(_FALLBACK_TASK)
    return tasks[task_num - 1]
