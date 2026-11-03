"""
Folder Structure Duplicator
POF 2828 | David Lowe

Simple GUI tool to duplicate folder structures with options:
- Main folders only (depth 1)
- All folders recursively (no files)
- All folders + files
- Deselect specific items before copying
"""
import os
import shutil
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class FolderDuplicator:
    def __init__(self, root):
        self.root = root
        self.root.title("Folder Structure Duplicator")
        self.root.geometry("800x650")
        self.root.configure(bg="#1a1a1a")

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TLabel', background='#1a1a1a', foreground='#e0e0e0', font=('Segoe UI', 10))
        style.configure('TButton', font=('Segoe UI', 10))
        style.configure('TRadiobutton', background='#1a1a1a', foreground='#e0e0e0', font=('Segoe UI', 10))
        style.configure('Treeview', background='#111', foreground='#ccc', fieldbackground='#111', font=('Consolas', 9))
        style.configure('Treeview.Heading', font=('Segoe UI', 9, 'bold'))

        self.source_var = tk.StringVar()
        self.dest_var = tk.StringVar()
        self.mode_var = tk.StringVar(value="folders_recursive")
        self.checked = {}

        # Source
        f1 = tk.Frame(root, bg='#1a1a1a')
        f1.pack(fill='x', padx=10, pady=(10,2))
        ttk.Label(f1, text="Source:").pack(side='left')
        ttk.Entry(f1, textvariable=self.source_var, width=60).pack(side='left', padx=5)
        ttk.Button(f1, text="Browse", command=self.pick_source).pack(side='left')

        # Destination
        f2 = tk.Frame(root, bg='#1a1a1a')
        f2.pack(fill='x', padx=10, pady=2)
        ttk.Label(f2, text="Dest:  ").pack(side='left')
        ttk.Entry(f2, textvariable=self.dest_var, width=60).pack(side='left', padx=5)
        ttk.Button(f2, text="Browse", command=self.pick_dest).pack(side='left')

        # Mode
        f3 = tk.Frame(root, bg='#1a1a1a')
        f3.pack(fill='x', padx=10, pady=8)
        ttk.Radiobutton(f3, text="Main folders only (depth 1)", variable=self.mode_var, value="folders_top").pack(side='left', padx=8)
        ttk.Radiobutton(f3, text="All folders recursively", variable=self.mode_var, value="folders_recursive").pack(side='left', padx=8)
        ttk.Radiobutton(f3, text="Folders + files", variable=self.mode_var, value="with_files").pack(side='left', padx=8)

        # Buttons row
        f4 = tk.Frame(root, bg='#1a1a1a')
        f4.pack(fill='x', padx=10, pady=4)
        ttk.Button(f4, text="Scan", command=self.scan).pack(side='left', padx=4)
        ttk.Button(f4, text="Select All", command=self.select_all).pack(side='left', padx=4)
        ttk.Button(f4, text="Deselect All", command=self.deselect_all).pack(side='left', padx=4)
        ttk.Button(f4, text="COPY", command=self.do_copy).pack(side='right', padx=4)

        # Tree
        tree_frame = tk.Frame(root, bg='#1a1a1a')
        tree_frame.pack(fill='both', expand=True, padx=10, pady=6)
        self.tree = ttk.Treeview(tree_frame, columns=('type','path'), show='tree headings', selectmode='extended')
        self.tree.heading('#0', text='Name')
        self.tree.heading('type', text='Type')
        self.tree.heading('path', text='Path')
        self.tree.column('#0', width=300)
        self.tree.column('type', width=60)
        self.tree.column('path', width=400)
        sb = ttk.Scrollbar(tree_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side='left', fill='both', expand=True)
        sb.pack(side='right', fill='y')
        self.tree.bind('<Button-1>', self.on_click)

        # Status
        self.status_var = tk.StringVar(value="Pick source and destination, choose mode, click Scan.")
        ttk.Label(root, textvariable=self.status_var, font=('Consolas', 9)).pack(fill='x', padx=10, pady=6)

    def pick_source(self):
        p = filedialog.askdirectory(title="Select source folder")
        if p: self.source_var.set(p)

    def pick_dest(self):
        p = filedialog.askdirectory(title="Select destination folder")
        if p: self.dest_var.set(p)

    def scan(self):
        src = self.source_var.get()
        if not src or not os.path.isdir(src):
            messagebox.showerror("Error", "Pick a valid source folder")
            return
        self.tree.delete(*self.tree.get_children())
        self.checked.clear()
        mode = self.mode_var.get()
        count = 0
        skip = {'.git', 'node_modules', '__pycache__', '.wrangler'}
        for dirpath, dirnames, filenames in os.walk(src):
            dirnames[:] = [d for d in dirnames if d not in skip]
            rel = os.path.relpath(dirpath, src)
            depth = 0 if rel == '.' else rel.count(os.sep) + 1
            if mode == "folders_top" and depth > 1:
                dirnames.clear()
                continue
            parent = '' if rel == '.' else rel.replace(os.sep, '/')
            # Add folders
            for d in sorted(dirnames):
                full_rel = os.path.join(rel, d) if rel != '.' else d
                key = full_rel.replace(os.sep, '/')
                parent_key = '' if rel == '.' else parent
                node = self.tree.insert(parent_key if parent_key in self.checked else '', 'end',
                                       iid=key, text=f"[✓] {d}", values=('DIR', key))
                self.checked[key] = True
                count += 1
            # Add files if mode includes them
            if mode == "with_files":
                for f in sorted(filenames):
                    full_rel = os.path.join(rel, f) if rel != '.' else f
                    key = full_rel.replace(os.sep, '/')
                    parent_key = '' if rel == '.' else parent
                    try:
                        self.tree.insert(parent_key if parent_key in self.checked else '', 'end',
                                        iid=key, text=f"[✓] {f}", values=('FILE', key))
                        self.checked[key] = True
                        count += 1
                    except: pass
        self.status_var.set(f"Scanned: {count} items. Click items to deselect. Click COPY when ready.")

    def on_click(self, event):
        item = self.tree.identify_row(event.y)
        if not item: return
        if item in self.checked:
            self.checked[item] = not self.checked[item]
            name = os.path.basename(item)
            mark = "[✓]" if self.checked[item] else "[✗]"
            self.tree.item(item, text=f"{mark} {name}")

    def select_all(self):
        for key in self.checked:
            self.checked[key] = True
            name = os.path.basename(key)
            self.tree.item(key, text=f"[✓] {name}")

    def deselect_all(self):
        for key in self.checked:
            self.checked[key] = False
            name = os.path.basename(key)
            self.tree.item(key, text=f"[✗] {name}")

    def do_copy(self):
        src = self.source_var.get()
        dest = self.dest_var.get()
        if not src or not dest:
            messagebox.showerror("Error", "Set both source and destination")
            return
        if not os.path.isdir(src):
            messagebox.showerror("Error", "Source folder doesn't exist")
            return
        copied_dirs = 0
        copied_files = 0
        for key, selected in sorted(self.checked.items()):
            if not selected: continue
            item_type = self.tree.item(key, 'values')[0]
            dest_path = os.path.join(dest, key.replace('/', os.sep))
            src_path = os.path.join(src, key.replace('/', os.sep))
            if item_type == 'DIR':
                os.makedirs(dest_path, exist_ok=True)
                copied_dirs += 1
            elif item_type == 'FILE':
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                shutil.copy2(src_path, dest_path)
                copied_files += 1
        msg = f"Done. Created {copied_dirs} folders"
        if copied_files: msg += f", copied {copied_files} files"
        self.status_var.set(msg)
        messagebox.showinfo("Complete", msg)

if __name__ == '__main__':
    root = tk.Tk()
    app = FolderDuplicator(root)
    root.mainloop()
