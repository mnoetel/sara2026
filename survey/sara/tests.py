"""Bots for the SARA survey — run:  otree test sara_usa 27

(27 = one participant per Muskan stimulus, so every cell — including the
control-only comprehension page — gets walked.)
"""
from otree.api import Bot, Submission, expect

from . import (
    _ATT_IDS,
    _ATT_REQUIRED,
    _PAGES,
    _SCALES,
    muskan,
    page_sequence,
)

_ITEMS_BY_ID = {it['id']: it
                for p in _PAGES for it in (p.get('items') or [])}


def _n_labels(item):
    if item.get('options'):
        return len(item['options'])
    sc = item.get('scale')
    return len(_SCALES[sc]['labels']) if sc in _SCALES else 0


class PlayerBot(Bot):
    """Walks the full survey, rendering every page (the submit machinery's
    HTML check catches template/render crashes, not just model errors).
    Answers vary by participant id so adaptive branches and option positions
    get exercised. Two participants take the failure paths instead: the first
    two NON-control participants (by id) play consent-decline and the
    attention-check screen-out — chosen from the assignment so the
    control-cell-only pages are still fully walked whenever the session is
    big enough to cover all stimuli (27+ participants)."""

    def play_round(self):
        mode = self._mode()
        me = self.player.id_in_subsession
        wrong_att = 2 if _ATT_REQUIRED == 1 else 1
        for cls in page_sequence:
            if not cls.is_displayed(self.player):
                continue
            if 'get_form_fields' in cls.__dict__:  # rgroup / adaptive slots
                fields = cls.__dict__['get_form_fields'](self.player)
            else:
                fields = list(cls.form_fields)
            values = {}
            for f in fields:
                item = _ITEMS_BY_ID.get(f)
                if f == 'consent':
                    values[f] = 2 if mode == 'decline' else 1
                elif f in _ATT_IDS:
                    values[f] = wrong_att if mode == 'screenout' else _ATT_REQUIRED
                elif f.startswith('dce_'):
                    values[f] = 1 + (me % 3)
                elif item and item.get('widget') == 'number':
                    values[f] = 10
                else:
                    values[f] = 1 + (me % max(_n_labels(item) if item else 1, 1))
            yield Submission(cls, values)
        if mode == 'consent':
            # Regression guard: the primary Muskan DV must have been asked
            # and answered on every completed walk.
            expect(self.player.field_maybe_none('muskan_support'), '!=', None)
        else:
            expect(self.player.field_maybe_none('muskan_support'), None)

    def _mode(self):
        non_control = [p.id_in_subsession
                       for p in self.player.subsession.get_players()
                       if not muskan.is_control(
                           p.field_maybe_none('muskan_stim') or '')]
        me = self.player.id_in_subsession
        if len(non_control) > 2:  # keep at least one full walk in tiny sessions
            if me == non_control[0]:
                return 'decline'
            if me == non_control[1]:
                return 'screenout'
        return 'consent'
