from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal
from typing import Optional


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
    """Barra lateral de navegación."""
    
    navigation_requested = pyqtSignal(str)
    open_editor = pyqtSignal()
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setObjectName("sidebar")
        self.setFixedWidth(220)
        
        self._setup_ui()
        self._apply_style()
        
        from src.gui.themes.theme_manager import theme_manager
        theme_manager.theme_changed.connect(self._apply_style)
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Botones de navegación
        nav_buttons = [
            ("🏠", "Inicio", "start"),
            ("📄", "Nuevo", "new"),
            ("🔧", "Reparar", "repair"),
            ("🔀", "Fusionar", "merge"),
            ("✂️", "Dividir", "split"),
            ("⚙️", "Ajustes", "settings"),
        ]
        
        for icon, text, page in nav_buttons:
            btn = self._create_nav_button(icon, text, page)
            layout.addWidget(btn)
        
        layout.addStretch()
    
    def _create_nav_button(self, icon: str, text: str, page: str) -> QPushButton:
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
        
        btn.clicked.connect(lambda: self.navigation_requested.emit(page))
        
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
