# SilverBullet libraries

Optional libraries maintained by the SilverBullet project, for both SilverBullet Server and Desktop. These are installed into your space, separately from the core library.

## Installation

Open **Workbench → Libraries** and add this repository:

```
https://github.com/silverbulletmd/silverbullet-libraries/blob/main/Repository/silverbulletmd.md
```

Then install **Dashboard** from the available libraries. You can also install [Dashboard](Library/silverbulletmd/Dashboard.md) directly using its GitHub URL.

## Available libraries

* [Dashboard](Library/silverbulletmd/Dashboard.md): `widgets.chip`, `widgets.bars`, `widgets.stat` and `widgets.grid`, with theme-aware styles, click handlers and usage examples. Previously bundled in core's edge builds; install this library to continue using the same API names.

## Development

Keep library pages under `Library/silverbulletmd/` and list every library in [Repository/silverbulletmd.md](Repository/silverbulletmd.md). Library pages include their documentation, `space-lua` implementation and `space-style` styles.

Tests use the real Space Lua runtime from a SilverBullet Server checkout. By default the checkout is expected at `../silverbullet` (as in the Desktop repository). For a standalone checkout, clone Server separately, install its npm dependencies, and set `SILVERBULLET_PATH` to its absolute path.

```sh
npm ci
npm test
# Or, with Server elsewhere:
SILVERBULLET_PATH=/path/to/silverbullet npm test
```

GitHub Actions runs the same suite against Server’s `main` branch on pushes and pull requests.
