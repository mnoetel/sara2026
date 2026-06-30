#!/usr/bin/env python3
"""Build the MRP post-stratification frame from ACS 2024 1-year PUMS (Census API).

Cells: state x age x sex x education x income, in the SARA survey's exact bins
(see ACS_poststratification_manual.md → "Survey ↔ ACS alignment"). Writes
poststrat_frame.csv, one row per cell, n = sum of person weights (PWGTP).

Dependency-free (stdlib only) — the no-tidycensus path. Needs a Census API key:
    export CENSUS_API_KEY=...      # or it is read from sara2026/.Renviron
    python3 build_poststrat.py
"""
import csv, json, os, re, time, urllib.request

BASE = "https://api.census.gov/data/2024/acs/acs1/pums"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "poststrat_frame.csv")


def _key():
    k = os.environ.get("CENSUS_API_KEY")
    if not k:  # fall back to the project .Renviron
        try:
            txt = open(os.path.join(HERE, ".Renviron")).read()
            m = re.search(r"CENSUS_API_KEY=(\S+)", txt)
            k = m.group(1) if m else None
        except FileNotFoundError:
            k = None
    if not k:
        raise SystemExit("Set CENSUS_API_KEY (env var or .Renviron). "
                         "Free key: https://api.census.gov/data/key_signup.html")
    return k


KEY = _key()

AGE_BINS = [(18, 24, "18-24"), (25, 34, "25-34"), (35, 44, "35-44"),
            (45, 54, "45-54"), (55, 64, "55-64"), (65, 74, "65-74"),
            (75, 200, "75 or older")]
INC_BINS = [(15000, "Under $15,000"), (25000, "$15,000-$24,999"),
            (35000, "$25,000-$34,999"), (50000, "$35,000-$49,999"),
            (75000, "$50,000-$74,999"), (100000, "$75,000-$99,999"),
            (150000, "$100,000-$149,999"), (200000, "$150,000-$199,999"),
            (10**12, "$200,000 or more")]


def age_cat(a):
    for lo, hi, lab in AGE_BINS:
        if lo <= a <= hi:
            return lab
    return None


def educ_cat(s):
    if s <= 15: return "Less than high school diploma"
    if s in (16, 17): return "High school graduate (or equivalent)"
    if s in (18, 19): return "Some college, no degree"
    if s == 20: return "Associate degree"
    if s == 21: return "Bachelor's degree"
    if s in (22, 23, 24): return "Graduate or professional degree"
    return None


def inc_cat(h):
    for ceil, lab in INC_BINS:
        if h < ceil:
            return lab
    return INC_BINS[-1][1]


def get(url):
    for attempt in range(4):
        try:
            with urllib.request.urlopen(url, timeout=120) as r:
                return json.loads(r.read().decode())
        except Exception:
            if attempt == 3:
                raise
            time.sleep(3)


def main():
    states = get("https://api.census.gov/data/2024/acs/acs1?get=NAME&for=state:*&key=%s" % KEY)
    fips = {row[1]: row[0] for row in states[1:] if row[1] != "72"}  # drop Puerto Rico
    print("states:", len(fips), flush=True)

    cells, total_w = {}, 0
    for code, name in sorted(fips.items(), key=lambda x: x[1]):
        d = get("%s?get=SEX,AGEP,SCHL,HINCP,PWGTP&for=state:%s&key=%s" % (BASE, code, KEY))
        h = d[0]
        iSEX, iAGE, iSCHL, iH, iW = (h.index(c) for c in
                                     ("SEX", "AGEP", "SCHL", "HINCP", "PWGTP"))
        kept = 0
        for r in d[1:]:
            if int(r[iAGE]) < 18:
                continue
            hv = r[iH]
            if hv in ("", ".", None):
                continue
            hinc = int(hv)
            if hinc == -60000:        # group quarters: no household income
                continue
            ac = age_cat(int(r[iAGE]))
            ec = educ_cat(int(r[iSCHL])) if r[iSCHL] not in ("", ".", None) else None
            if ac is None or ec is None:
                continue
            sex = "Male" if r[iSEX] == "1" else "Female"
            key = (name, ac, sex, ec, inc_cat(hinc))
            cells[key] = cells.get(key, 0) + int(r[iW])
            total_w += int(r[iW])
            kept += 1
        print("  %-22s %6d persons -> kept %6d" % (name, len(d) - 1, kept), flush=True)

    with open(OUT, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["state", "age", "sex", "education", "income", "n"])
        for (st, ac, sx, ec, ic), n in sorted(cells.items()):
            w.writerow([st, ac, sx, ec, ic, n])
    print("\nWROTE %d cells, %d weighted household adults -> %s" % (len(cells), total_w, OUT))


if __name__ == "__main__":
    main()
