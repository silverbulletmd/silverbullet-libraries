---
name: Library/silverbulletmd/Fonts/Gelasio
tags: meta/library
description: Gelasio, a free serif with Georgia's proportions that works on every device, to pick as your editor or interface font.
files:
- Gelasio/Gelasio-Variable.ttf
- Gelasio/Gelasio-Italic-Variable.ttf
- Gelasio/OFL.txt
---
**Gelasio** is an original serif by Eben Sorkin, made to be metrically compatible with Georgia: every letter takes the same width as in Georgia, in regular, bold, italic and bold italic. Its design comes from a French transitional typeface of the early 1700s, with rounded terminals that make it friendlier than its rational build suggests.

Georgia itself can't be shipped (Microsoft's license doesn't allow it), so Gelasio is the way to get a Georgia-like page on every device, including Linux and Android, where Georgia usually isn't installed. To use the Georgia that comes with macOS, Windows and iOS instead, install the [[Library/silverbulletmd/Fonts/Georgia|Georgia]] library.

Installing this library adds Gelasio to the fonts in Configuration → Appearance. Choose it as the Editor font (or Interface font) there, or in [[CONFIG]] with `config.set("fonts.editor", "gelasio")`. The font files install into your space, so it works offline and loads nothing from elsewhere; a browser only downloads a style once text uses it. Each style is one variable font file that covers every weight.

# License
Gelasio is licensed under the SIL Open Font License 1.1; the license text ships alongside the font files as `Gelasio/OFL.txt`. The files are byte for byte the project's own (only renamed, dropping the `[wght]` part that URLs handle badly) from https://github.com/google/fonts/tree/main/ofl/gelasio (Gelasio-Variable.ttf 168,556 bytes; Gelasio-Italic-Variable.ttf 174,212 bytes).

# Implementation
```space-lua
config.set("fonts.available.gelasio", {
  name = "Gelasio",
  family = "Gelasio, Georgia, serif",
  kind = "serif",
  faces = {
    { src = "Library/silverbulletmd/Fonts/Gelasio/Gelasio-Variable.ttf", weight = 400 },
    { src = "Library/silverbulletmd/Fonts/Gelasio/Gelasio-Variable.ttf", weight = 700 },
    { src = "Library/silverbulletmd/Fonts/Gelasio/Gelasio-Italic-Variable.ttf", weight = 400, style = "italic" },
    { src = "Library/silverbulletmd/Fonts/Gelasio/Gelasio-Italic-Variable.ttf", weight = 700, style = "italic" },
  },
  license = "OFL-1.1",
})
```
