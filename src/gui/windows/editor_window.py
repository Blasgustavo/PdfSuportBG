from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QFrame, QFileDialog, QSplitter,
    QToolBar, QToolButton, QStatusBar, QDialog, QListWidget, QListWidgetItem
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QEvent, QMargins
from PyQt6.QtGui import QAction, QIcon, QKeySequence, QShortcut, QKeyEvent
from PyQt6.QtPdf import QPdfDocument
from PyQt6.QtPdfWidgets import QPdfView
from pathlib import Path
from typing import Optional

from src.gui.themes.theme_manager import theme_manager


class PDFViewerWidget(QPdfView):
    """Custom QPdfView that emits signals for keyboard shortcuts."""
    
    # Signals for keyboard shortcuts
    zoom_in_requested = pyqtSignal()
    zoom_out_requested = pyqtSignal()
    zoom_reset_requested = pyqtSignal()
    next_page_requested = pyqtSignal()
    previous_page_requested = pyqtSignal()
    first_page_requested = pyqtSignal()
    last_page_requested = pyqtSignal()
    help_requested = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
    
    def keyPressEvent(self, event):
        """Handle key press events for zoom and navigation shortcuts."""
        key = event.key()
        modifiers = event.modifiers()
        
        # Ctrl + = or Ctrl + + (zoom in)
        if modifiers == Qt.KeyboardModifier.ControlModifier and (key == Qt.Key.Key_Equal or key == Qt.Key.Key_Plus):
            self.zoom_in_requested.emit()
            return
        
        # Ctrl + - (zoom out)
        if modifiers == Qt.KeyboardModifier.ControlModifier and key == Qt.Key.Key_Minus:
            self.zoom_out_requested.emit()
            return
        
        # Ctrl + 0 (zoom reset)
        if modifiers == Qt.KeyboardModifier.ControlModifier and key == Qt.Key.Key_0:
            self.zoom_reset_requested.emit()
            return
        
        # Ctrl + Right (next page)
        if modifiers == Qt.KeyboardModifier.ControlModifier and key == Qt.Key.Key_Right:
            self.next_page_requested.emit()
            return
        
        # Ctrl + Left (previous page)
        if modifiers == Qt.KeyboardModifier.ControlModifier and key == Qt.Key.Key_Left:
            self.previous_page_requested.emit()
            return
        
        # Home (first page)
        if key == Qt.Key.Key_Home:
            self.first_page_requested.emit()
            return
        
        # End (last page)
        if key == Qt.Key.Key_End:
            self.last_page_requested.emit()
            return
        
        # F1 or Ctrl + / (help)
        if key == Qt.Key.Key_F1 or (modifiers == Qt.KeyboardModifier.ControlModifier and key == Qt.Key.Key_Slash):
            self.help_requested.emit()
            return
        
        # Call parent for other keys
        super().keyPressEvent(event)


