---
name: Library/silverbulletmd/Themes/Ink
tags: meta/library meta/theme
description: Ink, a calm monochrome light theme set in EB Garamond, like a printed page.
displayName: Ink
scheme: light
fonts:
  editor: eb-garamond
  editorSize: 20
requires:
- ../Fonts/EBGaramond.md
---
**Ink** is a monochrome light theme that reads like a printed book: near-black text on white, with nothing colored unless it has to be. Links are underlined in the text color, tags are quiet gray words, the top bar fades into the page, and highlights are a pale yellow marker.

Pick it in Configuration → Appearance → Theme, or with ${widgets.commandButton("Theme: Select")}. Ink is a light theme only, so Theme: Toggle Light/Dark has nothing to switch to.

Ink suggests **EB Garamond** at 20px as the editor font. Installing Ink installs the [[Library/silverbulletmd/Fonts/EBGaramond|EB Garamond]] font library for you, unless you already have it. EB Garamond stays installed when you remove Ink; remove it separately if you no longer want it. The suggestion only applies while you haven't picked an editor font or size yourself.

```space-style
html {
  /* Ink's own variables: the one ink, and a gray for faint marks and rules */
  --ink-black: #111;
  --ink-gray: #8c8c8c;

  --root-background-color: #fff;
  --root-color: var(--ink-black);
  --subtle-color: #666;
  --subtle-background-color: rgba(0, 0, 0, 0.045);
  --ui-surface-border-color: #e3e3e3;

  --ui-accent-color: var(--ink-black);
  --ui-accent-contrast-color: #fff;

  --link-color: var(--ink-black);
  --link-missing-color: var(--subtle-color);
  --link-invalid-color: #a3262a;
  --meta-color: #555;
  --meta-subtle-color: var(--ink-gray);

  --highlight-color: #fff1a6;

  --tone-success: #2e6b3d;
  --tone-success-soft: #eaf3ec;
  --tone-warning: #855100;
  --tone-warning-soft: #faf0dc;
  --tone-danger: #a3262a;
  --tone-danger-soft: #f9e5e5;
  --tone-info: #3d3d3d;
  --tone-info-soft: #f1f1f1;

  --editor-code-color: var(--subtle-color);
  --editor-code-variable-color: #1f3d5c;
  --editor-code-typename-color: #3d5a2b;
  --editor-code-string-color: #6b4a1f;
  --editor-code-number-color: #74365a;
  --editor-code-operator-color: #5e5e5e;
  --editor-code-atom-color: var(--ink-black);
  /* Comments are read, not skimmed: the faint mark gray is too light for text */
  --editor-code-comment-color: var(--subtle-color);

  /* The top bar is part of the page, not a gray band with a line under it.
     The mobile keyboard bar shares these, so it blends into the page too */
  --top-background-color: var(--root-background-color);
  --top-border-color: var(--root-background-color);
  /* The bottom panels derive their edge from the top bar's: keep a hairline */
  --editor-panels-bottom-border-color: var(--ui-surface-border-color);
  /* Links, wiki links and bare URLs alike are underlined in the text color */
  --editor-link-text-decoration: underline;

  /* Headings in full ink: the default grays them toward the subtle color */
  --editor-heading-color: var(--ink-black);
  /* A light hairline, not a dark bar */
  --editor-ruler-color: var(--ink-gray);
  /* Links are underlined text, not tinted chips */
  --editor-wiki-link-page-background-color: transparent;
  /* Tags as plain gray words: no pill */
  --editor-hashtag-color: var(--subtle-color);
  --editor-hashtag-background-color: transparent;
  --editor-hashtag-border-color: transparent;
  --editor-hashtag-border-radius: 0;
  /* A bare quote with a hairline bar, like an indented passage in a book */
  --editor-blockquote-background-color: transparent;
  --editor-blockquote-border-color: var(--ink-gray);
  /* Frontmatter on a faint gray, not tinted yellow by the highlight color */
  --editor-frontmatter-background-color: color-mix(in srgb, var(--root-background-color), var(--ink-black) 2.5%);
  /* A pale gray selection: a quarter of the black accent reads as a heavy band */
  --editor-selection-background-color: color-mix(in srgb, var(--ink-black) 14%, var(--root-background-color));
  /* The subtle gray falls under 4.5:1 on the gray selected row */
  --modal-selected-option-description-color: var(--meta-color);
  /* A light head row with ink text, not the default inverted dark band */
  --editor-table-head-background-color: color-mix(in srgb, var(--root-background-color), var(--ink-black) 6%);
  --editor-table-head-color: var(--ink-black);
}
```
