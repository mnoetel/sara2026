"""
SARA USA 2026 oTree app.

All item text, response scales, page order, rationale, and triangulation are
defined in survey/sara_usa.md — the single source of truth (a Markdown doc
wrapping the YAML spec, so it can be edited/reviewed in HackMD, Google Docs,
or GitHub). This file reads it at class-definition time, validates it (fail loudly at
import rather than degrade silently at render), and builds the Player fields
and Page classes from it. It also wires the features the content needs but
plain items cannot express: between-subjects randomisation arms
(information-provision half, DCE block, Muskan briefing — assigned balanced,
see creating_session), per-participant page ordering (random_group), the
consent gate, the attention-check screen-out, the DCE (expanded into one page
per task from sara_dce_design.R's output), and Muskan's 3x3
superintelligence-briefing module. No item content is duplicated here — see
sara_usa.md.
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
from spec_loader import load_spec, validate_spec  # noqa: E402

_MD_PATH = os.path.join(os.path.dirname(__file__), '..', 'sara_usa.md')
SPEC = validate_spec(load_spec(_MD_PATH), _MD_PATH)

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
# The screen-out gate is the page marked `condition: att_failed` in the spec;
# every page after it is hidden for a screened-out participant.
_SCREENOUT_POS = next(
    (i for i, p in enumerate(_PAGES) if p.get('condition') == 'att_failed'), None)


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
    if not labels:
        # validate_spec catches this first; keep the belt-and-braces guard so
        # a choice item can never silently degrade to a free-text field.
        raise ValueError("item %r: no scale/options to build choices from"
                         % item['id'])
    choices = list(zip(range(1, len(labels) + 1), labels))
    w = None if widget == 'select' else widgets.RadioSelect()
    kw = dict(label=label, choices=choices, blank=not required)
    if w is not None:
        kw['widget'] = w
    return db.IntegerField(**kw)


# ── Constants / models ────────────────────────────────────────────────
class C(BaseConstants):
    NAME_IN_URL = 'sara'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


def _balanced(rng, pool, n):
    """n assignments drawn from pool in balanced blocks: the pool is repeated
    whole (shuffled anew each repeat) so counts never differ by more than one.
    Independent per-participant draws leave cell sizes binomially imbalanced;
    blocked assignment is the standard for between-subjects arms."""
    out = []
    while len(out) < n:
        block = list(pool)
        rng.shuffle(block)
        out.extend(block)
    return out[:n]


def creating_session(subsession):
    players = subsession.get_players()
    # Seeded on the session code so re-creating the session reproduces the
    # assignment; balanced within the session across every arm.
    rng = random.Random(subsession.session.code)
    info_arms = _balanced(rng, [True, False], len(players))
    stimuli = _balanced(rng, muskan.STIMULI, len(players))
    dce_blocks = _balanced(rng, range(1, dce.N_BLOCKS + 1), len(players))
    for p, arm, st, blk in zip(players, info_arms, stimuli, dce_blocks):
        p.info_arm = arm
        p.dce_block = blk
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
    cond = page.get('condition')
    # consent gate: declining shows ONLY the page marked `condition: declined`
    # (the no-consent close-out). The debrief (`end`) is hidden too — it
    # debriefs briefings a decliner never saw (issue #30).
    if cond == 'declined':
        return _declined(player)
    if _declined(player) and pid != 'consent':
        return False
    # attention-check screen-out: both checks wrong -> show the page marked
    # `condition: att_failed` and hide every page after it (they are
    # redirected to Prolific).
    failed = _att_failed(player)
    if cond == 'att_failed':
        return failed
    if failed and _SCREENOUT_POS is not None and _PAGE_IDS.index(pid) > _SCREENOUT_POS:
        return False
    if cond is None:
        return True
    if cond == 'info_arm':
        return bool(player.field_maybe_none('info_arm'))
    if cond == 'wtp_zero':
        # Protest-zero probe: only for respondents who answered "$0" (the
        # first option) on the willingness-to-pay item.
        return player.field_maybe_none('m5_wtp') == 1
    if cond == 'muskan_not_control':
        return not muskan.is_control(player.field_maybe_none('muskan_stim') or '')
    if cond == 'muskan_control':
        return muskan.is_control(player.field_maybe_none('muskan_stim') or '')
    if cond == 'muskan_one_sided':
        return muskan.is_one_sided(player.field_maybe_none('muskan_stim') or '')
    # validate_spec rejects unknown conditions at import; never show a
    # conditioned page to everyone because of a typo.
    raise ValueError("page %r: unknown condition %r" % (pid, cond))


def _clsname(pid):
    return ''.join(w.capitalize() for w in pid.split('_')) + 'Page'


# ── Page factories (ordn/total passed for the progress bar) ───────────
def _make_content_page(page, ordn, total):
    item_ids = [it['id'] for it in page.get('items', [])]
    is_brief = page['id'] == 'superintelligence_brief'
    is_consent = page['id'] == 'consent'

    class _P(Page):
        form_model = 'player'
        form_fields = item_ids
        template_name = 'sara/Page.html'

        def vars_for_template(player, ps=page, brief=is_brief, consent=is_consent,
                              ordn=ordn, total=total):
            body_html = ""
            if brief:
                st = muskan.get(player.field_maybe_none('muskan_stim') or '')
                body_html = render.paragraphs(st['body_text']) if st else ""
            elif consent:
                # The spec `body:` is a short lead-in; the full canonical
                # Participant Information Sheet is pulled in from the ethics doc.
                body_html = (ps.get('body') or '') + render.information_sheet_html()
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
    Every participant sees every item exactly once; fields save normally.

    Items flagged `last:` are forced after every un-flagged item: the whole
    group is shuffled, then a stable sort drops the flagged items to the
    tail. `last` may be `true` (== 1) or a number; flagged items are ordered
    by that number, with the shuffled order preserved within ties. Used so
    the disguised attention checks (`last: true`) always trail the real
    comparators, and the differently-stemmed sanity anchor (`last: 2`)
    trails the attention checks in turn."""
    gid = page['id']
    items = page.get('items', [])
    n = len(items)

    def _order(player):
        r = random.Random('%s|%s' % (player.participant.code, gid))
        idx = list(range(n))
        r.shuffle(idx)
        # Stable sort: un-flagged first (key 0), then `last` items by their
        # number (true == 1); shuffled order preserved within ties.
        idx.sort(key=lambda i: int(items[i].get('last') or 0))
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


