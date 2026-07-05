#!/usr/bin/env python3
"""Reconstruct each participant's randomised page orders from the export.

The oTree app randomises within-person page order (the severity ladder, the
comparator block, the expert estimates, the tradeoffs) with
random.Random('<participant.code>|<page_id>') — a pure function of data
already in the export. This script recomputes those orders for every
participant, so the pre-registered "first-seen rung" analysis (a clean
between-subjects estimate on each respondent's first ladder page,
PREREGISTRATION.md §4.1) needs no extra logging on the server. It works
identically on simulated and real exports.

Output: orders.csv with one row per participant:
    participant.code, <page_id>_order (pipe-separated item ids, shown order),
    <page_id>_first (the first-seen item id) for every random_group page.

Usage:
    python3 analysis/derive_orders.py <all_apps_wide.csv> <orders.csv>
"""
import csv
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "survey"))
import spec_loader  # noqa: E402

SPEC = spec_loader.load_spec(
    os.path.join(os.path.dirname(HERE), "survey", "sara_usa.md"))
RGROUPS = [p for p in SPEC["pages"] if p.get("type") == "random_group"]


def order_for(code, page):
    """EXACT replica of the engine's _order (survey/sara/__init__.py)."""
    items = page.get("items", [])
    r = random.Random("%s|%s" % (code, page["id"]))
    idx = list(range(len(items)))
    r.shuffle(idx)
    idx.sort(key=lambda i: int(items[i].get("last") or 0))
    return [items[i]["id"] for i in idx]


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    src, dst = sys.argv[1], sys.argv[2]
    with open(src, newline="") as fh:
        codes = [row["participant.code"] for row in csv.DictReader(fh)]
    with open(dst, "w", newline="") as fh:
        w = csv.writer(fh)
        head = ["participant.code"]
        for p in RGROUPS:
            head += ["%s_order" % p["id"], "%s_first" % p["id"]]
        w.writerow(head)
        for code in codes:
            row = [code]
            for p in RGROUPS:
                order = order_for(code, p)
                row += ["|".join(order), order[0]]
            w.writerow(row)
    print("wrote %s (%d participants, %d random_group pages)"
          % (dst, len(codes), len(RGROUPS)))


if __name__ == "__main__":
    main()
