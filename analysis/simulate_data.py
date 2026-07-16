#!/usr/bin/env python3
"""Simulate SARA USA 2026 data in EXACTLY the oTree server export format.

Purpose: the pre-registered report (analysis/report.Rmd) must be written and
tested end-to-end before any real data exist. This engine produces the three
files the oTree server will hand us —

    all_apps_wide.csv   (the "All apps" wide export; one row per participant)
    sara.csv            (the per-app export; same data, per-app prefixes)
    PageTimes.csv       (oTree's page-completion times export)

— plus truth.json, the ground-truth parameters of the data-generating
process, so every registered analysis can be checked for parameter recovery.

Fidelity guarantees (checked by analysis/check_export_schema.py against a
real `otree test sara_usa 27 --export` run):
  * column names, order, and value coding are identical to the live app's
    export (1-based choice codes, 0 = "Prefer not to answer", -1 = number
    opt-out, blank = never shown/never answered);
  * arm assignment replicates creating_session exactly (same _balanced
    blocks, same random.Random(session_code) stream);
  * page order, display conditions (consent gate, attention screen-out,
    wtp_zero probe, Muskan cell skips), the random_group shuffles (seeded
    on participant.code — reproducible from the export, see
    derive_orders.py) and the Berlin Numeracy adaptive routing replicate
    survey/sara/__init__.py;
  * DCE choices are simulated from the registered mixed logit
    (dce_model_utils.R's specification) with the same default truth vector
    as the archived identification simulations.

Everything item-level is driven by the instrument spec (sara_usa.md /
muskan_stimuli.md) — items added to the spec appear in the output
automatically (with a uniform-fallback DGP and a warning until given a
model here).

Usage:
    python3 analysis/simulate_data.py --out analysis/simdata --seed 1
    python3 analysis/simulate_data.py --waves 500,1170,1170,1160 --seed 1

Stdlib-only (like build_poststrat.py).
"""
import argparse
import csv
import importlib.util
import json
import math
import os
import random
import sys
from datetime import datetime, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SURVEY = os.path.join(REPO, "survey")
sys.path.insert(0, SURVEY)

import spec_loader  # noqa: E402
from spec_loader import OPT_OUT_NUMBER, OPT_OUT_VALUE, item_gets_opt_out  # noqa: E402


def _load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# survey/sara/dce.py and muskan.py are oTree-free; load them directly so the
# simulator shares the app's own design/stimulus loaders (no duplication).
dce = _load_module("sara_dce", os.path.join(SURVEY, "sara", "dce.py"))
muskan = _load_module("sara_muskan", os.path.join(SURVEY, "sara", "muskan.py"))

MD_PATH = os.path.join(SURVEY, "sara_usa.md")
SPEC = spec_loader.validate_spec(spec_loader.load_spec(MD_PATH), MD_PATH)
SCALES = SPEC["scales"]
PAGES = SPEC["pages"]

DCE_PAGE = next(p for p in PAGES if p.get("type") == "dce")
NUM_DCE_TASKS = DCE_PAGE.get("n_tasks", 10)

ATT_IDS = ("m3_att_bioweapons", "m3_att_nuclear")
ATT_REQUIRED = SCALES["strictness5_cantcompare"]["labels"].index("Much less strict") + 1

ITEMS_BY_ID = {it["id"]: it for p in PAGES for it in (p.get("items") or [])}


