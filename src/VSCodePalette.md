
# VSCode Palette

The VSCode Palette feature allows you to search and open content items (pages, commands, etc.) quickly. You can customize the objects to populate, like page, command, etc. The palette is a unique feature that provides a quick way to navigate your content.

```space-lua
-- This script populates the VSCode palette with content items from the enabled
-- object types. The palette is a feature that allows you to search for content
-- items (pages, commands, etc.) and open them quickly.

-- Define a table to hold VSCode related configurations
local vscode = {}
vscode.enabledObjectToPopulate = {"page", "command", "header"}--, "paragraph", "item"} -- Define objects to populate, like page, command, etc.
vscode.objectSymbols = {nil, ">", "!", "*", "#"} -- Symbols associated with each object type
vscode.debug = false -- Debug flag to enable or disable debug prints

-- Function to print debug information if debug mode is enabled
local debug = function(prefix, data)
    if vscode.debug == true then 
        print(">>>>>>>>>  " .. prefix .. "     " .. data) 
    end
end

-- Function to get help information on how to use the search feature
local getHelp = function()
    -- Construct a string with instructions on how to use the search feature
    local result = "Type to search content"
    for i in pairs(vscode.enabledObjectToPopulate) do
        if vscode.objectSymbols[i] ~= nil then
            result = result .. ",  '" .. vscode.objectSymbols[i] .. "' for " ..
                         vscode.enabledObjectToPopulate[i] .. "s"
        end
    end
    debug("help", result)
    return result
end

-- Function to clean data by removing specific symbols
local clean = function(data) return string.gsub(data, "-[!>*#]", "") end

-- Function to check if it's ready to sync, based on time elapsed
local readyToSync = function()
    -- Check if the time elapsed since the last sync is greater than 30 minutes
    local currentTime = os.time()
    if currentTime - vscode.previousCheck > 30 * 60 then
        -- If it is, populate the entries table and update the last check time
        vscode.entries = populate() -- Populate entries if time condition is met
        vscode.previousCheck = os.time() -- Update the last check time
    end
end

-- Function to populate options based on enabled object types
local populate = function()
    -- Notify the user that the sync is starting
    editor.flashNotification "Starting VSCode sync. "
    local options = {}
    -- Handle page type objects
    local kind = "page"
    if table.includes(vscode.enabledObjectToPopulate, kind) then
        local pages = query [[from index.tag "page" where  not ref:startsWith("Library") order by lastModified desc ]]
        for _, item in ipairs(pages) do
            table.insert(options, {
                name = (item.text or item.name or item.page),
                description = item.page,
                ref = item.ref,
                type = kind
            })
        end
    end
    -- Handle command type objects
    kind = "command"
    if table.includes(vscode.enabledObjectToPopulate, kind) then
        local commands = system.listCommands()
        for name, def in pairs(commands) do
            if #name > 2 then
                table.insert(options, {
                    name = ">" .. name,
                    description = def.description,
                    ref = name,
                    type = kind
                })
            end
        end
    end
    -- Handle paragraph type objects
    kind = "paragraph"
    if table.includes(vscode.enabledObjectToPopulate, kind) then
        local pages = query [[from index.tag "paragraph"]]
        for _, item in ipairs(pages) do
            local id = item.text or item.name or item.page
            id = clean(id)
            if #id > 1 then
                table.insert(options, {
                    name = "#" .. id,
                    description = item.page,
                    ref = item.ref,
                    type = kind
                })
            end
        end
    end
    -- Handle header type objects
    kind = "header"
    if table.includes(vscode.enabledObjectToPopulate, type) then
        local pages =
            query [[from index.tag "header" where  not ref:startsWith("Library") order by lastModified desc ]]
        for _, item in ipairs(pages) do
            local id = item.text or item.name or item.page
            id = clean(id)
            if #id > 1 then
                table.insert(options, {
                    name = "!" .. id,
                    description = item.page,
                    ref = item.ref,
                    type = kind
                })
            end
        end
    end
    -- Handle item type objects
    kind = "item"
    if table.includes(vscode.enabledObjectToPopulate, kind) then
        local pages = query [[from index.tag "item"]]
        for _, item in ipairs(pages) do
            local id = item.text or item.name or item.page
            id = clean(id)
            if #id > 1 then
                table.insert(options, {
                    name = "*" .. id,
                    description = item.page,
                    ref = item.ref,
                    type = kind
                })
            end
        end
    end
    -- Notify the user that the sync is complete
    local txt = "VSCode done (" .. vscode.enabledObjectToPopulate .. ")"
    editor.flashNotification(txt, "info")
    debug("option", options)
    return options
end

event.listen {
    name = "editor:pageCreating",
    run = function()
     readyToSync()
    end
}
event.listen {
    name = "cron:secondPassed",
    run = function()
     readyToSync()
    end
}


vscode.entries = populate() -- Populate entries if time condition is met
vscode.previousCheck = os.time() -- Update the last check time

-- Define a command to open the VSCode palette
command.define {
    name = "VSCode Palette",
    description = "palette llike VSCode",
    key = "Ctrl-p",
    priority =1,
    run = function()
        -- Get the help string for the search feature
        local help = getHelp()
        -- Filter the entries table based on the user's input
        if vscode.entries ~=nil then
          local selected = editor.filterBox("🎨", vscode.entries, help)
          debug("selected", selected)
          if selected then
              -- If the user selected a command, invoke it
              if selected.type == "command" then
                  system.invokeCommand(selected.ref)
              else
                  -- Otherwise, navigate to the selected page
                  editor.navigate(selected.ref)
              end
          end
      end
    end
}
```