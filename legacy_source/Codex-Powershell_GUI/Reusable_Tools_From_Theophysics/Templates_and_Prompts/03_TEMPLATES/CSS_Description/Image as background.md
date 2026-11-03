---
tags:
  - CSS
use: sets a background as image
---
## What this does?
Sets image as background for your entire vaults UI


## Example:
- ![](https://camo.githubusercontent.com/92408a36cff682751a3978c0179a448b10f08d10ae8a2c29f337db347d563467/68747470733a2f2f692e696d6775722e636f6d2f4f4c36394b79492e706e67)


## Source
- https://discord.com/login?redirect_to=/channels/686053708261228577/702656734631821413/893904428430680065

## Code
```css
/*
author: Chetachi
source: https://discord.com/channels/686053708261228577/702656734631821413/893904428430680065
*/

.workspace {
  background-image: url("https://images.wallpapersden.com/image/download/macos-12-monterey-stock-dark_bGxsaGiUmZqaraWkpJRmbmdlrWZlbWU.jpg");
  background-size: cover;
  --background-primary: #20202040;
  --background-primary-alt: #1a1a1a40;
  --background-secondary: #16161640;
  --background-secondary-alt: #00000040;
  --background-modifier-border: #00000040;
  --background-modifier-form-field: var(--background-primary-alt);
  --svg-faint: var(--text-muted);
}

.graph-controls {
  border: none;
}

.graph-controls,
.graph-controls.is-close,
.theme-light .nav-action-button.is-active,
.theme-dark .nav-action-button.is-active,
.theme-light .workspace-tab-header.is-active,
.theme-dark .workspace-tab-header.is-active {
  box-shadow: none !important;
}

.workspace-ribbon,
.workspace-split .workspace-tabs {
  background: var(--background-primary);
  background-color: var(--background-primary) !important;
}

.workspace-tabs .workspace-leaf {
  background-color: unset;
}

div.view-header,
.workspace-tab-header-container,
.workspace-split.mod-root .view-content,
.mod-root .CodeMirror-gutter.CodeMirror-linenumbers,
.mod-root .CodeMirror-gutter.CodeMirror-foldgutter {
  background-color: transparent !important;
}

/*
body:not(.no-svg-replace) svg.right-triangle,
body:not(.no-svg-replace)
  .markdown-preview-view
  .collapse-indicator
  > svg.right-triangle {
  background-color: var(--text-muted);
}
*/

body:not(.no-svg-replace) svg.right-triangle,
body:not(.no-svg-replace) span[title="Fold line"]:after,
body:not(.no-svg-replace) span[title="Unfold line"]:after,
body:not(.no-svg-replace) .CodeMirror-foldgutter-open:after,
body:not(.no-svg-replace) .CodeMirror-foldgutter-folded:after {
  color: var(--text-muted);
}
```


Canonical Hub: [[00_Canonical/CANONICAL_INDEX]]

