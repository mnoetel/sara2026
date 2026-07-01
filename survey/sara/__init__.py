"""
SARA USA 2026 oTree app.

All item text, response scales, page order, rationale, and triangulation are
defined in survey/sara_usa.md — the single source of truth (a Markdown doc
wrapping the YAML spec, so it can be edited/reviewed in HackMD, Google Docs,
or GitHub). This file reads it at class-definition time and builds the Player
fields and Page classes from it. It also wires the features the content needs
but plain items cannot express: between-subjects randomisation arms
(comparator, sanity activity, information-provision half, DCE block, Muskan
briefing), per-participant text substitution, the consent gate, the DCE
(expanded into one page per task from sara_dce_design.R's output), and
Muskan's 3x3 superintelligence-briefing module. No item content is duplicated
here — see sara_usa.md.
"""

import os
import random
import sys

from otree.api import (
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Page,
)
import otree.database as db
import otree.forms.widgets as widgets

from . import render, dce, muskan

# ── Load the single source of truth ─────────────────────────────────
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from spec_loader import load_spec  # noqa: E402

_MD_PATH = os.path.join(os.path.dirname(__file__), '..', 'sara_usa.md')
SPEC = load_spec(_MD_PATH)

_SCALES = SPEC['scales']
_PAGES = SPEC['pages']

_DCE_PAGE = next((p for p in _PAGES if p.get('type') == 'dce'), None)
NUM_DCE_TASKS = (_DCE_PAGE or {}).get('n_tasks', 10)

# ── Attention-check screen-out ────────────────────────────────────────
# The two disguised comparators (m3_att_bioweapons, m3_att_nuclear) both
# require the extreme endpoint "Much less strict". Prolific/Bastical needs two
# failures to exclude someone, so we screen a participant out only when BOTH
# are wrong. The screen_out page (defined in the spec) redirects them back to
# Prolific; every page after it is then hidden — see _page_displayed.
_ATT_IDS = ('m3_att_bioweapons', 'm3_att_nuclear')
_ATT_REQUIRED = _SCALES['strictness5_cantcompare']['labels'].index('Much less strict') + 1
_PAGE_IDS = [p['id'] for p in _PAGES]
_SCREENOUT_POS = _PAGE_IDS.index('screen_out') if 'screen_out' in _PAGE_IDS else None

# randomisation pools
COMPARATORS = ["nuclear power", "commercial aviation", "new prescription drugs",
               "cars", "large dams"]
SANITY_ACTS = [
    "Climbing Mount Everest kills roughly 1 in 100 people who attempt the summit",
    "BASE jumping kills roughly 1 in 2,300 jumps",
    "Bungee jumping kills roughly 1 in 500,000 jumps",
]


# ── Field builder ─────────────────────────────────────────────────────
def _make_field(item):
    widget = item.get('widget', 'radio')
    label = item['text'].strip()
    required = item.get('required', True)
    if widget == 'number':
        return db.IntegerField(label=label, blank=not required)
    options = item.get('options')
    scale = item.get('scale')
    labels = options if options else (_SCALES[scale]['labels'] if scale in _SCALES else None)
    if labels:
        choices = list(zip(range(1, len(labels) + 1), labels))
        w = None if widget == 'select' else widgets.RadioSelect()
        kw = dict(label=label, choices=choices, blank=not required)
        if w is not None:
            kw['widget'] = w
        return db.IntegerField(**kw)
    return db.StringField(label=label, blank=True)


# ── Constants / models ────────────────────────────────────────────────
class C(BaseConstants):
    NAME_IN_URL = 'sara'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


def creating_session(subsession):
    for i, p in enumerate(subsession.get_players()):
        r = random.Random(p.participant.code)
        p.comparator = r.choice(COMPARATORS)
        p.sanity_phrase = r.choice(SANITY_ACTS)
        p.info_arm = r.choice([True, False])
        p.dce_block = (i % dce.N_BLOCKS) + 1
        st = r.choice(muskan.STIMULI)
        p.muskan_stim = st['stimulus_id']
        p.muskan_cell = st['cell']
        p.muskan_for = st['for_arg']
        p.muskan_against = st['against_arg']
        p.muskan_version = st['version']
        p.muskan_order = st['order']


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # between-subjects arms (internal, not form fields)
    comparator = db.StringField(blank=True)
    sanity_phrase = db.StringField(blank=True)
    info_arm = db.BooleanField(blank=True)
    dce_block = db.IntegerField(blank=True)
    muskan_stim = db.StringField(blank=True)
    muskan_cell = db.IntegerField(blank=True)
    muskan_for = db.StringField(blank=True)
    muskan_against = db.StringField(blank=True)
    muskan_version = db.IntegerField(blank=True)
    muskan_order = db.StringField(blank=True)


# Attach the YAML item fields (skip the generated DCE page).
for _ps in _PAGES:
    if _ps.get('type') == 'dce':
        continue
    for _it in _ps.get('items', []):
        setattr(Player, _it['id'], _make_field(_it))

# DCE choice fields, one per task.
for _t in range(1, NUM_DCE_TASKS + 1):
    setattr(Player, 'dce_%d' % _t, db.IntegerField(
        choices=[(1, 'Option A'), (2, 'Option B'), (3, "Neither")],
        widget=widgets.RadioSelect(), blank=False,
        label='DCE task %d' % _t))


