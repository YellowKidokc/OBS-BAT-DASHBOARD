---
tags:
  - CSS
use: Clean tasks design
---
## What this does?
This CSS snippet redesigns the dialog popup of tasks to make it cleaner and easier to navigate.

You don't need to add the CSSclasses property for this to work.
## Example:
![[Pasted image 20230923084611.png]]


## Source
- [Obsidian Tasks CSS redesign for "Create or Edit Task" modal - Share & showcase - Obsidian Forum](https://forum.obsidian.md/t/obsidian-tasks-css-redesign-for-create-or-edit-task-modal/38039/10)

## Code
```.tasks-modal-priorities {
    display:inline-flex;
    grid-template-columns:auto;
    grid-column: auto;
    font-size: 10px;
    flex-wrap: wrap;
    width: auto;
    justify-items: start;
    justify-content: space-between;
}
.tasks-modal-section.tasks-modal-priorities label[for="priority-none"] {
    display: none;
}
.tasks-modal-section.tasks-modal-priorities label[for="priority-medium"] {
    margin-left: 0;
}
.modal-title {
    font-size: medium;
}
.modal {
    width: 600px ;
}
.tasks-modal input[type="text"] {
    width: auto;
}
.tasks-modal-dates {
    display:flow;
    column-gap: 0.5em;
    row-gap: 1px;
    font-size: small;
}
.tasks-modal-section + .tasks-modal-section > code {
    margin-top: 0px;
    margin-bottom: 5px;
    width: 45%;
    height: fit-content;
    width: fit-content;
}

.tasks-modal-section:not(.tasks-modal-priorities) label {
    font-size: small;
    display: none;
}

.tasks-modal-section #forwardOnly {
    display: none;
}

.tasks-modal > form {
    margin: 0rem;
  }
  .tasks-modal-section:nth-of-type(2) > label,
  .tasks-modal-section:nth-of-type(3) > label,
  .tasks-modal-date > label {
    width: 6em !important;
    text-align: left !important;
    padding-right: 0em;
    margin-right: 0;
    font-weight: 500;
    font-size: small;

  }
  .tasks-modal-section:nth-of-type(3) > label,
  .tasks-modal-date {
    display: table;
    align-items: center;
    font-size: small;
  }
  .tasks-modal-section i {
    height: 0;
    color: transparent;
}
  .tasks-modal-section:nth-of-type(5) > div {
    flex: 1 1 50%;
    font-size: small;
  }

  .tasks-modal-section button[type="submit"] {
    width: 60%;
    margin-left: 20%;
  }
  .tasks-modal-section button[type="button"] {
    color: transparent;
    width: 10%;
    margin-left: 70px;
    margin-right: 0;
    background-color: transparent;
    border-color: transparent;
    box-shadow: none;

  }

  .tasks-modal-section button[type="button"]:after {
    padding-left: 0;
    content: "❌";
    color: black;
    border-color: rgba(255, 0, 0, 0.637);
    border-radius: 6px;
  }
```


Canonical Hub: [[00_Canonical/CANONICAL_INDEX]]

