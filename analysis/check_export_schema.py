#!/usr/bin/env python3
"""Verify the simulator's output format against the REAL oTree export.

Runs the app's own bots with `otree test sara_usa 27 --export <tmp>` (the
same machinery a live server uses to build its export), then asserts that
the simulator's all_apps_wide.csv / sara.csv headers are byte-identical to
the bot export's, and that the simulator's page count matches the app's
participant._max_page_index. Fails loudly on any drift — e.g. after an
instrument edit, run `make -C analysis check-schema` to prove the simulator
still matches the app.

Usage:
    python3 analysis/check_export_schema.py [simdata_dir]
"""
import csv
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SURVEY = os.path.join(REPO, "survey")


def header(path):
    with open(path, newline="") as fh:
        return next(csv.reader(fh))


def main():
    simdir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "simdata")
    for f in ("all_apps_wide.csv", "sara.csv"):
        if not os.path.exists(os.path.join(simdir, f)):
            sys.exit("missing %s/%s — run simulate_data.py first" % (simdir, f))

    tmp = tempfile.mkdtemp(prefix="sara_bot_export_")
    try:
        print("running oTree bots with export (this is the ground truth)…")
        subprocess.run(
            ["otree", "test", "sara_usa", "27", "--export", tmp],
            cwd=SURVEY, check=True, capture_output=True, text=True)

        problems = []
        for f in ("all_apps_wide.csv", "sara.csv"):
            bot, sim = header(os.path.join(tmp, f)), header(os.path.join(simdir, f))
            if bot != sim:
                extra = [c for c in sim if c not in bot]
                missing = [c for c in bot if c not in sim]
                problems.append(
                    "%s: header mismatch (missing: %s; extra: %s; "
                    "or order differs)" % (f, missing or "-", extra or "-"))
            else:
                print("OK  %-18s header identical (%d columns)" % (f, len(bot)))

        with open(os.path.join(tmp, "all_apps_wide.csv"), newline="") as fh:
            bot_rows = list(csv.DictReader(fh))
        with open(os.path.join(simdir, "all_apps_wide.csv"), newline="") as fh:
            sim_rows = list(csv.DictReader(fh))
        bot_max = {r["participant._max_page_index"] for r in bot_rows}
        sim_max = {r["participant._max_page_index"] for r in sim_rows}
        if bot_max != sim_max:
            problems.append("_max_page_index differs: app %s vs simulator %s"
                            % (sorted(bot_max), sorted(sim_max)))
        else:
            print("OK  page count matches the app (max_page_index=%s)"
                  % sorted(bot_max)[0])

        if problems:
            sys.exit("SCHEMA DRIFT:\n  - " + "\n  - ".join(problems))
        print("schema check passed: simulator output is format-identical "
              "to the oTree export.")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
