"""Extract and parse the ```yaml fenced block from sara_usa.md.

sara_usa.md is the single source of truth: a Markdown document (so it can be
edited collaboratively in HackMD / Google Docs / GitHub, with comments and
prose living outside the fence) wrapping the exact YAML spec the pipeline
reads. This loader is dependency-free beyond PyYAML so both the oTree app
(survey/sara/__init__.py) and the standalone review-table renderer
(render/review_fallback.py) can import it without pulling in oTree.
"""
import re

import yaml

_FENCE_RE = re.compile(r"```ya?ml\n(.*?)\n```", re.DOTALL)


def load_spec(md_path):
    text = open(md_path, encoding="utf-8").read()
    m = _FENCE_RE.search(text)
    if not m:
        raise ValueError("No ```yaml fenced block found in %s — "
                         "the instrument must be a fenced code block." % md_path)
    return yaml.safe_load(m.group(1))
