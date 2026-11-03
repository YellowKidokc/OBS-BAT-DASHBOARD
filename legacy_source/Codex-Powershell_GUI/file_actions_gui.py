#!/usr/bin/env python3
"""Point-and-click file conversion and action window."""
from __future__ import annotations

import json
import sys
from pathlib import Path

from PySide6.QtCore import QProcess
from PySide6.QtWidgets import (
    QApplication, QComboBox, QFileDialog, QFormLayout, QHBoxLayout, QLabel,
    QLineEdit, QMainWindow, QMessageBox, QPushButton, QPlainTextEdit, QVBoxLayout, QWidget,
)


APP_DIR = Path(__file__).resolve().parent
ACTIONS = {
    "Excel workbook → CSV files": ("excel-to-csv", "file", "Excel (*.xlsx *.xlsm)"),
    "CSV → Excel workbook": ("csv-to-excel", "file", "CSV (*.csv);;All files (*)"),
    "Combine a Markdown folder": ("combine-markdown", "folder", ""),
    "Create folder inventory + hashes": ("folder-inventory", "folder", ""),
    "Verified safe copy": ("verified-copy", "file", "All files (*)"),
}


class FileActionsWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Codex File Actions")
        self.resize(920, 640)
        self.process: QProcess | None = None
        root = QWidget(); self.setCentralWidget(root)
        layout = QVBoxLayout(root)
        title = QLabel("File Actions & Conversions")
        title.setStyleSheet("font-size: 24px; font-weight: 700;")
        layout.addWidget(title)
        layout.addWidget(QLabel("Preview the source and destination. Outputs never overwrite existing files, and every run receives a SHA-256 receipt."))
        form = QFormLayout(); layout.addLayout(form)
        self.action = QComboBox(); self.action.addItems(ACTIONS); self.action.currentIndexChanged.connect(self._clear_source)
        form.addRow("Action", self.action)
        self.source = QLineEdit(); source_row = QHBoxLayout(); source_row.addWidget(self.source)
        browse_source = QPushButton("Browse…"); browse_source.clicked.connect(self.pick_source); source_row.addWidget(browse_source)
        form.addRow("Source", source_row)
        self.output = QLineEdit(str(APP_DIR / "outputs")); output_row = QHBoxLayout(); output_row.addWidget(self.output)
        browse_output = QPushButton("Browse…"); browse_output.clicked.connect(self.pick_output); output_row.addWidget(browse_output)
        form.addRow("Output folder", output_row)
        buttons = QHBoxLayout(); layout.addLayout(buttons)
        self.run_button = QPushButton("Run action"); self.run_button.clicked.connect(self.run_action); buttons.addWidget(self.run_button)
        receipts = QPushButton("Open receipts"); receipts.clicked.connect(lambda: self._open(APP_DIR / "receipts")); buttons.addWidget(receipts)
        outputs = QPushButton("Open outputs"); outputs.clicked.connect(lambda: self._open(Path(self.output.text()))); buttons.addWidget(outputs)
        buttons.addStretch()
        self.console = QPlainTextEdit(); self.console.setReadOnly(True); layout.addWidget(self.console, 1)
        self.setStyleSheet("QMainWindow,QWidget{background:#101827;color:#e8eef7} QLineEdit,QComboBox,QPlainTextEdit{background:#172338;border:1px solid #33445f;padding:7px} QPushButton{background:#176b87;padding:8px 14px;border-radius:4px} QPushButton:disabled{background:#39485d}")

    def current(self):
        return ACTIONS[self.action.currentText()]

    def _clear_source(self):
        self.source.clear()

    def pick_source(self):
        _, kind, pattern = self.current()
        if kind == "folder":
            value = QFileDialog.getExistingDirectory(self, "Choose source folder")
        else:
            value, _ = QFileDialog.getOpenFileName(self, "Choose source file", "", pattern)
        if value: self.source.setText(value)

    def pick_output(self):
        value = QFileDialog.getExistingDirectory(self, "Choose output folder", self.output.text())
        if value: self.output.setText(value)

    def run_action(self):
        source, output = Path(self.source.text()), Path(self.output.text())
        if not source.exists():
            QMessageBox.warning(self, "Source missing", "Choose an existing source file or folder."); return
        if not output:
            QMessageBox.warning(self, "Output missing", "Choose an output folder."); return
        action, _, _ = self.current()
        self.console.appendPlainText(f"\n{self.action.currentText()}\nSource: {source}\nOutput: {output}\n")
        self.run_button.setEnabled(False)
        self.process = QProcess(self)
        self.process.setWorkingDirectory(str(APP_DIR))
        self.process.readyReadStandardOutput.connect(lambda: self.console.appendPlainText(bytes(self.process.readAllStandardOutput()).decode(errors="replace")))
        self.process.readyReadStandardError.connect(lambda: self.console.appendPlainText(bytes(self.process.readAllStandardError()).decode(errors="replace")))
        self.process.finished.connect(self.finished)
        self.process.start(sys.executable, [str(APP_DIR / "file_actions.py"), action, str(source), str(output)])

    def finished(self, code, _status):
        self.run_button.setEnabled(True)
        self.console.appendPlainText(f"Finished with exit code {code}.")
        if code == 0: QMessageBox.information(self, "Complete", "The action completed and a receipt was written.")

    def _open(self, path: Path):
        path.mkdir(parents=True, exist_ok=True)
        import os
        os.startfile(path)


def main() -> int:
    app = QApplication(sys.argv)
    window = FileActionsWindow(); window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
