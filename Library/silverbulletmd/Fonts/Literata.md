---
name: Library/silverbulletmd/Fonts/Literata
tags: meta/library
description: Literata, a serif made for long reading on screens, to pick as your editor or interface font.
files:
- Literata/Literata-Variable.ttf
- Literata/Literata-Italic-Variable.ttf
- Literata/OFL.txt
---
**Literata** was commissioned for Google Play Books and designed by TypeTogether for hours of reading on screens. It adjusts its shapes to the text size (optical sizes).

Installing this library adds Literata to the fonts in Configuration → Appearance. Choose it as the Editor font there, or in [[Library/Config]] with `config.set("fonts.editor", "literata")`. The font files install into your space, so it works offline and loads nothing from elsewhere; a browser only downloads a style once text uses it. Each style is one variable font file that covers every weight.

# License
Literata is licensed under the SIL Open Font License 1.1; the license text ships alongside the font files as `Literata/OFL.txt`. The files are byte for byte the project's own (only renamed, dropping the `[wght]` part that URLs handle badly) from https://github.com/google/fonts/tree/main/ofl/literata (Literata-Variable.ttf 955,132 bytes; Literata-Italic-Variable.ttf 902,728 bytes).

# Implementation
```space-lua
config.set("fonts.available.literata", {
  name = "Literata",
  family = "Literata, Georgia, serif",
  kind = "serif",
  faces = {
    { src = "Library/silverbulletmd/Fonts/Literata/Literata-Variable.ttf", weight = 400 },
    { src = "Library/silverbulletmd/Fonts/Literata/Literata-Variable.ttf", weight = 700 },
    { src = "Library/silverbulletmd/Fonts/Literata/Literata-Italic-Variable.ttf", weight = 400, style = "italic" },
    { src = "Library/silverbulletmd/Fonts/Literata/Literata-Italic-Variable.ttf", weight = 700, style = "italic" },
  },
  license = "OFL-1.1",
})
```
