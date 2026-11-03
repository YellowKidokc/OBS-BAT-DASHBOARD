---
# Tagged Links Footer Template
# Add this to the bottom of notes to show all outgoing links
---

## 📎 Referenced Concepts

```dataview
TABLE WITHOUT ID
  link(file.link, file.name) as "Concept",
  file.folder as "Location"
FROM [[]]
WHERE file.name != this.file.name
SORT file.name ASC
```

---
*Auto-generated list of all concepts linked in this note*


Canonical Hub: [[00_Canonical/CANONICAL_INDEX]]

