# Organization Chart

This library provides a way to create Plantuml Organization Chart in SilverBullet Space.

With Organization Chart, you can:
- Create a visual representation of your organizational structure
- Show the hierarchy of departments and personnel
- Include information about individuals such as their roles and contact information


```space-lua
function prettyPrint(tbl, indent)
    indent = indent or 0
    local lines = {}
    local indentStr = string.rep("  ", indent)

    table.insert(lines, indentStr .. "{")
    for k, v in pairs(tbl) do
        local key
        if type(k) == "string" then
            key = string.format('["%s"]', k)
        else
            key = "[" .. tostring(k) .. "]"
        end

        local value
        if type(v) == "table" then
            value = prettyPrint(v, indent + 1)
        elseif type(v) == "string" then
            value = '"' .. v .. '"'
        else
            value = tostring(v)
        end

        table.insert(lines, string.rep("  ", indent + 1) .. key .. " = " .. value .. ",")
    end
    table.insert(lines, indentStr .. "}")
    return table.concat(lines, "\n")
end

local function mergeTablesRecursive(t1, t2)
    for k, v in pairs(t2) do
        if type(v) == "table" and type(t1[k]) == "table"  then
            mergeTablesRecursive(t1[k], v)
        else
            t1[k] = v
        end
    end
    return t1
end

local function join(tbl, sep)
    return table.concat(tbl, sep or ", ")
end
local function cleanAndLower(str)
  if str ~= nil and #str>1 then
    local cleaned = str:gsub("[^%w]", "")
    cleaned = str:gsub(" ", "")
    return cleaned:lower()
  end
  return ""
end

local function generatePerson(uml, person, path)
    local uml = {}
    table.insert(uml, "Enterprise_Boundary( "..cleanAndLower(person.job.company).." , \""..person.job.company.."\") {")
    for i,department in ipairs(person.job.department) do
      if #department>0 then
        table.insert(uml, string.rep(" ", i*4) .."Boundary( "..cleanAndLower(department).." , \""..department.."\") {")
      end
      if i== #person.job.department then
          local cleanPerson=cleanAndLower(person.first_name.. person.last_name)
          local pathPerson=" , \"[[/"..path.."/".. person.first_name.."%20"..person.last_name.." ".. person.first_name.." " ..person.last_name.."]]\""
          local positionPerson=", \""..join(person.job.position, ", ").."\""
          local spritePerson=""
          if person.image == nil then
            person.image="https://static.wikia.nocookie.net/villains/images/4/4a/Kevin_Spacey_John_Doe_Se7en.jpeg"
            person.image_scale=0.1
          end  
          local scalePerson=0.6
          if person.image_scale ~= nil then
            scalePerson=scalePerson * person.image_scale
          end
          spritePerson=",$sprite=\"img:"..person.image.."{scale="..scalePerson.."}\""
          table.insert(uml,  string.rep(" ", i*8).."Person( ".. cleanPerson..pathPerson..positionPerson..spritePerson..")")
      end 
    end
    for i,department in ipairs(person.job.department) do
      if #department>0 then
        table.insert(uml, string.rep(" ",(#person.job.department-i+1)*4) .."}")
      end
    end
    table.insert(uml, "}")
    return table.concat(uml, "\n")
end

function children(path)
    local crumbsChildren = {}
    local mypage = path or editor.getCurrentPage()
    for page in each(table.sort(space.listPages(), compareDate)) do
        --print(mypage,page.name,string.find(page.name,mypage) )
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

function organizationChart(path)
  path = path or editor.getCurrentPage()
  local uml = {}
  table.insert(uml, "```plantuml")
  table.insert(uml, "@startuml")
  table.insert(uml, "scale 1100 width")
  --table.insert(uml, "scale 768 height") 
  table.insert(uml, "<style>")
  table.insert(uml, "root {")
  table.insert(uml, "  HyperlinkColor #00000")
  table.insert(uml, "}")
  table.insert(uml, "</style>")
  table.insert(uml, "!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Context.puml") 
  table.insert(uml, "LAYOUT_TOP_DOWN()") 
  table.insert(uml, "") 
  local liste= children(path)
  for i,pag in ipairs(liste) do
        local frontM= getFrontMatter(pag.name)
        table.insert(uml, "'"..pag.name) 
        if frontM ~= nil and frontM.person ~= nil then
          if frontM.person.inherit ~= nil then
            local frontMParent= getFrontMatter(frontM.person.inherit)
            frontM=mergeTablesRecursive(frontMParent,frontM)
            --table.insert(uml, prettyPrint(frontM))
          end
          local person = frontM.person
          --table.insert(uml, "'"..frontM.person.first_name) 
          table.insert(uml, generatePerson(uml, person,path))
        end
  end
  table.insert(uml, "")
  table.insert(uml, "@enduml")
  table.insert(uml, "```")
  table.insert(uml, "")
  local result= table.concat(uml, "\n")  
  print(result)
  return result
  --system.invokeFunction("plantuml", result)
end

slashcommand.define {
  name = "organizationchart",
  run = function()
    editor.insertAtCursor(organizationChart(), false, true)
  end
}
```

```space-lua
-- add image
person={}

function person.insertImageFromFrontmatter()  
  -- Get current page frontmatter  
  local pageText = editor.getText()  
  local fm = index.extractFrontmatter(pageText)  
  local result="No image found" 
    
  -- Check if person.image exists in frontmatter  
  local types={"person","company"}
  for row,v in ipairs(types) do
    if fm.frontmatter and fm.frontmatter[v] and fm.frontmatter[v].image then  
      local imagePath = fm.frontmatter[v].image  
      local name=""
      if types == "company" then
        name =(fm.frontmatter[v].name or "")
      else
        name=(fm.frontmatter[v].first_name or "") .. " " ..  (fm.frontmatter[v].last_name or "")
      end
        
      -- Create markdown image syntax  
      if imagePath ~= nil then 
        result =  "![" .. name .. "|x200](" .. imagePath .. ")"  
        break 
      end
    end  
  end
  return result
end
```


\${organizationChart("work/ampere-regienov/contact") }
