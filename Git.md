
#meta

This library adds a basic git synchronization functionality to SilverBullet. It should be considered a successor to [silverbullet-git](https://github.com/silverbulletmd/silverbullet-git) implemented in Space Lua.

The following commands are implemented:

${widgets.commandButton("Git: Sync")}

* Adds all files in your folder to git
* Commits them with the default "Snapshot" commit message
* `git pull`s changes from the remote server
* `git push`es changes to the remote server

${widgets.commandButton("Git: Commit")}

* Asks you for a commit message
* Commits

# Configuration
There is currently only a single configuration option: `git.autoSync`. When set, the `Git: Sync` command will be run every _x_ minutes.

Example configuration:
```lua
config.set("git.autoSync", 5)
```

# Implementation
The full implementation of this integration follows.

## Configuration
```space-lua
-- priority: 100
config.define("git", {
  type = "object",
  properties = {
    autoSync = schema.number()
  }
})
```

## Commands
```space-lua
git = {}

function git.commit(message)
  message = message or "Snapshot"
  print "Comitting..."
  local ok, message = pcall(function()
    shell.run("git", {"add", "./*"})
    shell.run("git", {"commit", "-a", "-m", message})
  end)
  if not ok then
    print("Git commit failed: " .. message)
  end
end

function git.sync()
  git.commit()
  print "Pulling..."
  shell.run("git", {"pull"})
  print "Pushing..."
  shell.run("git", {"push"})
end

command.define {
  name = "Git: Commit",
  run = function()
    local message = editor.prompt "Commit message:"
    git.commit(message)
  end
}

command.define {
  name = "Git: Sync",
  run = function()
    git.sync()
    editor.flashNotification "Done!"
  end
}

```

```space-lua
-- priority: -1
local autoSync = config.get("git.autoSync")
if autoSync then
  print("Enabling git auto sync every " .. autoSync .. " minutes")

  local lastSync = 0
  
  event.listen {
    name = "cron:secondPassed",
    run = function()
      local now = os.time()
      if (now - lastSync)/60 >= autoSync then
        lastSync = now
        git.sync()
      end
    end
  }
end

```