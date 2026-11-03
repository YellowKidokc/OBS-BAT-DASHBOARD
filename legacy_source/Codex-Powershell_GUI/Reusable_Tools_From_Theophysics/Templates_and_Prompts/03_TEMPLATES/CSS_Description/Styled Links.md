---
tags:
  - CSS
use: Create a linked version of styles
---
## What this does?


## Example:
- ![[65761.png]]


## Source
- https://github.com/r-u-s-h-i-k-e-s-h/Obsidian-CSS-Snippets/blob/Collection/Snippets/Link%20styling%2001.md

## Code
```css
.markdown-source-view.mod-cm6 .is-unresolved .cm-underline,
.markdown-source-view.mod-cm6 .cm-underline.is-unresolved,
.markdown-source-view.mod-cm6 .cm-underline {
  text-decoration-line: underline;
  text-decoration-thickness: 2px;
  color: var(--text-normal);
  text-decoration-color: var(--color-accent);
  text-decoration-skip-ink: none;
  font-weight: 600;
}

.markdown-rendered .internal-link {
  text-decoration-line: underline;
  text-decoration-thickness: 2px;
  color: var(--text-normal);
  text-decoration-color: var(--color-accent);
  text-decoration-skip-ink: none;
  font-weight: 600;
}
.markdown-rendered .internal-link:hover {
  text-decoration: none;
  color: var(--text-accent);
  font-weight: 600;
}

.external-link {
  text-decoration-line: underline;
  text-decoration-thickness: 2px;
  color: var(--text-normal);
  text-decoration-color: var(--color-accent);
  text-decoration-skip-ink: none;
  font-weight: 600;
}

.external-link:hover {
  text-decoration: none;
  color: var(--text-accent);
  font-weight: 600;
}
```


Canonical Hub: [[00_Canonical/CANONICAL_INDEX]]