# ── Ground truth (defaults; everything lands in truth.json) ───────────
# DCE truth = the vector used by the archived identification simulations
# (sara_dce_design.R / dce_sequential.R --simulate), so the report's
# recovery check is comparable with the pre-freeze runs.
TRUTH = dict(
    dce=dict(logp=-0.9, logn=-0.35, ext=-0.7, ben_major=0.6, ben_transf=1.4,
             comp_pace=0.3, comp_lead=0.7, no_choice=-0.2, sd_logp=0.4),
    # Method 1 severity ladder: latent rung = ladder_base
    #   + ladder_slope_i * log10(deaths) + ext_bump_i * is_extinction
    #   + ladder_strict_load * strict_i + N(0, ladder_noise);
    # rung 1..8 = 10^-1..10^-8; > never_cut -> "Never allowed" (9).
    # Calibrated so Method 1 and DCE p* agree within one order of magnitude
    # on the overlap tiers (the §4.6 convergence gate passes by design).
    ladder=dict(base=0.75, slope_mean=0.22, slope_sd=0.07, flat_intercept=-0.8,
                flat_numeracy=-0.9, ext_bump_mean=0.6, ext_bump_share=0.65,
                strict_load=0.55, noise=0.45, never_cut=8.5,
                # absolute-refusal types: "Never allowed" at extinction,
                # about half of whom also refuse the 10%-of-humanity tier
                never_ext_share=0.12, never_800m_given_ext=0.5),
    info=dict(strict_shift=0.25),   # disclosure arm: latent strictness shift (M1/M3/M4/WTP)
    strict=dict(gender_f=0.20, age_per_band=0.06, educ_low=0.10, state_sd=0.10),
    m3=dict(mu=dict(m3_std_nuclear=-0.6, m3_std_aviation=-0.4, m3_std_dams=-0.3,
                    m3_sanity_everest=-1.3),
            strict_load=-0.6, cuts=[-1.5, -0.5, 0.5, 1.5], p_cantcompare=0.05),
    m4=dict(base=dict(m2_experts_lecun=-1.1, m2_experts_fri_super=0.2,
                      m2_experts_fri_domain=0.9, m2_experts_amodei=2.0),
            strict_load=0.7),       # P(Intolerable) = logistic(base + load*strict)
    wtp=dict(mu=-0.3, strict_load=0.35, income_load=0.25, noise=1.0,
             cuts=[-1.0, -0.3, 0.4, 1.2, 2.2], p_dk=0.06,
             zero_reason_probs=[0.30, 0.25, 0.25, 0.12, 0.08]),
    tradeoffs=dict(strict_load=-0.7, mu=dict(m5b_delay_uncond=-0.2,
                                             m5b_delay_cond=-0.5, m5_race=-0.3),
                   cuts=[-1.2, -0.2, 0.8, 1.8], cuts_support=[-1.0, 0.0, 1.0],
                   p_dk_uncond=0.05),
    bnt=dict(discrim=1.7, difficulty=dict(bnt_choir=0.0, bnt_five_die=-1.0,
                                          bnt_loaded_die=1.0, bnt_mushroom=0.3)),
    muskan=dict(mu=0.35, sd_person=0.8, strict_load=0.4,
                # latent ban-support effects of showing each argument
                for_elite=0.20, for_substantive=0.25,
                against_elite=-0.20, against_substantive=-0.45,
                cuts=[1.0, 0.0, -1.0],  # SS / S / O / SO on descending latent
                anti_cuts=[1.2, 0.4, -0.4, -1.2],  # agree5 on descending anti-latent
                p_dk=0.04, anti_noise=0.5, p_acquiescer=0.05,
                central_mu=0.3, central_sub=0.5, central_num=0.3,
                peripheral_mu=-0.3, peripheral_elite=0.5,
                p_comprehension_correct=0.80),
    bench=dict(cncexc=[0.08, 0.60, 0.32],   # Pew: 10/50/38 -> opt-in skew
               aireg=[0.18, 0.65, 0.17]),   # Pew: 21/58/21
    behaviour=dict(p_decline=0.010, p_careless_att=0.030, p_dce_random=0.05,
                   p_dropout=0.020, p_optout_item=0.004, p_speeder=0.05),
    politics=[0.10, 0.20, 0.36, 0.22, 0.12],
    ai_use=[0.10, 0.09, 0.10, 0.14, 0.27, 0.30],
)

# Sample (Prolific-ish, younger + more educated) vs population (ACS-ish)
# demographic marginals; the gap is what MRP must correct.
SAMPLE_DEMO = dict(
    age=[0.16, 0.26, 0.21, 0.14, 0.12, 0.08, 0.02, 0.01],   # incl. "Prefer not to say"
    gender=[0.47, 0.49, 0.04],
    education=[0.02, 0.16, 0.20, 0.10, 0.33, 0.18, 0.01],
    income=[0.07, 0.08, 0.09, 0.12, 0.19, 0.14, 0.17, 0.07, 0.06, 0.01],
)
POP_DEMO = dict(
    age=[0.115, 0.175, 0.165, 0.155, 0.165, 0.135, 0.09],
    gender=[0.49, 0.51],
    education=[0.09, 0.27, 0.19, 0.09, 0.22, 0.14],
    income=[0.08, 0.07, 0.07, 0.10, 0.16, 0.12, 0.17, 0.10, 0.13],
)
# Approximate 2023 state population shares (incl. DC), same order as the
# demo_state options in the instrument.
STATE_SHARES = [
    1.53, 0.22, 2.22, 0.92, 11.66, 1.76, 1.08, 0.31, 0.20, 6.77, 3.30, 0.43,
    0.59, 3.75, 2.05, 0.96, 0.88, 1.35, 1.37, 0.42, 1.85, 2.09, 3.00, 1.72,
    0.88, 1.85, 0.34, 0.59, 0.96, 0.42, 2.78, 0.63, 5.86, 3.24, 0.23, 3.52,
    1.21, 1.27, 3.87, 0.33, 1.60, 0.28, 2.13, 9.15, 1.02, 0.19, 2.61, 2.34,
    0.53, 1.77, 0.17,
]

CODE_CHARS = "abcdefghijklmnopqrstuvwxyz0123456789"


def _sigmoid(x):
    return 1.0 / (1.0 + math.exp(-x))


