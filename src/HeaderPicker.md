# Header Pick 

From community, move directly to the selected header.


```space-lua
local function headingsPicker(options)

  local text = editor.getText()
  local pageName = editor.getCurrentPage()
  local parsedMarkdown = markdown.parseMarkdown(text)

  -- Collect all headers
  local headers = {}
  for topLevelChild in parsedMarkdown.children do
    if topLevelChild.type then
      local headerLevel = string.match(topLevelChild.type, "^ATXHeading(%d+)")
      if headerLevel then
        local text = ""
        table.remove(topLevelChild.children, 1)
        for child in topLevelChild.children do
          text = text .. string.trim(markdown.renderParseTree(child))
        end

        if text != "" then
          table.insert(headers, {
            name = string.rep("⠀⠀", headerLevel-1) .. " 🔹 " .. text,
            pos = topLevelChild.from,
            description = "",
          })
        end
      end
    end
  end

    local result = editor.filterBox("Select:", headers, "Headers")

    if result and result.pos then
      editor.moveCursor(result.pos, true)
    end
end


command.define {
  name = "Headers: select",
  key = "Ctrl-r",
  run = function() headingsPicker({}) end
}
```