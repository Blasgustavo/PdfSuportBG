import tkinter as tk
from tkinter import ttk
from pathlib import Path
from datetime import datetime
from typing import Callable, Optional, List, Dict
from .theme_manager import theme_manager
from .document_card import DocumentCard, RecentDocumentsManager


class RecentPanel:
    def __init__(
        self,
        parent: tk.Widget,
        on_document_select: Callable[[str, str], None] = None,
        on_new_document: Callable = None,
        on_search: Callable[[str], None] = None,
        **kwargs
    ):
        self.parent = parent
        self.on_document_select = on_document_select
        self.on_new_document = on_new_document
        self.on_search = on_search
        self._frame = None
        self._document_cards: List[DocumentCard] = []
        self._create_widget(**kwargs)
        
    def _create_widget(self, **kwargs):
        colors = theme_manager.colors
        
        self._frame = tk.Frame(
            self.parent,
            bg=colors.get("bg_primary", "#282A31"),
            **kwargs
        )
        
        self._create_header()
        self._create_search_bar()
        self._create_documents_list()
        self._create_action_buttons()
        
    def _create_header(self):
        colors = theme_manager.colors
        
        header = tk.Frame(
            self._frame,
            bg=colors.get("bg_primary", "#282A31")
        )
        header.pack(fill="x", padx=20, pady=(30, 20))
        
        self._title_label = tk.Label(
            header,
            text="📄 Trabajos Recientes",
            font=("Segoe UI", 18, "bold"),
            bg=colors.get("bg_primary", "#282A31"),
            fg=colors.get("fg_primary", "#B2C2CD")
        )
        self._title_label.pack(side="left")
        
    def _create_search_bar(self):
        colors = theme_manager.colors
        
        search_frame = tk.Frame(
            self._frame,
            bg=colors.get("bg_primary", "#282A31")
        )
        search_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        self._search_var = tk.StringVar()
        self._search_var.trace_add("write", self._on_search_change)
        
        self._search_entry = tk.Entry(
            search_frame,
            textvariable=self._search_var,
            font=("Segoe UI", 11),
            bg=colors.get("bg_tertiary", "#2D333B"),
            fg=colors.get("fg_primary", "#B2C2CD"),
            insertbackground=colors.get("fg_primary", "#B2C2CD"),
            relief="flat",
            width=40
        )
        self._search_entry.pack(side="left", fill="x", expand=True)
        self._search_entry.insert(0, "🔍 Buscar documentos...")
        self._search_entry.bind("<FocusIn>", self._on_search_focus)
        self._search_entry.bind("<FocusOut>", self._on_search_blur)
        
        self._search_icon = tk.Label(
            search_frame,
            text="🔍",
            font=("Segoe UI", 12),
            bg=colors.get("bg_primary", "#282A31"),
            fg=colors.get("fg_secondary", "#8E9BAB")
        )
        self._search_icon.pack(side="left", padx=(10, 0))
        
    def _create_documents_list(self):
        colors = theme_manager.colors
        
        list_frame = tk.Frame(
            self._frame,
            bg=colors.get("bg_primary", "#282A31")
        )
        list_frame.pack(fill="both", expand=True, padx=20)
        
        self._canvas = tk.Canvas(
            list_frame,
            bg=colors.get("bg_primary", "#282A31"),
            highlightthickness=0,
            relief="flat"
        )
        self._canvas.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(
            list_frame,
            orient="vertical",
            command=self._canvas.yview,
            style="Custom.Vertical.TScrollbar"
        )
        scrollbar.pack(side="right", fill="y")
        
        self._scrollable_frame = tk.Frame(
            self._canvas,
            bg=colors.get("bg_primary", "#282A31")
        )
        
        self._canvas.configure(yscrollcommand=scrollbar.set)
        self._canvas.create_window((0, 0), window=self._scrollable_frame, anchor="nw")
        self._scrollable_frame.bind("<Configure>", lambda e: self._canvas.configure(scrollregion=self._canvas.bbox("all")))
        
    def _create_action_buttons(self):
        colors = theme_manager.colors
        
        action_frame = tk.Frame(
            self._frame,
            bg=colors.get("bg_primary", "#282A31")
        )
        action_frame.pack(fill="x", padx=20, pady=20)
        
        new_btn = tk.Button(
            action_frame,
            text="➕ Nuevo Documento",
            font=("Segoe UI", 11),
            bg=colors.get("accent", "#528BFF"),
            fg="white",
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2",
            command=self._on_new_click
        )
        new_btn.pack(side="left")
        
    def _on_search_focus(self, event):
        if self._search_var.get() == "🔍 Buscar documentos...":
            self._search_entry.delete(0, tk.END)
            self._search_entry.configure(fg=theme_manager.colors.get("fg_primary", "#B2C2CD"))
            
    def _on_search_blur(self, event):
        if not self._search_var.get():
            self._search_entry.insert(0, "🔍 Buscar documentos...")
            self._search_entry.configure(fg=theme_manager.colors.get("fg_secondary", "#8E9BAB"))
            
    def _on_search_change(self, *args):
        search_term = self._search_var.get()
        if search_term and search_term != "🔍 Buscar documentos...":
            self.filter_documents(search_term)
        else:
            self.load_documents()
            
    def _on_new_click(self):
        if self.on_new_document:
            self.on_new_document()
            
    def load_documents(self):
        if not hasattr(self, '_scrollable_frame') or self._scrollable_frame is None:
            return
            
        for card in self._document_cards:
            card.destroy()
        self._document_cards.clear()
        
        recent_docs = RecentDocumentsManager.get_recent_documents(limit=10)
        
        if not recent_docs:
            self._show_empty_state()
            return
            
        for doc in recent_docs:
            try:
                modified = datetime.fromisoformat(doc.get('modified', datetime.now().isoformat()))
            except Exception:
                modified = datetime.now()
                
            card = DocumentCard(
                self._scrollable_frame,
                file_path=doc.get('path', ''),
                file_name=doc.get('name', 'Documento'),
                modified_date=modified,
                on_click=self._on_document_click
            )
            self._document_cards.append(card)
            
    def _show_empty_state(self):
        colors = theme_manager.colors
        
        empty_frame = tk.Frame(
            self._scrollable_frame,
            bg=colors.get("bg_primary", "#282A31")
        )
        empty_frame.pack(fill="both", expand=True, pady=50)
        
        empty_label = tk.Label(
            empty_frame,
            text="📂",
            font=("Segoe UI", 48),
            bg=colors.get("bg_primary", "#282A31"),
            fg=colors.get("fg_secondary", "#8E9BAB")
        )
        empty_label.pack()
        
        empty_text = tk.Label(
            empty_frame,
            text="No hay trabajos recientes",
            font=("Segoe UI", 14),
            bg=colors.get("bg_primary", "#282A31"),
            fg=colors.get("fg_secondary", "#8E9BAB")
        )
        empty_text.pack(pady=10)
        
        empty_subtext = tk.Label(
            empty_frame,
            text="Crea un nuevo documento o abre uno existente",
            font=("Segoe UI", 10),
            bg=colors.get("bg_primary", "#282A31"),
            fg=colors.get("fg_disabled", "#5C6370")
        )
        empty_subtext.pack()
        
    def _on_document_click(self, file_path: str, file_name: str):
        if self.on_document_select:
            self.on_document_select(file_path, file_name)
            
    def filter_documents(self, search_term: str):
        for card in self._document_cards:
            card.destroy()
        self._document_cards.clear()
        
        recent_docs = RecentDocumentsManager.get_recent_documents(limit=20)
        search_lower = search_term.lower()
        
        filtered = [d for d in recent_docs if search_lower in d.get('name', '').lower()]
        
        for doc in filtered:
            try:
                modified = datetime.fromisoformat(doc.get('modified', datetime.now().isoformat()))
            except Exception:
                modified = datetime.now()
                
            card = DocumentCard(
                self._scrollable_frame,
                file_path=doc.get('path', ''),
                file_name=doc.get('name', 'Documento'),
                modified_date=modified,
                on_click=self._on_document_click
            )
            self._document_cards.append(card)
            
    def update_theme(self):
        colors = theme_manager.colors
        self._frame.configure(bg=colors.get("bg_primary", "#282A31"))
        
    def get_widget(self):
        return self._frame
