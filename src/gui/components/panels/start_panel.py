from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QScrollArea, QPushButton
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap
from typing import Optional
from pathlib import Path
import fitz

from src.gui.themes.theme_manager import theme_manager
from src.gui.components.panels.document_card import RecentDocumentsWidget
from src.utils.recent_files import SystemRecentFiles


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


class StartPanel(QWidget):
    """Panel de inicio con documentos recomendados y recientes."""
    
    document_selected = pyqtSignal(str)
    template_selected = pyqtSignal(str)
    
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
                doc_widget = self._create_template_card(name, pdf_file)
                scroll_layout.addWidget(doc_widget)
        else:
            doc_widget = self._create_template_card("Documento en blanco", None)
            scroll_layout.addWidget(doc_widget)
        
        scroll_layout.addStretch()
        
        scroll_area.setWidget(scroll_content)
        recommended_layout.addWidget(scroll_area)
        
        layout.addWidget(recommended_container)
        
        recent_label = QLabel("Documentos Recientes")
        recent_label.setObjectName("sectionTitle")
        layout.addWidget(recent_label)
        
        self.recent_docs = RecentDocumentsWidget()
        self.recent_docs.document_selected.connect(self._on_recent_doc_selected)
        layout.addWidget(self.recent_docs, 1)
        
        self._load_recent_documents()

    def _load_recent_documents(self):
        recent_docs = SystemRecentFiles.get_pdfs(limit=20)
        for doc in recent_docs:
            name = doc.get('name', 'Documento')
            path = doc.get('path', '')
            modified = doc.get('modified', '')
            self.recent_docs.add_document(path, name, modified)

    def _on_recent_doc_selected(self, file_path: str, file_name: str):
        if file_path:
            self.document_selected.emit(file_path)

    def _create_template_card(self, name: str, pdf_path: Optional[Path]) -> QWidget:
        doc_widget = QWidget()
        doc_widget.setObjectName("docCard")
        doc_widget.setFixedSize(160, 200)
        
        layout = QVBoxLayout(doc_widget)
        layout.setContentsMargins(5, 5, 5, 2)
        layout.setSpacing(2)
        
        preview_icon = QLabel()
        preview_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        preview_icon.setObjectName("previewIcon")
        
        if pdf_path and pdf_path.exists():
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
        
        doc_widget.mousePressEvent = lambda event: self._on_template_click(name, pdf_path)
        doc_widget.setCursor(Qt.CursorShape.PointingHandCursor)
        
        return doc_widget

    def _on_template_click(self, name: str, pdf_path: Optional[Path]):
        if pdf_path and pdf_path.exists():
            self.document_selected.emit(str(pdf_path))
        else:
            self.template_selected.emit(name)

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
                background-color: {colors['bg_primary']};
            }}
            QLabel#sectionTitle {{
                color: {colors['fg_secondary']};
                font-size: 16px;
                font-weight: bold;
                margin-top: 10px;
            }}
            QFrame#recentDocs {{
                background-color: {colors['bg_secondary']};
                border-radius: 12px;
            }}
            QWidget#docCard {{
                background-color: {colors['bg_secondary']};
                border: 1px solid {colors['border']};
                border-radius: 12px;
            }}
            QWidget#docCard:hover {{
                border-color: {colors['accent']};
                background-color: {colors['bg_current_line']};
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
