from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QStackedWidget
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon
from pathlib import Path

from src.gui.themes.theme_manager import theme_manager
from src.gui.windows.window_manager import window_manager
from src.gui.components import Sidebar, StartPanel, SettingsPanel, AccountPanel
from src.utils.logger import logger


APP_NAME = "Xebec PDF Fixer"
APP_VERSION = "1.0.0"


class MainWindow(QMainWindow):
    close_requested = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.log = logger.get_logger()
        self._setup_window()
        self._setup_ui()
        self._apply_theme()
        
        # Set window icon
        icon_path = Path(__file__).parent.parent.parent / "assets" / "icons" / "icono.png"
        if not icon_path.exists():
            icon_path = Path.cwd() / "assets" / "icons" / "icono.png"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))
        
        self.hide()
        
        theme_manager.theme_changed.connect(self._apply_theme)
        theme_manager.emit_change()
        
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
        
        self.sidebar.open_editor.connect(self._open_editor_window)
        self.sidebar.open_settings.connect(self._show_settings)
        self.sidebar.open_account.connect(self._show_account)
    
    def _open_editor_window(self, document_type: str = "blank"):
        logger.action(f"Solicitando abrir editor - tipo: {document_type}")
        window_manager.push_window("main")
        window_manager.show_editor(document_type=document_type)
    
    def _show_settings(self):
        logger.nav(f"Mostrando panel de Configuración")
        self.content_stack.setCurrentWidget(self.settings_panel)
    
    def _show_account(self):
        logger.nav(f"Mostrando panel de Cuenta")
        self.content_stack.setCurrentWidget(self.account_panel)

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

    def _create_content_area(self):
        content_container = QWidget()
        content_container.setObjectName("contentArea")
        
        content_layout = QHBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        self.sidebar = Sidebar()
        content_layout.addWidget(self.sidebar)
        
        self.content_stack = QStackedWidget()
        
        self.start_panel = StartPanel()
        self.start_panel.document_selected.connect(self._open_file_in_editor)
        self.start_panel.template_selected.connect(self._open_template_in_editor)
        
        self.settings_panel = SettingsPanel()
        self.account_panel = AccountPanel()
        
        self.content_stack.addWidget(self.start_panel)
        self.content_stack.addWidget(self.settings_panel)
        self.content_stack.addWidget(self.account_panel)
        
        content_layout.addWidget(self.content_stack, 1)
        
        self.main_layout.addWidget(content_container)
    
    def _open_file_in_editor(self, file_path: str):
        logger.file(f"Abriendo archivo en editor: {file_path}")
        window_manager.push_window("main")
        window_manager.show_editor(document_type="file", file_path=file_path)
    
    def _open_template_in_editor(self, template_name: str):
        logger.file(f"Abriendo plantilla en editor: {template_name}")
        window_manager.push_window("main")
        window_manager.show_editor(document_type="blank")

    def _apply_theme(self):
        self.setStyleSheet("""
            QMainWindow {
                background: #1A202C;
            }
            QFrame#titleBar {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1E3A5F, stop:0.5 #0E2A4F, stop:1 #1A202C) !important;
            }
            QLabel#titleLabel {
                color: #FFFFFF;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton#titleButton {
                background: transparent;
                color: #FFFFFF;
                border: none;
                font-size: 14px;
            }
            QPushButton#titleButton:hover {
                background: rgba(255, 255, 255, 0.2);
                color: white;
            }
            QPushButton#closeButton {
                background: transparent;
                color: #FFFFFF;
                border: none;
                font-size: 14px;
            }
            QPushButton#closeButton:hover {
                background: #E53E3E;
                color: white;
            }
        """)
        
        self.setPalette(theme_manager.get_palette())

    def _toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()
