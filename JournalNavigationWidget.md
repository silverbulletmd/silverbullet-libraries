# Journal Navigation Widget

Navigate Weekly/Daily Journals

⬅️ Previous | 📅 Journal/Week/2025-09-08 | Next ➡️

```space-lua

Journal = Journal or {}

local journalPath = "Journal/Week/"
local navigateDuration = 7 * 24 * 60 * 60 -- a week

-- local journalPath = "Journal/Daily/"
-- local navigateDuration = 24 * 60 * 60 -- a day

function Journal.navigateWidget(currentJournal)
    -- currentJournal should be in the format "path/year-month-day"
    local path, year, month, day = string.match(currentJournal, "(.+/)(%d+)%-(%d+)%-(%d+)")

    if not (path and year and month and day) then
        print("Invalid date format: " .. tostring(currentJournal))
        return "Invalid date format: " .. tostring(path) .. tostring(year) .. tostring(month) .. tostring(day)
    end

    local date = os.time({year = tonumber(year), month = tonumber(month), day = tonumber(day)})

    local prevWeek = os.date("%Y-%m-%d", date - navigateDuration)
    local nextWeek = os.date("%Y-%m-%d", date + navigateDuration)

    local prevWeekLink = path .. prevWeek
    local nextWeekLink = path .. nextWeek

    local link = "[[" .. prevWeekLink .. "|⬅️ Previous]] | [[" .. tostring(currentJournal) .."|📅 " .. tostring(currentJournal) .. "]] |[[" .. nextWeekLink .. "| Next ➡️]]"

    return link
end


event.listen {
  name = "hooks:renderTopWidgets", -- or hooks:renderBottomWidgets
  run = function(e)
    if not editor.getCurrentPage().startsWith(journalPath) then
        return
    end
    return widget.new {
      markdown = Journal.navigateWidget(editor.getCurrentPage())
    }
  end
}
```
