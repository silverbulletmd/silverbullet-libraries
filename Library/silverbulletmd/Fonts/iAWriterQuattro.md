---
name: Library/silverbulletmd/Fonts/iAWriterQuattro
tags: meta/library
description: iA Writer Quattro, the proportional sibling of iA Writer Mono, to pick as your editor or interface font.
files:
- iAWriterQuattro/iAWriterQuattroS-Regular.woff2
- iAWriterQuattro/iAWriterQuattroS-Bold.woff2
- iAWriterQuattro/iAWriterQuattroS-Italic.woff2
- iAWriterQuattro/iAWriterQuattroS-BoldItalic.woff2
- iAWriterQuattro/LICENSE.md
---
**iA Writer Quattro** is the proportional member of the iA Writer family by Information Architects, built on IBM Plex. Its letters have four widths instead of mono's one, so it keeps the even, typewriter-like rhythm of iA Writer Mono (SilverBullet's default font) while setting text more tightly. It suits you if you like the default but want prose to read less like code.

Installing this library adds iA Writer Quattro to the fonts in Configuration → Appearance. Choose it as the Editor font (or Interface font) there, or in [[CONFIG]] with `config.set("fonts.editor", "ia-writer-quattro")`. The font files install into your space, so it works offline and loads nothing from elsewhere; a browser only downloads a style once text uses it.

# License
iA Writer Quattro is licensed under the SIL Open Font License 1.1, with Reserved Font Names “iA Writer” and “Plex”; the license text ships alongside the font files as `iAWriterQuattro/LICENSE.md`. The files are byte for byte iA's own webfonts from https://github.com/iaolo/iA-Fonts/tree/master/iA%20Writer%20Quattro/Webfonts (Regular 44,416 bytes; Bold 45,252; Italic 41,152; Bold Italic 41,616).

# Implementation
```space-lua
config.set("fonts.available.ia-writer-quattro", {
  name = "iA Writer Quattro",
  family = "'iA Writer Quattro', system-ui, sans-serif",
  kind = "sans",
  faces = {
    { src = "Library/silverbulletmd/Fonts/iAWriterQuattro/iAWriterQuattroS-Regular.woff2", weight = 400 },
    { src = "Library/silverbulletmd/Fonts/iAWriterQuattro/iAWriterQuattroS-Bold.woff2", weight = 700 },
    { src = "Library/silverbulletmd/Fonts/iAWriterQuattro/iAWriterQuattroS-Italic.woff2", weight = 400, style = "italic" },
    { src = "Library/silverbulletmd/Fonts/iAWriterQuattro/iAWriterQuattroS-BoldItalic.woff2", weight = 700, style = "italic" },
  },
  license = "OFL-1.1",
})
```
