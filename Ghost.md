#meta/library

Implements [[^Library/Std/Export]] for [Ghost](https://ghost.org/). Currently only posts are supported.

# Config example
You need to create a Custom Integration key for this. Go to your Ghost admin panel > Advanced > Ingegrations > Custom > Add custom integration. Generate one, then copy the Admin API key and create a config somewhere in your SilverBullet space with `space-lua`:
```lua
config.set {
  ghost = {
    blog = {
      url = "https://xxx.ghost.io",
      key = "xxx"
    }
  }
}
```

# Publishing a post
You can now publish any page as a Ghost post using the `Export: Page or Selection` (Cmd-e/Ctrl-e) command. The only thing you need to do is set a `slug` key in your front matter (this slug will later also be used to determine if a post needs to be updated or created).

# Implementation
Sadly, the JavaScript Ghost Admin library doesn’t seem to work in the browser, therefore we have to fall back to custom implemented API calls.

```space-lua
ghost = {}

-- Convert hex string to byte array
local function fromHex(hexString)
  local bytes = {}
  
  for i = 1, #hexString, 2 do
      local byteValue = tonumber(hexString:sub(i, i + 1), 16)
      table.insert(bytes, byteValue)
  end
  return js.new(js.window.Uint8Array, bytes)
end

-- Generate JWT with the jose library
local function genToken(key)
  local jose = js.import "https://esm.sh/jose@6.0.10"

  local pieces = string.split(key, ":")

  local jwt = js.new(jose.SignJWT, {
    ['urn:example:claim'] = true
  }).setProtectedHeader({ alg = 'HS256', kid = pieces[1] })
    .setIssuedAt()
    .setAudience('/admin/')
    .setExpirationTime('5m')
    .sign(fromHex(pieces[2]))

  return jwt
end

-- Authenticated admin Ghost request
local function authenticatedRequest(cfg, path, method, body)
  local token = genToken(cfg.key)
  return http.request(cfg.url .. path, {
    method = method,
    headers = {
      Authorization = "Ghost " .. token,
      ["Content-Type"] = "application/json",
      Origin = cfg.url,
      ["Accept-Version"] = "v5.0"
    },
    body = body
  })
end

-- Create lexical object for markdown
local function markdownToLexical(text)
  return js.window.JSON.stringify {
    root = {
      children = {
        {
          type = "markdown",
          version = 1,
          markdown = text,
        }
      },
      direction = nil,
      format = "",
      indent = 0,
      type = "root",
      version = 1,
    }
  }
end

-- Export discovery
event.listen {
  name = "export:discover",
  run = function(event)
    local publishers = {}
    for name, cfg in pairs(config.get("ghost")) do
      -- We're going to offer one option per site
      table.insert(publishers, {
        -- encoding the site id in the event name
        id = "ghost-post::"..name,
        name = "Ghost: " .. name .. ": Post"
      })
    end
    if #publishers > 0 then
      return publishers
    end
  end
}

event.listen {
  name = "export:run:ghost-post::*",
  run = function(event)
    -- Extract Ghost config
    local cfgName = event.name:split("::")[2]
    local cfg = config.get("ghost")[cfgName]
    if not cfg then
      error("Could not find config")
    end
    -- Parse frontmatter: 'title' (optional) and 'slug'
    local pageName = editor.getCurrentPage()
    local pageNameBits = pageName:split("/")
    local title = pageNameBits[#pageNameBits]
    local text = editor.getText()
    local fm = index.extractFrontmatter(text, {
      removeFrontMatterSection=true
    })
    local frontmatter = fm.frontmatter
    text = fm.text
    title = title or frontmatter.title
    local id = frontmatter.id
    local slug = frontmatter.slug
    if not slug then
      editor.flashNotification("Please set the 'slug' key in your frontmatter", "error")
      return
    end
    -- Let's check if this posts was already created
    local r = authenticatedRequest(cfg, "/ghost/api/admin/posts/slug/" .. slug .. "/", "GET")
    if r.status == 404 then
      -- Doesn't exist yet, let's create
      local r = authenticatedRequest(cfg, "/ghost/api/admin/posts/", "POST", {
        posts = {{
          title = title,
          slug = slug,
          lexical = markdownToLexical(text),
          status = "draft"
        }}
      })
      if r.ok then
        editor.flashNotification "Created post successfully"
      else
        editor.flashNotification("Failed to create post, check logs", "error")
        js.log("Error", r)
      end
    else
      -- Existing post, let's update
      local oldPost = r.body.posts[1]
      local updatedAt = oldPost.updated_at
      local r = authenticatedRequest(cfg, "/ghost/api/admin/posts/" .. oldPost.id, "PUT", {
        posts = {{
          title = title,
          slug = slug,
          lexical = markdownToLexical(text),
          updated_at = updatedAt
        }}
      })
      if r.ok then
        editor.flashNotification "Updated post successfully"
      else
        editor.flashNotification("Failed to update post, check logs", "error")
        js.log("Error", r)
      end
    end
  end
}

```
