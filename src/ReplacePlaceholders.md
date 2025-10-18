---
replace: 
  t:  text 
  d: demonstration
---

# Replace Placeholders

The Replace Placeholders feature allows you to easily replace placeholders in your markdown content with specific values. You can use placeholders to customize your content dynamically.

To use the Replace Placeholders feature:
1. Add a YAML frontmatter block to the top of your markdown content.
2. Define the placeholders you want to replace in the frontmatter block using the \`replace\` key.
3. Use the placeholders in your markdown content by enclosing them in double underscores (e.g., `_placeholder_`).
4. Run the Replace Placeholders command to replace the placeholders with the specified values.

Note: The Replace Placeholders feature replaces placeholders in the entire markdown content of the current page.

Example:

_d_ with this _t_ will be transformed to `demonstration with this text`


```space-lua
local function replaceValue(content, tags)
  local c= content
  for k, v in pairs(tags) do
    local key="_"..k.."_"
    c=c:gsub(key, v)
  end
  return c
end

local function getParent(path)
    local parent = path:match("^(.*)/[^/]+$")
    return parent
end

local function getMeta(name)
  local tagsToReplace= index.extractFrontmatter(space.readPage(name)).frontmatter--space.getPageMeta(name)
  local parent = getParent(name)
  if (tagsToReplace == nil or (tagsToReplace ~=nil and   tagsToReplace["replace"] ==nil)) and parent ~=nil then 
    tagsToReplace = getMeta(parent)
  end
  if tagsToReplace ~=nil and tagsToReplace["replace"] ~=nil then 
    return tagsToReplace
  end
end


command.define {
  name = "Replace token",
  run = function()
    local pageName=editor.getCurrentPage()
    local tagsToReplace=getMeta(pageName)
    if tagsToReplace ~=nil then
      local content= space.readPage(pageName)
      local result=replaceValue(content, tagsToReplace["replace"])  
      space.writePage(pageName, result)
      editor.navigate(pageName)
    else
      print("Nothing to replace")
    end
  end
}
```



