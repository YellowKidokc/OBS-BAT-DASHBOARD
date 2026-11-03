"""
Series Scaffold Builder
POF 2828 | David Lowe

Compact CustomTkinter scaffold editor:
- Flat ordered list with indent/outdent controls.
- Live tree preview.
- Template save/load.
- Target folder scaffold creation.
"""
from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from tkinter import filedialog, messagebox, simpledialog, ttk

import customtkinter as ctk


BASE_DIR = Path(__file__).resolve().parent
TEMPLATE_STORE = BASE_DIR / "config" / "series_templates.json"

BUILTIN_SCHEMAS = {
    "Standard Series": [
        "articles",
        "data",
        "data/nlp",
        "data/nlp/input",
        "data/nlp/prompts",
        "data/nlp/outputs",
        "data/markdown",
        "data/markdown/drafts",
        "data/markdown/final",
        "data/audio",
        "data/audio/transcripts",
        "data/images",
        "data/images/source",
        "data/video",
        "data/video/source",
        "data/outputs",
        "data/outputs/export",
        "archive",
        "assets",
        "assets/images",
        "assets/images/source",
        "assets/audio",
        "assets/audio/source",
        "work",
        "work/tmp",
    ],
    "Publishing Series": [
        "articles",
        "data",
        "data/nlp",
        "data/nlp/input",
        "data/nlp/prompts",
        "data/nlp/outputs",
        "data/markdown",
        "data/markdown/drafts",
        "data/markdown/final",
        "data/audio",
        "data/audio/transcripts",
        "data/images",
        "data/images/source",
        "data/video",
        "data/video/source",
        "data/outputs",
        "data/outputs/export",
        "site",
        "site/assets",
        "site/css",
        "site/js",
        "site/images",
        "archive",
        "work",
        "work/tmp",
    ],
    "Axiom Layer": [
        "archive",
        "assets",
        "work",
        "work/tmp",
    ],
}


@dataclass
class StructureItem:
    name: str
    kind: str
    level: int


def load_custom_templates() -> dict[str, list[str]]:
    if not TEMPLATE_STORE.exists():
        return {}
    try:
        data = json.loads(TEMPLATE_STORE.read_text(encoding="utf-8"))
    except Exception:
        return {}
    templates = data.get("templates", {})
    cleaned: dict[str, list[str]] = {}
    for name, paths in templates.items():
        if isinstance(name, str) and isinstance(paths, list):
            cleaned[name] = [str(p).strip().strip("/\\") for p in paths if str(p).strip()]
    return cleaned


def save_custom_templates(templates: dict[str, list[str]]) -> None:
    TEMPLATE_STORE.parent.mkdir(parents=True, exist_ok=True)
    TEMPLATE_STORE.write_text(json.dumps({"templates": templates}, indent=2), encoding="utf-8")


def safe_name(value: str) -> str:
    cleaned = value.strip().replace("\\", "/").split("/")[-1]
    cleaned = re.sub(r'[<>:"|?*]', "-", cleaned)
    return cleaned.strip(" .")


def schema_to_items(paths: list[str]) -> list[StructureItem]:
    items: list[StructureItem] = []
    seen: set[str] = set()
    for rel in [path.strip("/\\").replace("\\", "/") for path in paths if path.strip("/\\")]:
        parts = rel.split("/")
        leaf_is_file = bool(Path(parts[-1]).suffix)
        for depth in range(len(parts)):
            partial = "/".join(parts[: depth + 1])
            if partial not in seen:
                kind = "File" if depth == len(parts) - 1 and leaf_is_file else "Folder"
                items.append(StructureItem(parts[depth], kind, depth))
                seen.add(partial)
    return items


