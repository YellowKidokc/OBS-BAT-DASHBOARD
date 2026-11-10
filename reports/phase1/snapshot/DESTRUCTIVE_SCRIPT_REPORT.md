# Destructive Script Report

Heuristic static scan. A hit means the code *can* delete, move, or rename; it does not prove it runs that path.
No script was executed.

## Deletes files/folders (10)

### `legacy_snapshot/Codex-Powershell_GUI/Reusable_Tools_From_Theophysics/API_Station_References/01_ENGINE/02_OPENAI/PAPER-REVIEW/rebuild_master_and_cleanup.py`
dry-run: N · receipts: N
```
208: f.unlink()
220: f.unlink()
```

### `legacy_snapshot/Codex-Powershell_GUI/Reusable_Tools_From_Theophysics/Conversions_and_Data_Tools/01_ENGINE/01_ENGINE/scripts/python_pipeline/data_command_center/app/core/scheduler.py`
dry-run: N · receipts: N
```
162: del self._schedules[schedule_id]
```

### `legacy_snapshot/Codex-Powershell_GUI/Reusable_Tools_From_Theophysics/Conversions_and_Data_Tools/01_ENGINE/Scripts/convert_vault_to_mdx.py`
dry-run: N · receipts: N
```
174: f.unlink()
```

### `legacy_snapshot/Codex-Powershell_GUI/Reusable_Tools_From_Theophysics/Obsidian_and_Documents/01_ENGINE/01_ENGINE/core/vault_health_engine.py`
dry-run: N · receipts: Y
```
578: p.unlink()
```

### `legacy_snapshot/Codex-Powershell_GUI/Reusable_Tools_From_Theophysics/Obsidian_and_Documents/01_ENGINE/01_ENGINE/scripts/python_pipeline/obsidian_programs/lossless_summary_engine/build_lossless_summary.ps1`
dry-run: N · receipts: Y
```
163: if (Test-Path $tmpTxt) { Remove-Item -Path $tmpTxt -Force -ErrorAction SilentlyContinue }
164: if (Test-Path $tmpPy) { Remove-Item -Path $tmpPy -Force -ErrorAction SilentlyContinue }
```

### `legacy_snapshot/Codex-Powershell_GUI/Reusable_Tools_From_Theophysics/Split_Combine_and_Organize/01_ENGINE/01_ENGINE/scripts/VaultTools.ps1`
dry-run: N · receipts: N
```
230: if (Test-Path -LiteralPath $zipPath) { Remove-Item -LiteralPath $zipPath -Force }
235: Remove-Item -LiteralPath $groupFolder -Recurse -Force
```

### `legacy_snapshot/Codex-Powershell_GUI/Reusable_Tools_From_Theophysics/Split_Combine_and_Organize/01_ENGINE/01_ENGINE/scripts/find_duplicates.py`
dry-run: Y · receipts: N
```
164: p.unlink()
```

### `legacy_snapshot/Codex-Powershell_GUI/file_actions.py`
dry-run: N · receipts: Y
```
135: target.unlink(missing_ok=True)
```

### `legacy_snapshot/Codex-Powershell_GUI/series_scaffold.py`
dry-run: N · receipts: N
```
397: del self.items[start:end]
438: del self.items[start:end]
454: del self.items[start:end]
```

### `legacy_snapshot/Codex-Powershell_GUI/uninstall_startup.bat`
dry-run: N · receipts: N
```
13: del "%SHORTCUT_PATH%"
```

## Moves or renames (8)

### `legacy_snapshot/Codex-Powershell_GUI/Reusable_Tools_From_Theophysics/Obsidian_and_Documents/01_ENGINE/01_ENGINE/core/vault_health_engine.py`
dry-run: N · receipts: Y
```
543: shutil.move(str(src), str(dst))
```

### `legacy_snapshot/Codex-Powershell_GUI/Reusable_Tools_From_Theophysics/Obsidian_and_Documents/01_ENGINE/01_ENGINE/scripts/python_pipeline/obsidian_programs/lossless_summary_engine/build_lossless_summary.ps1`
dry-run: N · receipts: Y
```
163: if (Test-Path $tmpTxt) { Remove-Item -Path $tmpTxt -Force -ErrorAction SilentlyContinue }
164: if (Test-Path $tmpPy) { Remove-Item -Path $tmpPy -Force -ErrorAction SilentlyContinue }
```

### `legacy_snapshot/Codex-Powershell_GUI/Reusable_Tools_From_Theophysics/Obsidian_and_Documents/01_ENGINE/03_VAULT_TOOLS/archive_and_relocate.py`
dry-run: Y · receipts: Y
```
86: shutil.move(str(src), str(dest))
```

### `legacy_snapshot/Codex-Powershell_GUI/Reusable_Tools_From_Theophysics/Obsidian_and_Documents/01_ENGINE/03_VAULT_TOOLS/file_loose_papers.py`
dry-run: Y · receipts: Y
```
4: Move stray single papers out of vault root / folder roots.
97: shutil.move(str(src), str(dest))
```

### `legacy_snapshot/Codex-Powershell_GUI/Reusable_Tools_From_Theophysics/Obsidian_and_Documents/01_ENGINE/03_VAULT_TOOLS/organize_canonical.py`
dry-run: Y · receipts: N
```
213: Move file to target category folder.
```

### `legacy_snapshot/Codex-Powershell_GUI/Reusable_Tools_From_Theophysics/Obsidian_and_Documents/01_ENGINE/03_VAULT_TOOLS/quarantine_mover.py`
dry-run: N · receipts: N
```
84: shutil.move(str(fp), str(dest))
```

### `legacy_snapshot/Codex-Powershell_GUI/Reusable_Tools_From_Theophysics/Split_Combine_and_Organize/01_ENGINE/01_ENGINE/scripts/VaultTools.ps1`
dry-run: N · receipts: N
```
84: Rename-Item -LiteralPath $f.FullName -NewName $tempName
121: Rename-Item -LiteralPath $row.TempFull -NewName $newName
216: Move-Item -LiteralPath $f.FullName -Destination $groupFolder
230: if (Test-Path -LiteralPath $zipPath) { Remove-Item -LiteralPath $zipPath -Force }
235: Remove-Item -LiteralPath $groupFolder -Recurse -Force
```

### `legacy_snapshot/Codex-Powershell_GUI/file_actions.py`
dry-run: N · receipts: Y
```
57: os.replace(temporary, target)
```
