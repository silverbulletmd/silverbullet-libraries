# Search and Grep

The Search and Grep feature allows you to search for specific text in your workspace using the `rg` command-line tool. You can search for text in your notes, attachments, and any other files supported by `rg`.

To use the Search and Grep feature:
1. Open the command palette and search for "Search Recursively".
2. Enter the text you want to search for in the prompt.
3. Press Enter to initiate the search.
4. The results will be displayed in the editor.

```space-lua
-- V2
command.define {
  name = "Search Recursively",
  run = function()
    local term = editor.prompt()
    local results = rg(term)
    local selection = {}

    if results == 0 then
      return editor.flashNotification("Nothing found", "warning")
    end
    
    for result in results do
      table.insert(selection, { 
        name = result.text,
        description = result.path,
        value = result
      })
    end
    
    local result = editor.filterBox("Select:", selection, "Found: " .. #results .. " entries")
    
    if result and result.value then
      local page, count = string.gsub(result.value.path, ".md", "")
      editor.navigate({ kind = "page", page = page })
      editor.moveCursorToLine(result.value.row, result.value.column, true)
    end
  end
}

function rg(term)
  local args = {"-nb", "--type", "markdown", term}
  local found, results = pcall(shell.run, "rg", args)
  
  if found then
    local matches = string.split(results.stdout, "\n")
    local results = {}
    
    for match in matches do
      local path, row, column, text = string.match(match, "^(.-):(.-):(.-):(.+)$")
      if (path ~= nil and row ~= nil and column ~= nil and text ~= nil) then
        table.insert(results, { path = path, row = row, column = column, text = text })
      end
    end
    
    return results
  else
    return 0 
  end
end
```