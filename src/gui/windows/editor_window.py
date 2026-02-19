from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QFrame, QFileDialog, QScrollArea, QSplitter, QSizePolicy,
    QToolBar, QToolButton, QStatusBar, QDialog
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QAction
from pathlib import Path
from typing import Optional

from src.gui.themes.theme_manager import theme_manager


class EditorWindow(QFrame):
    file_opened = pyqtSignal(str)
    close_requested = pyqtSignal()
    
    def __init__(self, document_type: str = "blank", parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.document_type = document_type
        self.current_file_path = None
        self._has_unsaved_changes = False
        self._setup_ui()
        
        theme_manager.theme_changed.connect(self._apply_style)
        
        self._load_document()
    
    def mark_as_modified(self):
        self._has_unsaved_changes = True
        self._update_window_title()
    
    def mark_as_saved(self):
        self._has_unsaved_changes = False
        self._update_window_title()
    
    def _update_window_title(self):
        if hasattr(self, 'file_name_label'):
            title = self.file_name_label.text()
            if self._has_unsaved_changes and not title.startswith("*"):
                self.file_name_label.setText(f"*{title}")
            elif not self._has_unsaved_changes and title.startswith("*"):
                self.file_name_label.setText(title[1:])
    
    def _load_document(self):
        if self.document_type == "blank":
            self.file_name_label.setText("Nuevo Documento en Blanco")
            self.info_label.setText("Documento en blanco - listo para editar")
            self.status_label.setText("Nuevo documento creado")
        elif self.document_type == "suggestion":
            self.file_name_label.setText("Documento de Sugerencia")
            self.info_label.setText("Documento de sugerencia")
            self.status_label.setText("Listo")
        elif self.document_type == "recent":
            self.file_name_label.setText("Documento Reciente")
            self.info_label.setText("Documento reciente")
            self.status_label.setText("Listo")
    
    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        self.ribbon_panel = self._create_ribbon_panel()
        main_layout.addWidget(self.ribbon_panel)
        
        content_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        self.left_panel = self._create_left_panel()
        content_splitter.addWidget(self.left_panel)
        
        center_container = QWidget()
        center_layout = QVBoxLayout(center_container)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(0)
        
        self.center_panel = self._create_center_panel()
        center_layout.addWidget(self.center_panel, 8)
        
        self.bottom_panel = self._create_bottom_panel()
        center_layout.addWidget(self.bottom_panel, 1)
        
        content_splitter.addWidget(center_container)
        
        self.right_panel = self._create_right_panel()
        content_splitter.addWidget(self.right_panel)
        
        content_splitter.setSizes([60, 800, 60])
        
        main_layout.addWidget(content_splitter, 1)
    
    def _create_left_panel(self):
        panel = QFrame()
        panel.setFixedWidth(60)
        panel.setObjectName("leftPanel")
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(5, 20, 5, 20)
        layout.setSpacing(15)
        
        btn_home = QPushButton("🏠")
        btn_home.setFixedSize(50, 50)
        btn_home.setToolTip("Inicio")
        btn_home.clicked.connect(self._go_home)
        
        btn_new = QPushButton("📄")
        btn_new.setFixedSize(50, 50)
        btn_new.setToolTip("Nuevo")
        btn_new.clicked.connect(self._new_document)
        
        btn_open = QPushButton("📂")
        btn_open.setFixedSize(50, 50)
        btn_open.setToolTip("Abrir")
        btn_open.clicked.connect(self._open_pdf)
        
        btn_save = QPushButton("💾")
        btn_save.setFixedSize(50, 50)
        btn_save.setToolTip("Guardar")
        btn_save.clicked.connect(self._save_pdf)
        
        layout.addWidget(btn_home)
        layout.addWidget(btn_new)
        layout.addWidget(btn_open)
        layout.addWidget(btn_save)
        
        layout.addStretch()
        
        return panel
    
    def _create_ribbon_panel(self):
        panel = QFrame()
        panel.setFixedHeight(120)
        panel.setObjectName("ribbonPanel")
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(5)
        
        self.file_name_label = QLabel("Sin archivo abierto")
        self.file_name_label.setObjectName("fileNameLabel")
        layout.addWidget(self.file_name_label)
        
        ribbon_toolbar = QFrame()
        ribbon_toolbar.setObjectName("ribbonToolbar")
        ribbon_layout = QHBoxLayout(ribbon_toolbar)
        ribbon_layout.setContentsMargins(10, 10, 10, 10)
        ribbon_layout.setSpacing(20)
        
        file_section = self._create_ribbon_section("Archivo", [
            ("📄", "Nuevo", self._new_document),
            ("📂", "Abrir", self._open_pdf),
            ("💾", "Guardar", self._save_pdf),
            ("📑", "Exportar", self._export_pdf),
        ])
        ribbon_layout.addWidget(file_section)
        
        edit_section = self._create_ribbon_section("Editar", [
            ("✂️", "Cortar", self._cut),
            ("📋", "Copiar", self._copy),
            ("📝", "Pegar", self._paste),
            ("↩️", "Deshacer", self._undo),
            ("↪️", "Rehacer", self._redo),
        ])
        ribbon_layout.addWidget(edit_section)
        
        view_section = self._create_ribbon_section("Ver", [
            ("🔍+", "Acercar", self._zoom_in),
            ("🔍-", "Alejar", self._zoom_out),
            ("📄", "Página", self._view_page),
            ("📑", "Todas", self._view_all),
        ])
        ribbon_layout.addWidget(view_section)
        
        tools_section = self._create_ribbon_section("Herramientas", [
            ("🔧", "Reparar", self._repair),
            ("🔀", "Ordenar", self._organize),
            ("🔒", "Proteger", self._protect),
        ])
        ribbon_layout.addWidget(tools_section)
        
        ribbon_layout.addStretch()
        
        layout.addWidget(ribbon_toolbar)
        
        return panel
    
    def _create_ribbon_section(self, title: str, buttons: list) -> QFrame:
        section = QFrame()
        section.setObjectName("ribbonSection")
        
        layout = QVBoxLayout(section)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(2)
        
        title_label = QLabel(title)
        title_label.setObjectName("ribbonSectionTitle")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(5)
        
        for icon, tooltip, callback in buttons:
            btn = QPushButton(icon)
            btn.setFixedSize(50, 50)
            btn.setToolTip(tooltip)
            btn.clicked.connect(callback)
            buttons_layout.addWidget(btn)
        
        layout.addLayout(buttons_layout)
        
        return section
    
    def _create_center_panel(self):
        panel = QFrame()
        panel.setObjectName("centerPanel")
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(10, 10, 10, 10)
        
        self.info_label = QLabel("Seleccione un archivo PDF para comenzar a trabajar")
        self.info_label.setObjectName("editorInfo")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.info_label, 1)
        
        return panel
    
    def _create_bottom_panel(self):
        panel = QFrame()
        panel.setFixedHeight(60)
        panel.setObjectName("bottomPanel")
        
        layout = QHBoxLayout(panel)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(20)
        
        self.page_info_label = QLabel("Página: -")
        self.page_info_label.setObjectName("pageInfo")
        layout.addWidget(self.page_info_label)
        
        self.zoom_info_label = QLabel("Zoom: 100%")
        self.zoom_info_label.setObjectName("zoomInfo")
        layout.addWidget(self.zoom_info_label)
        
        self.status_label = QLabel("Listo")
        self.status_label.setObjectName("editorStatus")
        layout.addWidget(self.status_label)
        
        layout.addStretch()
        
        return panel
    
    def _create_right_panel(self):
        panel = QFrame()
        panel.setFixedWidth(60)
        panel.setObjectName("rightPanel")
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(5, 20, 5, 20)
        layout.setSpacing(15)
        
        btn_zoom_in = QPushButton("🔍+")
        btn_zoom_in.setFixedSize(50, 40)
        btn_zoom_in.setToolTip("Acercar")
        
        btn_zoom_out = QPushButton("🔍-")
        btn_zoom_out.setFixedSize(50, 40)
        btn_zoom_out.setToolTip("Alejar")
        
        btn_rotate = QPushButton("🔄")
        btn_rotate.setFixedSize(50, 40)
        btn_rotate.setToolTip("Rotar")
        
        btn_tools = QPushButton("🔧")
        btn_tools.setFixedSize(50, 40)
        btn_tools.setToolTip("Herramientas")
        
        layout.addWidget(btn_zoom_in)
        layout.addWidget(btn_zoom_out)
        layout.addWidget(btn_rotate)
        layout.addWidget(btn_tools)
        
        layout.addStretch()
        
        return panel
    
    def _open_pdf(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar archivo PDF",
            "",
            "PDF Files (*.pdf)"
        )
        
        if file_path:
            self.current_file_path = file_path
            file_name = Path(file_path).name
            self.file_name_label.setText(file_name)
            self.info_label.setText(f"Archivo cargado: {file_name}")
            self.status_label.setText("Archivo abierto correctamente")
            self.file_opened.emit(file_path)
    
    def load_file(self, file_path: str):
        self.current_file_path = file_path
        file_name = Path(file_path).name
        self.file_name_label.setText(file_name)
        self.info_label.setText(f"Archivo cargado: {file_name}")
        self.status_label.setText("Archivo abierto correctamente")
        self.mark_as_saved()
        self.file_opened.emit(file_path)
    
    def _go_home(self):
        self.close_requested.emit()
    
    def _new_document(self):
        self.file_name_label.setText("Nuevo Documento")
        self.info_label.setText("Nuevo documento en blanco creado")
        self.status_label.setText("Listo para editar")
        self.current_file_path = None
        self.mark_as_modified()
    
    def _save_pdf(self):
        self.status_label.setText("Guardando...")
    
    def _export_pdf(self):
        self.status_label.setText("Exportando...")
    
    def _cut(self):
        self.status_label.setText("Cortando...")
    
    def _copy(self):
        self.status_label.setText("Copiando...")
    
    def _paste(self):
        self.status_label.setText("Pegando...")
    
    def _undo(self):
        self.status_label.setText("Deshacer")
    
    def _redo(self):
        self.status_label.setText("Rehacer")
    
    def _zoom_in(self):
        self.status_label.setText("Acercar")
    
    def _zoom_out(self):
        self.status_label.setText("Alejar")
    
    def _view_page(self):
        self.status_label.setText("Vista de página")
    
    def _view_all(self):
        self.status_label.setText("Ver todas las páginas")
    
    def _repair(self):
        self.status_label.setText("Reparando PDF...")
    
    def _organize(self):
        self.status_label.setText("Organizar páginas")
    
    def _protect(self):
        self.status_label.setText("Proteger PDF")
    
    def _apply_style(self):
        colors = theme_manager.colors
        self.setStyleSheet(f"""
            QFrame#leftPanel {{
                background-color: {colors['bg_secondary']};
                border-right: 1px solid {colors['border']};
            }}
            QFrame#ribbonPanel {{
                background-color: {colors['bg_tertiary']};
                border-bottom: 1px solid {colors['border']};
            }}
            QLabel#fileNameLabel {{
                color: {colors['fg_primary']};
                font-size: 14px;
                font-weight: bold;
            }}
            QFrame#ribbonSection {{
                background-color: transparent;
                border-radius: 4px;
            }}
            QLabel#ribbonSectionTitle {{
                color: {colors['fg_secondary']};
                font-size: 10px;
                font-weight: bold;
            }}
            QFrame#centerPanel {{
                background-color: {colors['bg_primary']};
            }}
            QLabel#editorInfo {{
                color: {colors['fg_secondary']};
                font-size: 16px;
            }}
            QFrame#rightPanel {{
                background-color: {colors['bg_secondary']};
                border-left: 1px solid {colors['border']};
            }}
            QFrame#bottomPanel {{
                background-color: {colors['bg_secondary']};
                border-top: 1px solid {colors['border']};
            }}
            QLabel#pageInfo, QLabel#zoomInfo {{
                color: {colors['fg_secondary']};
                font-size: 11px;
            }}
            QLabel#editorStatus {{
                color: {colors['fg_secondary']};
                font-size: 11px;
            }}
            QPushButton {{
                background-color: {colors['bg_tertiary']};
                color: {colors['fg_primary']};
                border: none;
                border-radius: 6px;
                font-size: 18px;
            }}
            QPushButton:hover {{
                background-color: {colors['accent']};
            }}
        """)


