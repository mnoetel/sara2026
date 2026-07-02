#!/usr/bin/env python3
"""
render/build_docs.py

Publish the protocol as a pretty, self-contained web page (docs/index.html,
served by GitHub Pages) so people who don't use GitHub can read it, with a
banner telling people who *do* use GitHub how to comment line-by-line.

The protocol Markdown stays the single source of truth: this script renders
"SARA USA — Survey Protocol v10.md" (whatever version glob-matches) to HTML
with the `markdown` package (already pinned in requirements.txt) and inlines
all CSS — no CDNs, no Jekyll, nothing to install for readers. Heading ids use
GitHub's slug rules so the doc's internal #section links keep working.

The output is deterministic, so it can be committed and drift-guarded the same
way as the protocol's auto-blocks:

Usage:
    python3 render/build_docs.py            # rewrite docs/index.html in place
    python3 render/build_docs.py --check    # exit 1 if docs/index.html is stale (CI/make)
"""

import glob
import html
import os
import re
import sys

try:
    import markdown
except ImportError:
    sys.exit("The 'markdown' package is required (it is pinned in "
             "requirements.txt): pip install markdown")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
OUT_DIR = os.path.join(REPO_ROOT, "docs")
OUT_HTML = os.path.join(OUT_DIR, "index.html")

GITHUB_REPO = "https://github.com/mnoetel/sara2026"
CONTACT_EMAIL = "noetel@gmail.com"


def find_protocol():
    """Version-proof: match the current protocol file whatever its vN."""
    matches = sorted(glob.glob(os.path.join(REPO_ROOT, "SARA USA*Protocol*.md")))
    if not matches:
        sys.exit("No protocol file matching 'SARA USA*Protocol*.md' found.")
    return matches[-1]


def gh_slug(value, separator="-"):
    """GitHub's heading-anchor algorithm (the doc's internal links assume it):
    lowercase, drop everything but word chars/spaces/hyphens, spaces->hyphens.
    Consecutive hyphens are kept (em-dashes in headings become '--')."""
    value = value.strip().lower()
    value = re.sub(r"[^\w\- ]", "", value, flags=re.UNICODE)
    return value.replace(" ", separator)


LIST_ITEM = r"([-*+]|\d{1,3}\.) "


def normalize_gfm_lists(md_text):
    """The protocol is written for GitHub's Markdown, which is looser than
    python-markdown in two ways that silently mangle the rendered page: a
    list may start on the line right after a paragraph (python-markdown
    needs a blank line first, else the items run on as paragraph text), and
    nested items may be indented two spaces (python-markdown needs four,
    and renders two-space nests as *siblings*). Normalise both so the page
    matches what reviewers see on GitHub."""
    out, prev, in_fence = [], "", False
    for line in md_text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
        elif not in_fence:
            if re.match(r"^ {1,3}" + LIST_ITEM, line):
                line = "    " + line.lstrip()
            elif (re.match(r"^" + LIST_ITEM, line) and prev.strip()
                  and not re.match(r"^ *" + LIST_ITEM, prev)
                  and not prev.lstrip().startswith(("#", ">", "|"))):
                out.append("")
        out.append(line)
        prev = line
    return "\n".join(out) + "\n"


def autolink_urls(md_text):
    """GitHub autolinks bare URLs (the protocol's citations rely on it);
    python-markdown leaves them as dead text. Wrap each bare URL in <...> so
    it renders as a link, trimming trailing prose punctuation and any close
    paren that isn't part of the URL (DOIs contain balanced parens)."""
    def repl(m):
        url = m.group(0)
        while True:
            if url[-1] in ".,;:!?'\"":
                url = url[:-1]
            elif url[-1] == ")" and url.count("(") < url.count(")"):
                url = url[:-1]
            else:
                break
        return "<" + url + ">" + m.group(0)[len(url):]

    return re.sub(r"(?<!<)(?<!\]\()(?<!=\")\bhttps?://[^\s<>]+", repl, md_text)