def _gumbel(rng):
    return -math.log(-math.log(rng.random()))


def _cat(rng, probs):
    """1-based categorical draw."""
    u, c = rng.random(), 0.0
    for i, p in enumerate(probs, 1):
        c += p
        if u < c:
            return i
    return len(probs)


def _ordinal(latent, cuts):
    """Category 1..len(cuts)+1 from a latent and ascending cutpoints."""
    k = 1
    for c in cuts:
        if latent > c:
            k += 1
    return k


# ── Replicas of the oTree engine's structural logic ───────────────────
def _balanced(rng, pool, n):
    out = []
    while len(out) < n:
        block = list(pool)
        rng.shuffle(block)
        out.extend(block)
    return out[:n]


def _clsname(pid):
    return "".join(w.capitalize() for w in pid.split("_")) + "Page"


def _adaptive_max_depth(page):
    by_id = {it["id"]: it for it in page.get("items", [])}

    def depth(node, seen):
        if node not in by_id or node in seen:
            return 0
        it = by_id[node]
        seen = seen | {node}
        return 1 + max(depth(it.get("next_if_correct"), seen),
                       depth(it.get("next_if_incorrect"), seen))

    return depth(page["root"], frozenset())


def build_units():
    """The flattened page sequence: (kind, page, arg, class_name), 1-indexed
    positions match participant._index_in_pages."""
    units = []
    for ps in PAGES:
        if ps.get("type") == "dce":
            for tn in range(1, NUM_DCE_TASKS + 1):
                units.append(("dce", ps, tn, "DceTask%dPage" % tn))
        elif ps.get("type") == "random_group":
            for si in range(len(ps.get("items", []))):
                units.append(("rgroup", ps, si,
                              _clsname("%s_slot%d" % (ps["id"], si + 1))))
        elif ps.get("type") == "adaptive":
            for si in range(_adaptive_max_depth(ps)):
                units.append(("adaptive", ps, si,
                              _clsname("%s_slot%d" % (ps["id"], si + 1))))
        else:
            units.append(("content", ps, None, _clsname(ps["id"])))
    return units


UNITS = build_units()
TOTAL_PAGES = len(UNITS)
SCREENOUT_POS = next(i for i, (_, p, _, _) in enumerate(UNITS)
                     if p.get("condition") == "att_failed")


def rgroup_order(code, page):
    """EXACT replica of the engine's per-participant random_group order."""
    items = page.get("items", [])
    r = random.Random("%s|%s" % (code, page["id"]))
    idx = list(range(len(items)))
    r.shuffle(idx)
    idx.sort(key=lambda i: int(items[i].get("last") or 0))
    return idx


# ── Player field list (must mirror __init__.py's declaration order) ───
ARM_FIELDS = ["info_arm", "dce_block", "muskan_stim", "muskan_cell",
              "muskan_for", "muskan_against", "muskan_version", "muskan_order"]
ITEM_FIELDS = [it["id"] for p in PAGES if p.get("type") != "dce"
               for it in p.get("items", [])]
DCE_FIELDS = ["dce_%d" % t for t in range(1, NUM_DCE_TASKS + 1)]
PLAYER_FIELDS = (["id_in_group", "role", "payoff"] + ARM_FIELDS
                 + ITEM_FIELDS + DCE_FIELDS)

PARTICIPANT_FIELDS = ["id_in_session", "code", "label", "_is_bot",
                      "_index_in_pages", "_max_page_index",
                      "_current_app_name", "_current_page_name",
                      "time_started_utc", "visited", "mturk_worker_id",
                      "mturk_assignment_id", "payoff"]
SESSION_FIELDS = ["code", "label", "mturk_HITId", "mturk_HITGroupId",
                  "comment", "is_demo"]

WIDE_HEADER = (["participant.%s" % f for f in PARTICIPANT_FIELDS]
               + ["session.%s" % f for f in SESSION_FIELDS]
               + ["session.config.name", "session.config.participation_fee",
                  "session.config.real_world_currency_per_point"]
               + ["sara.1.player.%s" % f for f in PLAYER_FIELDS]
               + ["sara.1.group.id_in_subsession",
                  "sara.1.subsession.round_number"])

APP_HEADER = (["participant.%s" % f for f in PARTICIPANT_FIELDS]
              + ["player.%s" % f for f in PLAYER_FIELDS]
              + ["group.id_in_subsession", "subsession.round_number"]
              + ["session.%s" % f for f in SESSION_FIELDS])

PAGETIMES_HEADER = ["session_code", "participant_id_in_session",
                    "participant_code", "page_index", "app_name", "page_name",
                    "epoch_time_completed", "round_number",
                    "timeout_happened", "is_wait_page"]