class EditorWindowContainer(QDialog):
    close_requested = pyqtSignal()
    
    def __init__(self, document_type: str = "blank", parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.document_type = document_type
        self._setup_ui()
        
        theme_manager.theme_changed.connect(self._apply_theme)
        
        if self.editor:
            self.editor.close_requested.connect(self._on_editor_close_requested)
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        title_bar = QFrame()
        title_bar.setFixedHeight(40)
        title_bar.setObjectName("titleBar")
        title_bar.setCursor(Qt.CursorShape.SizeAllCursor)
        
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(15, 0, 10, 0)
        
        title_label = QLabel("Editor de PDF - Xebec")
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
        close_btn.clicked.connect(self._on_close_clicked)
        
        title_layout.addWidget(minimize_btn)
        title_layout.addWidget(maximize_btn)
        title_layout.addWidget(close_btn)
        
        layout.addWidget(title_bar)
        
        self.editor = EditorWindow(document_type=self.document_type, parent=self)
        layout.addWidget(self.editor, 1)
        
        self._center_window()
    
    def _on_editor_close_requested(self):
        self._confirm_close()
    
    def _on_close_clicked(self):
        self._confirm_close()
    
    def _confirm_close(self):
        from PyQt6.QtWidgets import QMessageBox
        
        if self.editor and self.editor._has_unsaved_changes:
            reply = QMessageBox.question(
                self,
                "Cambios sin guardar",
                "¿Desea cerrar sin guardar los cambios?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.close()
                self.close_requested.emit()
        else:
            self.close()
            self.close_requested.emit()
    
    def _center_window(self):
        screen = self.screen()
        if screen is None:
            self.setGeometry(100, 100, 1200, 800)
            return
        screen_geometry = screen.geometry()
        window_width = 1200
        window_height = 800
        
        x = (screen_geometry.width() - window_width) // 2
        y = (screen_geometry.height() - window_height) // 2
        self.setGeometry(x, y, window_width, window_height)
    
    def _toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
            self._center_window()
        else:
            self.showMaximized()
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_position = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and hasattr(self, '_drag_position'):
            delta = event.globalPosition().toPoint() - self._drag_position
            self.move(self.pos() + delta)
            self._drag_position = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        if hasattr(self, '_drag_position'):
            self._drag_position = None
    
    def closeEvent(self, event):
        from PyQt6.QtWidgets import QMessageBox
        
        if self.editor and self.editor._has_unsaved_changes:
            reply = QMessageBox.question(
                self,
                "Cambios sin guardar",
                "¿Desea cerrar sin guardar los cambios?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                event.accept()
                self.close_requested.emit()
            else:
                event.ignore()
        else:
            event.accept()
            self.close_requested.emit()
    
    def _apply_theme(self):
        colors = theme_manager.colors
        self.setStyleSheet(f"""
            QFrame#titleBar {{
                background-color: {colors['bg_secondary']};
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
                background-color: {colors['bg_tertiary']};
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
        """)
