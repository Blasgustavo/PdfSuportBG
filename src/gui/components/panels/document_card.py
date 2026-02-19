from PyQt6.QtWidgets import QFrame, QVBoxLayout, QScrollArea, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from typing import Optional


class RecentDocumentsWidget(QFrame):
    """Widget de documentos recientes."""
    
    document_selected = pyqtSignal(str, str)
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setObjectName("recentDocs")
        self._setup_ui()
        
        from src.gui.themes.theme_manager import theme_manager
        theme_manager.theme_changed.connect(self._apply_style)
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_column_widths()
    
    def _update_column_widths(self):
        if self.table_widget:
            total_width = self.table_widget.viewport().width()
            if total_width > 0:
                self.table_widget.setColumnWidth(0, int(total_width * 2 / 3))
                self.table_widget.setColumnWidth(1, int(total_width * 1 / 3))
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        scroll_area = QScrollArea()
        scroll_area.setObjectName("recentScroll")
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        self.table_widget = QTableWidget()
        self.table_widget.setObjectName("recentTable")
        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(["Nombre", "Fecha de modificación"])
        
        header = self.table_widget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignLeft)
        
        self.table_widget.verticalHeader().setVisible(False)
        self.table_widget.setShowGrid(False)
        self.table_widget.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table_widget.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table_widget.cellDoubleClicked.connect(self._on_document_click)
        self.table_widget.currentItemChanged.connect(self._on_document_selected)
        
        scroll_area.setWidget(self.table_widget)
        layout.addWidget(scroll_area)
    
    def add_document(self, file_path: str, file_name: str, modified_date: str = ""):
        row = self.table_widget.rowCount()
        self.table_widget.insertRow(row)
        
        name_item = QTableWidgetItem(file_name)
        name_item.setData(Qt.ItemDataRole.UserRole, file_path)
        name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.table_widget.setItem(row, 0, name_item)
        
        date_item = QTableWidgetItem(modified_date)
        date_item.setFlags(date_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.table_widget.setItem(row, 1, date_item)
    
    def _on_document_click(self, row: int, column: int):
        name_item = self.table_widget.item(row, 0)
        if name_item:
            file_path = name_item.data(Qt.ItemDataRole.UserRole)
            file_name = name_item.text()
            if file_path:
                self._open_document(file_path, file_name)
    
    def _on_document_selected(self, current, previous):
        if current:
            row = current.row()
            name_item = self.table_widget.item(row, 0)
            if name_item:
                file_path = name_item.data(Qt.ItemDataRole.UserRole)
                file_name = name_item.text()
                if file_path:
                    self._open_document(file_path, file_name)
    
    def _open_document(self, file_path: str, file_name: str):
        self.document_selected.emit(file_path, file_name)
    
    def _apply_style(self):
        from src.gui.themes.theme_manager import theme_manager
        colors = theme_manager.colors
        self.setStyleSheet(f"""
            QFrame#recentDocs {{
                background-color: {colors['bg_tertiary']};
                border-radius: 12px;
            }}
            QScrollArea#recentScroll {{
                border: none;
                background-color: transparent;
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
                text-align: left;
            }}
            QScrollBar:vertical {{
                width: 10px;
                background: transparent;
                border: none;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                border: none;
                background: none;
            }}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background: none;
            }}
            QScrollBar::handle:vertical {{
                background: {colors['bg_current_line']};
                min-height: 40px;
                border-radius: 5px;
                margin: 2px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: {colors['accent']};
            }}
            QScrollBar::handle:vertical:pressed {{
                background: {colors['accent_hover']};
            }}
        """)
