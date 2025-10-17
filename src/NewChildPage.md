# New child page
Create quickly child page.

```space-lua
command.define {
  name = "new page",
  description = "new children page",
  key = "Alt-Ctrl-n",
  run = function()
    local pageName=editor.prompt("page name",editor.getCurrentPage().."/")
    editor.navigate(pageName)
  end
}
```


