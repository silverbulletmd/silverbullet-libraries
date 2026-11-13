---
name: Library/silverbulletmd/Fonts/JetBrainsMono
tags: meta/library
description: JetBrains Mono, a monospace font made for code, to pick as your code font.
files:
- JetBrainsMono/JetBrainsMono-Regular.woff2
- JetBrainsMono/JetBrainsMono-Bold.woff2
- JetBrainsMono/JetBrainsMono-Italic.woff2
- JetBrainsMono/JetBrainsMono-BoldItalic.woff2
- JetBrainsMono/OFL.txt
---
**JetBrains Mono** is a monospace font made for reading code, with a tall x-height and clear distinctions between similar characters. Pick it as your *code* font: it sets code, frontmatter and Lua expressions, and the column grid list markers sit on.

Installing this library adds JetBrains Mono to the fonts in Configuration → Appearance. Choose it as the Code font there, or in [[Library/Config]] with `config.set("fonts.code", "jetbrains-mono")`. The font files install into your space, so it works offline and loads nothing from elsewhere; a browser only downloads a style once text uses it.

# License
JetBrains Mono is licensed under the SIL Open Font License 1.1; the license text ships alongside the font files as `JetBrainsMono/OFL.txt`. The files are the project's own webfonts, unmodified, from https://github.com/JetBrains/JetBrainsMono/tree/master/fonts/webfonts (Regular 92,380, Bold 94,628, Italic 96,428, BoldItalic 98,684 bytes).

# Implementation
```space-lua
config.set("fonts.available.jetbrains-mono", {
  name = "JetBrains Mono",
  family = "'JetBrains Mono', ui-monospace, monospace",
  kind = "mono",
  faces = {
    { src = "Library/silverbulletmd/Fonts/JetBrainsMono/JetBrainsMono-Regular.woff2", weight = 400 },
    { src = "Library/silverbulletmd/Fonts/JetBrainsMono/JetBrainsMono-Bold.woff2", weight = 700 },
    { src = "Library/silverbulletmd/Fonts/JetBrainsMono/JetBrainsMono-Italic.woff2", weight = 400, style = "italic" },
    { src = "Library/silverbulletmd/Fonts/JetBrainsMono/JetBrainsMono-BoldItalic.woff2", weight = 700, style = "italic" },
  },
  license = "OFL-1.1",
})
```
