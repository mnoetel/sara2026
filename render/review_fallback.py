#!/usr/bin/env python3
"""
render/review_fallback.py

Reads survey/sara_usa.md (the single source of truth — a Markdown doc
wrapping the survey YAML) and produces render/review.html as a
self-contained, standalone HTML file with a sortable, searchable,
grouped review table.

This is the Python fallback for environments without R/reactable.
The output is functionally equivalent to the R version.

Usage:
    python3 render/review_fallback.py
"""

import json
import os
import sys
import html as html_lib

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, "..", "survey"))
try:
    from spec_loader import load_spec
except ImportError:
    sys.exit("PyYAML is required: pip install pyyaml")

MD_PATH = os.path.join(SCRIPT_DIR, "..", "survey", "sara_usa.md")
OUT_PATH = os.path.join(SCRIPT_DIR, "review.html")


def main():
    spec = load_spec(MD_PATH)

    scales = spec["scales"]
    pages = spec["pages"]

    # ── Build rows ───────────────────────────────────────────────────
    rows = []
    order = 0
    for page in pages:
        items = page.get("items", [])
        if not items:
            continue
        for item in items:
            order += 1
            scale_name = item.get("scale")
            if scale_name and scale_name in scales:
                scale_text = " / ".join(scales[scale_name]["labels"])
            elif item.get("options"):
                scale_text = " / ".join(item["options"])
            elif item.get("widget") == "number":
                scale_text = "(numeric entry)"
            else:
                scale_text = ""

            tri = item.get("triangulates", [])
            tri_text = ", ".join(tri) if tri else ""

            rows.append(
                {
                    "page": page["title"],
                    "order": order,
                    "id": item["id"],
                    "item": item["text"].strip(),
                    "scale": scale_text,
                    "rationale": (item.get("rationale") or "").strip(),
                    "triangulates": tri_text,
                }
            )

    # ── Validate: check for dangling scale references ────────────────
    for page in pages:
        for item in page.get("items", []):
            s = item.get("scale")
            if s and s not in scales:
                print(f"WARNING: dangling scale reference: {item['id']} -> {s}", file=sys.stderr)

    # ── Generate HTML ────────────────────────────────────────────────
    esc = html_lib.escape
    table_data_json = json.dumps(rows, ensure_ascii=False)
    version = esc(spec["meta"]["version"])
    n_items = len(rows)
    n_pages = len(set(r["page"] for r in rows))

    # ── Dumpster panel (items considered and cut) ────────────────────
    dumpster = spec.get("dumpster", [])
    if dumpster:
        d_rows = "".join(
            '<tr><td class="wrap"><b>{}</b></td><td class="wrap">{}</td></tr>'.format(
                esc(d.get("name", "")), esc((d.get("reason") or "").strip()))
            for d in dumpster)
        dumpster_html = (
            '<h2 class="dump-h">Dumpster <span class="count">({} cut)</span></h2>'
            '<p class="subtitle">Items and modules considered and deliberately not fielded.</p>'
            '<table class="dumpster"><thead><tr><th>Item / module</th><th>Why cut</th></tr>'
            '</thead><tbody>{}</tbody></table>'.format(len(dumpster), d_rows))
    else:
        dumpster_html = ""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>SARA USA 2026 -- Item Review Table</title>
