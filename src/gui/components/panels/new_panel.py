from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal
from typing import Optional

from src.gui.themes.theme_manager import theme_manager


class NewPanel(QWidget):
    """Panel para crear nuevo documento."""
    
    navigate = pyqtSignal(str)
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._setup_ui()
        
        theme_manager.theme_changed.connect(self._apply_style)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 30, 40, 30)
        
        title = QLabel("Nuevo Documento")
        title.setObjectName("panelTitle")
        layout.addWidget(title)
        
        layout.addSpacing(20)
        
        info = QLabel("Selecciona una opción para comenzar:")
        info.setObjectName("panelInfo")
        layout.addWidget(info)
        
        layout.addSpacing(20)
        
        options_layout = QHBoxLayout()
        
        repair_btn = self._create_option_card("Reparar PDF", "🔧", "Corregir problemas en archivos PDF dañados")
        repair_btn.clicked.connect(lambda: self.navigate.emit("repair"))
        options_layout.addWidget(repair_btn)
        
        merge_btn = self._create_option_card("Unir PDFs", "📑", "Combinar varios PDFs en uno solo")
        merge_btn.clicked.connect(lambda: self.navigate.emit("merge"))
        options_layout.addWidget(merge_btn)
        
        split_btn = self._create_option_card("Dividir PDF", "✂️", "Separar páginas de un PDF")
        split_btn.clicked.connect(lambda: self.navigate.emit("split"))
        options_layout.addWidget(split_btn)
        
        layout.addLayout(options_layout)
        
        layout.addStretch()

    def _create_option_card(self, title: str, icon: str, description: str) -> QPushButton:
        btn = QPushButton(f"{icon}\n\n{title}")
        btn.setFixedSize(180, 150)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        
        colors = theme_manager.colors
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {colors['bg_tertiary']};
                color: {colors['fg_primary']};
                border: 1px solid {colors['border']};
                border-radius: 16px;
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {colors['accent']}, stop:1 {colors['accent_light']});
                color: white;
                border-color: {colors['accent']};
            }}
            QPushButton:pressed {{
                background-color: {colors['accent_dark']};
            }}
        """)
        
        return btn

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
            QLabel#panelInfo {{
                color: {colors['fg_secondary']};
                font-size: 14px;
            }}
        """)
