from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QFrame, QListWidget, QListWidgetItem, QFileDialog, QLineEdit,
    QTextEdit, QTabWidget, QScrollArea, QScrollBar, QTableWidget, QTableWidgetItem
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import QBuffer, QIODevice
from typing import Optional
from pathlib import Path
import fitz

from src.gui.pyqt6.theme_manager import theme_manager
from src.core.pdf_repair import PDFRepairer
from src.gui.components.document_card import RecentDocumentsManager


import sys

def log(msg):
    pass


def generate_pdf_thumbnail(pdf_path: Path, width: int = 120, height: int = 100) -> Optional[QPixmap]:
    """Genera una miniatura de la primera página de un PDF usando PyMuPDF."""
    try:
        doc = fitz.open(str(pdf_path))
        page = doc[0]
        pix = page.get_pixmap(matrix=fitz.Matrix(width / page.rect.width, height / page.rect.height))
        doc.close()
        
        pixmap = QPixmap()
        pixmap.loadFromData(pix.tobytes("png"))
        return pixmap
    except Exception as e:
        print(f"Error generating thumbnail: {e}")
        return None


class SidebarButton(QPushButton):
    def __init__(self, text: str, icon: str = "", parent: Optional[QWidget] = None):
        super().__init__(text, parent)
        self.setFixedHeight(40)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        if icon:
            self.setText(f"  {icon}  {text}")
        
        self._apply_style()

    def _apply_style(self):
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
            }}
            QPushButton:pressed {{
                background-color: {colors['accent']};
                color: white;
            }}
        """)


class Sidebar(QFrame):
    navigation_requested = pyqtSignal(str)
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setFixedWidth(100)
        self.setObjectName("sidebar")
        self._setup_ui()
        
        theme_manager.theme_changed.connect(self._apply_style)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 15, 5, 15)
        layout.setSpacing(8)
        
        self.home_btn = self._create_nav_button("🏠", "Inicio")
        self.home_btn.clicked.connect(lambda: self.navigation_requested.emit("home"))
        
        self.new_btn = self._create_nav_button("📄", "Nuevo")
        self.new_btn.clicked.connect(lambda: self.navigation_requested.emit("new"))
        
        self.open_btn = self._create_nav_button("📂", "Abrir")
        self.open_btn.clicked.connect(self._open_file)
        
        layout.addWidget(self.home_btn)
        layout.addWidget(self.new_btn)
        layout.addWidget(self.open_btn)
        
        layout.addStretch()
        
        self.settings_btn = self._create_nav_button("⚙️", "Configuración")
        self.settings_btn.clicked.connect(lambda: self.navigation_requested.emit("settings"))
        
        self.account_btn = self._create_nav_button("👤", "Cuenta")
        
        layout.addWidget(self.settings_btn)
        layout.addWidget(self.account_btn)

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

    def _open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar archivo PDF",
            "",
            "PDF Files (*.pdf)"
        )
        if file_path:
            self.navigation_requested.emit("repair")

    def _apply_style(self):
        colors = theme_manager.colors
        self.setStyleSheet(f"""
            QFrame#sidebar {{
                background-color: {colors['bg_secondary']};
                border-right: 1px solid {colors['border']};
            }}
            QPushButton#navButton {{
                background-color: transparent;
                border: none;
                border-radius: 8px;
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


