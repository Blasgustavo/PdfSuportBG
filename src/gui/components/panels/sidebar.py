from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QPushButton, QWidget
from PyQt6.QtCore import Qt, pyqtSignal
from typing import Optional

from src.utils.logger import logger


class SidebarButton(QPushButton):
    """Botón de navegación para la sidebar."""
    
    def __init__(self, text: str, icon: str = "", parent: Optional[QWidget] = None):
        super().__init__(text, parent)
        self.setFixedHeight(40)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        if icon:
            self.setText(f"  {icon}  {text}")
        
        self._apply_style()

    def _apply_style(self):
        from src.gui.themes.theme_manager import theme_manager
        colors = theme_manager.colors
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {colors['fg_secondary']};
                border: none;
                text-align: left;
                padding-left: 20px;
                font-size: 13px;
                border-radius: 0px;
            }}
            QPushButton:hover {{
                background-color: {colors['bg_tertiary']};
                color: {colors['fg_primary']};
                border-left: 3px solid {colors['accent']};
            }}
            QPushButton:pressed {{
                background-color: {colors['accent']};
                color: white;
                border-left: 3px solid {colors['accent_dark']};
            }}
        """)


class Sidebar(QFrame):
    """Barra lateral de navegación simplificada."""
    
    open_editor = pyqtSignal()
    open_settings = pyqtSignal()
    open_account = pyqtSignal()
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setObjectName("sidebar")
        self.setFixedWidth(100)
        
        self._setup_ui()
        self._apply_style()
        
        from src.gui.themes.theme_manager import theme_manager
        theme_manager.theme_changed.connect(self._apply_style)
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 15, 5, 15)
        layout.setSpacing(8)
        
        self.home_btn = self._create_nav_button("🏠", "Inicio")
        
        self.new_btn = self._create_nav_button("📄", "Nuevo")
        self.new_btn.clicked.connect(self._on_new_clicked)
        
        layout.addWidget(self.home_btn)
        layout.addWidget(self.new_btn)
        
        layout.addStretch()
        
        self.settings_btn = self._create_nav_button("⚙️", "Configuración")
        self.settings_btn.clicked.connect(self._on_settings_clicked)
        
        self.account_btn = self._create_nav_button("👤", "Cuenta")
        self.account_btn.clicked.connect(self._on_account_clicked)
        
        layout.addWidget(self.settings_btn)
        layout.addWidget(self.account_btn)
    
    def _on_new_clicked(self):
        logger.action(f"Clic en botón Nuevo")
        self.open_editor.emit()
    
    def _on_settings_clicked(self):
        logger.action(f"Clic en botón Configuración")
        self.open_settings.emit()
    
    def _on_account_clicked(self):
        logger.action(f"Clic en botón Cuenta")
        self.open_account.emit()
    
    def _create_nav_button(self, icon: str, text: str) -> QPushButton:
        btn = QPushButton()
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setFixedSize(90, 80)
        btn.setObjectName("navButton")
        
        layout = QVBoxLayout(btn)
        layout.setContentsMargins(5, 10, 5, 5)
        layout.setSpacing(2)
        
        icon_label = QLabel(icon)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setObjectName("navIcon")
        
        text_label = QLabel(text)
        text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        text_label.setObjectName("navText")
        
        layout.addWidget(icon_label)
        layout.addWidget(text_label)
        
        return btn
    
    def _apply_style(self):
        from src.gui.themes.theme_manager import theme_manager
        colors = theme_manager.colors
        self.setStyleSheet(f"""
            QFrame#sidebar {{
                background-color: {colors['bg_secondary']};
                border-right: 1px solid {colors['border']};
            }}
            QPushButton#navButton {{
                background-color: transparent;
                border: none;
                border-radius: 12px;
            }}
            QPushButton#navButton:hover {{
                background-color: {colors['bg_tertiary']};
            }}
            QLabel#navIcon {{
                font-size: 40px;
            }}
            QLabel#navText {{
                color: {colors['fg_primary']};
                font-size: 11px;
            }}
        """)