# ── Display logic ─────────────────────────────────────────────────────
def _declined(player):
    return player.field_maybe_none('consent') == 2  # 2 = "I do not consent"


def _att_failed(player):
    """True once BOTH attention checks are answered and both are wrong. Guarded
    on being answered so it can't fire spuriously while the fields are blank."""
    vals = [player.field_maybe_none(i) for i in _ATT_IDS]
    return all(v is not None for v in vals) and all(v != _ATT_REQUIRED for v in vals)


def _page_displayed(player, page):
    pid = page['id']
    if _declined(player) and pid not in ('consent', 'end'):
        return False
    # attention-check screen-out gate: both checks wrong -> show the screen_out
    # page and hide every page after it (they are redirected to Prolific).
    failed = _att_failed(player)
    if pid == 'screen_out':
        return failed
    if failed and _SCREENOUT_POS is not None and _PAGE_IDS.index(pid) > _SCREENOUT_POS:
        return False
    cond = page.get('condition')
    if cond == 'info_arm':
        return bool(player.field_maybe_none('info_arm'))
    if cond == 'muskan_not_control':
        return not muskan.is_control(player.field_maybe_none('muskan_stim') or '')
    if cond == 'muskan_control':
        return muskan.is_control(player.field_maybe_none('muskan_stim') or '')
    return True


def _clsname(pid):
    return ''.join(w.capitalize() for w in pid.split('_')) + 'Page'


# ── Page factories (ordn/total passed for the progress bar) ───────────
def _make_content_page(page, ordn, total):
    item_ids = [it['id'] for it in page.get('items', [])]
    is_brief = page['id'] == 'superintelligence_brief'

    class _P(Page):
        form_model = 'player'
        form_fields = item_ids
        template_name = 'sara/Page.html'

        def vars_for_template(player, ps=page, brief=is_brief, ordn=ordn, total=total):
            body_html = ""
            if brief:
                st = muskan.get(player.field_maybe_none('muskan_stim') or '')
                body_html = render.paragraphs(st['body_text']) if st else ""
            return dict(page_title=ps.get('title', ''),
                        page_index=ordn, page_total=total,
                        body=render.page_body(ps, player, _SCALES, body_html))

        def is_displayed(player, ps=page):
            return _page_displayed(player, ps)

    _P.__name__ = _clsname(page['id'])
    return _P


def _make_rgroup_page(page, slot, ordn, total):
    """One page per item in a `type: random_group` page. Each participant sees
    the group's items one-per-page in a randomised order (seeded on their
    participant.code), so the sequence can't cue a monotone answering pattern.
    Every participant sees every item exactly once; fields save normally."""
    gid = page['id']
    items = page.get('items', [])
    n = len(items)

    def _order(player):
        r = random.Random('%s|%s' % (player.participant.code, gid))
        idx = list(range(n))
        r.shuffle(idx)
        return idx

    class _R(Page):
        form_model = 'player'
        template_name = 'sara/Page.html'

        def get_form_fields(player, _order=_order, slot=slot, items=items):
            return [items[_order(player)[slot]]['id']]

        def vars_for_template(player, ps=page, _order=_order, slot=slot,
                              items=items, ordn=ordn, total=total):
            it = items[_order(player)[slot]]
            single = dict(ps)
            single['items'] = [it]
            return dict(page_title=ps.get('title', ''),
                        page_index=ordn, page_total=total,
                        body=render.page_body(single, player, _SCALES))

        def is_displayed(player, ps=page):
            return _page_displayed(player, ps)

    _R.__name__ = _clsname('%s_slot%d' % (gid, slot + 1))
    return _R


def _make_dce_page(page, tn, ordn, total):
    rat = page.get('rationale', '')

    class _D(Page):
        form_model = 'player'
        form_fields = ['dce_%d' % tn]
        template_name = 'sara/Page.html'

        def vars_for_template(player, n=tn, ordn=ordn, total=total, rat=rat):
            block = player.field_maybe_none('dce_block') or 1
            return dict(page_title="Discrete choice experiment",
                        page_index=ordn, page_total=total,
                        body=render.dce_body(n, NUM_DCE_TASKS, dce.get_task(block, n), rat))

        def is_displayed(player):
            return not _declined(player)

    _D.__name__ = 'DceTask%dPage' % tn
    return _D


# ── Build the page sequence (flatten units, then number them) ─────────
_units = []
for _ps in _PAGES:
    if _ps.get('type') == 'dce':
        for _tn in range(1, NUM_DCE_TASKS + 1):
            _units.append(('dce', _ps, _tn))
    elif _ps.get('type') == 'random_group':
        for _si in range(len(_ps.get('items', []))):
            _units.append(('rgroup', _ps, _si))
    else:
        _units.append(('content', _ps, None))
_TOTAL = len(_units)

page_sequence = []
for _ordn, (_kind, _ps, _arg) in enumerate(_units, 1):
    if _kind == 'dce':
        _cls = _make_dce_page(_ps, _arg, _ordn, _TOTAL)
    elif _kind == 'rgroup':
        _cls = _make_rgroup_page(_ps, _arg, _ordn, _TOTAL)
    else:
        _cls = _make_content_page(_ps, _ordn, _TOTAL)
    globals()[_cls.__name__] = _cls
    page_sequence.append(_cls)
