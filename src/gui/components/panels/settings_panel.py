from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QFrame, QScrollArea, QCheckBox, QComboBox, QSpinBox, 
    QGroupBox, QFormLayout, QLineEdit, QSlider, QListWidget
)
from PyQt6.QtCore import Qt, pyqtSignal
from typing import Optional

from src.gui.themes.theme_manager import theme_manager
from src.utils.app_settings import app_settings


class SettingsPanel(QWidget):
    """Panel de configuración de la aplicación."""
    
    settings_changed = pyqtSignal()
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._setup_ui()
        
        theme_manager.theme_changed.connect(self._apply_style)

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        title = QLabel("Configuración")
        title.setObjectName("panelTitle")
        main_layout.addWidget(title)
        
        scroll = QScrollArea()
        scroll.setObjectName("settingsScroll")
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(20)
        
        scroll_layout.addWidget(self._create_appearance_group())
        scroll_layout.addWidget(self._create_modules_group())
        scroll_layout.addWidget(self._create_files_group())
        scroll_layout.addWidget(self._create_about_group())
        
        scroll_layout.addStretch()
        
        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)
    
    def _create_appearance_group(self) -> QGroupBox:
        group = QGroupBox("Apariencia")
        group.setObjectName("settingsGroup")
        layout = QFormLayout(group)
        layout.setSpacing(10)
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Oscuro", "Claro"])
        self.theme_combo.setCurrentText("Oscuro" if app_settings.theme == "dark" else "Claro")
        self.theme_combo.currentTextChanged.connect(self._on_theme_changed)
        layout.addRow("Tema:", self.theme_combo)
        
        self.font_family_combo = QComboBox()
        self.font_family_combo.addItems(["Segoe UI", "Arial", "Times New Roman", "Courier New", "Consolas"])
        self.font_family_combo.setCurrentText(app_settings.font_family)
        self.font_family_combo.currentTextChanged.connect(self._on_font_changed)
        layout.addRow("Familia de fuente:", self.font_family_combo)
        
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(8, 24)
        self.font_size_spin.setValue(app_settings.font_size)
        self.font_size_spin.valueChanged.connect(self._on_font_size_changed)
        layout.addRow("Tamaño de fuente:", self.font_size_spin)
        
        return group
    
    def _create_modules_group(self) -> QGroupBox:
        group = QGroupBox("Módulos")
        group.setObjectName("settingsGroup")
        layout = QVBoxLayout(group)
        layout.setSpacing(8)
        
        info = QLabel("Activa o desactiva los módulos disponibles en la aplicación:")
        info.setObjectName("groupInfo")
        layout.addWidget(info)
        
        self.modules = {}
        modules_list = [
            ("repair", "Reparar PDF"),
            ("merge", "Unir PDFs"),
            ("split", "Dividir PDF"),
            ("extract", "Extraer páginas"),
            ("compress", "Comprimir PDF"),
            ("encrypt", "Encriptar PDF"),
        ]
        
        for key, label in modules_list:
            checkbox = QCheckBox(label)
            checkbox.setChecked(app_settings.get(f"modules.{key}", True))
            checkbox.stateChanged.connect(lambda state, k=key: self._on_module_changed(k, state))
            self.modules[key] = checkbox
            layout.addWidget(checkbox)
        
        return group
    
    def _create_files_group(self) -> QGroupBox:
        group = QGroupBox("Archivos")
        group.setObjectName("settingsGroup")
        layout = QFormLayout(group)
        layout.setSpacing(10)
        
        self.max_file_size_spin = QSpinBox()
        self.max_file_size_spin.setRange(10, 2000)
        self.max_file_size_spin.setSuffix(" MB")
        self.max_file_size_spin.setValue(app_settings.get("supported_files.max_file_size_mb", 500))
        self.max_file_size_spin.valueChanged.connect(self._on_max_file_size_changed)
        layout.addRow("Tamaño máximo:", self.max_file_size_spin)
        
        self.recent_files_spin = QSpinBox()
        self.recent_files_spin.setRange(5, 50)
        self.recent_files_spin.setValue(app_settings.get("recent_files.max_count", 20))
        self.recent_files_spin.valueChanged.connect(self._on_recent_count_changed)
        layout.addRow("Archivos recientes:", self.recent_files_spin)
        
        return group
    
    def _create_about_group(self) -> QGroupBox:
        group = QGroupBox("Acerca de")
        group.setObjectName("settingsGroup")
        layout = QVBoxLayout(group)
        layout.setSpacing(8)
        
        name = QLabel("Xebec PDF Fixer")
        name.setObjectName("appName")
        layout.addWidget(name)
        
        version = QLabel("Versión 1.0.0")
        version.setObjectName("versionText")
        layout.addWidget(version)
        
        desc = QLabel("Herramienta de administración de PDFs\nDesarrollado por BGNC - Corporación Xebec")
        desc.setObjectName("descText")
        layout.addWidget(desc)
        
        return group
    
    def _on_theme_changed(self, text: str):
        theme = "dark" if text == "Oscuro" else "light"
        app_settings.theme = theme
        theme_manager.set_theme(theme)
        self.settings_changed.emit()
    
    def _on_font_changed(self, text: str):
        app_settings.font_family = text
        self.settings_changed.emit()
    
    def _on_font_size_changed(self, value: int):
        app_settings.font_size = value
        self.settings_changed.emit()
    
    def _on_module_changed(self, module: str, state: int):
        app_settings.set(f"modules.{module}", state == Qt.CheckState.Checked)
        self.settings_changed.emit()
    
    def _on_max_file_size_changed(self, value: int):
        app_settings.set("supported_files.max_file_size_mb", value)
        self.settings_changed.emit()
    
    def _on_recent_count_changed(self, value: int):
        app_settings.set("recent_files.max_count", value)
        self.settings_changed.emit()

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
            QGroupBox#settingsGroup {{
                color: {colors['fg_primary']};
                font-weight: bold;
                border: 1px solid {colors['border']};
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 5px;
            }}
            QLabel#groupInfo {{
                color: {colors['fg_secondary']};
                font-weight: normal;
                font-size: 12px;
            }}
            QLabel#appName {{
                color: {colors['fg_primary']};
                font-size: 18px;
                font-weight: bold;
            }}
            QLabel#versionText {{
                color: {colors['fg_secondary']};
                font-size: 12px;
            }}
            QLabel#descText {{
                color: {colors['fg_secondary']};
                font-size: 11px;
                line-height: 1.5;
            }}
            QComboBox, QSpinBox {{
                background-color: {colors['bg_tertiary']};
                color: {colors['fg_primary']};
                border: 1px solid {colors['border']};
                border-radius: 4px;
                padding: 5px;
                min-width: 150px;
            }}
            QComboBox::drop-down {{
                border: none;
                width: 20px;
            }}
            QComboBox::down-arrow {{
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 6px solid {colors['fg_secondary']};
            }}
            QCheckBox {{
                color: {colors['fg_primary']};
                spacing: 8px;
            }}
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                border-radius: 3px;
                border: 1px solid {colors['border']};
                background-color: {colors['bg_tertiary']};
            }}
            QCheckBox::indicator:checked {{
                background-color: {colors['accent']};
            }}
            QScrollArea#settingsScroll {{
                border: none;
                background-color: transparent;
            }}
            QScrollBar:vertical {{
                width: 8px;
                background: transparent;
            }}
            QScrollBar::handle:vertical {{
                background: {colors['bg_current_line']};
                border-radius: 4px;
                min-height: 40px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: {colors['accent']};
            }}
        """)