def render_body(md_text):
    md_text = autolink_urls(normalize_gfm_lists(md_text))
    # python-markdown treats a whole <details>…</details> span as one raw-HTML
    # block, which would leave the protocol's collapsible "as fielded" blocks
    # (and the tables inside them) as unrendered Markdown. md_in_html processes
    # the contents of any block tagged markdown="1", so inject that attribute.
    md_text = re.sub(r"<details>", '<details markdown="1">', md_text)
    md = markdown.Markdown(
        extensions=["tables", "footnotes", "toc", "md_in_html"],
        extension_configs={
            "toc": {"slugify": gh_slug, "toc_depth": "2-3"},
            "footnotes": {"BACKLINK_TITLE": "Back to text"},
        },
    )
    body = md.convert(md_text)
    return body, md.toc_tokens


FNREF_RE = re.compile(
    r'(<sup id="fnref\d*:([^"]+)"><a class="footnote-ref" '
    r'href="#fn:[^"]+">)(\d+)(</a></sup>)')


def renumber_footnotes(page):
    """The footnotes extension numbers notes by the order their *definitions*
    appear in the protocol, so the superscripts in the text jump around.
    Renumber by order of first reference, and reorder the end-of-page list to
    match (an <ol>, so each note's displayed number is its position).
    Footnotes defined but never referenced sink to the end, keeping their
    relative order (their dead backlinks are stripped separately)."""
    order = {}
    for m in FNREF_RE.finditer(page):
        order.setdefault(m.group(2), len(order) + 1)
    if not order:
        return page
    page = FNREF_RE.sub(
        lambda m: m.group(1) + str(order[m.group(2)]) + m.group(4), page)

    def reorder(m):
        chunks = re.split(r'(?=<li id="fn:)', m.group(2))
        head, items = chunks[0], chunks[1:]
        items.sort(key=lambda li: order.get(
            re.match(r'<li id="fn:([^"]+)"', li).group(1), len(order) + 1))
        return m.group(1) + head + "".join(items) + m.group(3)

    return re.sub(r'(<div class="footnote">.*?<ol>)(.*?)(</ol>)',
                  reorder, page, count=1, flags=re.S)


def separate_adjacent_fnrefs(page):
    """Back-to-back footnote references render as one run-on number
    (…catastrophe¹⁸¹⁹); put a superscript comma between them."""
    return page.replace('</sup><sup id="fnref',
                        '</sup><sup class="fn-sep">,</sup><sup id="fnref')


def drop_dead_backlinks(page):
    """Footnotes that are defined but never referenced in the text still get a
    '↩' backlink pointing at a #fnref: id that doesn't exist; strip those (and
    only those) so the published page has no dead links."""
    ids = set(re.findall(r'id="([^"]+)"', page))
    return re.sub(
        r'<a[^>]+href="#(fnref[^"]*)"[^>]*>.*?</a>',
        lambda m: "" if m.group(1) not in ids else m.group(0),
        page,
    )


def iter_h2(tokens):
    """The toc extension nests h2 tokens under the document's h1; flatten."""
    for tok in tokens:
        if tok["level"] == 2:
            yield tok
        else:
            yield from iter_h2(tok.get("children", []))


def build_nav(toc_tokens):
    """Sidebar TOC from the h2/h3 tokens the toc extension collected."""
    items = []
    for tok in iter_h2(toc_tokens):
        items.append('<li><a href="#{id}">{name}</a>'.format(
            id=tok["id"], name=html.escape(tok["name"])))
        subs = [t for t in tok.get("children", []) if t["level"] == 3]
        if subs:
            items.append("<ol>")
            items.extend('<li><a href="#{id}">{name}</a></li>'.format(
                id=t["id"], name=html.escape(t["name"])) for t in subs)
            items.append("</ol>")
        items.append("</li>")
    return "<ol>\n" + "\n".join(items) + "\n</ol>"