class SeriesScaffoldBuilder(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title("Series Scaffold Builder")
        self.geometry("1180x740")
        self.minsize(980, 620)

        self.custom_templates = load_custom_templates()
        self.items = schema_to_items(BUILTIN_SCHEMAS["Standard Series"])
        self.target_var = ctk.StringVar(value=str(Path.home() / "Desktop"))
        self.series_var = ctk.StringVar(value="new-series")
        self.template_var = ctk.StringVar(value="Standard Series")
        self.make_index_var = ctk.BooleanVar(value=True)
        self.make_docs_var = ctk.BooleanVar(value=True)
        self.status_var = ctk.StringVar(value="Build a structure, choose a target folder, then create the scaffold.")
        self.selected_index: int | None = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.configure_styles()
        self.build_header()
        self.build_editor()
        self.build_footer()
        self.refresh_all()

    def configure_styles(self) -> None:
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure(
            "Structure.Treeview",
            background="#111827",
            foreground="#e5e7eb",
            fieldbackground="#111827",
            bordercolor="#1f2937",
            rowheight=28,
            font=("Segoe UI", 10),
        )
        style.configure(
            "Structure.Treeview.Heading",
            background="#1f2937",
            foreground="#e5e7eb",
            font=("Segoe UI", 10, "bold"),
        )
        style.map("Structure.Treeview", background=[("selected", "#2563eb")])

    def build_header(self) -> None:
        header = ctk.CTkFrame(self, fg_color="#111827", corner_radius=0)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(1, weight=1)

        title = ctk.CTkLabel(header, text="Project Structure Builder", font=ctk.CTkFont(size=22, weight="bold"))
        title.grid(row=0, column=0, padx=18, pady=16, sticky="w")

        options = ctk.CTkFrame(header, fg_color="transparent")
        options.grid(row=0, column=1, padx=18, pady=12, sticky="e")

        ctk.CTkLabel(options, text="Series").grid(row=0, column=0, padx=(0, 6), sticky="e")
        series_entry = ctk.CTkEntry(options, textvariable=self.series_var, width=190)
        series_entry.grid(row=0, column=1, padx=(0, 14), sticky="ew")
        series_entry.bind("<KeyRelease>", lambda _event: self.refresh_preview())

        ctk.CTkLabel(options, text="Template").grid(row=0, column=2, padx=(0, 6), sticky="e")
        self.template_menu = ctk.CTkOptionMenu(
            options,
            variable=self.template_var,
            values=self.template_names(),
            width=190,
            command=lambda _value: self.load_template(),
        )
        self.template_menu.grid(row=0, column=3, sticky="ew")

    def build_editor(self) -> None:
        body = ctk.CTkFrame(self, fg_color="#0f131b", corner_radius=0)
        body.grid(row=1, column=0, sticky="nsew")
        body.grid_columnconfigure(0, weight=3)
        body.grid_columnconfigure(1, weight=2)
        body.grid_rowconfigure(0, weight=1)

        left = ctk.CTkFrame(body, fg_color="#151b25", corner_radius=8)
        left.grid(row=0, column=0, sticky="nsew", padx=(16, 8), pady=16)
        left.grid_columnconfigure(0, weight=1)
        left.grid_rowconfigure(1, weight=1)

        left_header = ctk.CTkFrame(left, fg_color="transparent")
        left_header.grid(row=0, column=0, sticky="ew", padx=12, pady=(12, 8))
        left_header.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(left_header, text="Structure List", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(left_header, text="Name / Type / Level", text_color="#9ca3af").grid(row=0, column=1, sticky="e")

        tree_frame = ctk.CTkFrame(left, fg_color="transparent")
        tree_frame.grid(row=1, column=0, sticky="nsew", padx=12)
        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)

        self.structure_tree = ttk.Treeview(
            tree_frame,
            columns=("type", "level"),
            show="tree headings",
            selectmode="browse",
            style="Structure.Treeview",
        )
        self.structure_tree.heading("#0", text="Name")
        self.structure_tree.heading("type", text="Type")
        self.structure_tree.heading("level", text="Level")
        self.structure_tree.column("#0", minwidth=220, width=420, stretch=True)
        self.structure_tree.column("type", minwidth=70, width=90, stretch=False)
        self.structure_tree.column("level", minwidth=50, width=70, stretch=False)
        self.structure_tree.grid(row=0, column=0, sticky="nsew")
        self.structure_tree.bind("<<TreeviewSelect>>", self.on_select)
        self.structure_tree.bind("<Double-1>", lambda _event: self.rename_item())

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.structure_tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.structure_tree.configure(yscrollcommand=scrollbar.set)

        controls = ctk.CTkFrame(left, fg_color="transparent")
        controls.grid(row=2, column=0, sticky="ew", padx=12, pady=12)
        for col in range(8):
            controls.grid_columnconfigure(col, weight=1)

        buttons = [
            ("Add Folder", self.add_folder),
            ("Add File", self.add_file),
            ("Rename", self.rename_item),
            ("Delete", self.delete_item),
            ("Up", self.move_up),
            ("Down", self.move_down),
            ("Outdent", self.outdent),
            ("Indent", self.indent),
        ]
        for col, (text, command) in enumerate(buttons):
            ctk.CTkButton(controls, text=text, height=34, corner_radius=6, command=command).grid(
                row=0, column=col, sticky="ew", padx=3
            )

        right = ctk.CTkFrame(body, fg_color="#151b25", corner_radius=8)
        right.grid(row=0, column=1, sticky="nsew", padx=(8, 16), pady=16)
        right.grid_columnconfigure(0, weight=1)
        right.grid_rowconfigure(1, weight=1)

        preview_header = ctk.CTkFrame(right, fg_color="transparent")
        preview_header.grid(row=0, column=0, sticky="ew", padx=12, pady=(12, 8))
        preview_header.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(preview_header, text="Live Preview", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, sticky="w")
        ctk.CTkButton(preview_header, text="Scan Folder", width=120, command=self.scan_folder_template).grid(row=0, column=1, sticky="e")

        self.preview_box = ctk.CTkTextbox(right, wrap="none", font=ctk.CTkFont(family="Consolas", size=13))
        self.preview_box.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 12))

        preview_actions = ctk.CTkFrame(right, fg_color="transparent")
        preview_actions.grid(row=2, column=0, sticky="ew", padx=12, pady=(0, 12))
        preview_actions.grid_columnconfigure((0, 1), weight=1)
        ctk.CTkButton(preview_actions, text="Save Template", command=self.save_template).grid(row=0, column=0, sticky="ew", padx=(0, 5))
        ctk.CTkButton(preview_actions, text="Reset Template", fg_color="#374151", hover_color="#4b5563", command=self.load_template).grid(
            row=0, column=1, sticky="ew", padx=(5, 0)
        )

    def build_footer(self) -> None:
        footer = ctk.CTkFrame(self, fg_color="#111827", corner_radius=0)
        footer.grid(row=2, column=0, sticky="ew")
        footer.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(footer, text="Target").grid(row=0, column=0, padx=(18, 8), pady=(14, 6), sticky="w")
        ctk.CTkEntry(footer, textvariable=self.target_var).grid(row=0, column=1, padx=(0, 8), pady=(14, 6), sticky="ew")
        ctk.CTkButton(footer, text="Browse", width=90, command=self.pick_target).grid(row=0, column=2, padx=(0, 18), pady=(14, 6))

        options = ctk.CTkFrame(footer, fg_color="transparent")
        options.grid(row=1, column=0, columnspan=2, padx=18, pady=(0, 14), sticky="w")
        ctk.CTkCheckBox(options, text="index.html", variable=self.make_index_var).grid(row=0, column=0, padx=(0, 14))
        ctk.CTkCheckBox(options, text="starter docs", variable=self.make_docs_var).grid(row=0, column=1)

        actions = ctk.CTkFrame(footer, fg_color="transparent")
        actions.grid(row=1, column=2, padx=18, pady=(0, 14), sticky="e")
        ctk.CTkButton(actions, text="Create Scaffold", width=140, command=self.create_scaffold).grid(row=0, column=0, padx=(0, 8))
        ctk.CTkButton(actions, text="Open Folder", width=120, fg_color="#374151", hover_color="#4b5563", command=self.open_target).grid(
            row=0, column=1
        )

        status = ctk.CTkLabel(footer, textvariable=self.status_var, text_color="#9ca3af", anchor="w")
        status.grid(row=2, column=0, columnspan=3, padx=18, pady=(0, 12), sticky="ew")

    def template_names(self) -> list[str]:
        return list(BUILTIN_SCHEMAS.keys()) + sorted(self.custom_templates.keys())

    def current_tree_id(self) -> str | None:
        selected = self.structure_tree.selection()
        return selected[0] if selected else None

    def selected_item_index(self) -> int | None:
        item_id = self.current_tree_id()
        if item_id is None:
            return self.selected_index
        try:
            return int(item_id)
        except ValueError:
            return None

    def on_select(self, _event=None) -> None:
        self.selected_index = self.selected_item_index()

    def ask_name(self, title: str, prompt: str, initial: str = "") -> str | None:
        value = simpledialog.askstring(title, prompt, initialvalue=initial, parent=self)
        if value is None:
            return None
        cleaned = safe_name(value)
        if not cleaned:
            messagebox.showerror("Invalid name", "Enter a usable file or folder name.")
            return None
        return cleaned

    def insertion_index_and_level(self) -> tuple[int, int]:
        index = self.selected_item_index()
        if index is None:
            return len(self.items), 0
        selected = self.items[index]
        return index + 1, selected.level + 1 if selected.kind == "Folder" else selected.level

    def add_folder(self) -> None:
        name = self.ask_name("Add Folder", "Folder name:", "new-folder")
        if not name:
            return
        index, level = self.insertion_index_and_level()
        self.items.insert(index, StructureItem(name, "Folder", level))
        self.selected_index = index
        self.refresh_all()

    def add_file(self) -> None:
        name = self.ask_name("Add File", "File name:", "new-file.md")
        if not name:
            return
        index, level = self.insertion_index_and_level()
        self.items.insert(index, StructureItem(name, "File", level))
        self.selected_index = index
        self.refresh_all()

    def rename_item(self) -> None:
        index = self.selected_item_index()
        if index is None or index >= len(self.items):
            return
        item = self.items[index]
        name = self.ask_name("Rename", "New name:", item.name)
        if not name:
            return
        item.name = name
        self.refresh_all()

    def delete_item(self) -> None:
        index = self.selected_item_index()
        if index is None or index >= len(self.items):
            return
        start, end = self.branch_range(index)
        item = self.items[start]
        count = end - index
        if count > 1 and not messagebox.askyesno("Delete branch", f"Delete '{item.name}' and {count - 1} child item(s)?"):
            return
        del self.items[start:end]
        self.selected_index = min(index, len(self.items) - 1) if self.items else None
        self.refresh_all()

    def branch_range(self, index: int) -> tuple[int, int]:
        item = self.items[index]
        end = index + 1
        while end < len(self.items) and self.items[end].level > item.level:
            end += 1
        return index, end

    def previous_branch_start(self, index: int) -> int | None:
        level = self.items[index].level
        probe = index - 1
        while probe >= 0:
            if self.items[probe].level <= level:
                return probe
            probe -= 1
        return None

    def next_branch_end(self, index: int) -> int | None:
        _start, end = self.branch_range(index)
        if end >= len(self.items):
            return None
        _next_start, next_end = self.branch_range(end)
        return next_end

    def shift_branch_level(self, index: int, delta: int) -> None:
        start, end = self.branch_range(index)
        for item in self.items[start:end]:
            item.level = max(0, item.level + delta)

    def move_up(self) -> None:
        index = self.selected_item_index()
        if index is None or index <= 0:
            return
        previous_start = self.previous_branch_start(index)
        if previous_start is None:
            return
        start, end = self.branch_range(index)
        branch = self.items[start:end]
        del self.items[start:end]
        insert_at = previous_start
        self.items[insert_at:insert_at] = branch
        self.selected_index = insert_at
        self.normalize_levels()
        self.refresh_all()

    def move_down(self) -> None:
        index = self.selected_item_index()
        if index is None or index >= len(self.items) - 1:
            return
        next_end = self.next_branch_end(index)
        if next_end is None:
            return
        start, end = self.branch_range(index)
        branch = self.items[start:end]
        del self.items[start:end]
        insert_at = next_end - len(branch)
        self.items[insert_at:insert_at] = branch
        self.selected_index = insert_at
        self.normalize_levels()
        self.refresh_all()

    def indent(self) -> None:
        index = self.selected_item_index()
        if index is None or index <= 0:
            return
        previous = self.items[index - 1]
        if previous.kind != "Folder":
            messagebox.showinfo("Indent", "An item can only be indented under a folder above it.")
            return
        if self.items[index].level >= previous.level + 1:
            return
        self.shift_branch_level(index, 1)
        self.selected_index = index
        self.normalize_levels()
        self.refresh_all()

    def outdent(self) -> None:
        index = self.selected_item_index()
        if index is None:
            return
        if self.items[index].level > 0:
            self.shift_branch_level(index, -1)
        self.selected_index = index
        self.normalize_levels()
        self.refresh_all()

    def normalize_levels(self) -> None:
        if not self.items:
            return
        self.items[0].level = max(0, self.items[0].level)
        for index in range(1, len(self.items)):
            previous = self.items[index - 1]
            current = self.items[index]
            current.level = max(0, min(current.level, previous.level + 1))
            if current.level > previous.level and previous.kind != "Folder":
                current.level = previous.level

    def refresh_all(self) -> None:
        self.normalize_levels()
        self.refresh_structure_tree()
        self.refresh_preview()

    def refresh_structure_tree(self) -> None:
        self.structure_tree.delete(*self.structure_tree.get_children())
        parent_stack: dict[int, str] = {-1: ""}
        for index, item in enumerate(self.items):
            parent = parent_stack.get(item.level - 1, "")
            item_id = str(index)
            label = f"{'  ' * item.level}{item.name}"
            self.structure_tree.insert(parent, "end", iid=item_id, text=label, values=(item.kind, item.level), open=True)
            if item.kind == "Folder":
                parent_stack[item.level] = item_id
            for level in list(parent_stack):
                if level > item.level:
                    parent_stack.pop(level, None)
        if self.selected_index is not None and 0 <= self.selected_index < len(self.items):
            iid = str(self.selected_index)
            self.structure_tree.selection_set(iid)
            self.structure_tree.see(iid)

    def refresh_preview(self) -> None:
        text = "\n".join(self.preview_lines())
        self.preview_box.configure(state="normal")
        self.preview_box.delete("1.0", "end")
        self.preview_box.insert("end", text)
        self.preview_box.configure(state="disabled")

    def preview_lines(self) -> list[str]:
        root = self.series_var.get().strip() or "new-series"
        lines = [root]
        path_stack: list[bool] = []
        for index, item in enumerate(self.items):
            next_levels = [future.level for future in self.items[index + 1 :]]
            has_next_same_level = item.level in next_levels
            while len(path_stack) > item.level:
                path_stack.pop()
            connector = "+-- " if has_next_same_level else "`-- "
            prefix = "".join("|   " if value else "    " for value in path_stack)
            suffix = "/" if item.kind == "Folder" else ""
            lines.append(f"{prefix}{connector}{item.name}{suffix}")
            if item.kind == "Folder":
                path_stack.append(has_next_same_level)
        return lines

    def item_paths(self) -> tuple[list[str], list[str]]:
        folders: list[str] = []
        files: list[str] = []
        stack: list[str] = []
        for item in self.items:
            stack = stack[: item.level]
            rel = "/".join([*stack, item.name]).strip("/")
            if item.kind == "Folder":
                folders.append(rel)
                stack.append(item.name)
            else:
                files.append(rel)
        return folders, files

    def load_template(self) -> None:
        name = self.template_var.get()
        if name in BUILTIN_SCHEMAS:
            paths = BUILTIN_SCHEMAS[name]
        else:
            paths = self.custom_templates.get(name, BUILTIN_SCHEMAS["Standard Series"])
        self.items = schema_to_items(paths)
        self.selected_index = 0 if self.items else None
        self.refresh_all()

    def save_template(self) -> None:
        name = simpledialog.askstring("Save Template", "Template name:", initialvalue=self.template_var.get(), parent=self)
        if name is None:
            return
        name = name.strip()
        if not name:
            messagebox.showerror("Missing name", "Enter a template name.")
            return
        if name in BUILTIN_SCHEMAS:
            messagebox.showerror("Name conflict", "Built-in template names are reserved.")
            return
        folders, files = self.item_paths()
        paths = folders + files
        self.custom_templates[name] = paths
        save_custom_templates(self.custom_templates)
        self.template_var.set(name)
        self.template_menu.configure(values=self.template_names())
        self.status_var.set(f"Saved template '{name}' with {len(paths)} item(s).")

    def scan_folder_template(self) -> None:
        source = filedialog.askdirectory(title="Scan folder into editable structure")
        if not source:
            return
        root = Path(source)
        skip = {".git", "node_modules", "__pycache__", ".wrangler", ".venv", "venv", "dist", "build"}
        rows: list[StructureItem] = []

        def walk(folder: Path, level: int) -> None:
            try:
                children = sorted(folder.iterdir(), key=lambda path: (path.is_file(), path.name.lower()))
            except OSError:
                return
            for child in children:
                if child.name in skip:
                    continue
                if child.is_dir():
                    rows.append(StructureItem(child.name, "Folder", level))
                    walk(child, level + 1)
                elif child.is_file():
                    rows.append(StructureItem(child.name, "File", level))

        walk(root, 0)
        if not rows:
            messagebox.showinfo("Scan Folder", "No files or folders found to import.")
            return
        self.items = rows
        self.series_var.set(root.name)
        self.selected_index = 0
        self.status_var.set(f"Imported {len(rows)} item(s) from {root}.")
        self.refresh_all()

    def pick_target(self) -> None:
        target = filedialog.askdirectory(title="Choose target folder")
        if target:
            self.target_var.set(target)

    def target_root(self) -> Path | None:
        base = self.target_var.get().strip()
        name = safe_name(self.series_var.get())
        if not base or not name:
            return None
        return Path(base) / name

    def create_scaffold(self) -> None:
        target = self.target_root()
        if target is None:
            messagebox.showerror("Missing input", "Enter a target folder and series name.")
            return
        folders, files = self.item_paths()
        if not messagebox.askyesno("Create Scaffold", f"Create scaffold here?\n\n{target}"):
            return

        created_dirs = 0
        created_files = 0
        target.mkdir(parents=True, exist_ok=True)
        for rel in folders:
            (target / rel).mkdir(parents=True, exist_ok=True)
            created_dirs += 1
        for rel in files:
            file_path = target / rel
            file_path.parent.mkdir(parents=True, exist_ok=True)
            if not file_path.exists():
                file_path.write_text("", encoding="utf-8")
                created_files += 1
        if self.make_index_var.get():
            index_path = target / "index.html"
            if not index_path.exists():
                index_path.write_text(self.index_html(target.name), encoding="utf-8")
                created_files += 1
        if self.make_docs_var.get():
            created_files += self.write_starter_docs(target)

        summary = f"Created {created_dirs} folders and {created_files} files at {target}"
        self.status_var.set(summary)
        messagebox.showinfo("Done", summary)

    def open_target(self) -> None:
        target = self.target_root()
        if target is None:
            messagebox.showerror("Missing input", "Enter a target folder and series name.")
            return
        os.startfile(str(target if target.exists() else target.parent))

    def write_starter_docs(self, target: Path) -> int:
        title = target.name
        docs_written = 0
        docs = {
            target / "README.md": self.root_readme(title),
            target / "archive" / "README.md": self.folder_readme(
                "Archive",
                "Keep rejected, deprecated, or historical material here.",
            ),
        }
        for optional in ["data", "articles", "assets", "site", "work"]:
            if (target / optional).exists():
                docs[target / optional / "README.md"] = self.folder_readme(
                    optional.replace("-", " ").title(),
                    f"Working area for {optional.replace('-', ' ')} material.",
                )
        for path, content in docs.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            if not path.exists():
                path.write_text(content, encoding="utf-8")
                docs_written += 1
        return docs_written

    @staticmethod
    def folder_readme(title: str, body: str) -> str:
        return f"# {title}\n\n{body}\n"

    def root_readme(self, title: str) -> str:
        folders, files = self.item_paths()
        folder_lines = "\n".join(f"- `{path}/`" for path in folders) or "- none"
        file_lines = "\n".join(f"- `{path}`" for path in files) or "- none"
        return f"""# {title}

This series was created with the Series Scaffold Builder.

## Folders

{folder_lines}

## Files

{file_lines}
"""

    @staticmethod
    def index_html(series_name: str) -> str:
        title = series_name.replace("-", " ").replace("_", " ").title()
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <style>
    body {{ font-family: Segoe UI, Arial, sans-serif; background:#111; color:#e6e2d5; margin:0; padding:40px; }}
    main {{ max-width: 760px; margin: 0 auto; }}
    h1 {{ color:#d4af37; }}
    code {{ color:#8be9fd; }}
  </style>
</head>
<body>
  <main>
    <h1>{title}</h1>
    <p>This is the landing page for the series.</p>
    <p>Keep working material in the scaffold folders and publish only approved files here.</p>
  </main>
</body>
</html>
"""


def main() -> None:
    app = SeriesScaffoldBuilder()
    app.mainloop()


if __name__ == "__main__":
    main()
