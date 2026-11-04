---
name: Library/silverbulletmd/Fonts/CrimsonPro
tags: meta/library
description: Crimson Pro, an old-style book serif, to pick as your editor or interface font.
files:
- CrimsonPro/CrimsonPro-Variable.ttf
- CrimsonPro/CrimsonPro-Italic-Variable.ttf
- CrimsonPro/OFL.txt
---
**Crimson Pro** is an old-style book face in the Garamond tradition by Jacques Le Bailly, tuned for contemporary screens.

Installing this library adds Crimson Pro to the fonts in Configuration → Appearance. Choose it as the Editor font (or Interface font) there, or in [[CONFIG]] with `config.set("fonts.editor", "crimson-pro")`. The font files install into your space, so it works offline and loads nothing from elsewhere; a browser only downloads a style once text uses it. Each style is one variable font file that covers every weight.

# License
Crimson Pro is licensed under the SIL Open Font License 1.1; the license text ships alongside the font files as `CrimsonPro/OFL.txt`. The files are byte for byte the project's own (only renamed, dropping the `[wght]` part that URLs handle badly) from https://github.com/google/fonts/tree/main/ofl/crimsonpro (CrimsonPro-Variable.ttf 246,324 bytes; CrimsonPro-Italic-Variable.ttf 253,176 bytes).

# Implementation
```space-lua
config.set("fonts.available.crimson-pro", {
  name = "Crimson Pro",
  family = "'Crimson Pro', Georgia, serif",
  kind = "serif",
  faces = {
    { src = "Library/silverbulletmd/Fonts/CrimsonPro/CrimsonPro-Variable.ttf", weight = 400 },
    { src = "Library/silverbulletmd/Fonts/CrimsonPro/CrimsonPro-Variable.ttf", weight = 700 },
    { src = "Library/silverbulletmd/Fonts/CrimsonPro/CrimsonPro-Italic-Variable.ttf", weight = 400, style = "italic" },
    { src = "Library/silverbulletmd/Fonts/CrimsonPro/CrimsonPro-Italic-Variable.ttf", weight = 700, style = "italic" },
  },
  license = "OFL-1.1",
})
```
