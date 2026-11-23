---
name: Library/silverbulletmd/Pele
tags: meta/library
description: Fast Mermaid-syntax diagrams with zoom, pan and theme-aware colors, drawn by Pele.
---
A Space Lua library that draws diagrams with [Pele](https://pele.run/), a small, fast renderer for [Mermaid](https://mermaid.js.org/) syntax.

```mermaid
flowchart LR
  A[Write a mermaid block] --> B(Move the cursor out)
  B --> C{Happy?}
  C -->|Yes| D[Done]
  C -->|No| A
```

Pele reads the same text as Mermaid, but draws it with its own layout engine. Compared to the [Mermaid library](https://github.com/silverbulletmd/silverbullet-diagram/blob/main/Mermaid.md) you get:

* **Speed:** diagrams render in well under a millisecond, so they keep up with typing and with live queries.
* **Zoom and pan:** a diagram wider than the page shrinks to fit; pinch or Ctrl/⌘-scroll to zoom, drag to pan.
* **Theming:** colors follow your SilverBullet theme, including dark mode, without re-rendering.
* **Size:** one 730 KB file (230 KB compressed), against about 1.6 MB compressed for Mermaid.

Layouts differ from Mermaid's, labels can't contain raw HTML, and Mermaid plugins such as ZenUML are not supported. See [Pele's compatibility notes](https://pele.run/compatibility).

> **warning** Pele or Mermaid: *not* both
> This library and the Mermaid library both draw ` ```mermaid ` blocks. Install one of the two.

# Installation
1. Run the **`Library: Install`** command (or open the **Libraries** manager and click **Install**).
2. When prompted for a library URI, paste: `github:silverbulletmd/silverbullet-libraries@main/Library/silverbulletmd/Pele.md`

By default Pele loads from [jsDelivr](https://www.jsdelivr.com/package/npm/pele). To work offline or without a CDN, run **`Pele: Download bundle for offline use`**: it saves Pele into your space, and from then on that copy is used.

# Static diagrams
Write a fenced `mermaid` block and move your cursor out of it:

    ```mermaid
    flowchart TD
        Start --> Stop
    ```

Put your cursor in a diagram to edit its source. Errors show the line and column Pele got stuck on.

## Links
Clicking a linked node navigates within your space. Two ways to link a node:

* `click A "Some Page"`: links node `A` to the page *Some Page*. Use `#quot;` for a `"` in a page name, and start a name that has a colon with `./` (`click A "./ADR:001"`), or Pele reads it as a web address.
* `class A internal-link`: links node `A` to the page named by its label (as in Obsidian).

`http`, `https`, `mailto` and `tel` links, such as `click A "https://silverbullet.md"`, open in a new browser tab.

# Dynamic diagrams
Diagrams can be generated from your space's data and redraw when it changes, like query tables. The view functions return Mermaid source, which you pass to `pele.diagram`:

    ${pele.diagram(pele.relationGraph{
      pages = query[[from index.pages("adr")]],
    })}

Because a view returns text, you can also look at it, adjust it, or paste it into a static block.

# API
## pele.diagram(source, opts)
Renders Mermaid `source` as a widget. `opts` *(optional)* is passed to Pele:

* `zoom`: `"auto"` (default; zoom and pan only when the diagram is shrunk to fit), `true` or `false`.
* `maxWidth`: maximum width in pixels.
* `fontSize`: base font size in pixels (default 16).
* `autoDirection`: on by default, so Pele turns wide flowcharts vertical when they don't fit; `false` keeps the direction as written.
* `padding`: padding around the diagram in pixels.
* `config`: Mermaid settings, such as `{ flowchart = { curve = "linear" } }`. Support varies by diagram type.

## pele.relationGraph(spec)
A flowchart of frontmatter relations between pages. Nodes are labeled with the last segment of the page name, and clicking one opens the page.

* `pages`: the pages to draw, e.g. `query[[from index.pages("adr")]]`.
* `relations` *(optional)*: frontmatter fields holding `[[page]]` links to draw as edges, e.g. `{"dependsOn", "related"}`. When omitted, every field whose values are `[[links]]` to pages in the set becomes an edge, labeled with the field name. `supersededBy` edges are dotted.
* `groupBy` *(optional)*: a field naming a container page; pages nest inside their container's box.
* `direction` *(optional)*: `"LR"` (default), `"TD"`, `"RL"` or `"BT"`.
* `color` *(optional)*: a field whose value becomes a CSS class on the node (`:::value`). Add matching `classDef` lines to style them.
* `max` *(optional, default 60)*: node limit.

## pele.timeline(spec)
A timeline of pages by a date field.

* `pages`: the pages to lay out.
* `dateField` *(default `"date"`)*: a field holding a `YYYY-MM-DD` date. Pages without one are skipped.
* `groupBy` *(default `"year"`)*: `"year"` groups entries under their year; `"none"` gives one entry per date.
* `labelField` *(optional)*: a field to use as the entry label, instead of the page name.
* `title` *(optional)*: the diagram title.
* `max` *(optional, default 100)*: entry limit.

## pele.distribution(spec)
A pie chart counting pages by a field, largest slice first. A list field, such as `tags`, counts each item.

* `pages`: the pages to count.
* `by`: the field to count by, e.g. `"status"`.
* `emptyLabel` *(optional)*: a label for pages without a value; omit to leave them out.
* `title` *(optional)*: the chart title.
* `showData` *(optional)*: show the counts next to the slices.

## Helpers
* `pele.id(text)`: a valid Mermaid node id for any text.
* `pele.label(text)`: `text` as a quoted Mermaid label, with `"` escaped.
* `pele.supports(source)`: whether Pele can draw `source`.
* `pele.detectType(source)`: the diagram type of `source`, such as `"flowchart"`, or `nil`.

# Configuration
Everything works out of the box. To change where Pele loads from:

```lua
config.set("pele", {
  -- Loaded when no offline copy exists, and fetched by the download command
  cdnUrl = "https://cdn.jsdelivr.net/npm/pele@1.13.0/dist/pele.js",
  -- Where the offline copy is saved and loaded from
  bundlePath = "Library/silverbulletmd/Pele/pele.js",
})
```

Diagram colors come from your theme. To change them, set Pele's [CSS variables](https://pele.run/theming) on `.sb-pele` in a `space-style` block:

```css
.sb-pele {
  --pele-accent: hotpink;
}
```

# Diagram types
The first line of a block names its type.

| Type | First line |
|------|------------|
| Flowchart | `flowchart` or `graph` |
| Swimlane | `swimlane-beta` |
| Sequence | `sequenceDiagram` |
| Class | `classDiagram` |
| State | `stateDiagram` or `stateDiagram-v2` |
| Entity relationship | `erDiagram` |
| Gantt | `gantt` |
| Git graph | `gitGraph` |
| Pie | `pie` |
| Mind map | `mindmap` |
| Kanban | `kanban` |
| Timeline | `timeline` |
| User journey | `journey` |
| Quadrant chart | `quadrantChart` |
| XY chart | `xychart` or `xychart-beta` |
| Requirement | `requirementDiagram` |
| Sankey | `sankey` or `sankey-beta` |
| Architecture | `architecture-beta` |
| C4 | `C4Context`, `C4Container`, `C4Component`, `C4Dynamic` or `C4Deployment` |
| Block | `block` or `block-beta` |
| Agent flow | `agentflow-beta` |
| Railroad | `railroad-beta`, `railroad-ebnf-beta`, `railroad-abnf-beta` or `railroad-peg-beta` |
| Tree view | `treeView-beta` |
| Cynefin | `cynefin-beta` |
| Wardley map | `wardley-beta` |
| Event modeling | `eventmodeling` |
| Use case | `usecase-beta` |
| Venn | `venn-beta` |
| Ishikawa | `ishikawa` or `ishikawa-beta` |
| Packet | `packet` or `packet-beta` |
| Radar | `radar-beta` |
| Treemap | `treemap` or `treemap-beta` |
| Info | `info` |

# Examples
Put your cursor in any example to see its source.

## Flowchart
```mermaid
flowchart TD
  Idea[Idea] --> Draft(Draft)
  Draft --> Review{Review}
  Review -->|Changes| Draft
  Review -->|Approved| Publish([Publish])
```

## Sequence
```mermaid
sequenceDiagram
  participant B as Browser
  participant S as Server
  B->>S: GET /page
  S-->>B: Markdown
  B->>B: Render
  B->>S: PUT /page
  S-->>B: 200 OK
```

## Class
```mermaid
classDiagram
  class Page {
    +String name
    +Date lastModified
    +render()
  }
  class Task {
    +String text
    +bool done
  }
  Page "1" --> "*" Task : contains
```

## State
```mermaid
stateDiagram-v2
  [*] --> Todo
  Todo --> Doing : start
  Doing --> Done : finish
  Doing --> Todo : pause
  Done --> [*]
```

## Entity relationship
```mermaid
erDiagram
  SPACE ||--o{ PAGE : contains
  PAGE ||--o{ TASK : has
  PAGE }o--o{ TAG : "tagged with"
```

## Gantt
```mermaid
gantt
  title Release plan
  dateFormat YYYY-MM-DD
  section Build
    Design      :done, d1, 2026-01-05, 7d
    Implement   :active, i1, after d1, 14d
  section Ship
    Test        :t1, after i1, 5d
    Release     :milestone, after t1, 0d
```

## Git graph
```mermaid
gitGraph
  commit
  branch feature
  checkout feature
  commit
  commit
  checkout main
  commit
  merge feature
  commit
```

## Pie
```mermaid
pie showData
  title Where the time goes
  "Writing" : 45
  "Editing" : 30
  "Linking" : 25
```

## Mind map
```mermaid
mindmap
  root((Notes))
    Projects
      Active
      Someday
    Areas
      Health
      Work
    Resources
```

## Timeline
```mermaid
timeline
  title A year of notes
  Q1 : Started a journal : Imported old notes
  Q2 : First queries
  Q3 : Custom widgets
  Q4 : Published a site
```

## User journey
```mermaid
journey
  title Capturing a thought
  section Capture
    Open quick note: 5: Me
    Type the thought: 4: Me
  section Later
    Find it again: 3: Me
    Link it to a project: 5: Me
```

## Quadrant chart
```mermaid
quadrantChart
  title Effort vs impact
  x-axis Low effort --> High effort
  y-axis Low impact --> High impact
  quadrant-1 Plan
  quadrant-2 Do now
  quadrant-3 Skip
  quadrant-4 Delegate
  Fix typo: [0.1, 0.2]
  New sync engine: [0.85, 0.9]
  Dark mode: [0.3, 0.7]
```

## XY chart
```mermaid
xychart
  title "Pages per month"
  x-axis [Jan, Feb, Mar, Apr, May, Jun]
  y-axis "Pages" 0 --> 100
  bar [20, 35, 42, 58, 70, 88]
  line [20, 35, 42, 58, 70, 88]
```

## Sankey
```mermaid
sankey
Inbox,Projects,12
Inbox,Archive,20
Inbox,Trash,8
Projects,Done,9
Projects,Archive,3
```

## Kanban
```mermaid
kanban
  todo[To do]
    t1[Write docs]
    t2[Add tests]
  doing[Doing]
    t3[Pele library]
  done[Done]
    t4[Mermaid library]
```

## Architecture
```mermaid
architecture-beta
  group cloud(cloud)[Server]
  service db(database)[Files] in cloud
  service api(server)[API] in cloud
  service web(internet)[Browser]
  web:R --> L:api
  api:R --> L:db
```

## From your space
The tags on your pages (outside `Library/`), counted live:

${pele.diagram(pele.distribution{
  pages = query[[from p = index.pages() where not p.name:startsWith("Library/") limit 500]],
  by = "tags",
  emptyLabel = "untagged",
  title = "Pages by tag",
})}

# Implementation

```space-lua
pele = pele or {}

local PELE_DEFAULTS = {
  cdnUrl = "https://cdn.jsdelivr.net/npm/pele@1.13.0/dist/pele.js",
  bundlePath = "Library/silverbulletmd/Pele/pele.js",
}

local function peleConfig()
  local cfg = config.get("pele", {})
  return {
    cdnUrl = cfg.cdnUrl or PELE_DEFAULTS.cdnUrl,
    bundlePath = cfg.bundlePath or PELE_DEFAULTS.bundlePath,
  }
end

function pele.load()
  if pele._module then return pele._module end
  local cfg = peleConfig()
  local m
  if space.fileExists(cfg.bundlePath) then
    m = js.importFromSpace(cfg.bundlePath)
  else
    m = js.import(cfg.cdnUrl)
  end
  pele._module = m
  return m
end

function pele.diagram(source, opts)
  local m = pele.load()
  local div = js.window.document.createElement("div")
  div.className = "sb-pele"
  local mountOpts = { zoom = "auto" }
  for k, v in pairs(opts or {}) do mountOpts[k] = v end
  m.mount(div, source, mountOpts)
  return widget.new {
    html = div,
    display = "block",
    markdown = "```mermaid\n" .. source .. "\n```",
    events = {
      click = function(e)
        local ok, internal, href = pcall(function()
          local a = e.data.target.closest("a")
          if not a then return nil end
          return a.getAttribute("data-href"), a.getAttribute("href")
        end)
        if not ok then return end
        -- Pele only sets data-href on `class X internal-link` nodes, so that is
        -- always a page; a plain href is a page unless it has one of the URL
        -- schemes Pele allows (page names like "Book: Dune" contain colons)
        local target = internal
        if not target and href then
          local lower = string.lower(href)
          if string.match(lower, "^https?:") or string.match(lower, "^mailto:")
              or string.match(lower, "^tel:") then
            -- Opening in place would replace SilverBullet in a browser tab
            e.data.preventDefault()
            editor.openUrl(href)
            return
          end
          target = href
        end
        if not target or target == "" then return end
        e.data.preventDefault()
        target = string.match(target, "^%[%[(.*)%]%]$") or target
        -- "./" lets a click target like "ADR:001" pass Pele's scheme check
        target = string.match(target, "^%./(.*)$") or target
        editor.navigate(target)
      end,
    },
  }
end

-- Text helpers ------------------------------------------------------------

-- A valid Mermaid identifier for an arbitrary string.
function pele.id(raw)
  local id = string.gsub(tostring(raw), "[^%w_]", "_")
  if not string.match(id, "^[%a_]") then id = "n_" .. id end
  return id
end

-- A double-quoted Mermaid label; `"` becomes Mermaid's #quot; entity.
function pele.label(text)
  return '"' .. string.gsub(tostring(text), '"', "#quot;") .. '"'
end

function pele.supports(source)
  return pele.load().supports(source)
end

function pele.detectType(source)
  return pele.load().detectType(source)
end

local function shortName(name)
  return (string.match(name, "[^/]+$")) or name
end

-- Strip surrounding [[ ]] from a link value (first value of a list).
local function deref(v)
  if type(v) == "table" then v = v[1] end
  if type(v) ~= "string" then return nil end
  v = string.gsub(v, "^%[%[", "")
  v = string.gsub(v, "%]%]$", "")
  return v
end

-- Views: Mermaid source built from the object index ------------------------

-- A flowchart of frontmatter relations between pages.
function pele.relationGraph(spec)
  spec = spec or {}
  local groupBy = spec.groupBy
  local max = spec.max or 60

  local pages = {}
  for _, p in ipairs(spec.pages or {}) do pages[#pages + 1] = p end
  table.sort(pages, function(a, b)
    return string.lower(a.name or "") < string.lower(b.name or "")
  end)

  local idOf, order = {}, {}
  for _, p in ipairs(pages) do
    if #order >= max then break end
    order[#order + 1] = p
    idOf[p.name] = "n" .. #order
  end

  local lines = { "flowchart " .. (spec.direction or "LR") }
  local function node(p, indent)
    local cls = spec.color and p[spec.color]
    lines[#lines + 1] = indent .. idOf[p.name] .. "(" .. pele.label(shortName(p.name)) .. ")" ..
      (cls and (":::" .. pele.id(cls)) or "")
    -- "./" keeps Pele from reading a name like "ADR:001" as a URL scheme
    lines[#lines + 1] = indent .. "click " .. idOf[p.name] .. " " .. pele.label("./" .. p.name)
  end

  -- Pages others point to with `groupBy` become subgraphs around them,
  -- nested as deep as the containers go
  local childrenOf, hasParent = {}, {}
  if groupBy then
    for _, p in ipairs(order) do
      local c = deref(p[groupBy])
      if c and idOf[c] and c ~= p.name then
        childrenOf[c] = childrenOf[c] or {}
        table.insert(childrenOf[c], p)
        hasParent[p.name] = true
      end
    end
  end
  local emitted = {}
  local function emit(p, indent)
    if emitted[p.name] then return end
    emitted[p.name] = true
    local children = childrenOf[p.name]
    if not children then
      node(p, indent)
      return
    end
    lines[#lines + 1] = indent .. "subgraph " .. idOf[p.name] .. " [" .. pele.label(shortName(p.name)) .. "]"
    for _, child in ipairs(children) do emit(child, indent .. "  ") end
    lines[#lines + 1] = indent .. "end"
  end
  for _, p in ipairs(order) do
    if not hasParent[p.name] then emit(p, "  ") end
  end
  -- Whatever is left belongs to a groupBy cycle
  for _, p in ipairs(order) do emit(p, "  ") end

  -- In auto mode only [[link]] values count; named relations take any value
  local function addEdges(fromId, field, value, requireLink)
    if type(value) == "string" then value = { value } end
    if type(value) ~= "table" then return end
    for _, t in ipairs(value) do
      if type(t) == "string" and (not requireLink or string.match(t, "^%[%[")) then
        local toId = idOf[deref(t)]
        if toId and toId ~= fromId then
          local op = field == "supersededBy" and "-.->" or "-->"
          lines[#lines + 1] = "  " .. fromId .. " " .. op .. "|" .. pele.label(field) .. "| " .. toId
        end
      end
    end
  end
  for _, p in ipairs(order) do
    local fromId = idOf[p.name]
    if spec.relations then
      for _, rel in ipairs(spec.relations) do addEdges(fromId, rel, p[rel], false) end
    else
      local keys = {}
      for key in pairs(p) do
        if type(key) == "string" and key ~= groupBy then keys[#keys + 1] = key end
      end
      table.sort(keys)
      for _, key in ipairs(keys) do addEdges(fromId, key, p[key], true) end
    end
  end

  if #order < #pages then
    lines[#lines + 1] = "  %% showing " .. #order .. " of " .. #pages .. " pages"
  end
  return table.concat(lines, "\n")
end

-- A timeline of pages by a YYYY-MM-DD date field.
function pele.timeline(spec)
  spec = spec or {}
  local dateField = spec.dateField or "date"
  local groupBy = spec.groupBy or "year"
  local max = spec.max or 100

  -- A colon separates timeline fields, so labels can't contain one
  local function clean(s)
    return (string.gsub(tostring(s), ":", " "))
  end
  local function labelOf(p)
    if spec.labelField and p[spec.labelField] then return clean(p[spec.labelField]) end
    return clean(shortName(p.name))
  end

  local pages = {}
  for _, p in ipairs(spec.pages or {}) do
    local d = p[dateField]
    if type(d) == "string" and string.match(d, "^%d%d%d%d%-%d%d%-%d%d") then
      pages[#pages + 1] = p
    end
  end
  table.sort(pages, function(a, b) return a[dateField] < b[dateField] end)

  local lines = { "timeline" }
  if spec.title then lines[#lines + 1] = "  title " .. clean(spec.title) end
  local shown = math.min(#pages, max)
  if groupBy == "year" then
    local years, byYear = {}, {}
    for i = 1, shown do
      local year = string.sub(pages[i][dateField], 1, 4)
      if not byYear[year] then
        byYear[year] = {}
        years[#years + 1] = year
      end
      table.insert(byYear[year], labelOf(pages[i]))
    end
    for _, year in ipairs(years) do
      lines[#lines + 1] = "  " .. year .. " : " .. table.concat(byYear[year], " : ")
    end
  else
    for i = 1, shown do
      lines[#lines + 1] = "  " .. clean(pages[i][dateField]) .. " : " .. labelOf(pages[i])
    end
  end
  if shown < #pages then
    lines[#lines + 1] = "  %% showing " .. shown .. " of " .. #pages
  end
  return table.concat(lines, "\n")
end

-- A pie counting pages by a field; list values (like tags) count once per item.
function pele.distribution(spec)
  spec = spec or {}
  local by = spec.by
  if not by then error("pele.distribution: `by` is required") end

  local counts, order = {}, {}
  local function count(v)
    if v == nil or v == "" then v = spec.emptyLabel end
    if v == nil then return end
    v = tostring(v)
    if not counts[v] then
      counts[v] = 0
      order[#order + 1] = v
    end
    counts[v] = counts[v] + 1
  end
  for _, p in ipairs(spec.pages or {}) do
    local v = p[by]
    if type(v) == "table" then
      if #v == 0 then count(nil) end
      for _, item in ipairs(v) do count(item) end
    else
      count(v)
    end
  end
  table.sort(order, function(a, b)
    if counts[a] ~= counts[b] then return counts[a] > counts[b] end
    return a < b
  end)

  local lines = { spec.showData and "pie showData" or "pie" }
  if spec.title then lines[#lines + 1] = "  title " .. spec.title end
  for _, label in ipairs(order) do
    lines[#lines + 1] = "  " .. pele.label(label) .. " : " .. counts[label]
  end
  return table.concat(lines, "\n")
end

-- Pele is one self-contained file, so going offline is a single download
command.define {
  name = "Pele: Download bundle for offline use",
  run = function()
    local cfg = peleConfig()
    editor.flashNotification("Downloading Pele…")
    local res = net.proxyFetch(cfg.cdnUrl, { responseEncoding = "text/plain" })
    if not (res and res.ok) then
      editor.flashNotification("Pele download failed: HTTP " .. tostring(res and res.status), "error")
      return
    end
    space.writeFile(cfg.bundlePath, js.new(js.window.TextEncoder).encode(res.body))
    editor.flashNotification(
      "Pele installed for offline use — reload to use it.",
      "info",
      { actions = { { name = "Reload", run = function() editor.reloadUI() end } } }
    )
  end
}

codeWidget.define {
  language = "mermaid",
  render = function(body)
    return pele.diagram(body)
  end
}
```

```space-style
/* Pele colors diagrams with CSS variables; map them onto the editor theme so
   light/dark switches apply without re-rendering. */
.sb-pele {
  --pele-bg: var(--root-background-color);
  --pele-fg: var(--root-color);
  --pele-line: color-mix(in srgb, var(--root-color) 75%, var(--root-background-color));
  --pele-muted: var(--subtle-color);
  --pele-surface: color-mix(in srgb, var(--root-color) 6%, var(--root-background-color));
  --pele-surface-alt: color-mix(in srgb, var(--root-color) 12%, var(--root-background-color));
  --pele-border: color-mix(in srgb, var(--root-color) 40%, var(--root-background-color));
  --pele-accent: var(--ui-accent-color);
  --pele-font: var(--ui-font);
}
```
