import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
from datetime import datetime
from typing import Callable, Optional
from .theme_manager import theme_manager
from .sidebar import SidebarPanel
from .header_templates import WelcomeHeader, TemplatesSection
from .recent_table import RecentDocumentsTable
from .document_card import RecentDocumentsManager
from .window_controls import WindowControls


class StartPanel:
    def __init__(
        self,
        parent: tk.Widget,
        on_document_select: Callable[[str, str], None] = None,
        on_navigate: Callable[[str], None] = None,
        **kwargs
    ):
        self.parent = parent
        self.on_document_select = on_document_select
        self.on_navigate = on_navigate
        self._frame = None
        self._sidebar = None
        self._create_widget(**kwargs)
        
    def _create_widget(self, **kwargs):
        colors = theme_manager.colors
        
        self._frame = tk.Frame(
            self.parent,
            bg=colors.get("bg_primary", "#282A31"),
            **kwargs
        )
        
        self._sidebar = SidebarPanel(
            self._frame,
            on_navigate=self._on_sidebar_navigate,
            width=220
        )
        
        content_frame = tk.Frame(
            self._frame,
            bg=colors.get("bg_primary", "#282A31")
        )
        content_frame.pack(side="left", fill="both", expand=True)
        
        self._welcome_header = WelcomeHeader(content_frame)
        self._welcome_header.get_widget().pack(fill="x")
        
        self._templates_section = TemplatesSection(
            content_frame,
            on_template_select=self._on_template_select
        )
        self._templates_section.get_widget().pack(fill="x")
        
        self._recent_table = RecentDocumentsTable(
            content_frame,
            on_document_select=self._on_document_select
        )
        self._recent_table.get_widget().pack(fill="both", expand=True)
        
    def _on_sidebar_navigate(self, nav_id: str):
        if self.on_navigate:
            self.on_navigate(nav_id)
            
    def _on_document_select(self, file_path: str, file_name: str):
        if self.on_document_select:
            self.on_document_select(file_path, file_name)
            
    def _on_template_select(self, template_name: str):
        messagebox.showinfo("Plantilla", f"Creando: {template_name}")
        
    def refresh_documents(self):
        if hasattr(self, '_recent_table'):
            self._recent_table.load_documents()
            
    def update_theme(self):
        colors = theme_manager.colors
        self._frame.configure(bg=colors.get("bg_primary", "#282A31"))
        if self._sidebar:
            self._sidebar.update_theme()
        if hasattr(self, '_welcome_header'):
            self._welcome_header.update_theme()
        if hasattr(self, '_templates_section'):
            self._templates_section.update_theme()
        if hasattr(self, '_recent_table'):
            self._recent_table.update_theme()
            
    def get_widget(self):
        return self._frame
