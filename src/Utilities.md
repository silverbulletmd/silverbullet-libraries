```space-lua

s=s or {}

-- Convert meeting note title
function s.getmeetingTitle()
  local t=string.split(string.split(editor.getCurrentPage(),"/")[#string.split(editor.getCurrentPage(),"/")],"_")
  table.remove(t,1)
  t=table.concat(t, " ")
  return t
end
```