class RecentDocumentsWidget(QFrame):
    document_selected = pyqtSignal(str, str)
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setObjectName("recentDocs")
        self._setup_ui()
        
        theme_manager.theme_changed.connect(self._apply_style)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        self.table_widget = QTableWidget()
        self.table_widget.setObjectName("recentTable")
        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(["Nombre", "Fecha de modificación"])
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        self.table_widget.verticalHeader().setVisible(False)
        self.table_widget.setShowGrid(False)
        self.table_widget.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table_widget.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table_widget.cellDoubleClicked.connect(self._on_document_click)
        layout.addWidget(self.table_widget)

    def add_document(self, file_path: str, file_name: str, modified_date: str = ""):
        row = self.table_widget.rowCount()
        self.table_widget.insertRow(row)
        
        name_item = QTableWidgetItem(file_name)
        name_item.setData(Qt.ItemDataRole.UserRole, file_path)
        self.table_widget.setItem(row, 0, name_item)
        
        date_item = QTableWidgetItem(modified_date)
        self.table_widget.setItem(row, 1, date_item)

    def _on_document_click(self, row: int, column: int):
        name_item = self.table_widget.item(row, 0)
        if name_item:
            file_path = name_item.data(Qt.ItemDataRole.UserRole)
            file_name = name_item.text()
            if file_path:
                self.document_selected.emit(file_path, file_name)

    def _apply_style(self):
        colors = theme_manager.colors
        self.setStyleSheet(f"""
            QFrame#recentDocs {{
                background-color: {colors['bg_tertiary']};
                border-radius: 12px;
            }}
            QTableWidget#recentTable {{
                background-color: transparent;
                color: {colors['fg_primary']};
                border: none;
                outline: none;
            }}
            QTableWidget::item {{
                padding: 10px;
                background-color: transparent;
            }}
            QTableWidget::item:hover {{
                background-color: {colors['bg_current_line']};
            }}
            QTableWidget::item:selected {{
                background-color: {colors['accent']};
            }}
            QHeaderView::section {{
                background-color: {colors['bg_tertiary']};
                color: {colors['fg_secondary']};
                padding: 8px;
                border: none;
                font-weight: bold;
            }}
        """)


