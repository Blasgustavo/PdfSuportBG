import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional, List, Dict
from datetime import datetime
from .theme_manager import theme_manager
from .document_card import RecentDocumentsManager


class RecentDocumentsTable:
    def __init__(
        self,
        parent: tk.Widget,
        on_document_select: Optional[Callable[[str, str], None]] = None,
        **kwargs
    ):
        self.parent = parent
        self.on_document_select = on_document_select
        self._frame = None
        self._tree = None
        self._documents: List[Dict] = []
        self._create_widget(**kwargs)
        
    def _create_widget(self, **kwargs):
        colors = theme_manager.colors
        
        self._frame = tk.Frame(
            self.parent,
            bg=colors.get("bg_primary", "#282A31"),
            **kwargs
        )
        
        title = tk.Label(
            self._frame,
            text="Documentos Recientes",
            font=("Segoe UI Semibold", 14),
            bg=colors.get("bg_primary", "#282A31"),
            fg=colors.get("fg_primary", "#B2C2CD"),
            anchor="w"
        )
        title.pack(fill="x", padx=30, pady=(20, 5))
        
        table_frame = tk.Frame(
            self._frame,
            bg=colors.get("border", "#3E4451"),
            padx=1,
            pady=1
        )
        table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        style = ttk.Style()
        style.theme_use("clam")
        
        style.configure(
            "Treeview",
            background=colors.get("bg_primary", "#282A31"),
            foreground=colors.get("fg_primary", "#B2C2CD"),
            fieldbackground=colors.get("bg_primary", "#282A31"),
            borderwidth=0,
            rowheight=36
        )
        
        style.configure(
            "Treeview.Heading",
            background=colors.get("bg_tertiary", "#2D333B"),
            foreground=colors.get("fg_secondary", "#8E9BAB"),
            borderwidth=0,
            font=("Segoe UI", 10, "semibold")
        )
        
        style.map(
            "Treeview",
            background=[("selected", colors.get("accent", "#528BFF"))],
            foreground=[("selected", "white")]
        )
        
        self._tree = ttk.Treeview(
            table_frame,
            columns=("name", "date"),
            show="headings",
            style="Treeview",
            selectmode="browse"
        )
        
        self._tree.heading("name", text="Nombre", anchor="w")
        self._tree.heading("date", text="Fecha de modificación", anchor="w")
        
        self._tree.column("name", width=400, minwidth=200)
        self._tree.column("date", width=200, minwidth=120)
        
        self._tree.pack(fill="both", expand=True)
        
        self._tree.bind("<ButtonRelease-1>", self._on_select)
        
        self.load_documents()
        
    def load_documents(self):
        for item in self._tree.get_children():
            self._tree.delete(item)
            
        recent_docs = RecentDocumentsManager.get_recent_documents(limit=20)
        
        for doc in recent_docs:
            name = doc.get('name', 'Documento')
            path = doc.get('path', '')
            modified = doc.get('modified', '')
            
            date_str = self._format_date(modified)
            
            self._tree.insert("", "end", values=(name, date_str), tags=(path,))
            
    def _format_date(self, date_str: str) -> str:
        try:
            date = datetime.fromisoformat(date_str)
            now = datetime.now()
            diff = now - date
            
            if diff.days == 0:
                return f"Hoy {date.strftime('%H:%M')}"
            elif diff.days == 1:
                return f"Ayer {date.strftime('%H:%M')}"
            elif diff.days < 7:
                return date.strftime('%a %H:%M')
            else:
                return date.strftime('%d %b %Y')
        except Exception:
            return date_str
            
    def _on_select(self, event):
        selection = self._tree.selection()
        if selection:
            item = selection[0]
            values = self._tree.item(item, "values")
            if values:
                name = values[0]
                path = self._tree.item(item, "tags")[0]
                if self.on_document_select and path:
                    self.on_document_select(path, name)
                    
    def update_theme(self):
        colors = theme_manager.colors
        self._frame.configure(bg=colors.get("bg_primary", "#282A31"))
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            background=colors.get("bg_primary", "#282A31"),
            foreground=colors.get("fg_primary", "#B2C2CD"),
            fieldbackground=colors.get("bg_primary", "#282A31")
        )
        
    def get_widget(self):
        return self._frame
