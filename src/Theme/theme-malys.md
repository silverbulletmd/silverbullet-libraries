---
pageDecoration:
  prefix: "🎄 "
  disableTOC: true
---

# Malys theme

Dark theme thought for readibility and productivity.

## Example
# 1 
## 2
### 3
#### 4
##### 5
###### 6

`code`

*emphasis*  

**strong**

## Editor

```space-style
html {
  --ui-font: ui-sans-serif, sans-serif !important;
  --editor-font: ui-sans-serif, sans-serif !important;
  --editor-width: 1100px !important;
  line-height: 1 !important;
}

.markmap {
  --markmap-text-color: #BBDEFB !important;
}

#sb-main .cm-editor {
  font-size: 15px;
  margin-top: 2rem;
}

.sb-line-h1 {
  font-size: 1.8em !important;
  color: #ee82ee !important;
}
.sb-line-h2 {
  font-size: 1.6em !important;
  color: #6a5acd !important;
}
.sb-line-h3 {
   font-size: 1.4em !important;
  color: #4169e1 !important;
}
.sb-line-h4 {
  font-size: 1.2em !important;
  color: #008000 !important;
}
.sb-line-h5 {
  font-size: 1em !important;
  color: #ffff00 !important;
}
.sb-line-h6 {
  font-size: 1em !important;
  color: #ffa500 !important;
}


.sb-line-h1::before {
  content: "h1";
  margin-right: 0.5em;
  font-size: 0.5em !important;
}

.sb-line-h2::before {
  content: "h2";
  margin-right: 0.5em;
  font-size: 0.5em !important;
}

.sb-line-h3::before {
  content: "h3";
  margin-right: 0.5em;
  font-size: 0.5em !important;
}

.sb-line-h4::before {
  content: "h4";
  margin-right: 0.5em;
  font-size: 0.5em !important;
}

.sb-line-h5::before {
  content: "h5";
  margin-right: 0.5em;
  font-size: 0.5em !important;
}

.sb-line-h6::before {
  content: "h6";
  margin-right: 0.5em;
  font-size: 0.5em !important;
}


.sb-code {
  color: grey !important;
}
.sb-emphasis {
  color: darkorange !important;
}
.sb-strong {
  color: salmon !important;
}

html {
  --treeview-phone-height: 25vh;
  --treeview-tablet-width: 25vw;
  --treeview-tablet-height: 100vh;
  --treeview-desktop-width: 20vw; 
}

.sb-bhs {
  height: var(--treeview-phone-height);
}
```

## Treeview
```space-style
.tree__label > span {
  font-size: calc(11px + 0.1vh);
}

@media (min-width: 960px) {
  #sb-root:has(.sb-lhs) #sb-main,
  #sb-root:has(.sb-lhs) #sb-top {
    margin-left: var(--treeview-tablet-width);
  }

  .sb-lhs {
    position: fixed;
    left: 0;
    height: var(--treeview-tablet-height);
    width: var(--treeview-tablet-width);
    border-right: 1px solid var(--top-border-color);
  }
}

@media (min-width: 1440px) {
  #sb-root:has(.sb-lhs) #sb-main,
  #sb-root:has(.sb-lhs) #sb-top {
    margin-left: var(--treeview-desktop-width);
  }

  .sb-lhs {
    width: var(--treeview-desktop-width);
  }
}
```

.tree__label > span {
    padding: 0 5px;
    font-size: 11px;
    line-height: 1.2;
}
.treeview-root {
    --st-label-height: auto;
    --st-subnodes-padding-left: 0.1rem;
    --st-collapse-icon-height: 2.1rem;
    --st-collapse-icon-width: 1.25rem;
    --st-collapse-icon-size: 1rem;
}

## Outline

```space-style
div.cm-scroller {
  scroll-behavior: smooth;
  scrollbar-width: thin;
}
```

