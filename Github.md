---
githubUrl: https://github.com/silverbulletmd/silverbullet-libraries/blob/main/Github.md
---

#meta

[[^Library/Std/Import]] and [[^Library/Std/Export]] support for [Github repo files](https://github.com/).

# Configuration
If you only want to _import_ from Gist URLs, no configuration is required.

To _export_ gists, you need to get a [personal Github token](https://github.com/settings/personal-access-tokens) (with at least Gist permissions). Configure your token somewhere in Space Lua (use a `space-lua` block):

```lua
config.set("github.token", "your token")
```

# Implementation: constants
```space-lua
-- priority: 50
github = {
  fmUrlKey = "githubUrl"
}
```

# Import implementation
```space-lua
-- Import discovery
event.listen {
  name = "import:discover",
  run = function(event)
    local url = event.data.url
    if githubGist.extractGistId(url) then
      return {
        {
          id = "github-gist",
          name = "Gist"
        },
      }
    end
  end
}

-- Gist export implementation
event.listen {
  name = "import:run:github-gist",
  run = function(event)
    local url = event.data.url
    local gistUrl = githubGist.extractGistId(url)
    local resp = http.request("https://api.github.com/gists/" .. gistUrl, {
      headers = {
        Accept = "application/vnd.github.v3+json"
      }
    })
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

# Export implementation
```space-lua
-- Utility functions
-- returns something/bla and path
function github.extractData(url)
  return url:match("github%.com/([^/]+/[^/]+)/[^/]+/[^/]+/(.+)")
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
      removeKeys = {githubGist.fmUrlKey, githubGist.fmFileKey}
    })
    local repo, path = github.extractData(fm.frontmatter[github.fmUrlKey])
    local sha = nil -- will be set for existing files
    if not repo then
      -- Not there? This will be a new file
      repo = editor.prompt "Github repo (user/repo):"
      if not repo then
        return
      end
      path = editor.prompt "File path (something.md):"
      if not path then
        return
      end
    else
      -- We did find an existing file, let's fetch it to get the SHA
      local oldContent = githubGist.request("https://api.github.com/repos/" .. repo .. "/contents/" .. path, "GET")
      if not oldContent.ok then
        editor.flashNotification("Could not fetch existing file", "error")
        return
      end
      sha = oldContent.body.sha
    end
    local resp = githubGist.request("https://api.github.com/repos/" .. repo .. "/contents/" .. path, "PUT", {
      message = "Commit",
      committer = {
        name = "Zef Hemel",
        email = "zef@zef.me"
      },
      sha = sha,
      content = encoding.base64Encode(text)
    })
    if resp.ok then
      editor.flashNotification "Published file successfully"
      local updated = index.patchFrontmatter(editor.getText(),
      {
        {op="set-key", path=github.fmUrlKey, value=resp.body.html_url},
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