# ── The respondent model ──────────────────────────────────────────────
class Resp:
    """One simulated participant: demographics + latent traits + behaviour
    flags, drawn once, then consumed by the per-item answer models."""

    def __init__(self, rng, truth, state_effects):
        t = truth
        # demographics (1-based codes into the instrument's option lists)
        self.demo_age = _cat(rng, SAMPLE_DEMO["age"])
        self.demo_gender = _cat(rng, SAMPLE_DEMO["gender"])
        self.demo_education = _cat(rng, SAMPLE_DEMO["education"])
        self.demo_income = _cat(rng, SAMPLE_DEMO["income"])
        self.demo_state = _cat(rng, [s / 100.0 for s in STATE_SHARES])
        self.m9_politics = _cat(rng, t["politics"])
        self.m9_ai_use = _cat(rng, t["ai_use"])

        # latent traits
        s = t["strict"]
        age_band = min(self.demo_age, 7)          # exclude "prefer not" from trend
        self.z_strict = (rng.gauss(0, 1)
                         + (s["gender_f"] if self.demo_gender == 2 else 0)
                         + s["age_per_band"] * (age_band - 4)
                         + (s["educ_low"] if self.demo_education <= 3 else 0)
                         + state_effects[self.demo_state - 1])
        self.z_num = rng.gauss(0, 1) + 0.15 * (self.demo_education - 4) / 2.0
        self.z_support = rng.gauss(0, 1)          # Muskan person effect
        inc_band = min(self.demo_income, 9)
        self.z_income = (inc_band - 5) / 2.5

        # behaviour flags
        b = t["behaviour"]
        self.decline = rng.random() < b["p_decline"]
        self.careless_att = rng.random() < b["p_careless_att"]
        self.dce_random = rng.random() < b["p_dce_random"]
        self.speeder = rng.random() < b["p_speeder"]
        self.acquiescer = rng.random() < t["muskan"]["p_acquiescer"]
        self.dropout_at = None
        if not self.decline and rng.random() < b["p_dropout"]:
            self.dropout_at = rng.randint(3, TOTAL_PAGES)   # 1-based unit index

        # ladder person parameters
        lad = t["ladder"]
        p_flat = _sigmoid(lad["flat_intercept"] + lad["flat_numeracy"] * self.z_num)
        self.ladder_flat = rng.random() < p_flat
        self.ladder_slope = 0.0 if self.ladder_flat else max(
            0.0, rng.gauss(lad["slope_mean"], lad["slope_sd"]))
        self.ext_bump = (max(0.0, rng.gauss(lad["ext_bump_mean"], 0.3))
                         if rng.random() < lad["ext_bump_share"] else 0.0)
        self.ladder_base = lad["base"] + rng.gauss(0, 0.6)
        self.never_ext = rng.random() < lad["never_ext_share"]
        self.never_800m = (self.never_ext
                           and rng.random() < lad["never_800m_given_ext"])

        # DCE person slope (registered random coefficient)
        d = t["dce"]
        self.b_logp = rng.gauss(d["logp"], d["sd_logp"])


SEV_TO_LOGN = {"A single death": 0.0, "100 deaths": 2.0,
               "1,000,000 deaths": 6.0,
               "~800,000,000 deaths (10% of humanity)": 8.9,
               "Human extinction (fewer than 5,000 people survive)": 9.9}
RISK_TO_LOGP = {"1 in 100": -2.0, "1 in 1,000": -3.0, "1 in 10,000": -4.0,
                "1 in 100,000": -5.0, "1 in 1,000,000": -6.0}
EXT_LEVEL = "Human extinction (fewer than 5,000 people survive)"
LADDER_LOGN = {"m4c_single": 0.0, "m4c_100": 2.0, "m4c_1m": 6.0,
               "m4c_800m": 8.9, "m4c_extinction": 9.9}

_FALLBACK_WARNED = set()


