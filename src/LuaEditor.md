
```space-lua
slashcommand.define {
  name = "luaeditor",
  description= "insert lua editor",
  run = function()
tpl=[[${embed.url("https://glot.io/new/lua","100%","800px")}]]
  editor.insertAtCursor(tpl, false, true)
  end
}

slashcommand.define {
  name = "plantumleditor",
  description= "insert plantuml editor",
  run = function()
tpl=[[${embed.url("https://plantuml.online/uml/","100%","800px")}]]
  editor.insertAtCursor(tpl, false, true)
  end
}
```


```space-lua
function embed.url(specOrUrl,w,h) 
  local width = w or "100%"
  local height = h or "400px"
  return widget.html(dom.iframe {
    src=specOrUrl,
    style="width: " .. width .. "; height: " .. height
  })
end
```