# The two audiences the page serves: readers who just want a pretty document,
# and reviewers who want line-by-line comments (which live on GitHub, next to
# the source Markdown — this page is a read-only rendering).
COMMENT_BANNER = """
<aside class="comment-box">
  <h2 id="how-to-comment">Reading vs. commenting</h2>
  <p><strong>Just reading?</strong> You are in the right place — this page is the
  full protocol, rendered from the project's source document. Use the contents
  list to jump around; click any <em>&ldquo;as fielded&rdquo;</em> box to expand the exact
  survey items.</p>
  <p><strong>Want to comment, line by line?</strong> The source of this page is a
  Markdown file in the project's GitHub repository, and GitHub is where review
  happens. With a free GitHub account:</p>
  <ol>
    <li>Open <a href="{source_url}">the source document on GitHub</a>.</li>
    <li>Click the <strong>pencil icon</strong> (&ldquo;Edit this file&rdquo;, top right of the
    file view). GitHub makes you a personal copy automatically.</li>
    <li>Type your suggested edits or add comments inline, then choose
    <strong>&ldquo;Commit changes&hellip;&rdquo; &rarr; &ldquo;Propose changes&rdquo; &rarr;
    &ldquo;Create pull request&rdquo;</strong>.</li>
    <li>That opens a review thread where every line can be discussed: in the
    pull request's <strong>Files changed</strong> tab, hover over a line and click the
    <strong>+</strong> to comment on exactly that line.</li>
  </ol>
  <p>Prefer to comment without editing? <a href="{issues_url}">Open an issue</a>
  and quote the section heading you are responding to. If GitHub shows you a
  404 (the repository may be private) or you would rather skip GitHub entirely,
  email <a href="mailto:{email}">{email}</a> — quoting section headings works
  just as well there.</p>
</aside>
"""

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
:root {{
  --bg: #fdfdfc; --fg: #1f2328; --muted: #59636e; --accent: #0a5cad;
  --border: #d1d9e0; --soft: #f6f8fa; --banner: #eef5fc; --banner-border: #b6d4f0;
  --mark-bg: #fff8c5;
}}
@media (prefers-color-scheme: dark) {{
  :root {{
    --bg: #14171b; --fg: #e6edf3; --muted: #9198a1; --accent: #6cb2f5;
    --border: #3d444d; --soft: #1c2128; --banner: #12283d; --banner-border: #24537d;
    --mark-bg: #4d3800;
  }}
}}
* {{ box-sizing: border-box; }}
html {{ scroll-behavior: smooth; scroll-padding-top: 1rem; }}
body {{
  margin: 0; background: var(--bg); color: var(--fg);
  font: 17px/1.65 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
        "Helvetica Neue", Arial, sans-serif;
  -webkit-text-size-adjust: 100%;
}}
.layout {{ display: grid; grid-template-columns: 19rem minmax(0, 46rem); gap: 3rem;
  max-width: 72rem; margin: 0 auto; padding: 0 1.25rem; }}
nav.toc {{ position: sticky; top: 0; align-self: start; max-height: 100vh;
  overflow-y: auto; padding: 2.5rem 0 2rem; font-size: .85rem; }}
nav.toc .toc-title {{ font-weight: 700; text-transform: uppercase;
  letter-spacing: .06em; font-size: .72rem; color: var(--muted); margin: 0 0 .6rem; }}
nav.toc ol {{ list-style: none; margin: 0; padding: 0; }}
nav.toc ol ol {{ padding-left: .9rem; border-left: 1px solid var(--border); margin: .15rem 0 .35rem; }}
nav.toc li {{ margin: .18rem 0; }}
nav.toc a {{ color: var(--muted); text-decoration: none; display: block;
  padding: .1rem .4rem; border-radius: 5px; }}
nav.toc a:hover {{ color: var(--accent); background: var(--soft); }}
main {{ padding: 2.5rem 0 5rem; }}
h1 {{ font-size: 1.9rem; line-height: 1.25; margin: 0 0 .4rem; letter-spacing: -.01em; }}
h2 {{ font-size: 1.4rem; margin: 2.6em 0 .6em; padding-top: .6em;
  border-top: 1px solid var(--border); letter-spacing: -.01em; }}
h3 {{ font-size: 1.12rem; margin: 2em 0 .5em; }}
h2 a.hl, h3 a.hl {{ color: inherit; text-decoration: none; }}
a {{ color: var(--accent); }}
p, ul, ol {{ margin: 0 0 1em; }}
li {{ margin: .25em 0; }}
blockquote {{ margin: 1.2em 0; padding: .1em 1.1em; border-left: 4px solid var(--border);
  color: var(--muted); background: var(--soft); border-radius: 0 8px 8px 0; }}
code {{ font: .85em/1.4 ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
  background: var(--soft); border: 1px solid var(--border);
  border-radius: 5px; padding: .1em .35em; }}
table {{ border-collapse: collapse; margin: 1.2em 0; width: 100%;
  font-size: .92rem; display: block; overflow-x: auto; }}
