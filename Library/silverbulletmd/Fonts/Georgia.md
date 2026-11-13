---
name: Library/silverbulletmd/Fonts/Georgia
tags: meta/library
description: Georgia, the screen serif that comes with macOS, Windows and iOS, to pick as your editor or interface font.
---
**Georgia** is Matthew Carter's serif for Microsoft, drawn in the 1990s to read well on screens. Its sturdy shapes and old-style numbers have made it a long-time favorite for writing on the web.

This library ships no font files: Georgia's license doesn't allow it to be passed on. It uses the copy installed with macOS, Windows and iOS. On a device without Georgia, such as most Linux and Android systems, the editor falls back to the browser's default serif. For a Georgia-like page everywhere, install the [[Library/silverbulletmd/Fonts/Gelasio|Gelasio]] library instead: a free font with the same letter widths.

Installing this library adds Georgia to the fonts in Configuration → Appearance. Choose it as the Editor font there, or in [[Library/Config]] with `config.set("fonts.editor", "georgia")`.

# Implementation
```space-lua
config.set("fonts.available.georgia", {
  name = "Georgia",
  family = "Georgia, serif",
  kind = "serif",
})
```
