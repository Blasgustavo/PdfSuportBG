from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog, QLineEdit
)
from PyQt6.QtCore import Qt
from typing import Optional
from pathlib import Path

from src.gui.themes.theme_manager import theme_manager


class SplitPanel(QWidget):
    """Panel para dividir un archivo PDF."""
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.current_pdf_path = None
        self._setup_ui()
        
        theme_manager.theme_changed.connect(self._apply_style)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 30, 40, 30)
        
        title = QLabel("Dividir PDF")
        title.setObjectName("panelTitle")
        layout.addWidget(title)
        
        layout.addSpacing(20)
        
        select_btn = QPushButton("Seleccionar archivo PDF")
        select_btn.clicked.connect(self._select_pdf)
        layout.addWidget(select_btn)
        
        self.selected_label = QLabel("")
        self.selected_label.setObjectName("selectedFile")
        layout.addWidget(self.selected_label)
        
        layout.addSpacing(20)
        
        self.pages_input = QLineEdit()
        self.pages_input.setPlaceholderText("Ej: 1-3, 5, 7-10")
        self.pages_input.setObjectName("pagesInput")
        layout.addWidget(self.pages_input)
        
        layout.addSpacing(10)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.split_btn = QPushButton("Dividir PDF")
        self.split_btn.setFixedSize(200, 45)
        self.split_btn.setEnabled(False)
        button_layout.addWidget(self.split_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)

    def _select_pdf(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar archivo PDF",
            "",
            "PDF Files (*.pdf)"
        )
        
        if file_path:
            self.current_pdf_path = Path(file_path)
            self.selected_label.setText(f"Archivo seleccionado: {self.current_pdf_path.name}")
            self.split_btn.setEnabled(True)

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
            QLabel#selectedFile {{
                color: {colors['success']};
                font-size: 14px;
            }}
            QLineEdit#pagesInput {{
                background-color: {colors['bg_tertiary']};
                color: {colors['fg_primary']};
                border: 1px solid {colors['border']};
                border-radius: 6px;
                padding: 8px;
                font-size: 14px;
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
