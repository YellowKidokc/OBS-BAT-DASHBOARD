---
tags:
  - CSS
use: Styles the divider in your notes
---
## What this does?
Styles the divider in your notes


## Example:

![[10529.png]]


## Source
- https://forum.obsidian.md/t/creating-fancy-horizontal-rule-lines/63700

## Code
```css
body {
    --hr-line-offset: 25%;
    --hr-color: lightsalmon;
}

:root hr {
    border-image-slice: 1;
    border-image-source: linear-gradient(
        to right,
        transparent,
        var(--hr-color) calc(50% - var(--hr-line-offset)),
        var(--hr-color) calc(50% + var(--hr-line-offset)),
        transparent
    );
}
```


Canonical Hub: [[00_Canonical/CANONICAL_INDEX]]

