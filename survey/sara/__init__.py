"""
SARA USA 2026 oTree app.

All item text, response scales, page order, rationale, and triangulation are
defined in survey/sara_usa.yaml — the single source of truth. This file reads
the YAML at class-definition time and builds the Player fields and Page classes
from it. It also wires the features the content needs but plain items cannot
express: between-subjects randomisation arms (comparator, sanity activity,
information-provision half, DCE block, Muskan briefing), per-participant text
substitution, the consent gate, the DCE (expanded into one page per task from
sara_dce_design.R's output), and Muskan's 3x3 superintelligence-briefing module.
No item content is duplicated here — see sara_usa.yaml.
"""

import os
import random

import yaml

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
_YAML_PATH = os.path.join(os.path.dirname(__file__), '..', 'sara_usa.yaml')
with open(_YAML_PATH) as _f:
    SPEC = yaml.safe_load(_f)

_SCALES = SPEC['scales']
_PAGES = SPEC['pages']

_DCE_PAGE = next((p for p in _PAGES if p.get('type') == 'dce'), None)
NUM_DCE_TASKS = (_DCE_PAGE or {}).get('n_tasks', 10)

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


def _page_displayed(player, page):
    if _declined(player) and page['id'] not in ('consent', 'end'):
        return False
    cond = page.get('condition')
    if cond == 'info_arm':
        return bool(player.field_maybe_none('info_arm'))
    if cond == 'muskan_not_control':
        return not muskan.is_control(player.field_maybe_none('muskan_stim') or '')
    return True


def _clsname(pid):
    return ''.join(w.capitalize() for w in pid.split('_')) + 'Page'


# ── Page factories ────────────────────────────────────────────────────
def _make_content_page(page):
    item_ids = [it['id'] for it in page.get('items', [])]
    is_brief = page['id'] == 'superintelligence_brief'

    class _P(Page):
        form_model = 'player'
        form_fields = item_ids
        template_name = 'sara/Page.html'

        def vars_for_template(player, ps=page, brief=is_brief):
            body_html = ""
            if brief:
                st = muskan.get(player.field_maybe_none('muskan_stim') or '')
                body_html = render.paragraphs(st['body_text']) if st else ""
            return dict(page_title=ps.get('title', ''),
                        body=render.page_body(ps, player, _SCALES, body_html))

        def is_displayed(player, ps=page):
            return _page_displayed(player, ps)

    _P.__name__ = _clsname(page['id'])
    return _P


def _make_dce_pages(page):
    pages = []
    for tn in range(1, NUM_DCE_TASKS + 1):
        class _D(Page):
            form_model = 'player'
            form_fields = ['dce_%d' % tn]
            template_name = 'sara/Page.html'

            def vars_for_template(player, n=tn):
                block = player.field_maybe_none('dce_block') or 1
                return dict(page_title="Discrete choice experiment",
                            body=render.dce_body(n, NUM_DCE_TASKS,
                                                 dce.get_task(block, n)))

            def is_displayed(player):
                return not _declined(player)

        _D.__name__ = 'DceTask%dPage' % tn
        pages.append(_D)
    return pages


# ── Build the page sequence ───────────────────────────────────────────
page_sequence = []
for _ps in _PAGES:
    if _ps.get('type') == 'dce':
        for _cls in _make_dce_pages(_ps):
            globals()[_cls.__name__] = _cls
            page_sequence.append(_cls)
    else:
        _cls = _make_content_page(_ps)
        globals()[_cls.__name__] = _cls
        page_sequence.append(_cls)
