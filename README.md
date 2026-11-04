# SilverBullet libraries

Optional libraries maintained by the SilverBullet project, for both SilverBullet Server and Desktop. These are installed into your space, separately from the core library.

## Installation

Open **Workbench → Libraries** and add this repository:

```
github:silverbulletmd/silverbullet-libraries@main/Repository/SilverBulletMD.md
```

Then install **Dashboard** from the available libraries. You can also install [Dashboard](Library/silverbulletmd/Dashboard.md) directly using this URI:

```
github:silverbulletmd/silverbullet-libraries@main/Library/silverbulletmd/Dashboard.md
```

## Available libraries

* [Dashboard](Library/silverbulletmd/Dashboard.md): `widgets.chip`, `widgets.bars`, `widgets.stat` and `widgets.grid`, with theme-aware styles, click handlers and usage examples. Previously bundled in core's edge builds; install this library to continue using the same API names.
* [iA Writer Quattro](Library/silverbulletmd/Fonts/iAWriterQuattro.md): the proportional sibling of iA Writer Mono, for the editor or interface. Adds it to Configuration → Appearance; SIL Open Font License, files included.
* [Georgia](Library/silverbulletmd/Fonts/Georgia.md): the screen serif that comes with macOS, Windows and iOS, for the editor or interface. Adds it to Configuration → Appearance; uses the installed copy, no files included (Georgia's license doesn't allow it).
* [Gelasio](Library/silverbulletmd/Fonts/Gelasio.md): a free serif with Georgia's proportions that works on every device, for the editor or interface. Adds it to Configuration → Appearance; SIL Open Font License, files included.
* [Lora](Library/silverbulletmd/Fonts/Lora.md): a serif with brushed, calligraphic curves, for the editor or interface. Adds it to Configuration → Appearance; SIL Open Font License, files included.
* [Literata](Library/silverbulletmd/Fonts/Literata.md): a serif made for long reading on screens, for the editor or interface. Adds it to Configuration → Appearance; SIL Open Font License, files included.
* [Crimson Pro](Library/silverbulletmd/Fonts/CrimsonPro.md): an old-style book serif, for the editor or interface. Adds it to Configuration → Appearance; SIL Open Font License, files included.
* [JetBrains Mono](Library/silverbulletmd/Fonts/JetBrainsMono.md): a monospace font made for code, for the code font. Adds it to Configuration → Appearance; SIL Open Font License, files included.

## Development

Keep library pages under `Library/silverbulletmd/` and list every library in [Repository/SilverBulletMD.md](Repository/SilverBulletMD.md). Library pages include their documentation, `space-lua` implementation and `space-style` styles.
