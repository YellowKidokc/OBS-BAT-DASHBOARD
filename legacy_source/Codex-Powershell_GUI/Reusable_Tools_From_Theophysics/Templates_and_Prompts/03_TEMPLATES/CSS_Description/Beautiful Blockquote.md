---
tags:
  - CSS
use: Change your blockquote style
---
## What this does?
Tired of viewing the same old styled blockquote. This CSS will add a better style to blockquotes.

You don't need to add the CSSclasses property for this to work.
## Example:
- [[Beautiful Blockquotes]]


## Source
- [Quote Block CSS - Share & showcase - Obsidian Forum](https://forum.obsidian.md/t/quote-block-css/4640)

## Code
```Beautiful Blockquote

/*`````````````Blockquote``````````````````````*/


.theme-light .HyperMD-quote.CodeMirror-line,
.theme-light .markdown-source-view.mod-cm6 .cm-line.HyperMD-quote,
.theme-light .markdown-preview-view blockquote {
    background-color: hsl(180, 47%, 93%);
    border-radius: 7px;
    border: 0px solid black;
    box-shadow: -10px 10px 10px #bae8e8;
    font-weight: 600;
    transition: 1s;
    font-family: "Karla";
    font-style: italic;
    font-size: 17px;
}


.theme-dark .HyperMD-quote.CodeMirror-line,
.theme-dark .markdown-source-view.mod-cm6 .cm-line.HyperMD-quote,
.theme-dark .markdown-preview-view blockquote {
    background-color: black;
    border-radius: 7px;
    border: 0px solid #666565;
    box-shadow: -10px 10px 10px #666565;
    font-weight: 600;
    transition: 1s;
    font-family: "Karla";
    font-style: italic;
    font-size: 17px;
}


.theme-light blockquote:before {
    font: 14px/20px "Catamaran", sans-serif;
    color: #272443;
    font-weight: 900;
    content: "“";
    font-size: 60px;
    line-height: 0.1em;
    vertical-align: -0.2em;
  }


  .theme-dark blockquote:before {
    font: 14px/20px "Catamaran", sans-serif;
    color: #666565;
    font-weight: 900;
    content: "“";
    font-size: 60px;
    line-height: 0.1em;
    vertical-align: -0.2em;
  }

  blockquote p { display: inline; }

  .theme-light blockquote:hover {
    background-color: hsl(50, 100%, 51%);
    box-shadow: -10px 10px 10px hsla(50, 100%, 51%, 0.534);
    transition: 1s;
  }

  .theme-dark blockquote:hover {
    background-color: darkblue;
    box-shadow: -10px 10px 10px darkslategrey;
    transition: 1s;
  }

  .theme-light blockquote:hover::before {
    font: 14px/20px "Catamaran", sans-serif;
    color: #ff9d00;
    font-weight: 900;
    content: "“";
    font-size: 60px;
    line-height: 0.1em;
    vertical-align: -0.2em;
  }

  .theme-dark blockquote:hover::before {
    font: 14px/20px "Catamaran", sans-serif;
    color: white;
    font-weight: 900;
    content: "“";
    font-size: 60px;
    line-height: 0.1em;
    vertical-align: -0.2em;
  }

```


Canonical Hub: [[00_Canonical/CANONICAL_INDEX]]

