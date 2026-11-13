---
tags: meta/theme
displayName: Paper Night
description: Warm cream ink on dark brown paper, with a soft terracotta accent.
scheme: dark
counterpart: "[[Library/silverbulletmd/Themes/Paper/Light]]"
fonts:
  editor: lora
---
The dark half of [[Library/silverbulletmd/Themes/Paper]].

```space-style
html {
  /* Paper's own variables: the ink and the hairline rules drawn with it */
  --paper-ink: #e8dfd2;
  --paper-rule: #3b332b;

  --root-background-color: #1f1b17;
  --root-color: var(--paper-ink);
  --subtle-color: #a39584;
  --subtle-background-color: rgba(232, 200, 160, 0.06);
  --ui-surface-border-color: var(--paper-rule);

  --ui-accent-color: #e08a6c;
  --ui-accent-contrast-color: #1f1b17;

  --link-color: #eaa286;
  --link-missing-color: #d9a55a;
  --link-invalid-color: #c98bd6;
  --meta-color: #c99a78;

  --highlight-color: rgba(235, 160, 70, 0.32);

  --tone-success: #9cc27a;
  --tone-success-soft: #27301d;
  --tone-warning: #e0b066;
  --tone-warning-soft: #3a2e1a;
  --tone-danger: #ec8f7f;
  --tone-danger-soft: #3d2420;
  --tone-info: #92bccb;
  --tone-info-soft: #1e2e33;

  --editor-code-variable-color: #8cc0c4;
  --editor-code-typename-color: #b8c47c;
  --editor-code-string-color: #d4a5cf;
  --editor-code-number-color: #e0b066;
  --editor-code-operator-color: #a39584;
  --editor-code-atom-color: #e08a6c;

  /* Headings in full ink: the default grays them toward the subtle color */
  --editor-heading-color: var(--paper-ink);
  /* Thin rules in the paper's own hairline, not a dark gray bar */
  --editor-ruler-color: color-mix(in srgb, var(--paper-rule), var(--paper-ink) 15%);
  --editor-blockquote-border-color: color-mix(in srgb, var(--paper-rule), var(--paper-ink) 25%);
  /* Tags as soft, round accent-tinted pills instead of solid ones */
  --editor-hashtag-background-color: color-mix(in srgb, var(--ui-accent-color) 16%, var(--root-background-color));
  --editor-hashtag-color: var(--ui-accent-color);
  --editor-hashtag-border-color: color-mix(in srgb, var(--ui-accent-color) 32%, var(--root-background-color));
  --editor-hashtag-border-radius: 1em;
}
```
