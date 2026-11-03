---
tags:
  - CSS
use: Adds a floating button to your mobile UI
---
## What this does?
Adds a floating button to your mobile UI

## Example:
![[47382.png]]


## Source
- https://forum.obsidian.md/t/adding-floating-action-button-fab-for-your-mobile-using-css/61388/10

## Code
```css
/* FAB option allow to select which Page Header button to be used for FAB 2nd button */
/* declare variables to be used for easy customisation
   other than these variables, other variables are obsidian's pre-defined */
   body.is-mobile .view-action {
	--lst-fab-view-y: calc(100vh - 120px);  /* change the 120px value to move it up/down */
	--lst-fab-view-x: 2vw;   /* set to 0 for flushed right position */
	--lst-fab-button-size: 50px;   /* set button box size */
	--lst-fab-button-radius: calc(var(--lst-fab-button-size) / 3);   /* divide 3 for square circle, divide 2 for circle */
	--lst-fab-toolbar-y-adj: 0px;
}

/* make the button "floating" and define customisation */
body.is-mobile div.view-actions > .view-action[aria-label^="Current view"] {
	position: absolute;
	top: var(--lst-fab-view-y);
	right: calc(0vw + var(--lst-fab-view-x));
	width: var(--lst-fab-button-size);
	aspect-ratio: 1;
    transform: translate(-40%, 5%);
	border-radius: var(--lst-fab-button-radius);
	background-color: var(--background-secondary);
	box-shadow: 0px 0px var(--size-4-2) rgba(0,0,0,0.3);
}

/* make sure FAB is higher than backlinks control */
body.is-mobile .view-header {
	z-index: 30;
}

/* change background-color when hover */
body.is-mobile div.view-actions > .view-action.clickable-icon:hover {
	background-color: var(--background-accent);
}
```


Canonical Hub: [[00_Canonical/CANONICAL_INDEX]]