class EditorWindow(QFrame):
    file_opened = pyqtSignal(str)
    close_requested = pyqtSignal()
    
    # Modos de operación
    MODE_READ = "read"
    MODE_EDIT = "edit"
    
    def __init__(self, document_type: str = "blank", parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.document_type = document_type
        self.current_file_path = None
        self._has_unsaved_changes = False
        
        # Estado del visor PDF
        self._current_mode = self.MODE_READ  # Modo lectura por defecto
        self._current_page = 0
        self._zoom_level = 1.0
        self._pdf_document = None  # QPdfDocument
        self._total_pages = 0
        
        # Cursor timer para restaurar cursor
        self._cursor_timer = QTimer()
        self._cursor_timer.timeout.connect(self._restore_cursor)
        
        # Install event filter for keyboard shortcuts
        self.installEventFilter(self)
        
        self._setup_ui()
        
        theme_manager.theme_changed.connect(self._apply_style)
        
        self._load_document()
    
    @property
    def mode(self):
        return self._current_mode
    
    @mode.setter
    def mode(self, value):
        self._current_mode = value
        self._update_mode_buttons()
        self._apply_mode_style()
    
    def set_mode_read(self):
        """Cambiar a modo lectura."""
        self.mode = self.MODE_READ
        self.status_label.setText("Modo Lectura")
    
    def set_mode_edit(self):
        """Cambiar a modo edición."""
        self.mode = self.MODE_EDIT
        self.status_label.setText("Modo Edición")
    
    def mark_as_modified(self):
        self._has_unsaved_changes = True
        self._update_window_title()
    
    def mark_as_saved(self):
        self._has_unsaved_changes = False
        self._update_window_title()
    
    def _set_temp_cursor(self, cursor_shape: Qt.CursorShape):
        """Cambia temporalmente el cursor y lo restaura después de 500ms."""
        if hasattr(self, 'pdf_view') and self.pdf_view:
            self.pdf_view.setCursor(cursor_shape)
        
        # Reiniciar timer
        self._cursor_timer.stop()
        self._cursor_timer.start(500)  # 500ms
    
    def _restore_cursor(self):
        """Restaura el cursor predeterminado."""
        self._cursor_timer.stop()
        if hasattr(self, 'pdf_view') and self.pdf_view:
            self.pdf_view.setCursor(Qt.CursorShape.ArrowCursor)
    
    def _go_to_first_page(self):
        """Ir a la primera página."""
        if self._pdf_document and self._total_pages > 0:
            self._current_page = 0
            nav = self.pdf_view.pageNavigator()
            from PyQt6.QtCore import QPointF
            current_zoom = self.pdf_view.zoomFactor()
            nav.jump(0, QPointF(), current_zoom)
            self.page_info_label.setText(f"Página: 1 / {self._total_pages}")
            self.status_label.setText("Primera página")
            self._set_temp_cursor(Qt.CursorShape.PointingHandCursor)
    
    def _go_to_last_page(self):
        """Ir a la última página."""
        if self._pdf_document and self._total_pages > 0:
            self._current_page = self._total_pages - 1
            nav = self.pdf_view.pageNavigator()
            from PyQt6.QtCore import QPointF
            current_zoom = self.pdf_view.zoomFactor()
            nav.jump(self._current_page, QPointF(), current_zoom)
            self.page_info_label.setText(f"Página: {self._total_pages} / {self._total_pages}")
            self.status_label.setText(f"Página {self._total_pages}")
            self._set_temp_cursor(Qt.CursorShape.PointingHandCursor)
    
    def _show_commands_dialog(self):
        """Muestra un diálogo con todos los comandos disponibles."""
        # Verificar si ya hay un diálogo abierto
        for widget in self.findChildren(QDialog, "commandsDialog"):
            widget.close()
        
        dialog = QDialog(self)
        dialog.setObjectName("commandsDialog")
        dialog.setWindowTitle("Atajos de Teclado")
        dialog.setMinimumSize(500, 400)
        
        # Centrar diálogo
        dialog.setGeometry(
            self.x() + (self.width() - 500) // 2,
            self.y() + (self.height() - 400) // 2,
            500, 400
        )
        
        layout = QVBoxLayout(dialog)
        
        # Título
        title = QLabel("Atajos de Teclado Disponibles")
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Lista de comandos
        commands_list = QListWidget()
        commands_list.setObjectName("commandsList")
        
        commands = [
            ("Ctrl + =", "Acercar (Zoom In)"),
            ("Ctrl + -", "Alejar (Zoom Out)"),
            ("Ctrl + 0", "Zoom 100%"),
            ("Ctrl + →", "Siguiente página"),
            ("Ctrl + ←", "Página anterior"),
            ("Home", "Primera página"),
            ("End", "Última página"),
            ("Ctrl + /", "Mostrar comandos"),
            ("F1", "Mostrar comandos"),
            ("Escape", "Cerrar este diálogo"),
        ]
        
        for shortcut, description in commands:
            item = QListWidgetItem(f"{shortcut:<15} → {description}")
            item.setData(1, shortcut)  # Guardar shortcut para referencia
            commands_list.addItem(item)
        
        layout.addWidget(commands_list)
        
        # Cerrar botón
        close_btn = QPushButton("Cerrar")
        close_btn.clicked.connect(dialog.close)
        layout.addWidget(close_btn)
        
        # Estilo del diálogo
        colors = theme_manager.colors
        dialog.setStyleSheet(f"""
            QDialog {{
                background-color: {colors['bg_primary']};
            }}
            QLabel {{
                color: {colors['fg_primary']};
            }}
            QListWidget {{
                background-color: {colors['bg_secondary']};
                color: {colors['fg_primary']};
                border: 1px solid {colors['border']};
                border-radius: 4px;
                padding: 5px;
            }}
            QListWidget::item {{
                padding: 8px;
                border-bottom: 1px solid {colors['border']};
            }}
            QListWidget::item:selected {{
                background-color: {colors['accent']};
                color: white;
            }}
            QPushButton {{
                background-color: {colors['accent']};
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                opacity: 0.9;
            }}
        """)
        
        dialog.exec()
    
    def _update_window_title(self):
        if hasattr(self, 'file_name_label'):
            title = self.file_name_label.text()
            if self._has_unsaved_changes and not title.startswith("*"):
                self.file_name_label.setText(f"*{title}")
            elif not self._has_unsaved_changes and title.startswith("*"):
                self.file_name_label.setText(title[1:])
    
    def _update_mode_buttons(self):
        """Actualiza la apariencia de los botones según el modo."""
        colors = theme_manager.colors
        if self._current_mode == self.MODE_READ:
            self.status_label.setText("Modo Lectura")
        else:
            self.status_label.setText("Modo Edición")
    
    def _apply_mode_style(self):
        """Aplica estilos según el modo actual."""
        self._update_mode_buttons()
    
    def _load_document(self):
        """Carga y renderiza el documento."""
        if self.document_type == "blank":
            # Mostrar mensaje de documento en blanco
            self.file_name_label.setText("Nuevo Documento en Blanco")
            self.info_label.setText("Cree un nuevo documento o abra un PDF existente")
            self.info_label.setVisible(True)
            self.pdf_view.setVisible(True)
            self._total_pages = 0
            self.page_info_label.setText("Sin páginas")
            self.status_label.setText("Listo para trabajar")
        elif self.document_type == "suggestion":
            self.file_name_label.setText("Documento de Sugerencia")
            self.info_label.setText("Documento de sugerencia")
            self.status_label.setText("Modo Lectura")
        elif self.document_type == "recent":
            self.file_name_label.setText("Documento Reciente")
            self.info_label.setText("Documento reciente")
            self.status_label.setText("Modo Lectura")
        
        # Por defecto siempre modo lectura
        self.set_mode_read()
    
    def eventFilter(self, obj, event):
        """Captura eventos de teclado para los atajos."""
        if event.type() == QEvent.Type.KeyPress:
            key = event.key()
            modifiers = event.modifiers()
            
            # Debug: print key press
            print(f"[EditorWindow eventFilter] Key: {key}, Modifiers: {modifiers}")
            
            # Ctrl + = o Ctrl + + (acercar)
            if modifiers == Qt.KeyboardModifier.ControlModifier and (key == Qt.Key.Key_Equal or key == Qt.Key.Key_Plus):
                self.zoom_in()
                self._set_temp_cursor(Qt.CursorShape.SizeVerCursor)
                return True
            
            # Ctrl + - (alejar)
            if modifiers == Qt.KeyboardModifier.ControlModifier and key == Qt.Key.Key_Minus:
                self.zoom_out()
                self._set_temp_cursor(Qt.CursorShape.SizeVerCursor)
                return True
            
            # Ctrl + Right (siguiente página)
            if modifiers == Qt.KeyboardModifier.ControlModifier and key == Qt.Key.Key_Right:
                self.next_page()
                self._set_temp_cursor(Qt.CursorShape.PointingHandCursor)
                return True
            
            # Ctrl + Left (página anterior)
            if modifiers == Qt.KeyboardModifier.ControlModifier and key == Qt.Key.Key_Left:
                self.previous_page()
                self._set_temp_cursor(Qt.CursorShape.PointingHandCursor)
                return True
            
            # Ctrl + 0 (zoom 100%)
            if modifiers == Qt.KeyboardModifier.ControlModifier and key == Qt.Key.Key_0:
                if hasattr(self, 'pdf_view') and self.pdf_view:
                    self.pdf_view.setZoomFactor(1.0)
                self.zoom_info_label.setText("Zoom: 100%")
                self._set_temp_cursor(Qt.CursorShape.SizeVerCursor)
                return True
            
            # Home (primera página)
            if key == Qt.Key.Key_Home:
                self._go_to_first_page()
                self._set_temp_cursor(Qt.CursorShape.PointingHandCursor)
                return True
            
            # End (última página)
            if key == Qt.Key.Key_End:
                self._go_to_last_page()
                self._set_temp_cursor(Qt.CursorShape.PointingHandCursor)
                return True
            
            # F1 o Ctrl + / (mostrar comandos)
            if key == Qt.Key.Key_F1 or (modifiers == Qt.KeyboardModifier.ControlModifier and key == Qt.Key.Key_Slash):
                self._show_commands_dialog()
                return True
        
        return super().eventFilter(obj, event)
    
    def load_pdf(self, file_path: str):
        """Carga un archivo PDF usando QPdfView."""
        try:
            self.current_file_path = file_path
            
            # Cargar el PDF en el documento
            self._pdf_document.load(file_path)
            
            # Verificar que se cargó correctamente
            if self._pdf_document.status() == QPdfDocument.Status.Ready:
                self._total_pages = self._pdf_document.pageCount()
                self._current_page = 0
                
                # Ocultar label de info, mostrar visor PDF
                self.info_label.setVisible(False)
                self.pdf_view.setVisible(True)
                
                # Actualizar información
                self.file_name_label.setText(Path(file_path).name)
                self.page_info_label.setText(f"Páginas: {self._total_pages}")
                self.status_label.setText(f"Modo Lectura - {self._total_pages} páginas")
                
                # Siempre abrir en modo lectura
                self.set_mode_read()
                
                self.file_opened.emit(file_path)
            else:
                self.status_label.setText(f"Error al cargar PDF: estado = {self._pdf_document.status()}")
            
        except Exception as e:
            self.status_label.setText(f"Error al cargar PDF: {str(e)}")
    
    def next_page(self):
        """Ir a la siguiente página usando QPdfView."""
        if self._pdf_document and self._current_page < self._total_pages - 1:
            self._current_page += 1
            nav = self.pdf_view.pageNavigator()
            from PyQt6.QtCore import QPointF
            current_zoom = self.pdf_view.zoomFactor()
            nav.jump(self._current_page, QPointF(), current_zoom)
            self.page_info_label.setText(f"Página: {self._current_page + 1} / {self._total_pages}")
            self._set_temp_cursor(Qt.CursorShape.PointingHandCursor)
    
    def previous_page(self):
        """Ir a la página anterior usando QPdfView."""
        if self._pdf_document and self._current_page > 0:
            self._current_page -= 1
            from PyQt6.QtCore import QPointF
            nav = self.pdf_view.pageNavigator()
            current_zoom = self.pdf_view.zoomFactor()
            nav.jump(self._current_page, QPointF(), current_zoom)
            self.page_info_label.setText(f"Página: {self._current_page + 1} / {self._total_pages}")
            self._set_temp_cursor(Qt.CursorShape.PointingHandCursor)
    
    def zoom_in(self):
        """Acercar usando QPdfView."""
        if hasattr(self, 'pdf_view') and self.pdf_view:
            current_zoom = self.pdf_view.zoomFactor()
            new_zoom = min(3.0, current_zoom + 0.25)
            self.pdf_view.setZoomFactor(new_zoom)
            # Forzar repintado
            self.pdf_view.update()
            self.pdf_view.repaint()
            self.zoom_info_label.setText(f"Zoom: {int(new_zoom * 100)}%")
            self._set_temp_cursor(Qt.CursorShape.SizeVerCursor)
    
    def zoom_out(self):
        """Alejar usando QPdfView."""
        if hasattr(self, 'pdf_view') and self.pdf_view:
            current_zoom = self.pdf_view.zoomFactor()
            new_zoom = max(0.25, current_zoom - 0.25)
            self.pdf_view.setZoomFactor(new_zoom)
            # Forzar repintado
            self.pdf_view.update()
            self.pdf_view.repaint()
            self.zoom_info_label.setText(f"Zoom: {int(new_zoom * 100)}%")
            self._set_temp_cursor(Qt.CursorShape.SizeVerCursor)
    
    def _on_zoom_reset_shortcut(self):
        """Restablecer zoom al 100%."""
        if hasattr(self, 'pdf_view') and self.pdf_view:
            self.pdf_view.setZoomFactor(1.0)
            # Forzar repintado
            self.pdf_view.update()
            self.pdf_view.repaint()
            self.zoom_info_label.setText("Zoom: 100%")
            self._set_temp_cursor(Qt.CursorShape.SizeVerCursor)
    
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
        
        btn_home = QPushButton("⌂")
        btn_home.setFixedSize(50, 50)
        btn_home.setToolTip("Inicio")
        btn_home.setStyleSheet("font-size: 22px;")
        btn_home.clicked.connect(self._go_home)
        
        btn_new = QPushButton("⊞")
        btn_new.setFixedSize(50, 50)
        btn_new.setToolTip("Nuevo")
        btn_new.setStyleSheet("font-size: 22px;")
        btn_new.clicked.connect(self._new_document)
        
        btn_open = QPushButton("📂")
        btn_open.setFixedSize(50, 50)
        btn_open.setToolTip("Abrir")
        btn_open.setStyleSheet("font-size: 22px;")
        btn_open.clicked.connect(self._open_pdf)
        
        btn_save = QPushButton("💾")
        btn_save.setFixedSize(50, 50)
        btn_save.setToolTip("Guardar")
        btn_save.setStyleSheet("font-size: 22px;")
        btn_save.clicked.connect(self._save_pdf)
        
        # Botones de navegación de páginas
        layout.addStretch()
        
        self.btn_prev = QPushButton("⏮")
        self.btn_prev.setFixedSize(50, 40)
        self.btn_prev.setToolTip("Página anterior")
        self.btn_prev.setStyleSheet("font-size: 18px;")
        self.btn_prev.clicked.connect(self.previous_page)
        
        self.btn_next = QPushButton("⏭")
        self.btn_next.setFixedSize(50, 40)
        self.btn_next.setToolTip("Página siguiente")
        self.btn_next.setStyleSheet("font-size: 18px;")
        self.btn_next.clicked.connect(self.next_page)
        
        # Botón de modo lectura/edición
        self.btn_mode = QPushButton("☰")
        self.btn_mode.setFixedSize(50, 40)
        self.btn_mode.setToolTip("Cambiar modo (Lectura/Escritura)")
        self.btn_mode.setStyleSheet("font-size: 20px;")
        self.btn_mode.clicked.connect(self._toggle_mode)
        
        layout.addWidget(btn_home)
        layout.addWidget(btn_new)
        layout.addWidget(btn_open)
        layout.addWidget(btn_save)
        layout.addWidget(self.btn_mode)
        layout.addWidget(self.btn_prev)
        layout.addWidget(self.btn_next)
        
        layout.addStretch()
        
        return panel
    
    def _toggle_mode(self):
        """Alterna entre modo lectura y edición."""
        if self._current_mode == self.MODE_READ:
            self.set_mode_edit()
            self.btn_mode.setText("✎")
            self.btn_mode.setStyleSheet("font-size: 20px;")
            self.btn_mode.setToolTip("Modo Edición - Clic para cambiar a Lectura")
        else:
            self.set_mode_read()
            self.btn_mode.setText("☰")
            self.btn_mode.setStyleSheet("font-size: 20px;")
            self.btn_mode.setToolTip("Modo Lectura - Clic para cambiar a Edición")
    
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
            ("⊞", "Nuevo", self._new_document),
            ("📂", "Abrir", self._open_pdf),
            ("💾", "Guardar", self._save_pdf),
            ("⤓", "Exportar", self._export_pdf),
        ])
        ribbon_layout.addWidget(file_section)
        
        edit_section = self._create_ribbon_section("Editar", [
            ("✂", "Cortar", self._cut),
            ("⎘", "Copiar", self._copy),
            ("⎗", "Pegar", self._paste),
            ("↶", "Deshacer", self._undo),
            ("↷", "Rehacer", self._redo),
        ])
        ribbon_layout.addWidget(edit_section)
        
        view_section = self._create_ribbon_section("Ver", [
            ("⤧", "Acercar", self._zoom_in),
            ("⤦", "Alejar", self._zoom_out),
            ("▤", "Página", self._view_page),
            ("⊟", "Todas", self._view_all),
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
        
        # Visor de PDF profesional usando PDFViewerWidget personalizado
        self.pdf_view = PDFViewerWidget(panel)
        self.pdf_view.setObjectName("pdfView")
        
        # Configurar modo de zoom Custom con 100% inicial
        self.pdf_view.setZoomMode(QPdfView.ZoomMode.Custom)
        self.pdf_view.setZoomFactor(1.0)  # 100% zoom inicial
        self.pdf_view.setPageMode(QPdfView.PageMode.MultiPage)
        
        # Configurar márgenes y espaciado
        self.pdf_view.setDocumentMargins(QMargins(30, 30, 30, 30))  # Márgenes alrededor del documento
        self.pdf_view.setPageSpacing(15)  # Espaciado entre páginas en MultiPage
        
        # Conectar señales de atajos de teclado
        self.pdf_view.zoom_in_requested.connect(self.zoom_in)
        self.pdf_view.zoom_out_requested.connect(self.zoom_out)
        self.pdf_view.zoom_reset_requested.connect(self._on_zoom_reset_shortcut)
        self.pdf_view.next_page_requested.connect(self.next_page)
        self.pdf_view.previous_page_requested.connect(self.previous_page)
        self.pdf_view.first_page_requested.connect(self._go_to_first_page)
        self.pdf_view.last_page_requested.connect(self._go_to_last_page)
        self.pdf_view.help_requested.connect(self._show_commands_dialog)
        
        # Crear documento PDF
        self._pdf_document = QPdfDocument(self.pdf_view)
        self.pdf_view.setDocument(self._pdf_document)
        
        # Conectar señales de navegación
        self._pdf_document.statusChanged.connect(self._on_pdf_loaded)
        
        # Ocultar info label inicialmente
        self.info_label = QLabel("Seleccione un archivo PDF para comenzar a trabajar")
        self.info_label.setObjectName("editorInfo")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_label.setVisible(True)
        
        # El visor PDF está siempre visible pero vacío
        self.pdf_view.setVisible(True)
        
        layout.addWidget(self.pdf_view, 1)
        
        return panel
    
    def _on_pdf_loaded(self):
        """Se ejecuta cuando el PDF se carga correctamente."""
        if self._pdf_document.status() == QPdfDocument.Status.Ready:
            self._total_pages = self._pdf_document.pageCount()
            self.page_info_label.setText(f"Páginas: {self._total_pages}")
            self.status_label.setText(f"PDF cargado: {self._total_pages} páginas")
    
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
        
        btn_zoom_in = QPushButton("⤧")
        btn_zoom_in.setFixedSize(50, 40)
        btn_zoom_in.setToolTip("Acercar (Ctrl+=)")
        btn_zoom_in.setStyleSheet("font-size: 18px;")
        btn_zoom_in.clicked.connect(self.zoom_in)
        
        btn_zoom_out = QPushButton("⤦")
        btn_zoom_out.setFixedSize(50, 40)
        btn_zoom_out.setToolTip("Alejar (Ctrl+-)")
        btn_zoom_out.setStyleSheet("font-size: 18px;")
        btn_zoom_out.clicked.connect(self.zoom_out)
        
        btn_rotate = QPushButton("↻")
        btn_rotate.setFixedSize(50, 40)
        btn_rotate.setToolTip("Rotar")
        btn_rotate.setStyleSheet("font-size: 18px;")
        
        btn_tools = QPushButton("⚙")
        btn_tools.setFixedSize(50, 40)
        btn_tools.setToolTip("Herramientas")
        btn_tools.setStyleSheet("font-size: 18px;")
        
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
            self.load_pdf(file_path)
    
    def load_file(self, file_path: str):
        """Carga un archivo PDF desde una ruta."""
        self.document_type = "file"
        self.load_pdf(file_path)
    
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
            QScrollArea#pdfScrollArea {{
                background-color: {colors['bg_tertiary']};
                border: none;
            }}
            QLabel#pdfPageLabel {{
                background-color: white;
                border: 1px solid {colors['border']};
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
    
    def __init__(self, document_type: str = "blank", file_path: str = None, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.document_type = document_type
        self.file_path = file_path
        
        # Install event filter for keyboard shortcuts
        self.installEventFilter(self)
        
        # Set window icon
        icon_path = Path(__file__).parent.parent.parent / "assets" / "icons" / "icono.png"
        if not icon_path.exists():
            icon_path = Path.cwd() / "assets" / "icons" / "icono.png"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))
        
        self._setup_ui()
        
        theme_manager.theme_changed.connect(self._apply_theme)
        
        if self.editor:
            self.editor.close_requested.connect(self._on_editor_close_requested)
            if file_path:
                self.editor.load_file(file_path)
    
    def eventFilter(self, obj, event):
        """Captura eventos de teclado para los atajos."""
        if event.type() == QEvent.Type.KeyPress:
            key = event.key()
            modifiers = event.modifiers()
            
            # Ctrl + = o Ctrl + + (acercar)
            if modifiers == Qt.KeyboardModifier.ControlModifier and (key == Qt.Key.Key_Equal or key == Qt.Key.Key_Plus):
                self._on_zoom_in()
                return True
            
            # Ctrl + - (alejar)
            if modifiers == Qt.KeyboardModifier.ControlModifier and key == Qt.Key.Key_Minus:
                self._on_zoom_out()
                return True
            
            # Ctrl + Right (siguiente página)
            if modifiers == Qt.KeyboardModifier.ControlModifier and key == Qt.Key.Key_Right:
                self._on_next_page()
                return True
            
            # Ctrl + Left (página anterior)
            if modifiers == Qt.KeyboardModifier.ControlModifier and key == Qt.Key.Key_Left:
                self._on_previous_page()
                return True
            
            # Ctrl + 0 (zoom 100%)
            if modifiers == Qt.KeyboardModifier.ControlModifier and key == Qt.Key.Key_0:
                self._on_zoom_reset()
                return True
            
            # Home (primera página)
            if key == Qt.Key.Key_Home:
                self._on_first_page()
                return True
            
            # End (última página)
            if key == Qt.Key.Key_End:
                self._on_last_page()
                return True
            
            # F1 o Ctrl + / (mostrar comandos)
            if key == Qt.Key.Key_F1 or (modifiers == Qt.KeyboardModifier.ControlModifier and key == Qt.Key.Key_Slash):
                self._on_show_commands()
                return True
        
        return super().eventFilter(obj, event)
    
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
        
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.editor.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        
        self._setup_keyboard_shortcuts()
        
        self._center_window()
    
    def _setup_keyboard_shortcuts(self):
        """Configura los atajos de teclado."""
        # Install event filter on application to capture all keyboard events
        from PyQt6.QtWidgets import QApplication
        app = QApplication.instance()
        if app:
            app.installEventFilter(self)
        
        # Ctrl + = (acercar)
        shortcut_zoom_in = QShortcut(QKeySequence("Ctrl+="), self)
        shortcut_zoom_in.activated.connect(self._on_zoom_in)
        
        # Ctrl + + (acercar alterno)
        shortcut_zoom_in_alt = QShortcut(QKeySequence("Ctrl++"), self)
        shortcut_zoom_in_alt.activated.connect(self._on_zoom_in)
        
        # Ctrl + - (alejar)
        shortcut_zoom_out = QShortcut(QKeySequence("Ctrl+-"), self)
        shortcut_zoom_out.activated.connect(self._on_zoom_out)
        
        # Ctrl + Right (siguiente página)
        shortcut_next = QShortcut(QKeySequence("Ctrl+Right"), self)
        shortcut_next.activated.connect(self._on_next_page)
        
        # Ctrl + Left (página anterior)
        shortcut_prev = QShortcut(QKeySequence("Ctrl+Left"), self)
        shortcut_prev.activated.connect(self._on_previous_page)
        
        # Ctrl + 0 (zoom 100%)
        shortcut_zoom_reset = QShortcut(QKeySequence("Ctrl+0"), self)
        shortcut_zoom_reset.activated.connect(self._on_zoom_reset)
        
        # Home (primera página)
        shortcut_home = QShortcut(QKeySequence("Home"), self)
        shortcut_home.activated.connect(self._on_first_page)
        
        # End (última página)
        shortcut_end = QShortcut(QKeySequence("End"), self)
        shortcut_end.activated.connect(self._on_last_page)
        
        # F1 o Ctrl + / (mostrar comandos)
        shortcut_help = QShortcut(QKeySequence("F1"), self)
        shortcut_help.activated.connect(self._on_show_commands)
        
        shortcut_help2 = QShortcut(QKeySequence("Ctrl+/"), self)
        shortcut_help2.activated.connect(self._on_show_commands)
    
    def _on_zoom_in(self):
        """Maneja el atajo de zoom in."""
        if self.editor:
            self.editor.zoom_in()
            self.editor._set_temp_cursor(Qt.CursorShape.SizeVerCursor)
    
    def _on_zoom_out(self):
        """Maneja el atajo de zoom out."""
        if self.editor:
            self.editor.zoom_out()
            self.editor._set_temp_cursor(Qt.CursorShape.SizeVerCursor)
    
    def _on_zoom_reset(self):
        """Maneja el atajo de zoom reset."""
        if self.editor and hasattr(self.editor, 'pdf_view'):
            self.editor.pdf_view.setZoomFactor(1.0)
            self.editor.zoom_info_label.setText("Zoom: 100%")
            self.editor._set_temp_cursor(Qt.CursorShape.SizeVerCursor)
    
    def _on_next_page(self):
        """Maneja el atajo de siguiente página."""
        if self.editor:
            self.editor.next_page()
            self.editor._set_temp_cursor(Qt.CursorShape.PointingHandCursor)
    
    def _on_previous_page(self):
        """Maneja el atajo de página anterior."""
        if self.editor:
            self.editor.previous_page()
            self.editor._set_temp_cursor(Qt.CursorShape.PointingHandCursor)
    
    def _on_first_page(self):
        """Maneja el atajo de primera página."""
        if self.editor:
            self.editor._go_to_first_page()
            self.editor._set_temp_cursor(Qt.CursorShape.PointingHandCursor)
    
    def _on_last_page(self):
        """Maneja el atajo de última página."""
        if self.editor:
            self.editor._go_to_last_page()
            self.editor._set_temp_cursor(Qt.CursorShape.PointingHandCursor)
    
    def _on_show_commands(self):
        """Maneja el atajo de mostrar comandos."""
        if self.editor:
            self.editor._show_commands_dialog()
    
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
        self.setStyleSheet("""
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
