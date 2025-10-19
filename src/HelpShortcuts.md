# Help: Shortcuts
Display helper on demand.

```space-lua
command.define {
  name = "Help: shortcuts",
  key = "Ctrl-h",
  run = function()
    local messages={ "ctrl+r: search header", "ctrl+s: search everywhere","ctrl+p: vscode palette","shift+alt+c:  cursor position","alt+ctrl+n: new page", "alt+c: magneto"}
    for i in pairs(messages) do
      editor.flashNotification(messages[i], "info")
    end
  end
}
```