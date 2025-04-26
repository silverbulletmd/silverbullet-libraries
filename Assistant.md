#meta #wip

AI features for SilverBullet.

Currently implemented commands:

* `AI: Chat` (bound to Cmd-Enter/Ctrl-Enter)
* `AI: Analyze With Prompt` (see below for an example)
* `AI: Suggest Page Name`: Suggest page names for the current pages (and can rename the page)

Supported providers:

* OpenAI
* Google AI

# Analyze with prompt
Create a page with the following content (`${text}` will be replace with the text of the page):

    ---
    model: gpt4
    tags: ai/prompt
    ---
    I want you to take a highly critical stance on the following document. Play devil’s advocate and challenge its arguments, assumptions, logic, and conclusions as rigorously as possible. Assume that you are an intelligent but skeptical reader looking for weaknesses, inconsistencies, missing evidence, and alternative perspectives. Where possible, highlight potential counterarguments and areas where the reasoning might be flawed or incomplete. Also, identify any vague, ambiguous, or potentially misleading statements. Be relentless in your critique, but ensure your feedback remains constructive and specific.
    
    Here is the full text of the document:
    
    ${text}

# Configuration
Example:
```lua
local openAi = assistant.openAIProvider{
  apiKey = "your-key-here"
}
config.set {
  assistant={
    models={
      gpt4 = openAi "gpt-4o",
      gpt4search = openAi "gpt-4o-search-preview",
    },
    defaultModel="gpt4"
  }
}
```

# Configuration schema
```space-lua
-- priority: 5
config.define("assistant", {
  type = "object",
  properties = {
    models = {
      type = "object",
    },
    defaultModel = {
      type="string"
    },
  },
  required={"models", "defaultModel"}
})
```

# In-page Chat
Allows user to have a chat with a model within a page. Simply write your prompt and run the `AI:Chat` command (Shift-Enter by default) to send and chat.

```space-lua
-- Reads the current page text and transforms it to a chat history table to be sent to the LLM
local function pageToHistory()
  local fm = index.extractFrontmatter(editor.getText(), {
    removeFrontmatterSection=true
  })
  local fullText = fm.text
  local history = {}
  -- Reassemble chat
  local role = "user"
  local message = ""
  for line in string.split(fullText, "\n") do
    local match = string.matchRegex(line, "^\\*\\*(\\w+):?\\*\\*\\s*(.+$)")
    if match then
      if message != "" then
        table.insert(history, {role=role, content=message})
      end
      role = match[2]
      message = match[3] + "\n"
    else
      message = message .. "\n" .. line
    end
  end
  if message != "" then
    table.insert(history, {role=role, content=message})
  end
  return history
end

local abortStreaming = false

command.define {
  name = "AI: Chat",
  key = "Shift-Enter",
  run = function()
    local iConfig = config.get("assistant")
    local meta = editor.getCurrentPageMeta()
    local modelName = meta.model or iConfig.defaultModel
    local model = iConfig.models[modelName]
    if not model then
      editor.flashNotification("Invalid model "..modelName, "error")
      return
    end
    local history = pageToHistory()

    -- Insert assistant response placeholder
    local pos = editor.getCursor() + string.len("\n\n**assistant:** ")
    editor.insertAtCursor("\n\n**assistant:** 🤔\n\n**user**: ", true)

    abortStreaming = false

    -- Call API and stream in tokens
    firstToken = true
    for token in assistant.streamChat(model, history) do
      if abortStreaming then
        print("Streaming aborted")
        return
      end
      if firstToken then
        -- Remove the 🤔
        editor.dispatch {
          changes={
            from=pos,
            to=pos + string.len("🤔")
          },
          scrollIntoView = true
        }
        firstToken = false
      end
      editor.dispatch {
        changes={
          from=pos,
          insert=token,
        },
        scrollIntoView = true
      }
      pos = pos + string.len(token)
    end
  end
}

event.listen {
  name = "editor:pageLoaded",
  run = function()
    -- Make sure that we stop streaming when we switch between pages
    abortStreaming = true
  end
}
```

# Analyze with prompt
Queries an LLM based on a selected prompt (prompts are pages tagged with `#ai/prompt`) and renders results in the RHS.

