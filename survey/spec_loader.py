"""Extract, parse, and validate the ```yaml fenced block from sara_usa.md.

sara_usa.md is the single source of truth: a Markdown document (prose and
commentary outside the fence, the exact YAML spec the pipeline reads inside
it). This loader is dependency-free beyond PyYAML so both the oTree app
(survey/sara/__init__.py) and the standalone review-table renderer
(render/review_fallback.py) can import it without pulling in oTree.

`validate_spec()` is the fail-loud guard: a research instrument must refuse
to run when the spec is inconsistent (an unknown scale name silently turning
a Likert DV into free text is exactly the failure mode this exists to stop).
The oTree app calls it at import time; CI calls it on every PR.
"""
import re

import yaml

_FENCE_RE = re.compile(r"```ya?ml\n(.*?)\n```", re.DOTALL)


def load_spec(md_path):
    with open(md_path, encoding="utf-8") as fh:
        text = fh.read()
    blocks = _FENCE_RE.findall(text)
    if not blocks:
        raise ValueError("No ```yaml fenced block found in %s — "
                         "the instrument must be a fenced code block." % md_path)
    if len(blocks) > 1:
        raise ValueError(
            "%d ```yaml fenced blocks found in %s — the instrument must be "
            "exactly one fence, or the loader can't tell which is the spec. "
            "Use a different language tag (e.g. ```yml-example) for examples "
            "in the prose." % (len(blocks), md_path))
    return yaml.safe_load(blocks[0])


# `condition:` values the oTree engine implements (survey/sara/__init__.py,
# _page_displayed). A condition the engine doesn't know would otherwise show
# the page to *everyone* — so an unknown one is a validation error, not a
# silent default.
KNOWN_CONDITIONS = frozenset([
    "info_arm",
    "att_failed",
    "muskan_not_control",
    "muskan_control",
    "muskan_one_sided",
])

# Widgets the engine can build a field for.
KNOWN_WIDGETS = frozenset(["radio", "select", "number"])


def validate_spec(spec, md_path="<spec>"):
    """Raise ValueError listing every structural problem in the spec.

    Checks: duplicate item/page ids, `scale:` names that don't exist,
    choice items with neither scale nor options (which would silently
    degrade to free text), unknown `widget:`/`condition:` values, and
    adaptive branch targets that point nowhere.
    """
    problems = []
    scales = spec.get("scales") or {}
    pages = spec.get("pages") or []

    page_ids, item_ids = [], []
    for page in pages:
        pid = page.get("id")
        if not pid:
            problems.append("a page has no id")
            continue
        page_ids.append(pid)

        cond = page.get("condition")
        if cond and cond not in KNOWN_CONDITIONS:
            problems.append(
                "page %r: unknown condition %r (engine knows: %s)"
                % (pid, cond, ", ".join(sorted(KNOWN_CONDITIONS))))

        items = page.get("items") or []
        for it in items:
            iid = it.get("id")
            if not iid:
                problems.append("page %r: an item has no id" % pid)
                continue
            item_ids.append(iid)

            widget = it.get("widget", "radio")
            if widget not in KNOWN_WIDGETS:
                problems.append("item %r: unknown widget %r" % (iid, widget))

            sc = it.get("scale")
            if sc and sc not in scales:
                problems.append(
                    "item %r: unknown scale %r (defined: %s)"
                    % (iid, sc, ", ".join(sorted(scales))))
            if widget != "number" and not sc and not it.get("options"):
                problems.append(
                    "item %r: no scale/options for a %s widget — it would "
                    "silently become a free-text field" % (iid, widget))

        if page.get("type") == "adaptive":
            by_id = {it.get("id") for it in items}
            root = page.get("root")
            if root not in by_id:
                problems.append(
                    "adaptive page %r: root %r is not one of its items"
                    % (pid, root))
            for it in items:
                for key in ("next_if_correct", "next_if_incorrect"):
                    target = it.get(key)
                    if target and target not in by_id \
                            and not str(target).startswith("quartile"):
                        problems.append(
                            "adaptive item %r: %s target %r is neither an "
                            "item nor a quartile_* outcome"
                            % (it.get("id"), key, target))

    for name, ids in (("page", page_ids), ("item", item_ids)):
        dupes = sorted({i for i in ids if ids.count(i) > 1})
        if dupes:
            problems.append("duplicate %s ids: %s" % (name, ", ".join(dupes)))

    if problems:
        raise ValueError(
            "Invalid instrument spec in %s:\n  - %s"
            % (md_path, "\n  - ".join(problems)))
    return spec


if __name__ == "__main__":
    # CLI for CI:  python3 spec_loader.py sara_usa.md [more.md ...]
    import sys
    paths = sys.argv[1:] or ["sara_usa.md"]
    for p in paths:
        spec = load_spec(p)
        if "pages" in spec:  # muskan_stimuli.md has no pages — parse-only
            validate_spec(spec, p)
        print("%s: OK" % p)