<style>
  :root {{ --accent: #2e5496; --bg: #f8f9fb; --card: #fff; --ink: #1c2733;
           --muted: #647281; --line: #e2e6eb; }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif;
          background: var(--bg); color: var(--ink); padding: 24px; line-height: 1.5; }}
  h1 {{ color: var(--accent); font-size: 22px; margin-bottom: 4px; }}
  .subtitle {{ color: var(--muted); font-size: 14px; margin-bottom: 16px; }}
  .controls {{ display: flex; gap: 12px; align-items: center; margin-bottom: 14px;
               flex-wrap: wrap; }}
  .search {{ padding: 8px 12px; border: 1.5px solid var(--line); border-radius: 8px;
             font: inherit; width: 280px; }}
  .search:focus {{ outline: none; border-color: var(--accent); }}
  .group-toggle {{ font: inherit; padding: 6px 14px; border: 1.5px solid var(--accent);
                   border-radius: 8px; background: var(--card); color: var(--accent);
                   cursor: pointer; font-size: 13px; }}
  .group-toggle:hover {{ background: var(--accent); color: #fff; }}
  table {{ width: 100%; border-collapse: collapse; background: var(--card);
           border-radius: 10px; overflow: hidden; box-shadow: 0 1px 6px rgba(0,0,0,.06); }}
  th {{ background: var(--accent); color: #fff; font-weight: 700; font-size: 13px;
        padding: 10px 12px; text-align: left; cursor: pointer; user-select: none;
        position: sticky; top: 0; z-index: 2; white-space: nowrap; }}
  th:hover {{ background: #1f3864; }}
  th .arrow {{ font-size: 10px; margin-left: 4px; opacity: .5; }}
  th.sorted .arrow {{ opacity: 1; }}
  td {{ padding: 8px 12px; border-bottom: 1px solid var(--line); vertical-align: top;
        font-size: 14px; }}
  td.wrap {{ white-space: normal; word-wrap: break-word; }}
  td.mono {{ font-family: ui-monospace, Menlo, monospace; font-size: 12px; }}
  tr:hover td {{ background: #f0f4fa; }}
  tr.group-header td {{ background: #eaf0fa; font-weight: 700; color: var(--accent);
                        font-size: 14px; cursor: pointer; user-select: none; }}
  tr.group-header td:first-child::before {{ content: "\\25BC "; font-size: 10px; }}
  tr.group-header.collapsed td:first-child::before {{ content: "\\25B6 "; }}
  tr.hidden {{ display: none; }}
  .count {{ color: var(--muted); font-weight: 400; font-size: 12px; margin-left: 8px; }}
  col.c-order {{ width: 55px; }} col.c-id {{ width: 130px; }}
  col.c-item {{ width: 28%; }} col.c-scale {{ width: 22%; }}
  col.c-rationale {{ width: 25%; }} col.c-tri {{ width: 140px; }}
  .dump-h {{ color: var(--muted); font-size: 18px; margin: 30px 0 2px; }}
  table.dumpster {{ margin-top: 6px; }}
  table.dumpster th {{ position: static; cursor: default; background: var(--muted); }}
  table.dumpster td:first-child {{ width: 34%; }}
</style>
</head>
<body>
<h1>SARA USA 2026 -- Item Review Table</h1>
<p class="subtitle">Generated from survey/sara_usa.md v{version}. {n_items} items across {n_pages} pages; {len(dumpster)} in the dumpster.</p>

<div class="controls">
  <input class="search" type="text" id="search" placeholder="Search items, IDs, scales...">
  <button class="group-toggle" id="toggleGroups">Collapse all</button>
</div>

<table id="reviewTable">
<colgroup>
  <col class="c-order"><col class="c-id"><col class="c-item">
  <col class="c-scale"><col class="c-rationale"><col class="c-tri">
</colgroup>
<thead>
<tr>
  <th data-col="order">Order <span class="arrow">&#9650;</span></th>
  <th data-col="id">ID <span class="arrow">&#9650;</span></th>
  <th data-col="item">Item <span class="arrow">&#9650;</span></th>
  <th data-col="scale">Scale <span class="arrow">&#9650;</span></th>
  <th data-col="rationale">Rationale <span class="arrow">&#9650;</span></th>
  <th data-col="triangulates">Triangulates <span class="arrow">&#9650;</span></th>
</tr>
</thead>
<tbody id="tbody"></tbody>
</table>

{dumpster_html}

<script>
const DATA = {table_data_json};
let sortCol = "order", sortAsc = true;
const tbody = document.getElementById("tbody");
const searchInput = document.getElementById("search");

function render() {{
  const q = searchInput.value.toLowerCase();
  let filtered = DATA;
  if (q) filtered = DATA.filter(r =>
    Object.values(r).some(v => String(v).toLowerCase().includes(q)));

  const groups = {{}};
  for (const r of filtered) {{
    if (!groups[r.page]) groups[r.page] = [];
    groups[r.page].push(r);
  }}
  for (const page in groups) {{
    groups[page].sort((a, b) => {{
      let va = a[sortCol], vb = b[sortCol];
      if (typeof va === "number") return sortAsc ? va - vb : vb - va;
      va = String(va).toLowerCase(); vb = String(vb).toLowerCase();
      return sortAsc ? va.localeCompare(vb) : vb.localeCompare(va);
    }});
  }}

  tbody.innerHTML = "";
  const pageOrder = [...new Set(DATA.map(r => r.page))];
  for (const page of pageOrder) {{
    if (!groups[page]) continue;
    const gr = document.createElement("tr");
    gr.className = "group-header";
    gr.dataset.page = page;
    gr.innerHTML = '<td colspan="6">' + esc(page) +
      ' <span class="count">(' + groups[page].length + ' items)</span></td>';
    gr.onclick = () => toggleGroup(page);
    tbody.appendChild(gr);
    for (const r of groups[page]) {{
      const tr = document.createElement("tr");
      tr.className = "data-row";
      tr.dataset.page = page;
      tr.innerHTML =
        '<td style="text-align:center">' + r.order + '</td>' +
        '<td class="mono">' + esc(r.id) + '</td>' +
        '<td class="wrap">' + esc(r.item) + '</td>' +
        '<td class="wrap" style="font-size:13px">' + esc(r.scale) + '</td>' +
        '<td class="wrap" style="font-size:13px">' + esc(r.rationale) + '</td>' +
        '<td class="mono wrap">' + esc(r.triangulates) + '</td>';
      tbody.appendChild(tr);
    }}
  }}
}}

function esc(s) {{ const d = document.createElement("div"); d.textContent = s; return d.innerHTML; }}

function toggleGroup(page) {{
  const rows = tbody.querySelectorAll('tr[data-page="' + CSS.escape(page) + '"]');
  const header = tbody.querySelector('tr.group-header[data-page="' + CSS.escape(page) + '"]');
  const collapsed = !header.classList.contains("collapsed");
  header.classList.toggle("collapsed", collapsed);
  rows.forEach(r => {{
    if (!r.classList.contains("group-header")) r.classList.toggle("hidden", collapsed);
  }});
}}

document.getElementById("toggleGroups").onclick = () => {{
  const headers = tbody.querySelectorAll("tr.group-header");
  const allCollapsed = [...headers].every(h => h.classList.contains("collapsed"));
  headers.forEach(h => {{
    const page = h.dataset.page;
    h.classList.toggle("collapsed", !allCollapsed);
    tbody.querySelectorAll('tr.data-row[data-page="' + CSS.escape(page) + '"]')
      .forEach(r => r.classList.toggle("hidden", !allCollapsed));
  }});
  document.getElementById("toggleGroups").textContent = allCollapsed ? "Collapse all" : "Expand all";
}};

document.querySelectorAll("th[data-col]").forEach(th => {{
  th.onclick = () => {{
    const col = th.dataset.col;
    if (sortCol === col) sortAsc = !sortAsc;
    else {{ sortCol = col; sortAsc = true; }}
    document.querySelectorAll("th").forEach(t => t.classList.remove("sorted"));
    th.classList.add("sorted");
    th.querySelector(".arrow").innerHTML = sortAsc ? "&#9650;" : "&#9660;";
    render();
  }};
}});

searchInput.oninput = render;
render();
</script>
</body>
</html>"""

    with open(OUT_PATH, "w") as f:
        f.write(html)

    print(f"Wrote {OUT_PATH} ({len(html):,} bytes, {n_items} items)")


if __name__ == "__main__":
    main()