class StartPanel(QWidget):
    document_selected = pyqtSignal(str)
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._setup_ui()
        
        theme_manager.theme_changed.connect(self._apply_style)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(15)
        
        welcome = QLabel("Bienvenido a Xebec Pdf Fixer")
        welcome.setObjectName("welcomeTitle")
        welcome.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(welcome)
        
        layout.addSpacing(10)
        
        recommended_label = QLabel("Documentos Recomendados")
        recommended_label.setObjectName("sectionTitle")
        layout.addWidget(recommended_label)
        
        recommended_container = QFrame()
        recommended_container.setObjectName("recentDocs")
        
        recommended_layout = QVBoxLayout(recommended_container)
        recommended_layout.setContentsMargins(10, 10, 10, 10)
        recommended_layout.setSpacing(0)
        
        scroll_area = QScrollArea()
        scroll_area.setObjectName("recommendedScroll")
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        
        scroll_content = QWidget()
        scroll_layout = QHBoxLayout(scroll_content)
        scroll_layout.setSpacing(15)
        scroll_layout.setContentsMargins(5, 5, 5, 5)
        
        templates_path = Path.cwd() / "assets" / "templates"
        
        if templates_path.exists():
            pdf_files = sorted(templates_path.glob("*.pdf"))
            for pdf_file in pdf_files:
                name = pdf_file.stem
                doc_widget = self._create_document_card(name, pdf_file)
                scroll_layout.addWidget(doc_widget)
        
        scroll_layout.addStretch()
        
        scroll_area.setWidget(scroll_content)
        recommended_layout.addWidget(scroll_area)
        
        layout.addWidget(recommended_container)
        
        recent_label = QLabel("Documentos Recientes")
        recent_label.setObjectName("sectionTitle")
        layout.addWidget(recent_label)
        
        self.recent_docs = RecentDocumentsWidget()
        layout.addWidget(self.recent_docs, 1)
        
        self._load_recent_documents()

    def _load_recent_documents(self):
        recent_docs = RecentDocumentsManager.get_recent_documents(limit=10)
        for doc in recent_docs:
            name = doc.get('name', 'Documento')
            path = doc.get('path', '')
            modified = doc.get('modified', '')
            self.recent_docs.add_document(path, name, modified)

    def _create_document_card(self, name: str, pdf_path: Path) -> QWidget:
        doc_widget = QWidget()
        doc_widget.setObjectName("docCard")
        doc_widget.setFixedSize(160, 200)
        
        layout = QVBoxLayout(doc_widget)
        layout.setContentsMargins(5, 5, 5, 2)
        layout.setSpacing(2)
        
        preview_icon = QLabel()
        preview_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        preview_icon.setObjectName("previewIcon")
        
        if pdf_path.exists():
            pixmap = generate_pdf_thumbnail(pdf_path, 150, 170)
            if pixmap:
                scaled = pixmap.scaled(150, 170, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                preview_icon.setPixmap(scaled)
            else:
                preview_icon.setText("📄")
                preview_icon.setStyleSheet("font-size: 48px;")
        else:
            preview_icon.setText("📄")
            preview_icon.setStyleSheet("font-size: 48px;")
        
        layout.addWidget(preview_icon)
        
        name_label = QLabel(name)
        name_label.setObjectName("docName")
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_label.setWordWrap(True)
        name_label.setStyleSheet("background: transparent; font-size: 10px;")
        layout.addWidget(name_label)
        
        return doc_widget

    def _on_doc_click(self, name: str, is_blank: bool):
        self.document_selected.emit(name)

    def _create_action_button(self, text: str, icon: str) -> QPushButton:
        btn = QPushButton(f"{icon}\n{text}")
        btn.setFixedSize(120, 100)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        
        colors = theme_manager.colors
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {colors['bg_tertiary']};
                color: {colors['fg_primary']};
                border: 1px solid {colors['border']};
                border-radius: 8px;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: {colors['accent']};
                color: white;
                border-color: {colors['accent']};
            }}
        """)
        
        return btn

    def _apply_style(self):
        colors = theme_manager.colors
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {colors['bg_primary']};
            }}
            QLabel#welcomeTitle {{
                color: {colors['fg_primary']};
                font-size: 28px;
                font-weight: bold;
            }}
            QLabel#sectionTitle {{
                color: {colors['fg_primary']};
                font-size: 16px;
                font-weight: bold;
                margin-top: 10px;
            }}
            QFrame#recentDocs {{
                background-color: {colors['bg_tertiary']};
                border-radius: 12px;
            }}
            QWidget#docCard {{
                background-color: {colors['bg_secondary']};
                border: 1px solid {colors['border']};
                border-radius: 8px;
            }}
            QWidget#docCard:hover {{
                border-color: {colors['accent']};
            }}
            QLabel#previewIcon {{
                font-size: 48px;
            }}
            QLabel#docName {{
                color: {colors['fg_primary']};
                background: transparent;
                font-size: 12px;
            }}
            QScrollArea#recommendedScroll {{
                border: none;
                background: transparent;
            }}
            QScrollBar:horizontal {{
                height: 8px;
                background: {colors['bg_secondary']};
            }}
            QScrollBar::handle:horizontal {{
                background: {colors['accent']};
                min-width: 60px;
                border-radius: 4px;
            }}
            QScrollBar::handle:horizontal:hover {{
                background: {colors['accent_hover']};
            }}
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
                border: none;
                background: none;
                width: 0px;
            }}
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
                background: none;
            }}
            QScrollBar:vertical {{
                width: 8px;
                background: {colors['bg_secondary']};
            }}
            QScrollBar::handle:vertical {{
                background: {colors['accent']};
                min-height: 60px;
                border-radius: 4px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: {colors['accent_hover']};
            }}
        """)


class NewPanel(QWidget):
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
                border-radius: 12px;
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {colors['accent']};
                color: white;
                border-color: {colors['accent']};
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


