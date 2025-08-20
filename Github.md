

#meta

[[^Library/Std/Import]] and [[^Library/Std/Export]] support for [Github repo files](https://github.com/).

# Configuration
If you only want to _import_ from Github URLs, no configuration is required.

To _export_ got a Github repo, you need to get a [personal Github token](https://github.com/settings/personal-access-tokens) (with repo permissions). Configure your token somewhere in Space Lua (use a `space-lua` block), ideally a `SECRETS` page. This configuration is shared with [[^Library/Std/Gist]].

```lua
config.set("github.token", "your token")
```

In addition, you need to configure a name and email that will be part of the commit:

```lua
config.set("github.name", "John Doe")
config.set("github.email", "john@doe.com")
```

# Implementation

## Constants
```space-lua
-- priority: 50
github = {
  fmUrlKey = "githubUrl",
}
```

## Import
```space-lua
-- Import discovery
event.listen {
  name = "import:discover",
  run = function(event)
    local url = event.data.url
    if github.extractData(url) then
      return {
        {
          id = "github-file",
          name = "Github file"
        },
      }
    end
  end
}

-- Gist export implementation
event.listen {
  name = "import:run:github-file",
  run = function(event)
    local url = event.data.url
    local repo, branch, path = github.extractData(url)
    local oldContent = githubGist.request("https://api.github.com/repos/" .. repo .. "/contents/" .. path .. "?ref=" .. branch, "GET")
    if not resp.ok then
      editor.flashNotification("Failed, see console for error")
      js.log("Error", resp)
      return
    end
    local files = resp.body.files
    for filename, meta in pairs(files) do
      if filename:endsWith(".md") then
        -- Fetch the content
        local content = http.request(meta.raw_url).body
        local fm = index.extractFrontmatter(content)
        local suggestedPath = filename:gsub("%.md$", "")
        if table.includes(fm.frontmatter.tags, "meta") then
          -- Maybe more of a library function
          suggestedPath = "Library/" .. suggestedPath
        end
        local localPath = editor.prompt("Save to", suggestedPath)
        if not localPath then
          return
        end
        if space.fileExists(localPath .. ".md") then
          editor.flashNotification("Page already exists, won't do that", "error")
          return
        end
        space.writePage(localPath, content)
        editor.flashNotification("Imported to " .. localPath)
        editor.navigate({kind="page", page=localPath})
        local updated = index.patchFrontmatter(editor.getText(),
        {
          {op="set-key", path="source", value="github-gist"},
          {op="set-key", path=githubGist.fmUrlKey, value=resp.body.html_url},
          {op="set-key", path=githubGist.fmFileKey, value=filename},
        })
        editor.setText(updated)
      end
    end
  end
}
```

## Export
```space-lua
-- returns (something/bla, branch, path)
function github.extractData(url)
  if url == nil then
    return nil
  end
  return url:match("github%.com/([^/]+/[^/]+)/[^/]+/([^/]+)/(.+)")
end

function github.buildUrl(repo, path)
  return "https://api.github.com/repos/" .. repo .. "/contents/" .. path
end

function github.buildUrlWithBranch(repo, branch, path)
  return github.buildUrl(repo, path) .. "?ref=" .. branch
end

-- Export discovery
event.listen {
  name = "export:discover",
  run = function(event)
    return {
      {
        id = "github-file",
        name = "Github file"
      },
    }
  end
}

-- Gist export implementation
event.listen {
  name = "export:run:github-file",
  run = function(event)
    -- Extract any existing gist URLs
    local text = event.data.text
    local fm = index.extractFrontmatter(text, {
      removeKeys = {github.fmUrlKey},
    })
    if not config.get("github.token") then
      editor.flashNotification("github.token needs to be set", "error")
      return
    end
    local repo, branch, path = github.extractData(fm.frontmatter[github.fmUrlKey])
    local sha = nil -- will be set for existing files
    if not repo then
      -- Not there? This will be a new file
      repo = editor.prompt "Github repo (user/repo):"
      if not repo then
        return
      end
      branch = editor.prompt("Branch:", "main")
      if not branch then
        return
      end
      path = editor.prompt("File path:", editor.getCurrentPage() .. ".md")
      if not path then
        return
      end
    else
      -- We did find an existing file, let's fetch it to get the SHA
      local oldContent = githubGist.request(github.buildUrlWithBranch(repo, branch, path), "GET")
      if not oldContent.ok then
        editor.flashNotification("Could not fetch existing file", "error")
        return
      end
      sha = oldContent.body.sha
    end
    -- Ask for a commit message
    local message = editor.prompt("Commit message:", "Commit")
    -- Check the configuration
    local name = config.get("github.name")
    local email = config.get("github.email")
    if not name or not email then
      editor.flashNotification("github.name and github.email need to be configured", "error")
      return
    end
    -- Push the change
    local resp = githubGist.request(github.buildUrl(repo, path), "PUT", {
      message = message,
      committer = {
        name = name,
        email = email
      },
      branch = branch,
      sha = sha,
      content = encoding.base64Encode(fm.text)
    })
    if resp.ok then
      editor.flashNotification "Published file successfully"
      local url = "https://github.com/" .. repo .. "/blob/" .. branch .. "/" .. path
      local updated = index.patchFrontmatter(editor.getText(),
      {
        {op="set-key", path=github.fmUrlKey, value=url}
      })
      editor.setText(updated)
      editor.flashNotification "Done!"
    else
      editor.flashNotification("Error, check console")
      js.log("Error", resp)
    end
  end
}
```