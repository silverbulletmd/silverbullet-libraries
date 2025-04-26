#meta

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