def _adaptive_max_depth(page):
    """Longest possible path (number of items shown) through a `type: adaptive`
    branch tree, so the engine can reserve that many slot pages. Walks the tree
    from `root`, following each item's next_if_correct / next_if_incorrect; a
    target that isn't another item (e.g. a `quartile_*` scoring outcome) ends
    that branch."""
    by_id = {it['id']: it for it in page.get('items', [])}

    def depth(node, seen):
        if node not in by_id or node in seen:
            return 0
        it = by_id[node]
        seen = seen | {node}
        return 1 + max(depth(it.get('next_if_correct'), seen),
                       depth(it.get('next_if_incorrect'), seen))

    return depth(page['root'], frozenset())


def _adaptive_path(player, page):
    """The ordered list of items this participant is routed through so far.
    Walks the branch tree from `root`, and at each answered item follows
    next_if_correct or next_if_incorrect depending on whether the recorded
    answer equals the item's correct_answer. Stops at the first unanswered item
    (the one to show now) or when a branch ends at a non-item target."""
    by_id = {it['id']: it for it in page.get('items', [])}
    path = []
    cur = page['root']
    while cur in by_id:
        it = by_id[cur]
        path.append(it)
        ans = player.field_maybe_none(it['id'])
        if ans is None:
            break
        cur = it['next_if_correct'] if ans == it.get('correct_answer') \
            else it['next_if_incorrect']
    return path


def _make_adaptive_page(page, slot, ordn, total):
    """One page per position (slot) on the longest branch of a `type: adaptive`
    page. The item shown at slot s is the s-th item on the participant's routed
    path (see _adaptive_path); the page is hidden once the path is shorter than
    s+1 (their branch terminated earlier)."""
    class _A(Page):
        form_model = 'player'
        template_name = 'sara/Page.html'

        def get_form_fields(player, ps=page, slot=slot):
            path = _adaptive_path(player, ps)
            return [path[slot]['id']] if len(path) > slot else []

        def vars_for_template(player, ps=page, slot=slot, ordn=ordn, total=total):
            it = _adaptive_path(player, ps)[slot]
            single = dict(ps)
            single['items'] = [it]
            return dict(page_title=ps.get('title', ''),
                        page_index=ordn, page_total=total,
                        body=render.page_body(single, player, _SCALES))

        def is_displayed(player, ps=page, slot=slot):
            return _page_displayed(player, ps) and len(_adaptive_path(player, ps)) > slot

    _A.__name__ = _clsname('%s_slot%d' % (page['id'], slot + 1))
    return _A


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
    elif _ps.get('type') == 'adaptive':
        for _si in range(_adaptive_max_depth(_ps)):
            _units.append(('adaptive', _ps, _si))
    else:
        _units.append(('content', _ps, None))
_TOTAL = len(_units)

page_sequence = []
for _ordn, (_kind, _ps, _arg) in enumerate(_units, 1):
    if _kind == 'dce':
        _cls = _make_dce_page(_ps, _arg, _ordn, _TOTAL)
    elif _kind == 'rgroup':
        _cls = _make_rgroup_page(_ps, _arg, _ordn, _TOTAL)
    elif _kind == 'adaptive':
        _cls = _make_adaptive_page(_ps, _arg, _ordn, _TOTAL)
    else:
        _cls = _make_content_page(_ps, _ordn, _TOTAL)
    globals()[_cls.__name__] = _cls
    page_sequence.append(_cls)