class Simulator:
    def __init__(self, truth, seed):
        self.truth = truth
        self.master = random.Random(seed)
        self.state_effects = [self.master.gauss(0, truth["strict"]["state_sd"])
                              for _ in STATE_SHARES]

    # ── item-level answer models ──────────────────────────────────────
    def answer(self, r, rng, item_id, f):
        t = self.truth
        item = ITEMS_BY_ID.get(item_id)

        # universal opt-out (never on attention checks: an opt-out there is a
        # fail, and the honest majority answers them)
        if (item_id not in ATT_IDS and item_id != "consent"
                and item is not None and item_gets_opt_out(item, SCALES)
                and rng.random() < t["behaviour"]["p_optout_item"]):
            return OPT_OUT_NUMBER if item.get("widget") == "number" else OPT_OUT_VALUE

        strict = r.z_strict + (t["info"]["strict_shift"] if f["info_arm"] else 0.0)

        if item_id == "consent":
            return 2 if r.decline else 1
        if item_id == "bench_pew_cncexc":
            return _cat(rng, t["bench"]["cncexc"])
        if item_id == "bench_pew_aireg":
            return _cat(rng, t["bench"]["aireg"])

        if item_id in LADDER_LOGN:
            lad = t["ladder"]
            if ((item_id == "m4c_extinction" and r.never_ext)
                    or (item_id == "m4c_800m" and r.never_800m)):
                return 9                                  # Never allowed
            y = (r.ladder_base + r.ladder_slope * LADDER_LOGN[item_id]
                 + (r.ext_bump if item_id == "m4c_extinction" else 0.0)
                 + lad["strict_load"] * strict + rng.gauss(0, lad["noise"]))
            if y > lad["never_cut"]:
                return 9                                  # Never allowed
            return min(8, max(1, int(round(y))))

        if item_id in ATT_IDS:
            if r.careless_att:
                wrong = [k for k in range(1, 7) if k != ATT_REQUIRED]
                return rng.choice(wrong)
            # attentive: near-perfect instructed response, rare single slips
            return ATT_REQUIRED if rng.random() < 0.985 else rng.choice(
                [k for k in range(1, 7) if k != ATT_REQUIRED])

        if item_id in t["m3"]["mu"]:
            m3 = t["m3"]
            if rng.random() < m3["p_cantcompare"]:
                return 6
            latent = m3["mu"][item_id] + m3["strict_load"] * strict + rng.gauss(0, 1)
            return _ordinal(latent, m3["cuts"])           # 1..5

        if item_id in t["m4"]["base"]:
            p_int = _sigmoid(t["m4"]["base"][item_id]
                             + t["m4"]["strict_load"] * strict)
            return 2 if rng.random() < p_int else 1

        if item_id == "m5_wtp":
            w = t["wtp"]
            if rng.random() < w["p_dk"]:
                return 7
            latent = (w["mu"] + w["strict_load"] * strict
                      + w["income_load"] * r.z_income + rng.gauss(0, w["noise"]))
            return _ordinal(latent, w["cuts"])            # 1..6
        if item_id == "m5_wtp_zero_reason":
            return _cat(rng, t["wtp"]["zero_reason_probs"])

        if item_id in t["tradeoffs"]["mu"]:
            tr = t["tradeoffs"]
            latent = (tr["mu"][item_id] + tr["strict_load"] * strict
                      + rng.gauss(0, 1))
            if item_id == "m5b_delay_uncond":
                # support5: SS/S/O/SO + "Don't know" (5, drawn separately)
                if rng.random() < tr["p_dk_uncond"]:
                    return 5
                return _ordinal(latent, tr["cuts_support"])   # 1..4
            return _ordinal(latent, tr["cuts"])               # worthwhile5, 1..5

        if item_id.startswith("bnt_"):
            b = t["bnt"]
            p = _sigmoid(b["discrim"] * (r.z_num - b["difficulty"][item_id]))
            correct = ITEMS_BY_ID[item_id]["correct_answer"]
            if rng.random() < p:
                return correct
            wrongs = {"bnt_choir": [20, 50, 10, 33], "bnt_five_die": [25, 10, 20],
                      "bnt_loaded_die": [35, 12, 10], "bnt_mushroom": [20, 4, 57, 80]}
            return rng.choice(wrongs[item_id])

        if item_id in ("m9_politics",):
            return r.m9_politics
        if item_id == "m9_ai_use":
            return r.m9_ai_use
        if item_id.startswith("demo_"):
            return getattr(r, item_id)

        if item_id == "muskan_support":
            return self._muskan_support(r, rng, f)[0]
        if item_id == "muskan_support_anti":
            return self._muskan_support(r, rng, f)[1]
        if item_id == "muskan_central_route":
            m = t["muskan"]
            latent = (m["central_mu"]
                      + (m["central_sub"] if "substantive" in
                         (f["muskan_for"], f["muskan_against"]) else 0.0)
                      + m["central_num"] * r.z_num + rng.gauss(0, 1))
            return _ordinal(latent, [-1.2, -0.4, 0.4, 1.2])
        if item_id == "muskan_peripheral_route":
            m = t["muskan"]
            latent = (m["peripheral_mu"]
                      + (m["peripheral_elite"] if "elite" in
                         (f["muskan_for"], f["muskan_against"]) else 0.0)
                      + rng.gauss(0, 1))
            return _ordinal(latent, [-1.2, -0.4, 0.4, 1.2])
        if item_id == "muskan_si_comprehension":
            if rng.random() < t["muskan"]["p_comprehension_correct"]:
                return 4
            return rng.choice([1, 2, 3])

        # spec-driven fallback: uniform over the item's labels
        if item_id not in _FALLBACK_WARNED:
            _FALLBACK_WARNED.add(item_id)
            print("WARNING: no DGP for item %r — using uniform fallback"
                  % item_id, file=sys.stderr)
        labels = (item.get("options")
                  or SCALES.get(item.get("scale"), {}).get("labels") or [1])
        return rng.randint(1, len(labels))

    def _muskan_support(self, r, rng, f):
        """(support, anti) pair, memoised per participant so the two DV pages
        share one latent (they are the same attitude asked twice)."""
        if "_muskan_pair" in f:
            return f["_muskan_pair"]
        m = self.truth["muskan"]
        eff = 0.0
        eff += {"elite": m["for_elite"], "substantive": m["for_substantive"],
                "none": 0.0}[f["muskan_for"]]
        eff += {"elite": m["against_elite"],
                "substantive": m["against_substantive"],
                "none": 0.0}[f["muskan_against"]]
        latent = (m["mu"] + eff + m["strict_load"] * r.z_strict
                  + m["sd_person"] * r.z_support)
        if r.acquiescer:
            pair = (rng.choice([1, 2]), rng.choice([1, 2]))
        else:
            # support5 codes DESCEND in support (1 = Strongly support), so
            # categorise -latent against the negated (ascending) cuts.
            sup = (5 if rng.random() < m["p_dk"]
                   else _ordinal(-(latent + rng.gauss(0, 0.5)),
                                 [-c for c in m["cuts"]]))
            # anti item is agree5 (1 = Strongly agree with the ANTI-ban
            # statement ... 5 = Strongly disagree): a pro-ban latent should
            # land at 4-5. Higher anti_lat = more anti-ban agreement.
            anti_lat = -latent + rng.gauss(0, m["anti_noise"])
            anti = _ordinal(-anti_lat, [-c for c in m["anti_cuts"]])
            pair = (sup, anti)
        f["_muskan_pair"] = pair
        return pair

    def dce_choice(self, r, rng, task, f):
        """Choice on one DCE task from the registered mixed logit."""
        if r.dce_random:
            return rng.choice([1, 2, 3])
        t = self.truth["dce"]

        def util(prefix):
            sev, risk = task["%s_severity" % prefix], task["%s_risk_annual" % prefix]
            ben, comp = task["%s_benefit" % prefix], task["%s_competition" % prefix]
            return (r.b_logp * RISK_TO_LOGP[risk]
                    + t["logn"] * SEV_TO_LOGN[sev]
                    + t["ext"] * (1 if sev == EXT_LEVEL else 0)
                    + t["ben_major"] * (1 if ben == "Major" else 0)
                    + t["ben_transf"] * (1 if ben == "Transformative" else 0)
                    + t["comp_pace"] * (1 if comp == "The US keeps pace" else 0)
                    + t["comp_lead"] * (1 if comp == "The US is ahead" else 0))

        u = [util("a") + _gumbel(rng), util("b") + _gumbel(rng),
             t["no_choice"] + _gumbel(rng)]
        return u.index(max(u)) + 1

    # ── display-condition replica (survey/sara/__init__.py) ──────────
    # The consent gate and attention screen-out are position-dependent and
    # handled in walk(); this covers the remaining conditions.
    def displayed(self, page, f):
        cond = page.get("condition")
        if cond is None:
            return True
        if cond == "info_arm":
            return bool(f["info_arm"])
        if cond == "wtp_zero":
            return f.get("m5_wtp") == 1
        if cond == "muskan_not_control":
            return not muskan.is_control(f["muskan_stim"])
        if cond == "muskan_control":
            return muskan.is_control(f["muskan_stim"])
        if cond == "muskan_one_sided":
            return muskan.is_one_sided(f["muskan_stim"])
        raise ValueError("unknown condition %r" % cond)

    # ── dwell-time model (for PageTimes.csv) ──────────────────────────
    def dwell(self, r, rng, kind, page, f):
        base = {"content": 12.0, "rgroup": 9.0, "adaptive": 20.0, "dce": 14.0}[kind]
        if page["id"] == "consent":
            base = 30.0
        if page["id"] == "superintelligence_brief":
            st = muskan.get(f["muskan_stim"])
            words = len(st["body_text"].split()) if st else 100
            base = words / 230.0 * 60.0
            if r.speeder:
                base *= 0.22
        return max(1.0, base * math.exp(rng.gauss(0, 0.45)))

    # ── one participant's full walk through the page sequence ────────
    def walk(self, r, code, session_code, id_in_session, start_epoch):
        rng = random.Random("%s|dgp|%s" % (self.master.random(), code))
        f = dict(r.arm_fields)          # muskan_stim etc. + info_arm, dce_block
        adaptive_state = {}
        pagetimes = []
        epoch = start_epoch
        stopped_at = None               # (index, class_name) if they never finish

        for pos, (kind, page, arg, clsname) in enumerate(UNITS, 1):
            declined = f.get("consent") == 2
            vals = [f.get(i) for i in ATT_IDS]
            failed = (all(v is not None for v in vals)
                      and all(v != ATT_REQUIRED for v in vals))

            # display logic (mirrors _page_displayed + the position rule)
            cond = page.get("condition")
            if cond == "declined":
                show = declined
            elif declined and page["id"] != "consent":
                show = False
            elif cond == "att_failed":
                show = failed
            elif failed and pos - 1 > SCREENOUT_POS:
                show = False
            else:
                show = self.displayed(page, f)
            if not show:
                continue

            # terminal pages the participant sits on (never submits)
            if cond in ("declined", "att_failed"):
                stopped_at = (pos, clsname)
                break

            if r.dropout_at is not None and pos >= r.dropout_at:
                stopped_at = (pos, clsname)
                break

            # answer the page's field(s)
            if kind == "content":
                for it in page.get("items", []):
                    f[it["id"]] = self.answer(r, rng, it["id"], f)
            elif kind == "rgroup":
                order = rgroup_order(code, page)
                it = page["items"][order[arg]]
                f[it["id"]] = self.answer(r, rng, it["id"], f)
            elif kind == "adaptive":
                path = adaptive_state.setdefault(page["id"], [page["root"]])
                if arg >= len(path):
                    continue            # branch terminated earlier
                iid = path[arg]
                by_id = {it["id"]: it for it in page["items"]}
                it = by_id[iid]
                ans = self.answer(r, rng, iid, f)
                f[iid] = ans
                nxt = (it["next_if_correct"] if ans == it.get("correct_answer")
                       else it["next_if_incorrect"])
                if nxt in by_id:
                    path.append(nxt)
            elif kind == "dce":
                task = dce.get_task(f["dce_block"], arg)
                f["dce_%d" % arg] = self.dce_choice(r, rng, task, f)

            epoch += self.dwell(r, rng, kind, page, f)
            pagetimes.append([session_code, id_in_session, code, pos, "sara",
                              clsname, int(epoch), 1, 0, 0])

        if stopped_at is None:
            index_in_pages, current_page = TOTAL_PAGES + 1, UNITS[-1][3]
        else:
            index_in_pages, current_page = stopped_at
        f.pop("_muskan_pair", None)
        _validate_fields(f)
        return f, pagetimes, index_in_pages, current_page


