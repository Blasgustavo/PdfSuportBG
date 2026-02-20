from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QFrame, QTabWidget, QListWidget, QLineEdit
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from typing import Optional

from src.gui.themes.theme_manager import theme_manager


class NewDocumentPanel(QWidget):
    """Panel para crear nuevo documento con plantillas."""
    
    template_selected = pyqtSignal(str)
    document_selected = pyqtSignal(str)
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._setup_ui()
        
        theme_manager.theme_changed.connect(self._apply_style)

    def _setup_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        sidebar = QVBoxLayout()
        sidebar.setContentsMargins(10, 20, 10, 20)
        sidebar.setSpacing(20)
        
        self.btn_inicio = self._create_sidebar_button("🏠", "Inicio")
        self.btn_inicio.clicked.connect(lambda: self.template_selected.emit("home"))
        
        self.btn_nuevo = self._create_sidebar_button("📄", "Nuevo")
        self.btn_nuevo.setObjectName("activeButton")
        
        self.btn_abrir = self._create_sidebar_button("📂", "Abrir")
        self.btn_abrir.clicked.connect(self._open_file)
        
        sidebar.addWidget(self.btn_inicio)
        sidebar.addWidget(self.btn_nuevo)
        sidebar.addWidget(self.btn_abrir)
        
        sidebar.addStretch()
        
        self.btn_config = self._create_sidebar_button("⚙️", "Configuración")
        self.btn_cuenta = self._create_sidebar_button("👤", "Cuenta")
        
        sidebar.addWidget(self.btn_config)
        sidebar.addWidget(self.btn_cuenta)
        
        line = QFrame()
        line.setObjectName("separatorLine")
        
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(40, 30, 40, 30)
        content_layout.setSpacing(20)
        
        lbl_nuevo = QLabel("Nuevo")
        lbl_nuevo.setObjectName("panelTitle")
        lbl_nuevo.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        
        templates_label = QLabel("Plantillas")
        templates_label.setObjectName("sectionTitle")
        templates_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        
        templates_layout = QHBoxLayout()
        templates_layout.setSpacing(15)
        
        templates = ["Documento en blanco", "Bienvenida!!", "Tutorial de edición", "Tutorial versión 2.0"]
        
        for name in templates:
            box = self._create_template_box(name)
            templates_layout.addWidget(box)
        
        templates_layout.addStretch()
        
        tabs = QTabWidget()
        tabs.setObjectName("docTabs")
        
        tab_recientes = QWidget()
        tab_favoritos = QWidget()
        tab_compartidos = QWidget()
        
        tabs.addTab(tab_recientes, "Recientes")
        tabs.addTab(tab_favoritos, "Favoritos")
        tabs.addTab(tab_compartidos, "Compartidos conmigo")
        
        recientes_layout = QVBoxLayout(tab_recientes)
        recientes_layout.setSpacing(10)
        
        search = QLineEdit()
        search.setObjectName("searchBox")
        search.setPlaceholderText("Buscar...")
        
        self.lista_recientes = QListWidget()
        self.lista_recientes.itemDoubleClicked.connect(self._on_document_click)
        
        recientes_layout.addWidget(search)
        recientes_layout.addWidget(self.lista_recientes)
        
        tab_favoritos_layout = QVBoxLayout(tab_favoritos)
        tab_favoritos_layout.addWidget(QLabel("No hay favoritos aún"))
        
        tab_compartidos_layout = QVBoxLayout(tab_compartidos)
        tab_compartidos_layout.addWidget(QLabel("No hay documentos compartidos"))
        
        content_layout.addWidget(lbl_nuevo)
        content_layout.addWidget(templates_label)
        content_layout.addLayout(templates_layout)
        content_layout.addWidget(tabs)
        
        main_layout.addLayout(sidebar, 1)
        main_layout.addWidget(line)
        main_layout.addLayout(content_layout, 4)

    def _create_sidebar_button(self, icon: str, text: str) -> QPushButton:
        btn = QPushButton()
        btn.setObjectName("sidebarButton")
        
        layout = QVBoxLayout(btn)
        layout.setContentsMargins(5, 10, 5, 10)
        layout.setSpacing(5)
        
        icon_label = QLabel(icon)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setObjectName("sidebarIcon")
        
        text_label = QLabel(text)
        text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        text_label.setObjectName("sidebarText")
        
        layout.addWidget(icon_label)
        layout.addWidget(text_label)
        
        return btn

    def _open_file(self):
        from PyQt6.QtWidgets import QFileDialog
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar archivo PDF",
            "",
            "PDF Files (*.pdf)"
        )
        if file_path:
            self.document_selected.emit(file_path)

    def _create_template_box(self, text: str) -> QFrame:
        frame = QFrame()
        frame.setObjectName("templateBox")
        frame.setFixedSize(150, 180)
        
        container = QVBoxLayout(frame)
        container.setContentsMargins(10, 10, 10, 10)
        
        label = QLabel(text)
        label.setObjectName("templateLabel")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setWordWrap(True)
        
        container.addStretch()
        container.addWidget(label)
        container.addStretch()
        
        return frame

    def _on_document_click(self, item):
        self.document_selected.emit(item.file_path)

    def _apply_style(self):
        colors = theme_manager.colors
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {colors['bg_primary']};
            }}
            QWidget#sidebarButton {{
                background-color: transparent;
                border-radius: 8px;
            }}
            QWidget#sidebarButton:hover {{
                background-color: {colors['bg_tertiary']};
            }}
            QWidget#sidebarButton#activeButton {{
                background-color: {colors['accent']};
            }}
            QLabel#sidebarIcon {{
                font-size: 28px;
            }}
            QLabel#sidebarText {{
                color: {colors['fg_primary']};
                font-size: 12px;
            }}
            QFrame#separatorLine {{
                background-color: {colors['border']};
                width: 1px;
            }}
            QLabel#panelTitle {{
                color: {colors['fg_primary']};
                font-size: 24px;
                font-weight: bold;
            }}
            QLabel#sectionTitle {{
                color: {colors['fg_secondary']};
                font-size: 14px;
                font-weight: bold;
            }}
            QFrame#templateBox {{
                background-color: {colors['bg_tertiary']};
                border: 1px solid {colors['border']};
                border-radius: 8px;
            }}
            QFrame#templateBox:hover {{
                border-color: {colors['accent']};
            }}
            QLabel#templateLabel {{
                color: {colors['fg_primary']};
                font-size: 12px;
            }}
            QTabWidget::pane {{
                border: 1px solid {colors['border']};
                background-color: {colors['bg_primary']};
            }}
            QTabBar::tab {{
                background-color: {colors['bg_secondary']};
                color: {colors['fg_secondary']};
                padding: 8px 16px;
                border: none;
            }}
            QTabBar::tab:selected {{
                background-color: {colors['bg_primary']};
                color: {colors['fg_primary']};
                border-bottom: 2px solid {colors['accent']};
            }}
            QTabBar::tab:hover {{
                background-color: {colors['bg_tertiary']};
            }}
            QLineEdit#searchBox {{
                background-color: {colors['bg_tertiary']};
                color: {colors['fg_primary']};
                border: 1px solid {colors['border']};
                border-radius: 6px;
                padding: 8px;
                font-size: 13px;
            }}
            QLineEdit#searchBox::placeholder {{
                color: {colors['fg_disabled']};
            }}
            QListWidget {{
                background-color: {colors['bg_tertiary']};
                color: {colors['fg_primary']};
                border: none;
                border-radius: 6px;
            }}
            QListWidget::item {{
                padding: 10px;
                border-bottom: 1px solid {colors['border']};
            }}
            QListWidget::item:hover {{
                background-color: {colors['bg_current_line']};
            }}
        """)