class RepairPanel(QWidget):
    repair_completed = pyqtSignal(bool, str)
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.current_pdf_path = None
        self._setup_ui()
        
        theme_manager.theme_changed.connect(self._apply_style)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 30, 40, 30)
        
        title = QLabel("Reparar PDF")
        title.setObjectName("panelTitle")
        layout.addWidget(title)
        
        layout.addSpacing(20)
        
        drop_area = QFrame()
        drop_area.setObjectName("dropArea")
        drop_area.setFixedHeight(200)
        
        drop_layout = QVBoxLayout(drop_area)
        
        drop_icon = QLabel("📄")
        drop_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        drop_icon.setStyleSheet("font-size: 48px;")
        drop_layout.addWidget(drop_icon)
        
        drop_text = QLabel("Arrastra un archivo PDF aquí")
        drop_text.setObjectName("dropText")
        drop_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        drop_layout.addWidget(drop_text)
        
        drop_subtext = QLabel("o")
        drop_subtext.setAlignment(Qt.AlignmentFlag.AlignCenter)
        drop_layout.addWidget(drop_subtext)
        
        self.select_btn = QPushButton("Seleccionar archivo")
        self.select_btn.clicked.connect(self._select_pdf)
        drop_layout.addWidget(self.select_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(drop_area)
        
        self.selected_file_label = QLabel("")
        self.selected_file_label.setObjectName("selectedFile")
        layout.addWidget(self.selected_file_label)
        
        layout.addSpacing(10)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.repair_btn = QPushButton("Reparar PDF")
        self.repair_btn.setFixedSize(200, 45)
        self.repair_btn.setEnabled(False)
        self.repair_btn.clicked.connect(self._repair_pdf)
        button_layout.addWidget(self.repair_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        layout.addStretch()

    def _select_pdf(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar archivo PDF",
            "",
            "PDF Files (*.pdf)"
        )
        
        if file_path:
            self.current_pdf_path = Path(file_path)
            self.selected_file_label.setText(f"Archivo seleccionado: {self.current_pdf_path.name}")
            self.repair_btn.setEnabled(True)

    def _repair_pdf(self):
        if not self.current_pdf_path:
            return
        
        output_path = self.current_pdf_path.parent / f"fixed_{self.current_pdf_path.name}"
        
        self.status_label.setText("Reparando PDF...")
        self.repair_btn.setEnabled(False)
        
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(100, lambda: self._do_repair(output_path))

    def _do_repair(self, output_path: Path):
        success, error = PDFRepairer.repair(self.current_pdf_path, output_path)
        
        colors = theme_manager.colors
        if success:
            self.status_label.setText(f"PDF reparado exitosamente: {output_path.name}")
            self.status_label.setStyleSheet(f"color: {colors['success']};")
            self.repair_completed.emit(True, str(output_path))
        else:
            self.status_label.setText(f"Error al reparar: {error}")
            self.status_label.setStyleSheet(f"color: {colors['error']};")
            self.repair_completed.emit(False, error)
        
        self.repair_btn.setEnabled(True)

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
            QFrame#dropArea {{
                background-color: {colors['bg_tertiary']};
                border: 2px dashed {colors['border']};
                border-radius: 12px;
            }}
            QLabel#dropText {{
                color: {colors['fg_primary']};
                font-size: 16px;
                font-weight: bold;
            }}
            QLabel {{
                color: {colors['fg_secondary']};
            }}
            QLabel#selectedFile {{
                color: {colors['success']};
                font-size: 14px;
            }}
            QPushButton {{
                background-color: {colors['accent']};
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                padding: 8px 16px;
            }}
            QPushButton:hover {{
                background-color: {colors['accent_hover']};
            }}
            QPushButton:disabled {{
                background-color: {colors['bg_tertiary']};
                color: {colors['fg_disabled']};
            }}
        """)


class MergePanel(QWidget):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.pdf_files = []
        self._setup_ui()
        
        theme_manager.theme_changed.connect(self._apply_style)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 30, 40, 30)
        
        title = QLabel("Unir PDFs")
        title.setObjectName("panelTitle")
        layout.addWidget(title)
        
        layout.addSpacing(20)
        
        add_btn = QPushButton("Agregar archivos PDF")
        add_btn.clicked.connect(self._add_files)
        layout.addWidget(add_btn)
        
        self.file_list = QListWidget()
        layout.addWidget(self.file_list)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.merge_btn = QPushButton("Unir PDFs")
        self.merge_btn.setFixedSize(200, 45)
        self.merge_btn.setEnabled(False)
        button_layout.addWidget(self.merge_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)

    def _add_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Seleccionar archivos PDF",
            "",
            "PDF Files (*.pdf)"
        )
        
        for f in files:
            if f not in self.pdf_files:
                self.pdf_files.append(f)
                self.file_list.addItem(Path(f).name)
        
        self.merge_btn.setEnabled(len(self.pdf_files) > 1)

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
            QListWidget {{
                background-color: {colors['bg_tertiary']};
                color: {colors['fg_primary']};
                border: 1px solid {colors['border']};
                border-radius: 8px;
            }}
            QPushButton {{
                background-color: {colors['accent']};
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                padding: 8px 16px;
            }}
            QPushButton:hover {{
                background-color: {colors['accent_hover']};
            }}
            QPushButton:disabled {{
                background-color: {colors['bg_tertiary']};
                color: {colors['fg_disabled']};
            }}
        """)