# ── Self-validation ───────────────────────────────────────────────────
# Every generated answer must be a value the live app could have saved:
# 1..n_labels for choice items (0 = opt-out), the BNT number widgets
# unrestricted (-1 = opt-out), DCE tasks in {0,1,2,3}. A DGP bug can then
# never produce plausible-looking but impossible data.
def _validate_fields(f):
    for iid, val in f.items():
        if val is None or iid in ARM_FIELDS:
            continue
        if iid.startswith("dce_"):
            if val not in (0, 1, 2, 3):
                raise AssertionError("%s: illegal value %r" % (iid, val))
            continue
        item = ITEMS_BY_ID.get(iid)
        if item is None:
            raise AssertionError("unknown field %r" % iid)
        if item.get("widget") == "number":
            if not isinstance(val, int):
                raise AssertionError("%s: non-integer %r" % (iid, val))
            continue
        labels = (item.get("options")
                  or SCALES.get(item.get("scale"), {}).get("labels") or [])
        legal = set(range(1, len(labels) + 1)) | {OPT_OUT_VALUE}
        if val not in legal:
            raise AssertionError(
                "%s: value %r outside 0..%d" % (iid, val, len(labels)))


# ── Output assembly ───────────────────────────────────────────────────
def _fmt(v):
    if v is None:
        return ""
    if isinstance(v, bool):
        return "1" if v else "0"
    if isinstance(v, float):
        return repr(v)
    return str(v)


