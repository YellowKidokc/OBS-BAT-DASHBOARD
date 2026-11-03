---
tags:
  - CSS
use: adds scrollbars on Obsidian slideshow slides
---
## What this does?
The slides plugin creates slideshows from your notes where — — — acts as a slide unit. And the slides are not much responsive with the core plugin. When you add more content to the slide, it overflows and the content is hidden below the container.

You don't need to add the CSSclasses property for this to work.
## Example:
- Use the slide plugin to see it in action


## Source
- https://github.com/JackCSheehan/obsidian-tweaks

## Code
```Scrollable Slides
/*
CSS snippet that adds scrollbars on Obsidian slideshow slides in cases where content
would normally overflow and be hidden
*/

/* Apply styles to containing divs for slides */
.slides {
    /* Set overflows to allow for auto vertical scroll bar and no horizontal scroll bar */
    overflow-x: hidden !important;
    overflow-y: auto !important;

    /* Enable pointer events so users can click and drag on scrollbars */
    pointer-events: auto !important;
}

/* Apply styles that apply directly to slides */
.slides > section {
    /* Create flex container to arrange auto-generated elements by Obsidian on each slide */
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}
```


Canonical Hub: [[00_Canonical/CANONICAL_INDEX]]

