# File actions

Drag a file or folder onto any `.bat`. Every action shows a preview first and changes nothing until you type `YES`.

| Launcher | What it does | Safety |
|---|---|---|
| `FLATTEN_FOLDER.bat` | Moves files up from all subfolders, then removes folders left empty | Reversible (manifest + `UNDO_FLATTEN.bat`) |
| `EXCEL_TO_CSV.bat` | Each workbook becomes a book folder: one CSV per sheet, in order, plus `_book.json` | Creates new files only |
| `CSV_TO_EXCEL.bat` | A book folder rebuilds the **same workbook** (sheet names, order, hidden state). A plain folder of CSVs becomes one workbook with a sheet per CSV | Creates new files only |
| `ANY_TO_MARKDOWN.bat` | Word, PowerPoint, Excel, PDF, HTML, EPUB, CSV, JSON, Outlook .msg, ZIP… → `.md` (Microsoft MarkItDown). Adds provenance frontmatter | Creates new files only |
| `MARKDOWN_TO.bat` | `.md` → Word, HTML, PDF, PowerPoint, ODT, RTF, EPUB, plain text (pandoc) | Creates new files only |

Conversions write to a new `_converted\<action>_<time>\` folder next to the source, or to the in-house workspace if you choose option 2. Each run writes a `_receipt.json` with input and output hashes. To undo a conversion, delete its output folder.

First time: run `SETUP_CONVERTERS.bat`.

## What does not survive a conversion

- **Excel → CSV:** values only. Formulas, formatting, charts, merged cells and comments are not kept, and you get a warning when a workbook has formulas. CSV → Excel restores values, types and sheet structure.
- **Number-like text is kept as text:** codes with leading zeros (`00123`) and long IDs stay text so nothing gets rounded.
- **Markdown → Word/PDF and back:** Obsidian `[[wikilinks]]` become ordinary links, and callouts or plugin syntax are flattened.
- **Scanned PDFs or images → Markdown:** these give empty output unless OCR is added, and you get a warning when that happens.
