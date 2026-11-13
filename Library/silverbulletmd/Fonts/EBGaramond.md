---
name: Library/silverbulletmd/Fonts/EBGaramond
tags: meta/library
description: EB Garamond, a revival of the classic Garamond serif, to pick as your editor or interface font.
files:
- EBGaramond/EBGaramond-Variable.ttf
- EBGaramond/EBGaramond-Italic-Variable.ttf
- EBGaramond/OFL.txt
---
**EB Garamond** is Georg Duffner and Octavio Pardo's revival of the Garamond serif, based on the 16th-century types of Claude Garamont. It reads like a printed book: elegant, a little formal, and easy on long text.

Its letters are small for their size, so 20px is a good editor size: `config.persist("fonts.editorSize", 20)`, or Configuration → Appearance.

Installing this library adds EB Garamond to the fonts in Configuration → Appearance. Choose it as the Editor font there, or in [[Library/Config]] with `config.set("fonts.editor", "eb-garamond")`. The font files install into your space, so it works offline and loads nothing from elsewhere; a browser only downloads a style once text uses it. Each style is one variable font file that covers every weight.

# License
EB Garamond is licensed under the SIL Open Font License 1.1 (no Reserved Font Name); the license text ships alongside the font files as `EBGaramond/OFL.txt`. The files are byte for byte the project's own (only renamed, dropping the `[wght]` part that URLs handle badly) from https://github.com/google/fonts/tree/main/ofl/ebgaramond (EBGaramond-Variable.ttf 851,176 bytes; EBGaramond-Italic-Variable.ttf 754,468 bytes).

# Implementation
```space-lua
config.set("fonts.available.eb-garamond", {
  name = "EB Garamond",
  family = "'EB Garamond', Garamond, Georgia, serif",
  kind = "serif",
  faces = {
    { src = "Library/silverbulletmd/Fonts/EBGaramond/EBGaramond-Variable.ttf", weight = 400 },
    { src = "Library/silverbulletmd/Fonts/EBGaramond/EBGaramond-Variable.ttf", weight = 700 },
    { src = "Library/silverbulletmd/Fonts/EBGaramond/EBGaramond-Italic-Variable.ttf", weight = 400, style = "italic" },
    { src = "Library/silverbulletmd/Fonts/EBGaramond/EBGaramond-Italic-Variable.ttf", weight = 700, style = "italic" },
  },
  license = "OFL-1.1",
})
```
