---
tags:
  - CSS
use: Hides and shows the properties view on hover
---
## What this does?
Hides and shows the properties view on hover


## Example:
![[68747470733a2f2f692e696d6775722e636f6d2f4a53304539537a2e676966.gif]]


## Source
- https://discord.com/channels/686053708261228577/702656734631821413/1144209029464342538

## Code
```css
/*
author: The Useful Walrus
source: https://discord.com/channels/686053708261228577/702656734631821413/1144209029464342538
*/

.metadata-properties-title {
  transition: 500ms;
  opacity: 0.2;
  pointer-events: none;
}
.metadata-container:hover .metadata-properties-title {
  opacity: 1;
  color: var(--text-accent);
  pointer-events: auto;
}

.metadata-content {
  transition: 200ms cubic-bezier(0.25, 1, 0.5, 1);
  opacity: 0;
  height: 0;
  margin-bottom: -1.8em;
  pointer-events: none;
}
.metadata-container:hover .metadata-content {
  opacity: 1;
  height: auto;
  margin-bottom: 0.5em;
  pointer-events: auto;
}
```


Canonical Hub: [[00_Canonical/CANONICAL_INDEX]]

