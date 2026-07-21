import os
import sys
from pathlib import Path
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QDragEnterEvent, QDragLeaveEvent, QDragMoveEvent, QDropEvent
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTextEdit,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QFileDialog,
    QSizePolicy,
)

from ptg.converter import convert_html_to_tikz


def extract_paths_from_mime(mime_data) -> list[str]:
    paths = []
    if mime_data.hasUrls():
        for url in mime_data.urls():
            local = url.toLocalFile()
            if local:
                paths.append(local)
            elif url.toString().startswith("file://"):
                paths.append(QUrl(url).toLocalFile() or url.toString()[7:])
    if not paths and mime_data.hasFormat("text/uri-list"):
        try:
            raw_text = mime_data.data("text/uri-list").data().decode("utf-8", errors="ignore")
            for line in raw_text.splitlines():
                line = line.strip()
                if line.startswith("file://"):
                    paths.append(QUrl(line).toLocalFile() or line[7:])
                elif line and not line.startswith("#"):
                    paths.append(line)
        except Exception:
            pass
    return paths


class DragDropWidget(QWidget):
    def __init__(self, log_widget: QTextEdit):
        super().__init__()
        self.log_widget = log_widget
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.button = QPushButton("Plotly HTML-Datei(en) hierher ziehen\\noder klicken zur Auswahl")
        self.button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.button.clicked.connect(self.open_file_dialog)
        self.reset_label_style()

        layout.addWidget(self.button)
        self.setLayout(layout)

    def reset_label_style(self):
        self.button.setStyleSheet("""
            QPushButton {
                border: 3px dashed #aaa;
                border-radius: 12px;
                background-color: #fafafa;
                font-size: 15px;
                color: #555;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
                border-color: #888;
            }
        """)

    def set_active_label_style(self):
        self.button.setStyleSheet("""
            QPushButton {
                border: 3px dashed #4CAF50;
                border-radius: 12px;
                background-color: #E8F5E9;
                font-size: 15px;
                color: #2E7D32;
                font-weight: bold;
            }
        """)

    def open_file_dialog(self):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Plotly HTML-Dateien auswählen",
            "",
            "HTML Dateien (*.html);;Alle Dateien (*)"
        )
        for file_path in files:
            self.process_html(file_path)

    def log(self, message: str):
        self.log_widget.append(message)

    def process_html(self, html_path: str):
        filename = os.path.basename(html_path)
        try:
            self.log(f"⏳ Verarbeite: {filename}...")
            tex_path = convert_html_to_tikz(html_path)
            self.log(f"✅ Erfolgreich! Gespeichert unter:\n➡️ {tex_path}\n")
        except Exception as e:
            self.log(f"❌ Fehler bei {filename}: {str(e)}\n")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Plotly HTML zu TikZ Konverter")
        self.resize(550, 450)
        
        # MainWindow acts as the single receiver for all Drag & Drop events
        self.setAcceptDrops(True)

        central_widget = QWidget()
        layout = QVBoxLayout()

        self.log_widget = QTextEdit()
        self.log_widget.setReadOnly(True)
        # Prevent QTextEdit from stealing drag events
        self.log_widget.setAcceptDrops(False)
        self.log_widget.setPlaceholderText("Hier erscheinen die Statusmeldungen...")
        self.log_widget.setStyleSheet(
            "QTextEdit { background-color: #222; color: #0F0; font-family: monospace; }"
        )

        self.drag_widget = DragDropWidget(self.log_widget)

        layout.addWidget(self.drag_widget, stretch=3)
        layout.addWidget(self.log_widget, stretch=2)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls() or event.mimeData().hasFormat("text/uri-list"):
            event.acceptProposedAction()
            self.drag_widget.set_active_label_style()
        else:
            event.ignore()

    def dragMoveEvent(self, event: QDragMoveEvent):
        if event.mimeData().hasUrls() or event.mimeData().hasFormat("text/uri-list"):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragLeaveEvent(self, event: QDragLeaveEvent):
        self.drag_widget.reset_label_style()

    def dropEvent(self, event: QDropEvent):
        self.drag_widget.reset_label_style()
        paths = extract_paths_from_mime(event.mimeData())
        
        if paths:
            event.acceptProposedAction()
            for path in paths:
                if path.lower().endswith(".html"):
                    self.drag_widget.process_html(path)
                else:
                    self.drag_widget.log(f"⚠️ Übersprungen (keine HTML-Datei): {os.path.basename(path)}")
        else:
            event.ignore()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
