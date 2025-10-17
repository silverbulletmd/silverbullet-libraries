# Fast tag explorer

From community, generate tags of children page

```space-style
.fastnav-tags button {
  margin-top: 5px;
  margin-right: -5px;
  padding: 0.1em 0.1em;
  border: none;
  border-radius: 6px;
  background-color: #f0f0f0;
  color: #222;
  font-size: 0.9em;
  font-weight: 500;
  cursor: pointer;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}
.fastnav-tags button:hover {
  background-color: #dcdcdc;
  color: #000;
}
.fastnav-tags button.active-tag {
  background-color: #d0e8ff; 
  color: #000;
}
.fastnav-tags button span.fn-c {
  font-size: 0.7em;
  vertical-align: super;
  opacity: 0.5;
  margin-left: 4px;
}
.fastnav-pages {
  padding-top: 5px;
  font-size: 0.9em;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.fastnav-pages span {
  flex: 1 1 calc(20% - 8px);
  background-color: #f7f7f7;
  border: 1px solid #ddd;
  padding: 0.4em 0.6em;
  text-align: center;
  border-radius: 2px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
}
.fastnav-pages span:hover {
  cursor: pointer;
  background-color: #e6e6e6;
}

.fastnav-block {
  color: #222;
}
```

```space-lua
fastnav = fastnav or {}

-- Fetch all relevant page and tag data
--     where p.page.startsWith("projects/")
local function fetchTagAndPageData(dir)
  return query[[
  from p = index.tag "page"
  where p.name.startsWith(dir)
  order by p.name 
  select {
      name = p.name,
      tags = p.tags
    }
  ]]
end

-- Convert skiplist into a lookup set
local function buildSkipSet(skiplist)
  local skip = {}
  for _, name in ipairs(skiplist or {}) do
    skip[name] = true
  end
  return skip
end

-- Analyse all pages: count tags, check for untagged pages
local function analyseTags(data, skip)
  local tagCounts = {}
  local hasUntagged = false
  for _, page in ipairs(data) do
    local tags = page.tags
    if not tags or #tags == 0 then
      hasUntagged = true
    else
      for _, tag in ipairs(tags) do
        if not skip[tag] then
          tagCounts[tag] = (tagCounts[tag] or 0) + 1
        end
      end
    end
  end
  return tagCounts, hasUntagged
end

-- Convert tag count map to sorted array
local function sortedTagList(counts)
  local tags = {}
  for tag, count in pairs(counts) do
    table.insert(tags, {name=tag, count=count})
  end
  table.sort(tags, function(a, b) return a.name < b.name end)
  return tags
end

-- Generate HTML for all tags
function fastnav.TagsHtml(data, skip)
  local tagCounts, hasUntagged = analyseTags(data, skip)
  local sortedTags = sortedTagList(tagCounts)
  -- Generate the default tags
  local html = {}
  table.insert(html, fastnav.TagHtml("AllTags"))
  if hasUntagged then
    table.insert(html, fastnav.TagHtml("NoTags"))
  end
  -- Generate tag buttons associated with the pages
  local b = 1
  for _, tag in ipairs(sortedTags) do
    table.insert(html, fastnav.TagHtml(tag.name, tag.count))
  end
  return html
end

-- Generate HTML for all pages
function fastnav.PagesHtml(data, skip)
  local html = {}
  for _, page in ipairs(data) do
    local tags = page.tags or {}
    local skipPage = false
    for _, tag in ipairs(tags) do
      if skip[tag] then
        skipPage = true
        break
      end
    end
    if not skipPage then
      local tagList = (#tags == 0) and { "NoTags" } or tags
      table.insert(html, fastnav.PageHtml(page.name, tagList))
    end
  end
  return html
end

-- Individual page blocks
function fastnav.PageHtml(name, tagList)
  local tagClass = table.concat(tagList, " ")
  local basename = string.match(name, "[^/]+$") or name
  local js = "window.location='"..name.."';"
  return '<span onclick="'..js.. '" class="'..tagClass..'">'..basename..'</span>'
end

-- Individual tag buttons
function fastnav.TagHtml(name, count)
  local js = ""
  local all = "AllTags"
  if name == all then
    js = js .. "window.activeTags=[];"
    js = js .. "let t=document.getElementsByClassName('fn-tag');"
    js = js .. "for(let i=0;i<t.length;i++){t[i].classList.remove('active-tag');}"
    js = js .. "event.currentTarget.classList.add('active-tag');"
    js = js .. "let s=document.querySelectorAll('.fastnav-pages span');"
    js = js .. "for(let j=0;j<s.length;j++){s[j].style.display='inline';}"
  else
    js = js .. "window.activeTags=window.activeTags||[];"
    js = js .. "let i=window.activeTags.indexOf('" .. name .. "');"
    js = js .. "if(i==-1){"
    js = js .. "window.activeTags.push('" .. name .. "');"
    js = js .. "event.currentTarget.classList.add('active-tag');"
    js = js .. "let allbtn=document.querySelector('.fn-tag." .. all .. "');"
    js = js .. "if(allbtn){allbtn.classList.remove('active-tag');}"
    js = js .. "}else{"
    js = js .. "window.activeTags.splice(i,1);"
    js = js .. "event.currentTarget.classList.remove('active-tag');"
    js = js .. "if(window.activeTags.length==0){"
    js = js .. "let allbtn=document.querySelector('.fn-tag." .. all .. "');"
    js = js .. "if(allbtn){allbtn.classList.add('active-tag');}"
    js = js .. "}}"
    js = js .. "let s=document.querySelectorAll('.fastnav-pages span');"
    js = js .. "for(let j=0;j<s.length;j++){"
    js = js .. "let c=s[j].className.split(' ');"
    js = js .. "let show=false;"
    js = js .. "for(let k=0;k<window.activeTags.length;k++){"
    js = js .. "if(c.indexOf(window.activeTags[k])!=-1){show=true;break;}"
    js = js .. "}"
    js = js .. "s[j].style.display=(window.activeTags.length==0||show)?'inline':'none';"
    js = js .. "}"
  end
  local c = ""
  if count and count ~= "" then
    c = "<span class=\"fn-c\">("..count..")</span>"
  end
  local activeClass = (name == "AllTags") and " active-tag" or ""
  return '<button class="sb-command-button fn-tag '..name..activeClass..'" onClick="'..js.. '">'..name..c..'</button>'
end

-- Pull it all together
function fastnav.Widget(dir, skiplist)
  local skip = buildSkipSet(skiplist)
  local data = fetchTagAndPageData(dir)
  local tags = fastnav.TagsHtml(data, skip)
  local pages = fastnav.PagesHtml(data, skip)
  local tagsHtml = '<div class="fastnav-tags">' .. table.concat(tags, " ") .. '</div>'
  local pagesHtml = '<div class="fastnav-pages">' .. table.concat(pages, " ") .. '</div>'
  local headerHtml = "<b>Pages:</b>"..pages.length.." <b>Tags:</b>"..tags.length
  return widget.new {
    html = headerHtml..tagsHtml..pagesHtml,
    display = "block",
    cssClasses = { "fastnav-block"}
  }
end
```