th, td {{ border: 1px solid var(--border); padding: .5em .8em;
  text-align: left; vertical-align: top; }}
th {{ background: var(--soft); }}
tr:nth-child(2n) td {{ background: var(--soft); }}
hr {{ border: none; border-top: 1px solid var(--border); margin: 2.5em 0; }}
details {{ background: var(--soft); border: 1px solid var(--border);
  border-radius: 10px; padding: .7rem 1rem; margin: 1.2em 0; }}
details[open] {{ padding-bottom: .9rem; }}
details > summary {{ cursor: pointer; font-weight: 600; color: var(--accent); }}
details > :last-child {{ margin-bottom: 0; }}
.subtitle {{ color: var(--muted); margin: 0 0 1.6rem; }}
aside.comment-box {{ background: var(--banner); border: 1px solid var(--banner-border);
  border-radius: 12px; padding: 1.1rem 1.4rem; margin: 1.8rem 0 2.4rem;
  font-size: .95rem; }}
aside.comment-box h2 {{ border: none; margin: 0 0 .5em; padding: 0; font-size: 1.15rem; }}
.footnote {{ font-size: .88rem; color: var(--muted); }}
.footnote hr {{ margin: 3em 0 1em; }}
.footnote-ref {{ text-decoration: none; font-weight: 600; }}
.fn-sep {{ color: var(--muted); }}
#fn-preview {{ position: absolute; z-index: 10; max-width: 26rem;
  background: var(--bg); border: 1px solid var(--border); border-radius: 10px;
  padding: .7rem .9rem; box-shadow: 0 6px 24px rgba(0, 0, 0, .18);
  font-size: .85rem; line-height: 1.5; overflow-wrap: break-word; }}
#fn-preview > :last-child {{ margin-bottom: 0; }}
:target {{ animation: flash 1.6s ease-out 1; }}
@keyframes flash {{ from {{ background: var(--mark-bg); }} to {{ background: transparent; }} }}
footer {{ margin-top: 4rem; padding-top: 1rem; border-top: 1px solid var(--border);
  color: var(--muted); font-size: .85rem; }}
