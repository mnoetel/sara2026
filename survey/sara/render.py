"""Server-side HTML rendering for the SARA survey pages.

The engine (``__init__.py``) builds one oTree page per YAML page; this module
turns a YAML page (+ the player's randomised arms) into the HTML body. Inputs
are rendered manually so question text can be personalised per participant
(comparator / sanity activity) and so the DCE and Muskan briefing can be drawn
from generated data — things oTree's fixed-label ``{{ formfields }}`` can't do.
Submitted ``name=<item_id> value=<1-based index>`` matches each item's oTree
IntegerField(choices=...), so answers still save the normal way.
"""
import html
import random

# default arm values (used before creating_session / in admin previews)
_DEF_COMPARATOR = "nuclear power"
_DEF_SANITY = "Climbing Mount Everest kills roughly 1 in 100 people who attempt the summit"


def esc(s):
    return html.escape(str(s), quote=True)


def substitute(text, player):
    text = text.replace("{comparator}",
                        player.field_maybe_none("comparator") or _DEF_COMPARATOR)
    text = text.replace("{sanity}",
                        player.field_maybe_none("sanity_phrase") or _DEF_SANITY)
    return text


def _options_for(item, scales):
    if item.get("options"):
        return item["options"]
    sc = item.get("scale")
    if sc and sc in scales:
        return scales[sc]["labels"]
    return None


def _numbered_options(item, scales, player=None):
    """(value, label) pairs where value is the option's ORIGINAL 1-based index
    (so the saved answer maps to the same option regardless of display order).
    If the item sets ``shuffle_options: true``, the display order is shuffled
    per-participant (seeded on participant.code + item id) so it's stable across
    re-renders but the correct answer isn't always in a fixed position."""
    pairs = list(enumerate(_options_for(item, scales) or [], 1))
    if item.get("shuffle_options") and player is not None:
        code = getattr(getattr(player, "participant", None), "code", None)
        if code:
            random.Random("%s|%s" % (code, item["id"])).shuffle(pairs)
    return pairs


def input_html(item, scales, player=None):
    iid = item["id"]
    widget = item.get("widget", "radio")
    if widget == "number":
        return ('<input type="number" inputmode="numeric" class="sara-num" '
                'name="%s" id="id_%s">' % (iid, iid))
    pairs = _numbered_options(item, scales, player)
    if widget == "select":
        out = ['<select class="sara-select" name="%s" id="id_%s">'
               '<option value="">— select —</option>' % (iid, iid)]
        for i, o in pairs:
            out.append('<option value="%d">%s</option>' % (i, esc(o)))
        out.append("</select>")
        return "".join(out)
    # radio (default)
    out = ['<div class="sara-opts">']
    for i, o in pairs:
        out.append('<label class="sara-opt"><input type="radio" name="%s" value="%d">'
                   '<span>%s</span></label>' % (iid, i, esc(o)))
    out.append("</div>")
    return "".join(out)


def _info_bits(rationale):
    """Return (info-button html, inline-note html) for a rationale string."""
    rationale = (rationale or "").strip()
    if not rationale:
        return "", ""
    info = ('<span class="sara-info" tabindex="0" data-tip="%s" '
            'title="Why this question is designed this way">i</span>' % esc(rationale))
    note = '<div class="sara-rat"><b>Why this is designed this way.</b> %s</div>' % esc(rationale)
    return info, note


def item_block(item, player, scales):
    text = substitute(item["text"].strip(), player)
    info, note = _info_bits(item.get("rationale"))
    return ('<div class="sara-item"><div class="sara-qhead">'
            '<p class="sara-q">%s</p>%s</div>%s%s</div>'
            % (text, info, input_html(item, scales, player), note))


def page_body(page, player, scales, body_html=""):
    parts = []
    note = page.get("note")
    if note:
        parts.append('<div class="alert alert-info">%s</div>' % esc(note.strip()))
    body = body_html or page.get("body")
    if body:
        parts.append('<div class="sara-readbox">%s</div>' % body)
    for item in page.get("items", []):
        parts.append(item_block(item, player, scales))
    return "".join(parts)


# ── DCE ──────────────────────────────────────────────────────────────
_DCE_ROWS = [
    ("Worst catastrophe it could cause", "a_severity", "b_severity"),
    ("Annual chance of that catastrophe", "a_risk_annual", "b_risk_annual"),
    ("What AI delivers for society", "a_benefit", "b_benefit"),
    ("Global position", "a_competition", "b_competition"),
]

# Plain-language definitions of the "benefit" levels, shown once under each
# choice table so the short in-cell labels are unambiguous.
_BENEFIT_LEGEND = [
    ("Modest", "AI stays roughly as capable as it is today. It becomes more "
               "reliable and makes fewer mistakes, so it gets used more widely"),
    ("Major", "AI clearly improves daily life: better, cheaper health care, "
              "lower prices, and more time for what people care about"),
    ("Transformative", "AI cures most major diseases. It also makes life's "
                       "essentials cheap and plentiful, so almost everyone "
                       "is far better off"),
]


def dce_body(task_num, total, t, rationale=""):
    rows = "".join(
        '<tr><th>%s</th><td>%s</td><td>%s</td></tr>'
        % (esc(lbl), esc(t.get(ka, "—")), esc(t.get(kb, "—")))
        for lbl, ka, kb in _DCE_ROWS)
    legend = '<dl class="sara-dce-legend">%s</dl>' % "".join(
        '<div><dt>%s</dt><dd>%s</dd></div>' % (esc(name), esc(desc))
        for name, desc in _BENEFIT_LEGEND)
    field = "dce_%d" % task_num
    radios = "".join(
        '<label class="sara-opt"><input type="radio" name="%s" value="%d"><span>%s</span></label>'
        % (field, i, lbl)
        for i, lbl in [(1, "Option A"), (2, "Option B"),
                       (3, "Neither — keep today's status quo")])
    info, note = _info_bits(rationale)
    return (
        '<div class="sara-item"><div class="sara-qhead">'
        '<p class="sara-q">Here are two possible futures for advanced AI in the US, '
        'plus the option to keep things as they are. Which do you prefer? '
        '(Task %d of %d)</p>%s</div>'
        '<table class="sara-dce"><tr><th></th><th>Option A</th><th>Option B</th></tr>'
        '%s</table>%s<div class="sara-opts">%s</div>%s</div>'
        % (task_num, total, info, rows, legend, radios, note))


def paragraphs(text):
    """Turn a plain passage with blank-line breaks into <p> HTML."""
    return "".join("<p>%s</p>" % esc(p.strip())
                   for p in str(text).split("\n\n") if p.strip())
