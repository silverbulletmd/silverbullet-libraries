---
name: Library/silverbulletmd/Share Collections
tags: meta/library
description: Publish sets of pages together, see every shared page in one view, and share everything that changed in one go.
---
Builds on [Share](https://docs.silverbullet.md/Share) for publishing many pages at once:
* **Collections**: publish a _set_ of pages together under one location, keeping the links between them: a blog, or a set of documentation pages.
* The **Shared Pages** view: every shared page, collection, library and repository in one place, with its status.
* `Share: All Changed`: share everything that changed, in one go.

**Warning:** Very experimental, not very well tested. Very much a work in progress.

Sharing a single page with `Share: Page` is part of SilverBullet itself and needs no library.

# Collections
Define collections in a `space-lua` block in [[Library/Config]] rather than with frontmatter:

```lua
config.set("share.collections", {
  blog = {
    pages = function()
      return index.contentPages("pub")
    end,
    uri = "github:sam-example/moonshot-notes@main/content",  -- target root
    -- optional
    path = function(page)
      return page.name:gsub("^Blog/", "")
    end,
    transform = { bake = false },
  },
})
```

* The key (`blog`) names the collection in `Share: Collection` and in the Shared Pages view.
* `pages` is a function returning the member pages, as page objects or page names.
* `uri` is the target root. Each member is written under the root, named after its `<path>`: the page name, or what `path(page)` returns. How the name is formed depends on the location, see below.
* `transform` (optional) turns off steps of [What gets published](https://docs.silverbullet.md/Share#What%20gets%20published), like `share.transform` on a single page.
* `mode` (optional) can only be `push`.

`Share: Collection` asks which collection to publish, then writes the members whose published copy differs from them (or is missing) and leaves the others alone. Links between members point to their published copies. Links to pages outside the collection become plain text. The pages themselves are not changed: nothing is added to their frontmatter. A page that is in a collection and also has its own `share.uri` is shared both ways, independently.

**Use a target root dedicated to the collection.** When publishing, the library lists what is under the root, and anything no member maps to is offered for removal: every `.md` file under the root on GitHub, every `.md` file of a gist, and every page under the root on a SilverBullet space. The files are listed unticked, and only those you tick are deleted. A page you renamed shows up as its new file plus the old one in that list.

Where the collection goes:
* **GitHub repository**: a folder in a repository, such as `github:sam-example/moonshot-notes@main/content`. All changes of one publish go into a single commit, and you are asked for its commit message.
* **Gist**: an existing gist, such as `https://gist.github.com/me/abc123`, with each member a file in it.
* **SilverBullet space**: a page prefix in another space, such as `https://notes.example.com/Blog`. Each member becomes a page under it. The root can also be the space itself (`https://notes.example.com`): members become pages at the top of that space.

# Share: All Changed
`Share: All Changed` shares every _sync_ page you changed since its last share (as its `share.hash` tells), every _push_ page whose remote differs from it or is missing (it reads each push page’s remote to find out), and every collection with a member whose published copy differs or is missing, including one that has gained a page (a newly tagged or renamed one) or was never published. _Pull_ pages are left alone. A collection whose target can’t be read is left to `Share: Collection`.

# Shared Pages view
The Shared Pages view lists every page in your space that is shared, in four groups:
* **Pages**: pages you push, pull or sync.
* **Collections**: your collections, each with its number of pages and its target (in a narrow sidebar the target may not fit), and its member pages under it. When a collection’s `pages` function fails, the error is shown under it instead.
* **Libraries**: installed [libraries](https://docs.silverbullet.md/Library).
* **Repositories**: installed library repositories.

Open it with ${widgets.commandButton("Navigate: Shared Pages")}. It opens in the right sidebar. From its dock menu you can move it to the left sidebar, the bottom panel or a modal. Each row shows the page’s status. Clicking a row opens the page.

## Status
Without asking the remote, the view shows how a _pull_ or _sync_ page compares with its `share.hash`, the record of its last pull or sync:
* no status: unchanged since its last share.
* _changed here_: changed since its last share.
* _no record_: the page has no `share.hash` to compare with, for example because it was never pulled or synced.

_Push_ pages and the pages of collections keep no such record, so they show no status until you Check them.

Hover a status for the full explanation and the page’s share mode (`push`, `pull` or `sync`).

## Check
The **Check** button on a group reads the remote of each page in it and shows what it found, until you next act on that page:
* _up to date_: the remote has what a share would send.
* _missing_: nothing is on the remote yet.
* _changed here_: only your page changed.
* _remote changed_: only the remote changed.
* _changed both sides_: both changed.
* _differs_: they differ. For a push page or a collection’s page this means sharing would write it. For a pull or sync page, it means there is no `share.hash` to tell which side changed.
* _check failed_: the remote couldn’t be read. Hover the status for the reason. Check never signs in, so a remote you haven’t connected to from this device fails here until you share to it once.

A result is also dropped when you edit the page, since it no longer says how the page compares.

Check on a collection reads its target once where the target can list its files, and also adds a row for each file there that is no longer in the collection: _removed_ (hover it for the explanation). Publishing the collection offers those files for removal. When the target can’t be read, for example because you haven’t signed in to it from this device, every page of the collection shows _check failed_ with the reason. Check on the Collections group checks every collection.

## Actions
On a page:
* **Share**: shares the page, the same as `Share: Page` on it.
* **Open Remote**: opens the shared copy in your browser, where the location has a web address.
* **Copy Link**: copies that web address.

On a collection:
* **Share Collection**: publishes it, the same as `Share: Collection`.

On a collection’s page: **Open Remote** and **Copy Link**, for its published copy.

On a library or repository:
* **Update**: updates it from its source, as in the Libraries tab of the [Workbench](https://docs.silverbullet.md/Workbench).
* **Open in Libraries tab**: opens the Workbench’s Libraries tab.

In a read-only space, Check, Share, Share Collection and Update are hidden.

# API
These build on the [share API](https://docs.silverbullet.md/API/share) of SilverBullet itself.

## share.list()
Returns every page with a `share.uri`, sorted by name, as `{name, uri, mode, kind}`: `mode` is `push` when unset, `kind` is `library` for pages tagged `meta/library`, `repository` for `meta/repository` and `page` for everything else. Read from the index, so a page shared a moment ago appears once it is indexed. The Shared Pages view lists these.

## share.changedPages()
Returns the names of the pages `Share: All Changed` shares: the `sync` pages whose `share.status` is `localChanged`, and the `push` pages whose `share.check` is `differs` or `missing` (so their remotes are read, a push page whose check fails, say because its remote needs a sign-in, is left out for its own share to report). `pull` pages never.

## share.collections()
Returns the names of the collections configured in `share.collections`, sorted.

## share.collection(name)
Returns the collection as `{name, root, mode, members}`: `root` is the configured `uri` without trailing slashes, `mode` is always `push`, and `members` lists `{page, path, uri}` in the order `pages()` returned them, a page listed twice only once. `uri` is built by the `memberUri` of the root’s `share:target` descriptor. Errors with `Unknown collection: <name>`, or `Collection <name>: ...` when the `mode` isn’t `push`, `pages` or `path` fails, or two members go to the same member URI (on a gist, `Blog/Post` and `Blog-Post` both go to `Blog-Post.md`).

## share.checkCollection(name)
Reads the remote and compares it with what each member would send, like `share.check`. Where the target has a `net.listURI` listing, one listing is read, and a member whose entry has a `hash` is compared by its git blob SHA (`share.gitBlobSha`) without reading it. Otherwise each member is read. Never prompts, connects, signs in or writes. Returns `{members, removed}`: `members` is keyed by page name with `{uri, state}`, `state` being `upToDate`, `missing`, `differs` or `error` (with the message in `error`), and `removed` lists the URIs of the listed files no member maps to (empty without a listing).

## share.publishCollection(name)
Publishes a collection, the same as `Share: Collection`: first prepares the root’s transport with `share.ensureTransport` (which may ask to connect or sign in), so the members’ URIs are those of the root’s `share:target` even when the transport was set up just now. Then resolves the collection and transforms every member with the collection as the share set (afresh, so baked content is current, see `members` of `share.transform`), lists the root (letting the provider sign in, `{signIn = true}`), writes the members whose text differs from the remote (by the listed `hash`, or else by reading the member’s remote, one that can’t be read is written) and offers the listed files no member maps to for removal with `editor.pickMany`, every item unticked. Only ticked files are deleted. Writes and deletes go in one call to a `share:writeBatch:<root>` service when the root has one, and otherwise through `net.writeURI` and `net.deleteURI` one by one.

Returns `{written, unchanged, removed, failed, cancelled?}`: the pages written, the pages left alone, the URIs deleted, and `{page?, uri, error}` for each write or delete that failed. `cancelled` is true when the batch service reported that the user cancelled it (for example dismissing GitHub’s commit message prompt): then nothing was written or deleted, and nothing counts as failed. A failed member’s remote still differs, so the next publish tries it again. Errors before anything is written: a failing listing or a broken collection (see `share.collection`).

## share.changedCollections()
Returns the names of the collections `Share: All Changed` publishes: those with a member that is `missing` or `differs` by `share.checkCollection` (so their remotes are read). A collection whose check fails is left out, for its own publish to report.

## share.notifyPublished(name, ok, result)
Tells the user how a publish went, from what `pcall(share.publishCollection, name)` returned: `Published <name>: N written, M unchanged` (and `, K removed`), and the first failure as an error, or `Publish of <name> cancelled` when the user cancelled the batch.

## share.collectionFailure(f)
Returns one entry of the `failed` list of `share.publishCollection` as text: its page (or URI) and error.

## share.collectionLabel(root, uri)
Returns how a file under `root` is shown: its path below `root`, URL-decoded (`Old%20Page` reads `Old Page`, a path that doesn’t decode, such as the gist file `50% off.md`, is shown as it is), or `uri` itself when it isn’t under `root`.

## Providers
A share provider supports collections through services of SilverBullet itself, see the [share API](https://docs.silverbullet.md/API/share): the `memberUri` of its `share:target` descriptor, `net.listURI` and `net.deleteURI` to list and remove files under a root, and optionally `share:writeBatch:<root>` to write a whole publish in one call. GitHub, gists and SilverBullet spaces support all of these.

# Implementation
## Collections
```space-lua
-- priority: 8

config.define("share.collections", {
  type = "object",
  additionalProperties = {
    type = "object",
    properties = {
      pages = schema.func(),
      uri = schema.string(),
      path = schema.func(),
      mode = schema.string(),
      transform = {},
    },
    required = {"pages", "uri"},
  },
})

local function definitions()
  return config.get("share.collections") or {}
end

function share.collections()
  local names = {}
  for name in pairs(definitions()) do
    table.insert(names, name)
  end
  table.sort(names)
  return names
end

-- A collection's target root: its uri without trailing slashes, so member
-- URIs match the listing
local function rootOf(def)
  return (def.uri:gsub("/+$", ""))
end

-- The collection and its config entry
local function resolve(name)
  local def = definitions()[name]
  if def == nil then
    error("Unknown collection: " .. name)
  end
  local prefix = "Collection " .. name .. ": "
  if def.mode != nil and def.mode != "push" then
    error(prefix .. "mode must be push")
  end
  local ok, pages = pcall(def.pages)
  if not ok then
    error(prefix .. tostring(pages))
  end
  local root = rootOf(def)
  local memberUri = share.target(root).memberUri or share.genericTarget.memberUri
  -- pageAt is by member URI: a provider may map two paths to one file
  local members, pageAt, seen = {}, {}, {}
  -- The path of page p (only the first result: gsub also returns a count)
  local function pathOf(p)
    if not def.path then
      return p.name
    end
    local ok, path = pcall(function()
      return (def.path(p))
    end)
    if not ok then
      error(prefix .. tostring(path))
    end
    return path
  end
  -- pages() may return a query collection (e.g. index.contentPages) or an
  -- array; nil means no members
  local rows = {}
  if pages != nil then
    rows = query[[from p = pages select p]]
  end
  for _, p in ipairs(rows) do
    if type(p) == "string" then
      p = {name = p}
    end
    -- A page listed twice is one member
    if not seen[p.name] then
      seen[p.name] = true
      local path = pathOf(p)
      local uri = memberUri(root, path)
      if pageAt[uri] then
        error(prefix .. pageAt[uri] .. " and " .. p.name .. " both go to " .. path)
      end
      pageAt[uri] = p.name
      table.insert(members, {page = p.name, path = path, uri = uri})
    end
  end
  return {name = name, root = root, mode = "push", members = members}, def
end

function share.collection(name)
  return (resolve(name))
end

-- How c shares its members: its target and the member URIs by page
local function shareSet(c)
  local uris = {}
  for _, m in ipairs(c.members) do
    uris[m.page] = m.uri
  end
  return {target = share.target(c.root), uris = uris}
end

-- What member m sends, its page being text: transformed with the collection
-- as the share set
local function outgoingOf(set, def, m, text)
  return share.transform(text, {
    page = m.page,
    uri = m.uri,
    target = set.target,
    members = set.uris,
    steps = share.resolveSteps(m.page, text, set.target, def.transform),
  })
end

-- What each member sends, by page
local function outgoingTexts(c, def)
  local set = shareSet(c)
  local texts = {}
  for _, m in ipairs(c.members) do
    texts[m.page] = outgoingOf(set, def, m, space.readPage(m.page))
  end
  return texts
end

-- The files under root as listed, by URI, or nil when the target can't list.
-- signIn lets the provider sign in to list (publish only: check never prompts).
local function listing(root, signIn)
  local entries = net.listURI(root, {signIn = signIn})
  if entries == nil then
    return nil
  end
  local files = {}
  for _, entry in ipairs(entries) do
    files[entry.uri] = entry
  end
  return files
end

-- Listed files no member maps to, sorted
local function unmapped(c, files)
  local memberUris = {}
  for _, m in ipairs(c.members) do
    memberUris[m.uri] = true
  end
  local uris = {}
  for uri in pairs(files) do
    if not memberUris[uri] then
      table.insert(uris, uri)
    end
  end
  table.sort(uris)
  return uris
end

local function checkMember(m, outgoing, files)
  local entry = files and files[m.uri]
  local remote
  if entry and entry.hash then
    remote = {sha = entry.hash}
  elseif entry or not files then
    -- Not listed, or listed without a hash: read it
    local remoteText = share.readRemote(m.uri)
    remote = remoteText and {text = remoteText}
  end -- Not in the listing: missing
  return share.remoteState {remote = remote, outgoing = outgoing}
end

-- Reads the remote (one listing where the target can list) and compares it
-- with the members. Never prompts, connects or writes.
function share.checkCollection(name)
  local c, def = resolve(name)
  local outgoing = outgoingTexts(c, def)
  local files = listing(c.root)
  local members = {}
  for _, m in ipairs(c.members) do
    local ok, state = pcall(checkMember, m, outgoing[m.page], files)
    if ok then
      members[m.page] = {uri = m.uri, state = state}
    else
      members[m.page] = {uri = m.uri, state = "error", error = tostring(state)}
    end
  end
  return {members = members, removed = files and unmapped(c, files) or {}}
end

-- Whether the remote differs from text: by the listed hash, else by reading
-- it. A remote that can't be read is written all the same.
local function needsWrite(m, text, files)
  if files then
    local entry = files[m.uri]
    if entry == nil then
      return true
    end
    if entry.hash then
      return share.gitBlobSha(text) != entry.hash
    end
  end
  local ok, remoteText = pcall(share.readRemote, m.uri)
  return not ok or remoteText != text
end

-- How a file under root reads to the user: its path below root, decoded
-- (gist file names aren't encoded, so a "%" may not decode)
function share.collectionLabel(root, uri)
  if uri:startsWith(root .. "/") then
    local tail = uri:sub(#root + 2)
    local ok, decoded = pcall(encoding.urlDecode, tail)
    return ok and decoded or tail
  end
  return uri
end

-- The listed files no member maps to that the user ticks for deletion
local function pickDeletes(c, files)
  local stale = files and unmapped(c, files) or {}
  if #stale == 0 then
    return {}
  end
  local items = {}
  for _, uri in ipairs(stale) do
    table.insert(items, {id = uri, label = share.collectionLabel(c.root, uri)})
  end
  return editor.pickMany {
    title = "Remove from " .. c.root .. "?",
    message = "These files are no longer in the collection.",
    items = items,
    confirmLabel = "Remove",
  } or {}
end

local function sendBatch(match, c, writes, deletes, result)
  local payload = {root = c.root, writes = {}, deletes = deletes}
  for _, w in ipairs(writes) do
    table.insert(payload.writes, {uri = w.uri, content = w.content})
  end
  local ok, err = pcall(service.invoke, match, payload)
  -- The user dismissed the batch (e.g. GitHub's commit message prompt)
  if ok and type(err) == "table" and err.cancelled then
    result.cancelled = true
    return
  end
  if not ok then
    for _, w in ipairs(writes) do
      table.insert(result.failed, {page = w.page, uri = w.uri, error = tostring(err)})
    end
    for _, uri in ipairs(deletes) do
      table.insert(result.failed, {uri = uri, error = tostring(err)})
    end
    return
  end
  for _, w in ipairs(writes) do
    table.insert(result.written, w.page)
  end
  result.removed = deletes
end

local function sendEach(writes, deletes, result)
  for _, w in ipairs(writes) do
    local ok, err = pcall(net.writeURI, w.uri, w.content)
    if ok then
      table.insert(result.written, w.page)
    else
      table.insert(result.failed, {page = w.page, uri = w.uri, error = tostring(err)})
    end
  end
  for _, uri in ipairs(deletes) do
    local ok, err = pcall(net.deleteURI, uri)
    if ok then
      table.insert(result.removed, uri)
    else
      table.insert(result.failed, {uri = uri, error = tostring(err)})
    end
  end
end

-- Writes the members that changed and deletes the files the user picks from
-- those no member maps to: in one call to a share:writeBatch service where
-- the target has one. Failed writes and deletes are in failed ({page?, uri,
-- error}); their remotes still differ, so the next publish retries them.
-- A batch the user cancelled writes nothing and sets cancelled.
function share.publishCollection(name)
  -- First, so the target (and so the member URIs) is that of a transport
  -- set up just now
  local entry = definitions()[name]
  if entry != nil then
    share.ensureTransport(rootOf(entry))
  end
  local c, def = resolve(name)
  local outgoing = outgoingTexts(c, def)
  local files = listing(c.root, true)
  local result = {written = {}, unchanged = {}, removed = {}, failed = {}}
  local writes = {}
  for _, m in ipairs(c.members) do
    local text = outgoing[m.page]
    if needsWrite(m, text, files) then
      table.insert(writes, {page = m.page, uri = m.uri, content = text})
    else
      table.insert(result.unchanged, m.page)
    end
  end
  local deletes = pickDeletes(c, files)
  if #writes == 0 and #deletes == 0 then
    return result
  end
  local batch = service.discover("share:writeBatch:" .. c.root, {root = c.root})
  if batch and #batch > 0 then
    sendBatch(batch[1], c, writes, deletes, result)
  else
    sendEach(writes, deletes, result)
  end
  return result
end

-- Collections with a member whose remote differs or is missing, as
-- share.checkCollection tells (so their remotes are read)
function share.changedCollections()
  local names = {}
  for _, name in ipairs(share.collections()) do
    -- A collection that can't be checked is left for its own publish to report
    local ok, checked = pcall(share.checkCollection, name)
    if ok then
      for _, m in pairs(checked.members) do
        if m.state == "differs" or m.state == "missing" then
          table.insert(names, name)
          break
        end
      end
    end
  end
  return names
end

-- One entry of publishCollection's failed, for a notification
function share.collectionFailure(f)
  return (f.page or f.uri) .. ": " .. f.error
end

-- Tells the user how a publish went, from what
-- pcall(share.publishCollection, name) returned
function share.notifyPublished(name, ok, r)
  if not ok then
    editor.flashNotification("Error: " .. r, "error")
    return
  end
  if r.cancelled then
    editor.flashNotification("Publish of " .. name .. " cancelled")
    return
  end
  local summary = "Published " .. name .. ": " .. #r.written .. " written, "
    .. #r.unchanged .. " unchanged"
  if #r.removed > 0 then
    summary = summary .. ", " .. #r.removed .. " removed"
  end
  editor.flashNotification(summary)
  if #r.failed > 0 then
    editor.flashNotification(share.collectionFailure(r.failed[1]), "error")
  end
end

command.define {
  name = "Share: Collection",
  requireMode = "rw",
  run = function()
    local options = {}
    for _, name in ipairs(share.collections()) do
      table.insert(options, {name = name})
    end
    if #options == 0 then
      editor.flashNotification("No collections configured", "error")
      return
    end
    local picked = editor.filterBox("Collection", options)
    if picked then
      share.notifyPublished(picked.name,
        pcall(share.publishCollection, picked.name))
    end
  end
}
```

## Shared pages and Share: All Changed
```space-lua
-- priority: 7

local function kindOf(tags)
  for _, tag in ipairs(tags or {}) do
    if tag == "meta/library" then
      return "library"
    elseif tag == "meta/repository" then
      return "repository"
    end
  end
  return "page"
end

-- Every page with a share.uri, by name
function share.list()
  local shared = {}
  for _, p in ipairs(index.queryLuaObjects("page", {})) do
    if type(p.share) == "table" and p.share.uri then
      table.insert(shared, {
        name = p.name,
        uri = p.share.uri,
        mode = p.share.mode or "push",
        kind = kindOf(p.tags),
      })
    end
  end
  table.sort(shared, function(a, b)
    return a.name < b.name
  end)
  return shared
end

-- The shared pages Share: All Changed shares: sync pages changed since their
-- last share (as share.hash tells), and push pages whose remote differs or is
-- missing (read to tell). Pull pages never.
function share.changedPages()
  local names = {}
  for _, p in ipairs(share.list()) do
    -- A page that can't be prepared or checked is left for its own share to
    -- report
    if p.mode == "sync" then
      local ok, status = pcall(share.status, p.name)
      if ok and status.state == "localChanged" then
        table.insert(names, p.name)
      end
    elseif p.mode == "push" then
      local state = share.check({p.name})[p.name].state
      if state == "differs" or state == "missing" then
        table.insert(names, p.name)
      end
    end
  end
  return names
end

command.define {
  name = "Share: All Changed",
  requireMode = "rw",
  run = function()
    local names = share.changedPages()
    local collections = share.changedCollections()
    local total = #names + #collections
    if total == 0 then
      editor.flashNotification "Nothing to share"
      return
    end
    local results = share.shareMany(names)
    local shared, firstFailure = 0, nil
    local function failed(name, message)
      firstFailure = firstFailure or (name .. ": " .. message)
    end
    for _, name in ipairs(names) do
      local r = results[name]
      if r.ok then
        shared = shared + 1
      else
        failed(name, r.error)
      end
    end
    for _, name in ipairs(collections) do
      local ok, r = pcall(share.publishCollection, name)
      if not ok then
        failed(name, tostring(r))
      elseif r.cancelled then
        -- Neither shared nor failed: the user knows
      elseif #r.failed > 0 then
        failed(name, share.collectionFailure(r.failed[1]))
      else
        shared = shared + 1
      end
    end
    editor.flashNotification("Shared " .. shared .. " of " .. total)
    if firstFailure then
      editor.flashNotification(firstFailure, "error")
    end
  end
}
```

## Shared Pages view
```space-lua
-- priority: 5

-- The unit separator (Space Lua has no decimal escapes, so not "\31")
local SEP = "\x1f"

local groups = {
  {kind = "page", label = "Pages"},
  {kind = "collection", label = "Collections"},
  {kind = "library", label = "Libraries"},
  {kind = "repository", label = "Repositories"},
}

-- Every row has a kind: group, collection, page, member, removed, error,
-- library or repository
local icons = {
  group = "folder",
  collection = "folder",
  page = "share-2",
  member = "share-2",
  removed = "file-minus",
  error = "alert-triangle",
  library = "package",
  repository = "database",
}

-- Chip text, and the full sentence for its tooltip. A push page's offline
-- "unchecked" has none: only a Check tells.
local statusLabels = {
  localChanged = {"changed here", "Changed since its last share"},
  unknown = {"no record", "The page has no share.hash to compare with"},
  upToDate = {"up to date", "The remote has what a share would send"},
  remoteChanged = {"remote changed", "Only the remote changed"},
  differs = {"differs", "Differs from the remote; sharing would write it"},
  missing = {"missing", "Not on the remote"},
  bothChanged = {"changed both sides", "Changed here and on the remote"},
  error = {"check failed", "The remote couldn't be read"},
  removed = {"removed", "On the remote, but no longer in the collection"},
}

-- Pull and sync pages differ only without a share.hash, and sharing them may
-- take the remote's version
local pullDiffers = {
  "differs",
  "Differs from the remote, and there's no share.hash to tell which side changed",
}

-- The last Check results, by row name, until an action on the row or a change
-- to its page's text: a page's or member's {result, text}, with the page's
-- text when checked; a collection's {removed}, the files a Check found on the
-- remote but not in the collection
local checks = {}

-- A group's folder comes from the tree, not from a row, so it has no kind
local function kindOf(obj)
  return obj.kind or "group"
end

-- A page's text, or nil when it can't be read (renamed or deleted before the
-- index caught up)
local function textOf(name)
  local ok, text = pcall(space.readPage, name)
  return ok and text or nil
end

-- Row name's Check result while page's text still holds, else offline()
local function statusOf(name, page, offline)
  local check = checks[name]
  if check and check.text != nil and check.text == textOf(page) then
    return check.result
  end
  return offline()
end

-- Forgets the Check results of a collection's folder and everything in it
local function forgetCollection(folder)
  local prefix = folder .. SEP
  local stale = {}
  for name in pairs(checks) do
    if name == folder or name:startsWith(prefix) then
      table.insert(stale, name)
    end
  end
  for _, name in ipairs(stale) do
    checks[name] = nil
  end
end

local function pageStatus(name)
  local ok, status = pcall(share.status, name)
  if ok then
    return status
  end
  return {state = "error", error = tostring(status)}
end

-- row with the status chip fields for a share in mode
local function withChip(row, mode, status)
  local label = statusLabels[status.state] or {}
  if status.state == "differs" and mode != "push" then
    label = pullDiffers
  end
  row.status = label[1]
  -- The mode only shows here, a second chip doesn't fit a sidebar row
  row.statusTitle = label[1] and (mode .. " · " .. (status.error or label[2]))
  return row
end

local function collectionFolder(name)
  return "Collections" .. SEP .. name
end

local function collectionRows(name)
  local folder = collectionFolder(name)
  local rows = {}
  local ok, err = pcall(function()
    local c = share.collection(name)
    table.insert(rows, {
      name = folder,
      label = name,
      kind = "collection",
      collection = name,
      root = c.root,
      count = #c.members,
    })
    for _, m in ipairs(c.members) do
      local rowName = folder .. SEP .. m.page
      table.insert(rows, withChip({
        name = rowName,
        page = m.page,
        uri = m.uri,
        mode = c.mode,
        kind = "member",
        collection = name,
      }, c.mode, statusOf(rowName, m.page, function()
        -- No chip until a Check: there is nothing to compare with offline
        return {}
      end)))
    end
    local check = checks[folder]
    for _, uri in ipairs(check and check.removed or {}) do
      table.insert(rows, withChip({
        -- Apart from the members' rows: no page name has a control character
        name = folder .. SEP .. "\x1e" .. uri,
        label = share.collectionLabel(c.root, uri),
        uri = uri,
        kind = "removed",
        collection = name,
      }, c.mode, {state = "removed"}))
    end
  end)
  if ok then
    return rows
  end
  return {
    {name = folder, label = name, kind = "collection", collection = name},
    {
      name = folder .. SEP .. "error",
      label = tostring(err),
      kind = "error",
      collection = name,
    },
  }
end

local function sharedRows()
  local byKind = {}
  for _, p in ipairs(share.list()) do
    byKind[p.kind] = byKind[p.kind] or {}
    table.insert(byKind[p.kind], p)
  end
  local rows = {}
  for _, group in ipairs(groups) do
    if group.kind == "collection" then
      for _, name in ipairs(share.collections()) do
        for _, row in ipairs(collectionRows(name)) do
          table.insert(rows, row)
        end
      end
    end
    for _, p in ipairs(byKind[group.kind] or {}) do
      local rowName = group.label .. SEP .. p.name
      table.insert(rows, withChip({
        name = rowName,
        page = p.name,
        uri = p.uri,
        mode = p.mode,
        kind = p.kind,
      }, p.mode, statusOf(rowName, p.name, function()
        return pageStatus(p.name)
      end)))
    end
  end
  return rows
end

local function pagesIn(groupLabel)
  local kind
  for _, group in ipairs(groups) do
    if group.label == groupLabel then
      kind = group.kind
    end
  end
  local names = {}
  for _, p in ipairs(share.list()) do
    if p.kind == kind then
      table.insert(names, p.name)
    end
  end
  return names
end

local function checkGroup(groupLabel)
  local names = pagesIn(groupLabel)
  local texts = {}
  for _, name in ipairs(names) do
    texts[name] = textOf(name)
  end
  for name, result in pairs(share.check(names)) do
    checks[groupLabel .. SEP .. name] = {result = result, text = texts[name]}
  end
end

-- A collection that can't be checked (say its listing needs a sign-in) shows
-- the error on every member
local function checkCollection(name)
  local c = share.collection(name)
  local texts = {}
  for _, m in ipairs(c.members) do
    texts[m.page] = textOf(m.page)
  end
  local ok, result = pcall(share.checkCollection, name)
  if not ok then
    local members = {}
    for _, m in ipairs(c.members) do
      members[m.page] = {uri = m.uri, state = "error", error = tostring(result)}
    end
    result = {members = members, removed = {}}
  end
  local folder = collectionFolder(name)
  forgetCollection(folder)
  checks[folder] = {removed = result.removed}
  for page, checked in pairs(result.members) do
    checks[folder .. SEP .. page] = {result = checked, text = texts[page]}
  end
end

local function isKind(...)
  local kinds = {...}
  return function(obj)
    for _, kind in ipairs(kinds) do
      if kindOf(obj) == kind then
        return true
      end
    end
    return false
  end
end

-- A group's folder, or a collection's (also one without members, which the
-- tree doesn't mark as a folder)
local isFolder = isKind("group", "collection")

-- An action on a page, which forgets that page's Check result (a member's is
-- the collection's, forgotten by Share Collection)
local function onPage(fn)
  return function(obj)
    if obj.kind != "member" then
      checks[obj.name] = nil
    end
    fn(obj)
  end
end

local function statusChip(obj)
  if obj.status then
    return {{text = obj.status, title = obj.statusTitle}}
  end
end

-- By kind; the rest show their status chip, if any
local decorations = {
  -- One that couldn't be resolved has no root
  collection = function(obj)
    if obj.root then
      local pages = obj.count == 1 and " page" or " pages"
      -- The count first: chips that don't fit drop from the end
      return {{text = obj.count .. pages}, {text = obj.root}}
    end
  end,
}

view.define {
  name = "std.sharedPages",
  title = "Shared Pages",
  command = "Navigate: Shared Pages",
  menu = { location = "view", group = "1_views", order = 7, label = "Shared Pages" },
  dock = "rhs",
  supportedDocks = {"rhs", "lhs", "bhs", "modal"},
  refreshOnOpen = true,
  source = sharedRows,
  presentation = {
    mode = "tree",
    hierarchy = {field = "name", separator = SEP},
    expandAll = true,
    foldersFirst = false,
    row = {
      label = function(obj)
        return obj.label or obj.page or obj.name
      end,
      decorations = function(obj)
        return (decorations[kindOf(obj)] or statusChip)(obj)
      end,
      icon = function(obj)
        return icons[kindOf(obj)]
      end,
    },
  },
  actions = {
    {
      icon = "refresh-cw",
      label = "Check",
      -- A read-only server reaches no remotes
      requireMode = "rw",
      when = isFolder,
      run = function(obj)
        if kindOf(obj) == "collection" then
          checkCollection(obj.collection)
        elseif obj.name == "Collections" then
          -- One that can't be resolved already shows its error
          for _, name in ipairs(share.collections()) do
            pcall(checkCollection, name)
          end
        else
          checkGroup(obj.name)
        end
      end,
    },
    {
      icon = "upload",
      label = "Share",
      requireMode = "rw",
      when = isKind("page"),
      run = onPage(function(obj)
        share.notifyShared(pcall(share.sharePage, obj.page))
      end),
    },
    {
      icon = "upload-cloud",
      label = "Share Collection",
      requireMode = "rw",
      when = isKind("collection"),
      run = function(obj)
        forgetCollection(obj.name)
        share.notifyPublished(obj.collection,
          pcall(share.publishCollection, obj.collection))
      end,
    },
    {
      icon = "external-link",
      label = "Open Remote",
      when = isKind("page", "member"),
      run = onPage(function(obj)
        share.openRemote(obj.uri)
      end),
    },
    {
      icon = "link",
      label = "Copy Link",
      when = isKind("page", "member"),
      run = onPage(function(obj)
        share.copyLink(obj.uri)
      end),
    },
    {
      icon = "download",
      label = "Update",
      requireMode = "rw",
      when = isKind("library", "repository"),
      run = onPage(function(obj)
        editor.invokeCommand("Library: Update", {{name = obj.page}})
      end),
    },
    {
      icon = "package",
      label = "Open in Libraries tab",
      when = isKind("library", "repository"),
      run = function()
        editor.invokeCommand("Workbench: Libraries")
      end,
    },
  },
  onSelect = function(obj)
    if obj.page then
      editor.navigate(obj.page)
    end
  end,
}
```
