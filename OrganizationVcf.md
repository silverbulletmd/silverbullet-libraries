# Organization Contacts in VCard format

This library provides a way to export your SilverBullet Space organization contacts in VCard format. VCard is a standard format for electronic business cards.

With Organization Contacts in VCard format, you can:
- Export your organization contacts in a standardized format
- Share your contacts with other people or applications
- Import your contacts into other applications or services that support VCard format

```space-lua
local function join(tbl, sep)
    return table.concat(tbl, sep or ", ")
end

local function cleanAndLower(str)
  if str ~= nil and #str>1 then
    local cleaned = str:gsub("[^%w]", "")
    cleaned = str:gsub(" ", "")
    cleaned = str:gsub("[éè]", "e")
    return cleaned:lower()
  end
  return ""
end

local function generatePerson(source, person, path)
    local uml={}
    table.insert(uml, "BEGIN:VCARD")
    table.insert(uml, "VERSION:3.0")
    table.insert(uml, "FN:"..person.first_name.." "..person.last_name)
    table.insert(uml, "EMAIL;TYPE=INTERNET;TYPE=WORK:"..cleanAndLower(person.first_name).."."..cleanAndLower(person.last_name).."@scopandco.fr")
    table.insert(uml, "END:VCARD") 
    return table.concat(uml, "\n")
end

function children(path)
    local crumbsChildren = {}
    local mypage = path or editor.getCurrentPage()
    for page in each(table.sort(space.listPages(), compareDate)) do
        if (string.find(page.name,mypage) and mypage ~= page.name)
        then
              table.insert(crumbsChildren, {name = page.ref})
        end
    end
    return crumbsChildren
end

function getFrontMatter(page)
    return index.extractFrontmatter(space.readPage(page)).frontmatter
end 

function organizationVcf(path)
  path = path or editor.getCurrentPage()
  local uml = {}
  local liste= children(path)
  for i,pag in ipairs(liste) do
        local frontM= getFrontMatter(pag.name)
        if frontM ~= nil and frontM.person ~= nil then
          local person = frontM.person
          table.insert(uml, generatePerson(uml, person,path))
        end
  end
  table.insert(uml, "")
  local result= table.concat(uml, "\n")  
  print(result)
  return result
end

slashcommand.define {
  name = "organizationvcf",
  run = function()
    editor.insertAtCursor(organizationVcf("work/scopandco/contact"), false, true)
  end
}
```
${children("work/scopandco/contact")}
