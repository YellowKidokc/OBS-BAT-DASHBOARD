---
tags:
  - CSS
use: Adds a background image to your vault
---
## What this does?
Bored with the colors? Add a custom background image of your choices. You can also change other properties like opacity, blur, brightness, etc. in the code.

You don't need to add the CSSclasses property for this to work.
## Example:
- Enable the CSS from appearance to see the CSS in action


## Source
- [Custom background image on obsidian - Help - Obsidian Forum](https://forum.obsidian.md/t/custom-background-image-on-obsidian/10598/15)
- [How to add a custom image as a background - Help - Obsidian Forum](https://forum.obsidian.md/t/how-to-add-a-custom-image-as-a-background/53416/2)
## Code
```css
.theme-light .workspace {
    backdrop-filter: brightness(1) blur(5px); /* filter for light mode */
    background-color: transparent;
}
.theme-dark .workspace {
    backdrop-filter: brightness(0.35) blur(5px); /* filter for dark mode */
    background-color: transparent;
}
.horizontal-main-container { /* below is the background image. Change it to whatever you want */
    background: url(https://images.unsplash.com/photo-1454496522488-7a8e488e8606?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2076&q=80);
    background-size: cover;
}
.workspace-split.mod-root {
    background-color: var(--background-primary);
}

body {
/* the background-primary makes the main note pane completely transparent.
You can change it to be semi-transparent if you want.
I changed background-secondary and divider-width because it
looks a bit cleaner in my opinion. You can delete those modifications if you want.*/
    --background-primary: transparent;
    --background-secondary: transparent;
    --divider-width: 0px;
}

```


Canonical Hub: [[00_Canonical/CANONICAL_INDEX]]

