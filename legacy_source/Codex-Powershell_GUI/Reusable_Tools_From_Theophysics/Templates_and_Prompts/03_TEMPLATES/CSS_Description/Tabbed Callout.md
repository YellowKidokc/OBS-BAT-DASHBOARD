---
tags:
  - CSS
use: Create a Tabbed view with layouts
---
## What this does?

Creates a tab like view by creating callouts and subcallouts.

Implementation like this. **Will only work when the CSS enabled**

> [!tabbed]
>
> <label>First<input type="radio" name="test" />l</label>
>
> > Lorem, ipsum dolor sit amet consectetur, adipisicing elit. (First)
> > [[Obsidian CSS|Internal Link]] > > **bold** _italic_
>
> <label>Second<input type="radio" name="test" /></label>
>
> > Lorem, ipsum dolor sit amet consectetur, adipisicing elit. (Second)
> > [External Link](https://google.com) > > $\LaTeX$
>
> <label>Third<input type="radio" name="test" />l</label>
>
> > Lorem, ipsum dolor sit amet consectetur, adipisicing elit. (Third)
> >
> > - bullet item
> > - [ ] checkbox
> > - [x] #tag

## Example:
- ![](https://camo.githubusercontent.com/2f37d3b8068c1b5c1eb15506b200a44f2b14b11706e11b1c6cc26206f05d4c26/68747470733a2f2f692e696d6775722e636f6d2f616936783848612e676966)


## Source
- [https://discord.com/channels/686053708261228577/702656734631821413/1092995965583114341](https://discord.com/channels/686053708261228577/702656734631821413/1092995965583114341)

## Code
```css
/*
author: FireIsGood
source: https://discord.com/channels/686053708261228577/702656734631821413/1092995965583114341
*/

[data-callout="tabbed"] {
  outline: 1px solid var(--color-base-30);
  border-radius: 0.5rem;
}
[data-callout="tabbed"] > .callout-content {
  padding: 0.25rem;

  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(5rem, max-content));
  gap: 0 1rem;
}
[data-callout="tabbed"] > .callout-title {
  display: none;
}
[data-callout="tabbed"] > .callout-content p {
  margin: 0;
}
[data-callout="tabbed"] > .callout-content label > input {
  display: none;
}
[data-callout="tabbed"] > .callout-content label {
  width: 100%;
  display: inline-block;
  padding: 0.15rem 0.75ch;
  border-radius: 1rem;

  color: #ccc;
  background-color: #2e7d32;

  text-align: center;
  font-weight: bold;
  font-size: 1.15rem;
  cursor: pointer;
}
[data-callout="tabbed"] > .callout-content label:has(input:checked) {
  color: white;
  background-color: #8bc34a;
}
[data-callout="tabbed"]
  > .callout-content
  p:not(:has(label input:checked))
  + blockquote {
  display: none;
}
[data-callout="tabbed"] > .callout-content > blockquote {
  order: 999;
  grid-column: 1 / -1;

  background-color: transparent;
  padding-left: 0;
  border: 0;
}
```


Canonical Hub: [[00_Canonical/CANONICAL_INDEX]]