class SplitPanel(QWidget):
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
                background-color: {colors['accent']};
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                padding: 8px 16px;
            }}
            QPushButton:hover {{
                background-color: {colors['accent_hover']};
            }}
            QPushButton:disabled {{
                background-color: {colors['bg_tertiary']};
                color: {colors['fg_disabled']};
            }}
        """)


class SettingsPanel(QWidget):
    theme_changed = pyqtSignal(str)
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._setup_ui()
        
        theme_manager.theme_changed.connect(self._apply_style)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 30, 40, 30)
        
        title = QLabel("Configuración")
        title.setObjectName("panelTitle")
        layout.addWidget(title)
        
        layout.addSpacing(30)
        
        theme_section = QLabel("Tema")
        theme_section.setObjectName("sectionTitle")
        layout.addWidget(theme_section)
        
        theme_layout = QHBoxLayout()
        
        self.dark_btn = QPushButton("Oscuro")
        self.dark_btn.setCheckable(True)
        self.dark_btn.setChecked(theme_manager.colors == theme_manager.theme)
        self.dark_btn.clicked.connect(lambda: self._set_theme("dark"))
        theme_layout.addWidget(self.dark_btn)
        
        self.light_btn = QPushButton("Claro")
        self.light_btn.setCheckable(True)
        self.light_btn.setChecked(False)
        self.light_btn.clicked.connect(lambda: self._set_theme("light"))
        theme_layout.addWidget(self.light_btn)
        
        theme_layout.addStretch()
        layout.addLayout(theme_layout)
        
        layout.addSpacing(30)
        
        about_section = QLabel("Acerca de")
        about_section.setObjectName("sectionTitle")
        layout.addWidget(about_section)
        
        about_text = QLabel(
            "Xebec Pdf Fixer v0.0.1\n\n"
            "Herramienta de administración de PDFs\n"
            "Desarrollado por BGNC - Corporación Xebec"
        )
        about_text.setObjectName("aboutText")
        layout.addWidget(about_text)
        
        layout.addStretch()

    def _set_theme(self, theme_name: str):
        theme_manager.set_theme(theme_name)
        self.dark_btn.setChecked(theme_name == "dark")
        self.light_btn.setChecked(theme_name == "light")

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
            QLabel#sectionTitle {{
                color: {colors['fg_primary']};
                font-size: 16px;
                font-weight: bold;
            }}
            QLabel#aboutText {{
                color: {colors['fg_secondary']};
                font-size: 13px;
                line-height: 1.6;
            }}
            QPushButton {{
                background-color: {colors['bg_tertiary']};
                color: {colors['fg_primary']};
                border: 1px solid {colors['border']};
                border-radius: 6px;
                font-size: 14px;
                padding: 8px 20px;
                min-width: 100px;
            }}
            QPushButton:hover {{
                background-color: {colors['accent']};
                color: white;
                border-color: {colors['accent']};
            }}
            QPushButton:checked {{
                background-color: {colors['accent']};
                color: white;
                border-color: {colors['accent']};
            }}
        """)


class NewDocumentPanel(QWidget):
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