```space-lua
command.define {
  name = "AI: Analyze With Prompt",
  run = function()
    local iConfig = config.get("assistant")

    -- Find all ai prompts
    local aiPrompts = query[[from index.tag "ai/prompt"]]

    if #aiPrompts == 0 then
      editor.flashNotification("No #ai/prompt tagged prompts", "error")
      return
    end

    local selectedPrompt = editor.filterBox("Select prompt", aiPrompts, "Prompt you'd like to run against this page")

    if not selectedPrompt then
      return
    end

    -- Read prompt page and parse frontmatter
    local pageContent = space.readPage(selectedPrompt.name)
    local fm = index.extractFrontmatter(pageContent, {
      removeFrontmatterSection = true,
    })
    local frontmatter = fm.frontmatter

    -- Select model to use
    local model = iConfig.models[frontmatter.model or iConfig.defaultModel]
    if not model then
      editor.flashNotification("Invalid model "..modelName, "error")
      return
    end

    -- Instantiate template
    local tpl = template.new(fm.text)

    local renderedPrompt = tpl {
      name=editor.getCurrentPage(),
      text=editor.getText()
    }

    -- Call API and stream tokens
    updatePanel "Processing..."
    local accumulated = ""
    for token in assistant.streamText(model, renderedPrompt) do
      accumulated = accumulated .. token
      updatePanel(markdown.markdownToHtml(accumulated))
    end
  end
}

local function updatePanel(html)
  editor.showPanel("rhs", 1, [==[
    <style>
    body {
      font-family: georgia, times, serif;
      font-size: 14pt;
    }
    </style>
    ]==] .. html)
end

command.define {
  name = "AI: Hide Panel",
  run = function()
    editor.hidePanel "rhs"
  end
}
```

# AI Generated Page name recommendation

```space-lua
local namingPrompt = [[
Please suggest up to 5 appropriate note names for the note below the ---. When suggesting note names, do not suggest options longer than 40 characters.
---
]]
command.define {
  name = "AI: Suggest Page Name";
  run = function()
    local iConfig = config.get("assistant")
    local model = iConfig.models[iConfig.defaultModel]

    local suggestions = assistant.generateObject(model, namingPrompt .. editor.getText(), {
      type = "object",
      properties = {
        suggestions = {
          type = "array",
          items = { type = "string" },
        },
      }
    })
    local options = {}
    for _, suggestion in ipairs(suggestions.suggestions) do
      table.insert(options, {name=suggestion, hint="Rename"})
    end
    local choice = editor.filterBox("Page name", options, "Select the page name of your choice")
    if not choice then
      return
    end
    system.invokeFunction("index.renamePageCommand", 
      {page=choice.name})
  end
}
```

# AI SDK Wrapper
```space-lua
-- priority: 1
assistant = {}

local aiImport = "https://esm.sh/ai@4.2.9"

local function createProvider(moduleUrl, factoryName)
  return function(spec)
    return function(modelName)
      return function()
        local provider = js.import(moduleUrl)
        return provider[factoryName](spec)(modelName)
      end
    end
  end
end

assistant.googleAIProvider = createProvider("https://esm.sh/@ai-sdk/google@1.2.5", "createGoogleGenerativeAI")

assistant.openAIProvider = createProvider("https://esm.sh/@ai-sdk/openai@1.3.5", "createOpenAI")

function assistant.streamChat(model, messages)
  local ai = js.import(aiImport)
  local result = ai.streamText {
    model = model(),
    messages = messages
  }
  local iterator = js.eachIterable(result.textStream)
  return function()
    return iterator()
  end
end

function assistant.streamText(model, prompt)
  local ai = js.import(aiImport)
  local result = ai.streamText {
    model = model(),
    prompt = prompt
  }
  local iterator = js.eachIterable(result.textStream)
  return function()
    return iterator()
  end
end

function assistant.generateObject(model, prompt, schema)
  local ai = js.import(aiImport)
  local result = ai.generateObject {
    model = model(),
    prompt = prompt,
    schema = ai.jsonSchema(schema),
  }
  return result.object
end
```
