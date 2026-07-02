#!/usr/bin/env Rscript
# render/review.R
# Reads survey/sara_usa.md (the single source of truth — a Markdown doc
# wrapping the survey YAML in a fenced ```yaml block, so it can be edited and
# reviewed in HackMD/Google Docs/GitHub) and produces render/review.html using
# reactable for an interactive, self-contained review table.
#
# Usage:
#   Rscript render/review.R
#   # or from project root:
#   make -C render
#
# Requires: yaml, reactable, htmltools, htmlwidgets

library(yaml)
library(reactable)
library(htmltools)
library(htmlwidgets)

# ── Resolve the script directory (works under Rscript and source()) ──

script_dir <- {
  a <- commandArgs(trailingOnly = FALSE)
  f <- grep("^--file=", a, value = TRUE)
  if (length(f)) {
    dirname(normalizePath(sub("^--file=", "", f[1])))
  } else {
    fr <- sys.frames()
    if (length(fr) && !is.null(fr[[1]]$ofile)) dirname(fr[[1]]$ofile) else "."
  }
}

# ── Load the spec (extract the ```yaml fenced block from sara_usa.md) ─

md_path <- file.path(script_dir, "..", "survey", "sara_usa.md")
if (!file.exists(md_path)) md_path <- file.path("..", "survey", "sara_usa.md")
md_text <- paste(readLines(md_path, warn = FALSE), collapse = "\n")
m <- regmatches(md_text, regexpr("(?s)```ya?ml\\n(.*?)\\n```", md_text, perl = TRUE))
if (length(m) == 0) stop("No ```yaml fenced block found in ", md_path)
fenced <- sub("^```ya?ml\\n", "", m)
fenced <- sub("\\n```$", "", fenced)
spec <- yaml.load(fenced)

scales <- spec$scales
pages <- spec$pages

# ── Build the data frame ─────────────────────────────────────────────

rows <- list()
order <- 0L

for (page in pages) {
  items <- page$items
  if (is.null(items) || length(items) == 0) next

  for (item in items) {
    order <- order + 1L

    # Resolve scale labels
    scale_name <- item$scale
    if (!is.null(scale_name) && scale_name %in% names(scales)) {
      scale_text <- paste(scales[[scale_name]]$labels, collapse = " / ")
    } else if (!is.null(item$options)) {
      scale_text <- paste(item$options, collapse = " / ")
    } else if (!is.null(item$widget) && item$widget == "number") {
      scale_text <- "(numeric entry)"
    } else {
      scale_text <- ""
    }

    # Triangulates
    tri <- item$triangulates
    tri_text <- if (!is.null(tri) && length(tri) > 0) paste(tri, collapse = ", ") else ""

    # Rationale
    rationale <- item$rationale %||% ""

    rows[[length(rows) + 1]] <- data.frame(
      Page = page$title,
      Order = order,
      Item = trimws(item$text),
      Scale = scale_text,
      Rationale = trimws(rationale),
      ID = item$id,
      Triangulates = tri_text,
      stringsAsFactors = FALSE
    )
  }
}

df <- do.call(rbind, rows)

# ── Build the reactable ──────────────────────────────────────────────

tbl <- reactable(
  df,
  groupBy = "Page",
  searchable = TRUE,
  defaultExpanded = TRUE,
  striped = TRUE,
  highlight = TRUE,
  bordered = TRUE,
  defaultPageSize = 100,
  columns = list(
    Page = colDef(minWidth = 140),
    Order = colDef(maxWidth = 60, align = "center"),
    ID = colDef(
      minWidth = 130,
      style = list(fontFamily = "ui-monospace, Menlo, monospace", fontSize = "13px")
    ),
    Item = colDef(minWidth = 250, style = list(whiteSpace = "normal")),
    Scale = colDef(minWidth = 200, style = list(whiteSpace = "normal", fontSize = "13px")),
    Rationale = colDef(minWidth = 250, style = list(whiteSpace = "normal", fontSize = "13px")),
    Triangulates = colDef(
      minWidth = 160,
      style = list(
        fontFamily = "ui-monospace, Menlo, monospace",
        fontSize = "12px",
        whiteSpace = "normal"
      )
    )
  ),
  theme = reactableTheme(
    headerStyle = list(
      background = "#2e5496",
      color = "#fff",
      fontWeight = 700,
      fontSize = "13px"
    )
  )
)

# ── Dumpster table (plain HTML, items considered and cut) ────────────