@media (max-width: 63rem) {{
  .layout {{ display: block; }}
  nav.toc {{ position: static; max-height: none; padding: 1.5rem 0 0; }}
  nav.toc .toc-title {{ display: none; }}
  nav.toc > details {{ margin: 0; }}
  main {{ padding-top: 1.5rem; }}
}}
@media (min-width: 63.01rem) {{
  nav.toc > details {{ background: none; border: none; padding: 0; margin: 0; }}
  nav.toc > details > summary {{ display: none; }}
}}
</style>
</head>
<body>
<div class="layout">
<nav class="toc" aria-label="Table of contents">
<p class="toc-title">Contents</p>
<details open>
<summary>Contents</summary>
{nav}
<ol><li><a href="#how-to-comment">How to comment on this document</a></li></ol>
</details>
</nav>
<main>
{body}
<footer>
<p>Rendered from <a href="{source_url}">the source document</a> in
<a href="{repo_url}">{repo_name}</a> by <code>render/build_docs.py</code>.
To suggest changes, see <a href="#how-to-comment">how to comment</a>.</p>
</footer>
</main>
</div>
<script>
// Ship the TOC expanded (so it works without JS on desktop, where the summary
// is hidden); on narrow screens collapse it into a tap-to-open "Contents" box.
// Track the media query rather than checking once — the window may be resized
// (or start small) after load.
(function () {{
  var toc = document.querySelector("nav.toc > details");
  var mq = window.matchMedia("(max-width: 63rem)");
  function sync() {{
    if (mq.matches) toc.removeAttribute("open");
    else toc.setAttribute("open", "");
  }}
  if (mq.addEventListener) mq.addEventListener("change", sync);
  sync();
}})();
// Footnote previews: hovering a superscript shows the note in a popup, so
// readers don't lose their place jumping to the bottom of the page. Clicking
// still navigates (the only behaviour on touch devices, which can't hover).
(function () {{
  var pop = null, hideTimer = null;
  function hide() {{ if (pop) {{ pop.remove(); pop = null; }} }}
  function scheduleHide() {{ hideTimer = setTimeout(hide, 300); }}
  function cancelHide() {{ clearTimeout(hideTimer); }}
  document.addEventListener("mouseover", function (e) {{
    var ref = e.target.closest && e.target.closest("a.footnote-ref");
    if (!ref) return;
    cancelHide();
    var note = document.getElementById(ref.getAttribute("href").slice(1));
    if (!note) return;
    hide();
    pop = document.createElement("div");
    pop.id = "fn-preview";
    pop.innerHTML = note.innerHTML;
    pop.querySelectorAll(".footnote-backref").forEach(function (a) {{ a.remove(); }});
    // Keep the popup open while the pointer is inside it (its links are live).
    pop.addEventListener("mouseenter", cancelHide);
    pop.addEventListener("mouseleave", scheduleHide);
    document.body.appendChild(pop);
    var r = ref.getBoundingClientRect();
    var pad = 8;
    var left = window.scrollX + r.left + r.width / 2 - pop.offsetWidth / 2;
    var maxLeft = window.scrollX + document.documentElement.clientWidth
                  - pop.offsetWidth - pad;
    left = Math.max(window.scrollX + pad, Math.min(left, maxLeft));
    var top = window.scrollY + r.bottom + pad;
    if (r.bottom + pop.offsetHeight + 2 * pad > window.innerHeight &&
        r.top - pop.offsetHeight - pad > 0)
      top = window.scrollY + r.top - pop.offsetHeight - pad;
    pop.style.left = left + "px";
    pop.style.top = top + "px";
  }});
  document.addEventListener("mouseout", function (e) {{
    if (e.target.closest && e.target.closest("a.footnote-ref")) scheduleHide();
  }});
}})();
</script>
</body>
</html>
"""


def build():
    protocol_path = find_protocol()
    with open(protocol_path, encoding="utf-8") as f:
        md_text = f.read()

    body, toc_tokens = render_body(md_text)

    # The H1 becomes the <title>.
    m = re.search(r"<h1[^>]*>(.*?)</h1>", body, re.S)
    title = re.sub(r"<[^>]+>", "", m.group(1)) if m else "SARA USA Survey Protocol"

    source_url = GITHUB_REPO + "/blob/main/" + \
        os.path.basename(protocol_path).replace(" ", "%20")
    banner = COMMENT_BANNER.format(
        source_url=source_url,
        issues_url=GITHUB_REPO + "/issues/new",
        email=CONTACT_EMAIL,
    )

    # Slot the banner in right after the H1 and its bold subtitle line (if the
    # next element is one), so the page still opens with the document's title.
    m = re.search(r"</h1>\s*(?:<p><strong>.*?</strong></p>)?", body, re.S)
    if m:
        body = body[:m.end()] + "\n" + banner + body[m.end():]
    else:
        body = banner + body

    page = PAGE_TEMPLATE.format(
        title=html.escape(title),
        nav=build_nav(toc_tokens),
        body=body,
        source_url=source_url,
        repo_url=GITHUB_REPO,
        repo_name=GITHUB_REPO.rsplit("/", 1)[-1],
    )
    return drop_dead_backlinks(separate_adjacent_fnrefs(renumber_footnotes(page)))


def main():
    check = "--check" in sys.argv[1:]
    page = build()

    os.makedirs(OUT_DIR, exist_ok=True)
    nojekyll = os.path.join(OUT_DIR, ".nojekyll")

    current = None
    if os.path.exists(OUT_HTML):
        with open(OUT_HTML, encoding="utf-8") as f:
            current = f.read()

    if check:
        stale = []
        if current != page:
            stale.append("docs/index.html")
        if not os.path.exists(nojekyll):
            stale.append("docs/.nojekyll")
        if stale:
            sys.exit("Stale: %s — run `make -C render docs` (or "
                     "`python3 render/build_docs.py`) and commit."
                     % ", ".join(stale))
        print("docs/index.html is in sync with the protocol.")
        return

    if current == page:
        print("docs/index.html already up to date.")
    else:
        with open(OUT_HTML, "w", encoding="utf-8") as f:
            f.write(page)
        print("Wrote docs/index.html.")
    if not os.path.exists(nojekyll):
        open(nojekyll, "w").close()
        print("Wrote docs/.nojekyll.")


if __name__ == "__main__":
    main()
