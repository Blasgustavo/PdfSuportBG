from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QMessageBox,
    QStackedWidget
)
from PyQt6.QtCore import Qt, QTimer, QPoint, pyqtSignal
from PyQt6.QtGui import QAction, QMouseEvent
from typing import Optional

from src.gui.pyqt6.theme_manager import theme_manager
from src.gui.pyqt6.window_manager import window_manager
from src.gui.pyqt6.components import Sidebar, StartPanel, NewDocumentPanel, RepairPanel, MergePanel, SplitPanel, SettingsPanel
from src.utils.logger import logger


APP_NAME = "Xebec PDF Fixer"
APP_VERSION = "1.0.0"


class MainWindow(QMainWindow):
    close_requested = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.log = logger.get_logger()
        self._setup_window()
        self._apply_theme()  # Aplicar tema inmediatamente
        self._setup_ui()
        
        theme_manager.theme_changed.connect(self._apply_theme)
        
        self._drag_position = None

    def closeEvent(self, event):
        if window_manager.has_editor_open:
            event.ignore()
            return
        self.close_requested.emit()
        event.accept()

    def _setup_window(self):
        self.setWindowTitle(APP_NAME)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setMinimumSize(900, 600)
        self.showMaximized()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_position = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self._drag_position:
            delta = event.globalPosition().toPoint() - self._drag_position
            self.move(self.pos() + delta)
            self._drag_position = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self._drag_position = None

    def _setup_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        self._create_title_bar()
        self._create_content_area()
        
        self._setup_panels()
        
        self.sidebar.navigation_requested.connect(self._on_navigation)
        self.sidebar.open_editor.connect(self._open_editor_window)
    
    def _open_editor_window(self, document_type: str = "blank"):
        window_manager.push_window("main")
        window_manager.show_editor(document_type=document_type)
    
    def _on_editor_closed(self):
        window_manager.close_editor()

    def _create_title_bar(self):
        title_bar = QFrame()
        title_bar.setFixedHeight(40)
        title_bar.setObjectName("titleBar")
        title_bar.setCursor(Qt.CursorShape.SizeAllCursor)
        
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(15, 0, 10, 0)
        
        title_label = QLabel("Xebec Pdf")
        title_label.setObjectName("titleLabel")
        title_layout.addWidget(title_label)
        
        title_layout.addStretch()
        
        minimize_btn = QPushButton("─")
        minimize_btn.setFixedSize(40, 30)
        minimize_btn.setObjectName("titleButton")
        minimize_btn.clicked.connect(self.showMinimized)
        
        maximize_btn = QPushButton("□")
        maximize_btn.setFixedSize(40, 30)
        maximize_btn.setObjectName("titleButton")
        maximize_btn.clicked.connect(self._toggle_maximize)
        
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(40, 30)
        close_btn.setObjectName("closeButton")
        close_btn.clicked.connect(self.close)
        
        title_layout.addWidget(minimize_btn)
        title_layout.addWidget(maximize_btn)
        title_layout.addWidget(close_btn)
        
        self.main_layout.addWidget(title_bar)

    def _setup_panels(self):
        self.panels = {}
        
        self.start_panel = StartPanel()
        self.panels["home"] = self.start_panel
        self.panels["new"] = NewDocumentPanel()
        self.panels["new"].template_selected.connect(self._on_navigation)
        self.panels["repair"] = RepairPanel()
        self.panels["merge"] = MergePanel()
        self.panels["split"] = SplitPanel()
        self.panels["settings"] = SettingsPanel()
        
        for name, panel in self.panels.items():
            self.content_stack.addWidget(panel)
        
        self.content_stack.setCurrentWidget(self.start_panel)

    def _on_navigation(self, page: str):
        if page in self.panels:
            self.content_stack.setCurrentWidget(self.panels[page])
            self.log.info(f"Navegando a: {page}")

    def _create_content_area(self):
        content_container = QWidget()
        content_container.setObjectName("contentArea")
        
        content_layout = QHBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        self.sidebar = Sidebar()
        content_layout.addWidget(self.sidebar)
        
        self.content_stack = QStackedWidget()
        content_layout.addWidget(self.content_stack)
        
        self.main_layout.addWidget(content_container)

    def _create_menu_bar(self):
        self._menubar = self.menuBar()
        
        file_menu = self._menubar.addMenu("Archivo")
        
        open_action = QAction("Abrir PDF...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(lambda: self._on_navigation("repair"))
        file_menu.addAction(open_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Salir", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        tools_menu = self._menubar.addMenu("Herramientas")
        
        repair_action = QAction("Reparar PDF", self)
        repair_action.triggered.connect(lambda: self._on_navigation("repair"))
        tools_menu.addAction(repair_action)
        
        merge_action = QAction("Unir PDFs", self)
        merge_action.triggered.connect(lambda: self._on_navigation("merge"))
        tools_menu.addAction(merge_action)
        
        split_action = QAction("Dividir PDF", self)
        split_action.triggered.connect(lambda: self._on_navigation("split"))
        tools_menu.addAction(split_action)
        
        help_menu = self._menubar.addMenu("Ayuda")
        
        about_action = QAction("Acerca de", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)

    def _apply_theme(self):
        colors = theme_manager.colors
        
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {colors['bg_primary']};
            }}
            QFrame#titleBar {{
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {colors['primary']}, stop:1 {colors['primary_light']});
            }}
            QLabel#titleLabel {{
                color: {colors['fg_primary']};
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton#titleButton {{
                background-color: transparent;
                color: {colors['fg_secondary']};
                border: none;
                font-size: 14px;
            }}
            QPushButton#titleButton:hover {{
                background-color: rgba(255, 255, 255, 0.1);
                color: white;
            }}
            QPushButton#closeButton {{
                background-color: transparent;
                color: {colors['fg_secondary']};
                border: none;
                font-size: 14px;
            }}
            QPushButton#closeButton:hover {{
                background-color: {colors['error']};
                color: white;
            }}
            QFrame#contentArea {{
                background-color: {colors['bg_primary']};
            }}
            QLabel#welcomeLabel {{
                color: {colors['fg_primary']};
                font-size: 28px;
                font-weight: bold;
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
            QMenuBar {{
                background-color: {colors['bg_secondary']};
                color: {colors['fg_primary']};
                border-bottom: 1px solid {colors['border']};
            }}
            QMenuBar::item:selected {{
                background-color: {colors['bg_tertiary']};
            }}
            QMenu {{
                background-color: {colors['bg_secondary']};
                color: {colors['fg_primary']};
                border: 1px solid {colors['border']};
                border-radius: 4px;
            }}
            QMenu::item:selected {{
                background-color: {colors['accent']};
            }}
        """)
        
        self.setPalette(theme_manager.get_palette())

    def _toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def _show_about(self):
        QMessageBox.about(
            self,
            "Acerca de Xebec Pdf Fixer",
            f"<h3>{APP_NAME}</h3>"
            f"<p>Versión: {APP_VERSION}</p>"
            f"<p>Herramienta de administración de PDFs para Windows</p>"
            f"<p>Desarrollado por BGNC - Corporación Xebec</p>"
        )
