from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QFileDialog
)
from PyQt6.QtCore import Qt, pyqtSignal
from typing import Optional
from pathlib import Path

from src.gui.themes.theme_manager import theme_manager
from src.core.pdf_repair import PDFRepairer


class RepairPanel(QWidget):
    """Panel para reparar archivos PDF."""
    
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
                border-radius: 16px;
            }}
            QFrame#dropArea:hover {{
                border-color: {colors['accent']};
                background-color: {colors['bg_secondary']};
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
        """)
