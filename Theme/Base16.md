

#meta

A dark theme implemented [by Keith Yao](https://community.silverbullet.md/t/base16-based-theme/3052).

> **note** Note
>  Only active in dark mode (`Editor: Toggle Dark Mode`).


# Implementation
```space-style

/* based on Ayu Dark https://github.com/tinted-theming/home/blob/main/styling.md#ayu-darkyaml */
:root {
  --base00: #0f1419; /* Black (Background) - Default Background */
  --base01: #131721; /* (Darkest Gray) - Lighter Background (Used for status bars) */
  --base02: #272d38; /* (Dark Gray) - Selection Background */
  --base03: #3e4b59; /* Bright Black (Gray) - Comments, Invisibles, Line Highlighting */
  --base04: #bfbdb6; /* (Light Gray) - Dark Foreground (Used for status bars) */
  --base05: #e6e1cf; /* White - Default Foreground, Caret, Delimiters, Operators */
  --base06: #e6e1cf; /* (Lighter White) - Light Foreground */
  --base07: #f3f4f5; /* Bright White - The Lightest Foreground */
  --base08: #f07178; /* Red and Bright Red - Variables, XML Tags, Markup Link Text, Markup Lists, Diff Deleted */
  --base09: #ff8f40; /* (Orange) - Integers, Boolean, Constants, XML Attributes, Markup Link Url */
  --base0A: #ffb454; /* Yellow and Bright Yellow - Classes, Markup Bold, Search Text Background */
  --base0B: #b8cc52; /* Green and Bright Green - Strings, Inherited Class, Markup Code, Diff Inserted */
  --base0C: #95e6cb; /* Cyan and Bright Cyan - Support, Regular Expressions, Escape Characters, Markup Quotes */
  --base0D: #59c2ff; /* Blue and Bright Blue - Functions, Methods, Attribute IDs, Headings */
  --base0E: #d2a6ff; /* Magenta and Bright Magenta - Keywords, Storage, Selector, Markup Italic, Diff Changed */
  --base0F: #e6b673; /* (Dark Red or Brown) - Deprecated, Opening/Closing Embedded Language Tags, e.g. <?php ?> */
}

html[data-theme="dark"] {
  color-scheme: dark;

  --ui-accent-color: var(--base0D);
  --ui-accent-text-color: color-mix(in srgb, var(--ui-accent-color), white 50%);
  --highlight-color: color-mix(in srgb, var(--base0A), transparent 50%);
  --link-color: var(--base0D);
  --link-missing-color: var(--base09);
  --meta-color: var(--base08);
  --meta-subtle-color: var(--base03);
  --subtle-color: var(--base03);
  --subtle-background-color: color-mix(in srgb, var(--base03), transparent 90%);

  --root-background-color: var(--base00);
  --root-color: var(--base05);

  --top-color: var(--base06);
  --top-background-color: var(--base01);
  --top-border-color: var(--base03);
  --top-sync-error-color: var(--top-color);
  --top-sync-error-background-color: color-mix(in srgb, var(--base08), black 50%);
  --top-saved-color: var(--base06);
  --top-unsaved-color: var(--base04);
  --top-loading-color: var(--base04);

  --panel-background-color: var(--base00);
  --panel-border-color: var(--base03);

  --bhs-background-color: var(--base00);
  --bhs-border-color: var(--base03);

  --modal-color: var(--base05);
  --modal-background-color: var(--base01);
  --modal-border-color: var(--base03);
  --modal-header-label-color: var(--ui-accent-text-color);
  --modal-help-background-color: var(--base02);
  --modal-help-color: var(--base05);
  --modal-selected-option-background-color: var(--ui-accent-color);
  --modal-selected-option-color: var(--base07);
  --modal-hint-background-color: color-mix(in srgb, var(--base0D), black 50%);
  --modal-hint-color: var(--base07);
  --modal-hint-inactive-background-color: var(--base02);
  --modal-hint-inactive-color: var(--base04);
  --modal-description-color: var(--base04);
  --modal-selected-option-description-color: var(--base06);

  --notifications-background-color: var(--base02);
  --notifications-border-color: var(--base04);
  --notification-info-background-color: var(--base0D);
  --notification-error-background-color: var(--base08);

  --button-background-color: var(--base03);
  --button-hover-background-color: color-mix(in srgb, var(--base03), var(--base04) 40%);
  --button-color: var(--base07);
  --button-border-color: var(--base03);
  --primary-button-background-color: var(--ui-accent-color);
  --primary-button-hover-background-color: color-mix(
    in srgb,
    var(--ui-accent-color),
    black 35%
  );
  --primary-button-color: var(--base07);
  --primary-button-border-color: transparent;

  --progress-background-color: var(--base03);
  --progress-sync-color: var(--base07);
  --progress-index-color: var(--base0A);

  --text-field-background-color: var(--button-background-color);

  --action-button-background-color: transparent;
  --action-button-color: var(--base04);
  --action-button-hover-color: var(--base0D);
  --action-button-active-color: var(--base0D);

  --editor-caret-color: var(--base07);
  --editor-selection-background-color: color-mix(in srgb, var(--base02), transparent 30%);
  --editor-panels-bottom-color: var(--base06);
  --editor-panels-bottom-background-color: var(--base01);
  --editor-panels-bottom-border-color: var(--base03);
  --editor-completion-detail-color: var(--base04);
  --editor-completion-detail-selected-color: var(--base06);
  --editor-list-bullet-color: var(--base04);
  --editor-heading-color: var(--base06);
  --editor-heading-meta-color: var(--meta-subtle-color);
  --editor-hashtag-background-color: color-mix(in srgb, var(--base0D), transparent 50%);
  --editor-hashtag-color: var(--base07);
  --editor-hashtag-border-color: color-mix(in srgb, var(--base0D), transparent 60%);
  --editor-ruler-color: var(--base03);
  --editor-naked-url-color: var(--link-color);
  --editor-link-color: var(--link-color);
  --editor-link-url-color: var(--link-color);
  --editor-link-meta-color: var(--meta-subtle-color);
  --editor-wiki-link-page-background-color: color-mix(in srgb, var(--base0D), transparent 92%);
  --editor-wiki-link-page-color: var(--link-color);
  --editor-wiki-link-page-missing-color: var(--link-missing-color);
  --editor-wiki-link-color: color-mix(in srgb, var(--base0D), var(--base05) 30%);
  --editor-command-button-color: var(--base07);
  --editor-command-button-background-color: var(--base03);
  --editor-command-button-hover-background-color: color-mix(in srgb, var(--base03), var(--base04) 40%);
  --editor-command-button-meta-color: var(--meta-subtle-color);
  --editor-command-button-border-color: var(--base03);
  --editor-line-meta-color: var(--meta-subtle-color);
  --editor-meta-color: var(--meta-color);
  --editor-table-head-background-color: color-mix(in srgb, var(--base03), transparent 60%);
  --editor-table-head-color: var(--base07);
  --editor-table-even-background-color: color-mix(in srgb, var(--base03), transparent 70%);
  --editor-blockquote-background-color: var(--subtle-background-color);
  --editor-blockquote-color: var(--subtle-color);
  --editor-blockquote-border-color: var(--base03);
  --editor-code-background-color: var(--subtle-background-color);
  --editor-struct-color: var(--base08);
  --editor-highlight-background-color: var(--highlight-color);
  --editor-code-comment-color: var(--meta-subtle-color);
  --editor-code-variable-color: var(--base0D);
  --editor-code-typename-color: var(--base0B);
  --editor-code-string-color: var(--base0A);
  --editor-code-number-color: var(--base0E);
  --editor-code-info-color: var(--subtle-color);
  --editor-code-atom-color: var(--base08);
  --editor-frontmatter-background-color: color-mix(in srgb, var(--base02), transparent 50%);
  --editor-frontmatter-color: var(--subtle-color);
  --editor-frontmatter-marker-color: var(--base07);
  --editor-widget-background-color: color-mix(in srgb, var(--base03), transparent 50%);
  --editor-task-marker-color: var(--subtle-color);
  --editor-task-state-color: var(--subtle-color);

  --editor-directive-mark-color: var(--base08);
  --editor-directive-color: var(--base04);
  --editor-directive-background-color: color-mix(in srgb, var(--base03), transparent 50%);
}
```