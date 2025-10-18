# Embedded editor

Create IFrame to insert editors on current page.

## Lua
```space-lua
slashcommand.define {
  name = "luaeditor",
  description= "insert lua editor",
  run = function()
tpl=[[${utilities.embedUrl("https://glot.io/new/lua","100%","1000px")}]]
  editor.insertAtCursor(tpl, false, true)
  end
}
```
## Plantuml
```space-lua
slashcommand.define {
  name = "plantumleditor",
  description= "insert plantuml editor",
  run = function()
tpl=[[${utilities.embedUrl("https://plantuml.online/uml/","100%","1000px")}]]
  editor.insertAtCursor(tpl, false, true)
  end
}
```

