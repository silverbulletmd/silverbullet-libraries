---
name: Library/silverbulletmd/Dashboard
tags: meta/library
description: Chips, bars, number cards and responsive grids for dashboards.
---
A set of widgets you can use to build “dashboard” like pages. 

# Tones
The visual widgets color by meaning to make theming easier. The same colours are available to your own CSS as `--tone-<name>` and `--tone-<name>-soft`, see [Space Style](https://docs.silverbullet.md/Space%20Style).

For a colour no tone covers, pass `color` with any CSS colour (`"#c0603a"`, `"teal"`, `"rgb(40 120 90)"`) instead: the widget uses that colour, with a light tint of it as the background, and `color` wins over `tone`. A literal colour stays the same in light and dark mode, so check it in both; prefer a tone where one fits. An invalid colour is ignored and the tone applies.

Examples:

${widgets.chip("info", { tone = "info" })} ${widgets.chip("#c0603a", { color = "#c0603a" })} ${widgets.chip("teal", { color = "teal" })}

# Click handling
`widgets.chip`, `widgets.stat` and `widgets.bars` take an `onClick` function. With it, the element becomes clickable. For `widgets.bars` the function receives the row that was clicked. To open a page, navigate in the callback, e.g.:

```lua
widgets.chip("Harbor", {
  onClick = function()
    editor.navigate("Projects/Harbor")
  end
})
```

All text the widgets show (labels, values, captions) is shown literally: `**bold**`, `<b>`, `[[links]]` and `${...}` are not interpreted.

# API
## widgets.chip(label, opts?)
A small rounded label, shaped like a hashtag, for statuses and categories. Inline.

| Option | Effect |
| --- | --- |
| `tone` | Tone name; default `neutral`. An unknown name falls back to `neutral`. |
| `color` | A CSS colour, used instead of the tone. |
| `title` | Tooltip. |
| `onClick` | Function run when the chip is clicked. |

Examples:
${widgets.chip("shipped", { tone = "success" })} ${widgets.chip("blocked", { tone = "danger" })} ${widgets.chip("review", { tone = "info" })} ${widgets.chip("draft")}

## widgets.bars(rows, opts?)
Horizontal bars, one per row, for counts or a distribution. `rows` is a list of tables or a [query](https://docs.silverbullet.md/Space%20Lua/Integrated%20Query) result. Each row shows its label, a bar whose length is the value relative to the maximum, and the value. Block-level.

| Option | Effect |
| --- | --- |
| `label` | Field name holding the label, or a function of the row; default `"label"`. |
| `value` | Field name holding the number, or a function of the row; default `"value"`. |
| `tone` | Tone name, or a function of the row returning one; default the row's own `tone` field, else `accent`. |
| `color` | A CSS colour, or a function of the row returning one, used instead of the tone; default the row's own `color` field. |
| `max` | The value that fills the whole width; default the largest value. |
| `onClick` | Function run with the row when it is clicked. |

${widgets.bars {
  { label = "Open", value = 7, tone = "warning" },
  { label = "Waiting", value = 3, tone = "info" },
  { label = "Closed", value = 12, tone = "success" },
}}

Over a query, with computed values:

```lua
widgets.bars(query[[
  from p = index.pages("project") order by p.name
]], {
  label = "name",
  value = function(p) return #query[[from t = index.tag "task" where t.page == p.name]] end,
  onClick = function(p) editor.navigate(p.name) end,
})
```

With no rows it shows "Nothing to show".

## widgets.stat(label, value, opts?)
A number card: a label, a large value and an optional caption and progress bar.

| Option | Effect |
| --- | --- |
| `tone` | Colours the value and the bar; default `neutral` (plain text colour). |
| `color` | A CSS colour, used instead of the tone. |
| `sub` | Caption below the value. |
| `bar` | A fraction from 0 to 1, drawn as a thin progress bar (clamped). |
| `onClick` | Function run when the card is clicked. |

${widgets.stat("Tasks done", "8/20", {
  tone = "success",
  sub = "40% overall",
  bar = 0.4
})}

## widgets.grid(items, fn?, opts?)
Lays cells out side by side in columns: as many columns as fit across the page, each at least `opts.min` wide, wrapping onto more rows as the page narrows. Block-level.

`items` is the list you want one cell each for. It can be used in two ways:

* **Without `fn`, `items` are the cells.** Pass a list of ready-made widgets, and each becomes one cell.
* **With `fn`, `items` is data and `fn(item)` builds the cell for each item.** This is the usual way with a [query](https://docs.silverbullet.md/Space%20Lua/Integrated%20Query): `items` is the query result, and `fn` is called once per item and returns the widget for it.

A cell can be any widget (`widgets.stat`, `widgets.chip`, `widget.html(...)`), a [DOM element](https://docs.silverbullet.md/API/dom), or a string or number (shown as literal text). Cells keep their own click handlers.

| Option | Effect |
| --- | --- |
| `min` | Minimum column width as a CSS length; default `12rem`. |

When you don't pass `fn`, the options can go second: `widgets.grid(cells, { min = "10rem" })`.

### Cells you build yourself
${widgets.grid {
  widgets.stat("Open", 7, { tone = "warning" }),
  widgets.stat("Closed", 12, { tone = "success" }),
  widgets.stat("Overdue", 2, { tone = "danger" }),
}}

### Data plus a function
The same grid from a list of data, with `fn` turning each entry into a card:

${widgets.grid({
  { label = "Open", count = 7, tone = "warning" },
  { label = "Closed", count = 12, tone = "success" },
  { label = "Overdue", count = 2, tone = "danger" },
}, function(s)
  return widgets.stat(s.label, s.count, { tone = s.tone })
end)}

### From a query
One card per page tagged `project`, each opening its page when clicked:

```lua
widgets.grid(query[[from p = index.pages("project") order by p.name]], function(p)
  return widgets.stat(p.name, p.status or "?", {
    sub = p.owner,
    onClick = function() editor.navigate(p.name) end,
  })
end)
```

# Implementation
## Chips, bars, stats and grids
Built with the [DOM](https://docs.silverbullet.md/API/dom) builder; labels go in as `dom.text`, so they stay literal. With `onClick` an element becomes a button (`role="button"`, focusable, Enter runs it too). Their CSS is in the Styles block below.
```space-lua
-- priority: 10
widgets = widgets or {}

local tones = {
  success = true, warning = true, danger = true,
  info = true, neutral = true, accent = true,
}

local function isColour(value)
  if type(value) ~= "string" or value == "" then return false end
  local css = js.window.CSS
  if css and css.supports then return css.supports("color", value) end
  return true
end

-- The class and style for a literal CSS colour if valid, else a tone name,
-- else the default tone
local function toneOf(tone, color, default)
  if isColour(color) then
    return "sb-tone-custom", {
      ["--sb-tone"] = color,
      ["--sb-tone-soft"] = "color-mix(in srgb, " .. color .. " 16%, transparent)",
    }
  end
  if tones[tone] then return "sb-tone-" .. tone, nil end
  return "sb-tone-" .. default, nil
end

local function text(s)
  if s == nil then return dom.text("") end
  return dom.text(tostring(s))
end

-- Makes an element act as a button for `handler`: click or Enter runs it
local function clickable(spec, handler)
  if handler then
    spec.role = "button"
    spec.tabindex = "0"
    spec.onclick = function() handler() end
    spec.onkeydown = function(e)
      if e.key == "Enter" then handler() end
    end
  end
  return spec
end

-- Reads a field (by name) or computes a value (by function) from a row
local function pick(row, getter)
  if type(getter) == "function" then return getter(row) end
  if getter == nil then return nil end
  return row[getter]
end

local function percent(fraction)
  if fraction ~= fraction or fraction < 0 then fraction = 0 end
  if fraction > 1 then fraction = 1 end
  return tostring(math.floor(fraction * 100 + 0.5)) .. "%"
end

local function empty(message)
  return widget.htmlBlock(dom.div { class = "sb-empty", dom.text(message) })
end

--- Renders a small rounded label in a tone colour
--- @param label string the text to show
--- @param opts? table `tone` (default "neutral"), `color` (CSS colour, used instead of the tone), `title` (tooltip), `onClick` (function run on click)
--- @return table an inline widget
--- @see Library/silverbulletmd/Dashboard
function widgets.chip(label, opts)
  opts = opts or {}
  local toneClass, toneStyle = toneOf(opts.tone, opts.color, "neutral")
  return widget.html(dom.span(clickable({
    class = { "sb-chip", toneClass },
    style = toneStyle,
    title = opts.title,
    text(label),
  }, opts.onClick)))
end

--- Renders horizontal bars for counts or a distribution, one per row.
--- @param rows table a list or query result
--- @param opts? table `label`, `value` (field names or functions, default "label" and "value"), `tone` (name or function of the row, default the row's `tone` field, else "accent"), `color` (CSS colour or function of the row, used instead of the tone; default the row's `color` field), `max` (full-width value, default the largest), `onClick` (function run with the clicked row)
--- @return table a block widget
--- @see Library/silverbulletmd/Dashboard
function widgets.bars(rows, opts)
  opts = opts or {}
  local labelOf = opts.label or "label"
  local valueOf = opts.value or "value"
  local items = {}
  local max = 0
  for _, row in ipairs(rows or {}) do
    local value = tonumber(pick(row, valueOf)) or 0
    local tone = opts.tone
    if type(tone) == "function" then
      tone = tone(row)
    elseif tone == nil and type(row) == "table" then
      tone = row.tone
    end
    local color = opts.color
    if type(color) == "function" then
      color = color(row)
    elseif color == nil and type(row) == "table" then
      color = row.color
    end
    table.insert(items, {
      label = pick(row, labelOf),
      value = value,
      tone = tone,
      color = color,
      row = row,
    })
    if value > max then max = value end
  end
  if #items == 0 then return empty("Nothing to show") end
  max = tonumber(opts.max) or max
  local bars = {}
  for _, item in ipairs(items) do
    local toneClass, toneStyle = toneOf(item.tone, item.color, "accent")
    table.insert(bars, dom.div(clickable({
      class = { "sb-bars-row", toneClass },
      style = toneStyle,
      dom.span { class = "sb-bars-label", text(item.label) },
      dom.span {
        class = "sb-bars-track",
        dom.span {
          class = "sb-bars-fill",
          style = { width = percent(max > 0 and item.value / max or 0) },
        },
      },
      dom.span { class = "sb-bars-value", text(item.value) },
    }, opts.onClick and function() opts.onClick(item.row) end)))
  end
  return widget.htmlBlock(dom.div { class = "sb-bars", bars })
end

--- Renders a number card, for use alone or in `widgets.grid`.
--- @param label string what the number is
--- @param value any the number (or short text) to show
--- @param opts? table `tone` (default "neutral"), `color` (CSS colour, used instead of the tone), `sub` (caption), `bar` (fraction 0..1 drawn as a thin bar), `onClick` (function run on click)
--- @return table a block widget
--- @see Library/silverbulletmd/Dashboard
function widgets.stat(label, value, opts)
  opts = opts or {}
  local toneClass, toneStyle = toneOf(opts.tone, opts.color, "neutral")
  return widget.htmlBlock(dom.div(clickable({
    class = { "sb-stat", toneClass },
    style = toneStyle,
    dom.div { class = "sb-stat-label", text(label) },
    dom.div { class = "sb-stat-value", text(value) },
    opts.sub ~= nil and dom.div { class = "sb-stat-sub", text(opts.sub) },
    opts.bar ~= nil and dom.div {
      class = "sb-stat-bar",
      dom.span { style = { width = percent(tonumber(opts.bar) or 0) } },
    },
  }, opts.onClick)))
end

-- A grid cell: widgets and DOM nodes as they are (event handlers included),
-- text and numbers shown literally
local function cell(w)
  if type(w) == "table" and w._isWidget then
    return w
  end
  if type(w) == "string" or type(w) == "number" then
    return dom.div { class = "sb-grid-text", text(w) }
  end
  return w
end

--- Lays out widgets in a responsive grid.
--- @param items table a list or query result
--- @param fn? function returns the widget (or DOM node) for an item (default: the item itself)
--- @param opts? table `min`: minimum column width (default "12rem")
--- @return table a block widget
--- @see Library/silverbulletmd/Dashboard
function widgets.grid(items, fn, opts)
  if type(fn) == "table" and opts == nil then
    opts, fn = fn, nil
  end
  opts = opts or {}
  local cells = {}
  for _, item in ipairs(items or {}) do
    local w = item
    if fn then w = fn(item) end
    table.insert(cells, cell(w))
  end
  if #cells == 0 then return empty("Nothing to show") end
  return widget.htmlBlock(dom.div {
    class = "sb-grid",
    style = opts.min and { ["--sb-grid-min"] = tostring(opts.min) } or nil,
    cells,
  })
end
```

### Styles
```space-style
/* Colours come from the tone tokens (Space Style#Tone colours), so both
   themes work; `color` sets --sb-tone/--sb-tone-soft inline instead. */
.sb-tone-success { --sb-tone: var(--tone-success); --sb-tone-soft: var(--tone-success-soft); }
.sb-tone-warning { --sb-tone: var(--tone-warning); --sb-tone-soft: var(--tone-warning-soft); }
.sb-tone-danger { --sb-tone: var(--tone-danger); --sb-tone-soft: var(--tone-danger-soft); }
.sb-tone-info { --sb-tone: var(--tone-info); --sb-tone-soft: var(--tone-info-soft); }
.sb-tone-neutral { --sb-tone: var(--tone-neutral); --sb-tone-soft: var(--tone-neutral-soft); }
.sb-tone-accent { --sb-tone: var(--tone-accent); --sb-tone-soft: var(--tone-accent-soft); }

/* Chips share the hashtag's geometry (editor.scss .sb-hashtag) so they sit in
   running text like tags do; the tone only sets the colours. */
.sb-chip {
  display: inline-block;
  padding: 0 4px;
  margin: 0 1px 0 0;
  border-radius: 6px;
  font-size: 0.9em;
  line-height: inherit;
  white-space: nowrap;
  vertical-align: baseline;
  color: var(--sb-tone, var(--tone-neutral));
  background: var(--sb-tone-soft, var(--tone-neutral-soft));
  border: 1px solid color-mix(in srgb, var(--sb-tone, var(--tone-neutral)) 25%, transparent);
}

/* widgets.* with onClick: role="button", focusable, Enter runs it too */
.sb-chip[role="button"],
.sb-stat[role="button"],
.sb-bars-row[role="button"] {
  cursor: pointer;
}

.sb-chip[role="button"]:hover {
  border-color: var(--sb-tone, var(--tone-neutral));
}

.sb-chip[role="button"]:focus-visible,
.sb-stat[role="button"]:focus-visible,
.sb-bars-row[role="button"]:focus-visible {
  outline: 2px solid var(--ui-accent-color);
  outline-offset: 1px;
}

.sb-bars {
  display: grid;
  grid-template-columns: minmax(4em, max-content) 1fr auto;
  gap: 0.3em 0.75em;
  align-items: center;
}

/* Each row spans the grid and lines its cells up with the others; a real
   box (not display: contents) so a clickable row can take focus. */
.sb-bars-row {
  display: grid;
  grid-column: 1 / -1;
  grid-template-columns: subgrid;
  align-items: center;
  border-radius: 3px;
}

.sb-bars-row[role="button"]:hover {
  background: var(--ui-surface-hover-background-color);
}

.sb-bars-track {
  height: 0.55em;
  min-width: 4em;
  border-radius: 3px;
  overflow: hidden;
  background: var(--sb-tone-soft);
}

.sb-bars-fill {
  display: block;
  height: 100%;
  border-radius: inherit;
  background: var(--sb-tone);
}

.sb-bars-value {
  text-align: right;
  color: var(--subtle-color);
  font-variant-numeric: tabular-nums;
}

/* Stat cards are flat surfaces like page widgets: a hairline border, no
   fill; the tone colours the number (except neutral) and the optional bar. */
.sb-stat {
  display: block;
  box-sizing: border-box;
  padding: 0.5em 0.75em;
  border: 1px solid var(--ui-surface-border-color);
  border-radius: 5px;
  color: inherit;
  text-decoration: none;
}

.sb-stat[role="button"]:hover {
  background: var(--ui-surface-hover-background-color);
}

.sb-stat-label {
  font-size: 0.85em;
  color: var(--subtle-color);
}

.sb-stat-value {
  font-size: 1.5em;
  font-weight: 600;
  line-height: 1.25;
  font-variant-numeric: tabular-nums;
}

.sb-stat:not(.sb-tone-neutral) .sb-stat-value {
  color: var(--sb-tone);
}

.sb-stat-sub {
  font-size: 0.85em;
  color: var(--subtle-color);
}

.sb-stat-bar {
  height: 4px;
  margin-top: 0.4em;
  border-radius: 3px;
  overflow: hidden;
  background: var(--sb-tone-soft);
}

.sb-stat-bar > span {
  display: block;
  height: 100%;
  background: var(--sb-tone);
}

.sb-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(var(--sb-grid-min, 12rem), 1fr));
  gap: 0.75em;
}

/* Cards fill their column; chips and buttons keep their own width. */
.sb-grid > .sb-chip,
.sb-grid > button {
  justify-self: start;
  align-self: start;
}

/* Like the navigator's empty state (.sb-nav-empty) */
.sb-empty {
  font-size: 0.9em;
  color: var(--subtle-color);
}

/* A chip is its own frame, like a hashtag in running text: drop the inline
   widget frame around it. */
#sb-main .cm-editor .sb-lua-directive-inline:has(> .sb-chip) {
  border: none;
  border-radius: 0;
  padding: 0;
}
```
