# Formatter

Format entire document or selected text with `Editor: Format` command.

Uses [Prettier](https://prettier.io/) under the hood.

A plug [silverbullet-formatter](https://github.com/LogeshG5/silverbullet-formatter) is also available for the same.

```space-lua
formatter = formatter or {}

local prettier = js.import("https://cdn.jsdelivr.net/npm/prettier@3.6.2/standalone/+esm")
local prettierMarkdown = js.import("https://cdn.jsdelivr.net/npm/prettier@3.6.2/plugins/markdown/+esm")

function formatter.formatText(text)
  return prettier.format(text, { parser = 'markdown', plugins =  { prettierMarkdown } })
end

function formatter.cleanupLLMText()
  contents = editor.getText()
  contents = string.gsub(contents, "\\%. ", ". ")
  contents = string.gsub(contents, "%* %[ %] ", "- [ ] ")
  contents = string.gsub(contents, "%* %[x%] ", "- [x] ")
  contents = string.gsub(contents, "\\%[", "[")
  contents = string.gsub(contents, "\\%]", "]")
  contents = string.gsub(contents, ":%*%*", "**:")
  editor.setText(contents)
end

function formatter.formatDocument()
  local text = editor.getText()
  local formattedText = formatter.formatText(text)
  editor.setText(formattedText)
end

function formatter.formatSelection()
  local selection = editor.getSelection()
  if selection.from == selection.to then
    return
  end
  local text = editor.getText()
  local selectedText = text.slice(selection.from, selection.to)
  local formattedText = formatter.formatText(selectedText)
  formattedText = text.substring(0, selection.from) + formattedText.slice(0, -1) + text.substring(selection.to)
  editor.setText(formattedText)
end

function formatter.formatContext()
  formatter.cleanupLLMText()
  local selection = editor.getSelection()
  if selection.from != selection.to then
    formatter.formatSelection()
  else
    formatter.formatDocument()
  end
end

function formatter.formatAndSave()
  formatter.formatContext()
  editor.save()
  editor.flashNotification "Formatted & Saved!"
end

command.define {
  name = "Editor: Format",
  run = formatter.formatContext,
}

command.define {
  name = "Save document (with Formatting)",
  -- key = "Ctrl-s",
  run = formatter.formatAndSave,
}
```