def simulate(waves, seed, truth, start_dt):
    sim = Simulator(truth, seed)
    codegen = random.Random(seed + 104729)
    used = set()

    def new_code(k=8):
        while True:
            c = "".join(codegen.choice(CODE_CHARS) for _ in range(k))
            if c not in used:
                used.add(c)
                return c

    wide_rows, app_rows, pt_rows = [], [], []
    for w, n in enumerate(waves, 1):
        session_code = new_code()
        # EXACT replica of creating_session's assignment stream
        arng = random.Random(session_code)
        info_arms = _balanced(arng, [True, False], n)
        stimuli = _balanced(arng, muskan.STIMULI, n)
        blocks = _balanced(arng, range(1, dce.N_BLOCKS + 1), n)

        wave_start = start_dt + timedelta(days=14 * (w - 1))
        for i in range(n):
            r = Resp(sim.master, truth, sim.state_effects)
            st = stimuli[i]
            r.arm_fields = dict(
                info_arm=info_arms[i], dce_block=blocks[i],
                muskan_stim=st["stimulus_id"], muskan_cell=st["cell"],
                muskan_for=st["for_arg"], muskan_against=st["against_arg"],
                muskan_version=st["version"], muskan_order=st["order"])
            code = new_code()
            label = "".join(codegen.choice("0123456789abcdef") for _ in range(24))
            started = (wave_start
                       + timedelta(seconds=sim.master.uniform(0, 3 * 86400)))
            f, pts, idx, curpage = sim.walk(
                r, code, session_code, i + 1, started.timestamp())

            participant = [i + 1, code, label, 0, idx, TOTAL_PAGES, "sara",
                           curpage, started.strftime("%Y-%m-%d %H:%M:%S.%f"),
                           1, "", "", "0.0"]
            session = [session_code, "wave%d" % w, "", "", "", 0]
            config = ["sara_usa", "0.0", "1.0"]
            player = [i + 1, "", "0.0"]
            player += [f.get(a) for a in ARM_FIELDS]
            player += [f.get(iid) for iid in ITEM_FIELDS]
            player += [f.get(d) for d in DCE_FIELDS]

            wide_rows.append([_fmt(v) for v in
                              participant + session + config + player + [1, 1]])
            app_rows.append([_fmt(v) for v in
                             participant + player + [1, 1] + session])
            pt_rows.extend(pts)
    return wide_rows, app_rows, pt_rows


