---
tags: meta/theme
displayName: Paper
description: Brown ink on warm off-white paper, with a muted red accent.
scheme: light
counterpart: "[[Library/silverbulletmd/Themes/Paper/Night]]"
fonts:
  editor: lora
---
The light half of [[Library/silverbulletmd/Themes/Paper]].

```space-style
html {
  /* Paper's own variables: the ink and the hairline rules drawn with it */
  --paper-ink: #3b2f25;
  --paper-rule: #e4d9c6;

  --root-background-color: #faf6ee;
  --root-color: var(--paper-ink);
  --subtle-color: #74644f;
  --subtle-background-color: rgba(120, 88, 50, 0.08);
  --ui-surface-border-color: var(--paper-rule);

  --ui-accent-color: #a8432f;
  --ui-accent-contrast-color: #fdf8f1;

  --link-color: #963a27;
  --link-missing-color: #8f5a14;
  --link-invalid-color: #9b3fa6;
  --meta-color: #6e4a2a;

  --highlight-color: rgba(240, 196, 80, 0.45);

  --tone-success: #4c6f2e;
  --tone-success-soft: #ebeed9;
  --tone-warning: #8f5a14;
  --tone-warning-soft: #f6e8cc;
  --tone-danger: #a3302a;
  --tone-danger-soft: #f6e0d8;
  --tone-info: #3a6378;
  --tone-info-soft: #e3ebea;

  --editor-code-variable-color: #2d5f66;
  --editor-code-typename-color: #5f6f2a;
  --editor-code-string-color: #7a4a7a;
  --editor-code-number-color: #8f5a14;
  --editor-code-operator-color: #7d6d5b;
  --editor-code-atom-color: #a8432f;
  /* Comments are read, not skimmed: the faint markup color is too light on paper */
  --editor-code-comment-color: var(--subtle-color);

  /* Headings in full ink: the default grays them toward the subtle color */
  --editor-heading-color: var(--paper-ink);
  /* Thin rules in the paper's own hairline, not a dark gray bar */
  --editor-ruler-color: var(--paper-rule);
  --editor-blockquote-border-color: color-mix(in srgb, var(--paper-rule), var(--paper-ink) 25%);
  /* A tinted head row like a printed table, not the default inverted dark band */
  --editor-table-head-background-color: color-mix(in srgb, var(--root-background-color), var(--paper-rule) 75%);
  --editor-table-head-color: var(--paper-ink);
  /* Tags as soft, round accent-tinted pills instead of solid ones */
  --editor-hashtag-background-color: color-mix(in srgb, var(--ui-accent-color) 11%, var(--root-background-color));
  --editor-hashtag-color: #8a3523;
  --editor-hashtag-border-color: color-mix(in srgb, var(--ui-accent-color) 28%, var(--root-background-color));
  --editor-hashtag-border-radius: 1em;
}
```
