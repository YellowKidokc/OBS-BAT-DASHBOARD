---
tags:
  - CSS
use: Adds a colored folder style
---
## What this does?
Adds a colored folder style to file explorer


## Example:
- ![](https://camo.githubusercontent.com/30e185e3594c364561c27e0d95771ec8e13724433483c6fe0da68d6af0c08a51/68747470733a2f2f692e696d6775722e636f6d2f7a6a5a485338322e706e67)


## Source
- https://github.com/r-u-s-h-i-k-e-s-h/Obsidian-CSS-Snippets/blob/Collection/Snippets/File%20explorer%20styling%20-%20Rainbow%20folder%20background.md

## Code
```css
/* updated snippet for version 1.6.3 */

.nav-folder-children > .nav-folder,
.nav-files-container > div > .nav-folder {
  background-color: var(--folder-color);
  --nav-item-color: black;
  --nav-item-color-hover: black;
  --nav-collapse-icon-color: black;
  --nav-item-color-active: black;
  border-radius: 10px;
}
.nav-folder-children > .nav-folder,
.nav-files-container > div > .nav-folder:hover {
  filter: brightness(0.9);
}
.nav-folder-children > .nav-folder,
.nav-files-container > div > .nav-folder:nth-child(11n + 2) {
  --folder-color: rgb(243, 139, 168);
}
.nav-folder-children > .nav-folder,
.nav-files-container > div > .nav-folder:nth-child(11n + 3) {
  --folder-color: rgb(235, 160, 172);
}
.nav-folder-children > .nav-folder,
.nav-files-container > div > .nav-folder:nth-child(11n + 4) {
  --folder-color: rgb(250, 179, 135);
}
.nav-folder-children > .nav-folder,
.nav-files-container > div > .nav-folder:nth-child(11n + 5) {
  --folder-color: rgb(249, 226, 175);
}
.nav-folder-children > .nav-folder,
.nav-files-container > div > .nav-folder:nth-child(11n + 6) {
  --folder-color: rgb(166, 227, 161);
}
.nav-folder-children > .nav-folder,
.nav-files-container > div > .nav-folder:nth-child(11n + 7) {
  --folder-color: rgb(148, 226, 213);
}
.nav-folder-children > .nav-folder,
.nav-files-container > div > .nav-folder:nth-child(11n + 8) {
  --folder-color: rgb(137, 220, 235);
}
.nav-folder-children > .nav-folder,
.nav-files-container > div > .nav-folder:nth-child(11n + 9) {
  --folder-color: rgb(116, 199, 236);
}
.nav-folder-children > .nav-folder,
.nav-files-container > div > .nav-folder:nth-child(11n + 10) {
  --folder-color: rgb(135, 176, 249);
}
.nav-folder-children > .nav-folder,
.nav-files-container > div > .nav-folder:nth-child(11n + 11) {
  --folder-color: rgb(180, 190, 254);
}
.nav-folder-children > .nav-folder,
.nav-files-container > div > .nav-folder:nth-child(11n + 12) {
  --folder-color: rgb(203, 166, 247);
}
```


Canonical Hub: [[00_Canonical/CANONICAL_INDEX]]

