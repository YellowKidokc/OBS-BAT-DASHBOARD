---
tags:
  - CSS
use: Add a background to kanban board
---
## What this does?
This custom CSS adds a custom background. You can change the wallpaper by changing the URL in the CSS.

You don't need to add the CSSclasses property for this to work.

## Example
- [[Kanban Background|Kanban Background]]
![[1281.png]]

## Source
- [Add background to kanban plugin - Share & showcase - Obsidian Forum](https://forum.obsidian.md/t/add-background-to-kanban-plugin/47248)
## Code:

```
.theme-dark .view-content .kanban-plugin::after {
  content: "";
  position: fixed;
  background-image: url(http://m.gettywallpapers.com/wp-content/uploads/2021/05/4k-Wallpaper-Cool-2048x1152.jpg);
  background-repeat: no-repeat;
  background-size: cover;
  filter: blur(1px) brightness(70%) saturate(100%);
  left: 0;
  top: 0;
  right: 0;
  bottom: 0;
  z-index: -1;
}

.theme-light .view-content .kanban-plugin::after {
  content: "";
  position: fixed;
  background-image: url(http://m.gettywallpapers.com/wp-content/uploads/2021/05/4k-Wallpaper-Cool-2048x1152.jpg);
  background-repeat: no-repeat;
  background-size: cover;
  filter: blur(1px) brightness(70%) saturate(100%);
  left: 0;
  top: 0;
  right: 0;
  bottom: 0;
  z-index: -1;
}
```


Canonical Hub: [[00_Canonical/CANONICAL_INDEX]]