def write_poststrat_frame(path, seed):
    """SYNTHETIC post-stratification frame (same columns as
    build_poststrat.py's Census output) so the MRP stage of the report runs
    end-to-end without a Census API key. Clearly not real ACS data."""
    ages = ["18-24", "25-34", "35-44", "45-54", "55-64", "65-74", "75 or older"]
    sexes = ["Male", "Female"]
    edus = ["Less than high school diploma", "High school graduate (or equivalent)",
            "Some college, no degree", "Associate degree", "Bachelor's degree",
            "Graduate or professional degree"]
    incs = ["Under $15,000", "$15,000-$24,999", "$25,000-$34,999",
            "$35,000-$49,999", "$50,000-$74,999", "$75,000-$99,999",
            "$100,000-$149,999", "$150,000-$199,999", "$200,000 or more"]
    states = ITEMS_BY_ID["demo_state"]["options"][:-1]   # drop "Prefer not to say"
    total_adults = 258e6
    rng = random.Random(seed + 7)
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["state", "age", "sex", "education", "income", "n"])
        for si, stt in enumerate(states):
            for ai, a in enumerate(ages):
                for xi, x in enumerate(sexes):
                    for ei, e in enumerate(edus):
                        for ii, inc in enumerate(incs):
                            p = (STATE_SHARES[si] / 100.0
                                 * POP_DEMO["age"][ai] * POP_DEMO["gender"][xi]
                                 * POP_DEMO["education"][ei] * POP_DEMO["income"][ii])
                            # mild positive educ x income association
                            p *= 1.0 + 0.10 * (ei - 2.5) * (ii - 4) / 10.0
                            n = int(round(p * total_adults * rng.uniform(0.97, 1.03)))
                            if n > 0:
                                w.writerow([stt, a, x, e, inc, n])


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", default=os.path.join(HERE, "simdata"))
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--n", type=int, default=None,
                    help="single-session shortcut (overrides --waves)")
    ap.add_argument("--waves", default="500,1170,1170,1160",
                    help="comma-separated wave sizes (default: registered plan)")
    ap.add_argument("--start-date", default="2026-08-03")
    args = ap.parse_args()

    waves = ([args.n] if args.n
             else [int(x) for x in args.waves.split(",") if x.strip()])
    start_dt = datetime.fromisoformat(args.start_date)
    os.makedirs(args.out, exist_ok=True)

    wide, app, pts = simulate(waves, args.seed, TRUTH, start_dt)

    def dump(name, header, rows):
        p = os.path.join(args.out, name)
        with open(p, "w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(header)
            w.writerows(rows)
        print("wrote %-20s %6d rows" % (name, len(rows)))

    dump("all_apps_wide.csv", WIDE_HEADER, wide)
    dump("sara.csv", APP_HEADER, app)
    dump("PageTimes.csv", PAGETIMES_HEADER, pts)
    write_poststrat_frame(os.path.join(args.out, "poststrat_frame_synthetic.csv"),
                          args.seed)
    print("wrote poststrat_frame_synthetic.csv (SYNTHETIC frame for pipeline"
          " testing; real MRP uses build_poststrat.py output)")

    meta = dict(seed=args.seed, waves=waves, n_total=sum(waves),
                start_date=args.start_date, total_pages=TOTAL_PAGES,
                truth=TRUTH, sample_demo=SAMPLE_DEMO, pop_demo=POP_DEMO)
    with open(os.path.join(args.out, "truth.json"), "w") as fh:
        json.dump(meta, fh, indent=2)
    print("wrote truth.json")


if __name__ == "__main__":
    main()