dump <- spec$dumpster
dump_html <- ""
if (!is.null(dump) && length(dump) > 0) {
  # Resolve an item's response scale to its labels (same logic as the live table)
  dump_scale_text <- function(item) {
    s <- item$scale
    if (!is.null(s) && s %in% names(scales)) return(paste(scales[[s]]$labels, collapse = " / "))
    if (!is.null(item$options)) return(paste(item$options, collapse = " / "))
    if (!is.null(item$widget) && item$widget == "number") return("(numeric entry)")
    ""
  }
  drows <- vapply(dump, function(d) {
    cell <- sprintf("<b>%s</b>", htmlEscape(d$name %||% ""))
    for (it in (d$items %||% list())) {
      cell <- paste0(cell, "<div class='d-item'><div>",
                     htmlEscape(trimws(it$text %||% "")), "</div>")
      if (!is.null(it$rows)) {
        cell <- paste0(cell, "<ul class='d-rows'>",
                       paste0("<li>", vapply(it$rows, htmlEscape, character(1)), "</li>",
                              collapse = ""), "</ul>")
      }
      st <- dump_scale_text(it)
      if (nzchar(st)) cell <- paste0(cell, "<div class='d-scale'>", htmlEscape(st), "</div>")
      if (!is.null(it$note)) cell <- paste0(cell, "<div class='d-note'>",
                                            htmlEscape(trimws(it$note)), "</div>")
      cell <- paste0(cell, "<span class='d-id'>", htmlEscape(it$id %||% ""), "</span></div>")
    }
    if (!is.null(d$note)) cell <- paste0(cell, "<div class='d-note'>",
                                         htmlEscape(trimws(d$note)), "</div>")
    sprintf("<tr><td>%s</td><td>%s</td></tr>", cell, htmlEscape(trimws(d$reason %||% "")))
  }, character(1))
  dump_html <- paste0(
    "<h2 class='dump-h'>Dumpster <span style='color:#647281;font-weight:400;font-size:12px'>(",
    length(dump), " cut)</span></h2>",
    "<p class='subtitle' style='color:#647281;font-size:14px;margin:0 24px 6px'>",
    "Items and modules considered and deliberately not fielded.</p>",
    "<table class='dumpster'><thead><tr><th>Item / module</th><th>Why cut</th></tr></thead><tbody>",
    paste(drows, collapse = ""), "</tbody></table>")
}

# ── Save the interactive table, then inject header + dumpster ─────────

out_path <- file.path(script_dir, "review.html")
saveWidget(tbl, out_path, selfcontained = TRUE, title = "SARA USA 2026 — Item Review Table")

header_html <- paste0(
  "<h1 style='color:#2e5496;font-size:22px;margin:24px 24px 4px'>SARA USA 2026 — Item Review Table</h1>",
  "<p class='subtitle' style='color:#647281;font-size:14px;margin:0 24px 16px'>",
  "Generated from survey/sara_usa.md v", spec$meta$version, ". ",
  nrow(df), " items across ", length(unique(df$Page)),
  " pages; ", length(dump), " in the dumpster.</p>")
style_html <- paste0(
  "<style>body{font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif;",
  "background:#f8f9fb;color:#1c2733} .dump-h{color:#647281;font-size:18px;margin:30px 24px 2px}",
  " table.dumpster{width:calc(100% - 48px);margin:6px 24px;border-collapse:collapse;background:#fff}",
  " table.dumpster th{background:#647281;color:#fff;text-align:left;padding:8px 12px}",
  " table.dumpster td{border-bottom:1px solid #e2e6eb;padding:8px 12px;vertical-align:top;font-size:14px}",
  " table.dumpster td:first-child{width:46%}",
  " .d-item{margin-top:8px;padding-left:10px;border-left:3px solid #e2e6eb}",
  " .d-scale{color:#647281;font-size:12.5px;margin-top:2px}",
  " .d-note{color:#647281;font-size:12px;font-style:italic;margin-top:2px}",
  " .d-id{font-family:ui-monospace,Menlo,monospace;font-size:11px;color:#647281}",
  " ul.d-rows{margin:2px 0 0 18px;font-size:13px}</style>")

content <- paste(readLines(out_path, warn = FALSE), collapse = "\n")
content <- sub("</head>", paste0(style_html, "</head>"), content, fixed = TRUE)
content <- sub("(<body[^>]*>)", paste0("\\1", header_html), content)
content <- sub("</body>", paste0(dump_html, "</body>"), content, fixed = TRUE)
writeLines(content, out_path)
cat("Wrote", out_path, "(", nrow(df), "items,", length(dump), "dumpster)\n")
