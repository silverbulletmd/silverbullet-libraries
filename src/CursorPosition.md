# Wikilink of cursor position

From community, get cursor position to clipboard.

```space-lua
command.define {
  name = "Cursor: Copy Reference",
  key = "Shift-Alt-c",
  run = function()
    local pageName = editor.getCurrentPage()
    local pos = editor.getCursor()
    local ref = string.format("[[%s@%d]]", pageName, pos)
    editor.copyToClipboard(ref)
    editor.flashNotification("Copied reference: " .. ref, "info")
  end
}
```