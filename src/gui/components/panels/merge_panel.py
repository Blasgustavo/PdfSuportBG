from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget, QFileDialog
)
from PyQt6.QtCore import Qt
from typing import Optional
from pathlib import Path

from src.gui.themes.theme_manager import theme_manager


class MergePanel(QWidget):
    """Panel para fusionar múltiples archivos PDF."""
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.pdf_files = []
        self._setup_ui()
        
        theme_manager.theme_changed.connect(self._apply_style)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 30, 40, 30)
        
        title = QLabel("Unir PDFs")
        title.setObjectName("panelTitle")
        layout.addWidget(title)
        
        layout.addSpacing(20)
        
        add_btn = QPushButton("Agregar archivos PDF")
        add_btn.clicked.connect(self._add_files)
        layout.addWidget(add_btn)
        
        self.file_list = QListWidget()
        layout.addWidget(self.file_list)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.merge_btn = QPushButton("Unir PDFs")
        self.merge_btn.setFixedSize(200, 45)
        self.merge_btn.setEnabled(False)
        button_layout.addWidget(self.merge_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)

    def _add_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Seleccionar archivos PDF",
            "",
            "PDF Files (*.pdf)"
        )
        
        for f in files:
            if f not in self.pdf_files:
                self.pdf_files.append(f)
                self.file_list.addItem(Path(f).name)
        
        self.merge_btn.setEnabled(len(self.pdf_files) > 1)

    def _apply_style(self):
        colors = theme_manager.colors
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {colors['bg_primary']};
            }}
            QLabel#panelTitle {{
                color: {colors['fg_primary']};
                font-size: 24px;
                font-weight: bold;
            }}
            QListWidget {{
                background-color: {colors['bg_tertiary']};
                color: {colors['fg_primary']};
                border: 1px solid {colors['border']};
                border-radius: 8px;
            }}
            QPushButton {{
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {colors['accent']}, stop:1 {colors['accent_light']});
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 600;
                padding: 10px 20px;
            }}
            QPushButton:hover {{
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {colors['accent_light']}, stop:1 {colors['accent']});
            }}
            QPushButton:pressed {{
                background-color: {colors['accent_dark']};
            }}
            QPushButton:disabled {{
                background-color: {colors['bg_tertiary']};
                color: {colors['fg_disabled']};
            }}
        """)
