import tkinter as tk
from tkinter import ttk
from pathlib import Path
from datetime import datetime
from typing import Callable, Optional, List, Dict
import json
from .theme_manager import theme_manager


class DocumentCard:
    def __init__(
        self,
        parent: tk.Widget,
        file_path: str,
        file_name: str,
        modified_date: datetime,
        on_click: Optional[Callable] = None,
        on_delete: Optional[Callable] = None,
        **kwargs
    ):
        self.parent = parent
        self.file_path = file_path
        self.file_name = file_name
        self.modified_date = modified_date
        self.on_click = on_click
        self.on_delete = on_delete
        self._frame = None
        self._create_widget(**kwargs)
        
    def _create_widget(self, **kwargs):
        colors = theme_manager.colors
        font = theme_manager.get_font
        font_bold = theme_manager.get_font
        
        self._frame = tk.Frame(
            self.parent,
            bg=colors.get("bg_secondary", "#16181F"),
            relief="flat",
            cursor="hand2",
            **kwargs
        )
        self._frame.pack(fill="x", pady=4, padx=8)
        
        self._icon_label = tk.Label(
            self._frame,
            text="📄",
            font=("Segoe UI", 20),
            bg=colors.get("bg_secondary", "#16181F"),
            fg=colors.get("fg_primary", "#B2C2CD"),
            width=3
        )
        self._icon_label.pack(side="left", padx=(12, 8), pady=12)
        
        info_frame = tk.Frame(
            self._frame,
            bg=colors.get("bg_secondary", "#16181F")
        )
        info_frame.pack(side="left", fill="x", expand=True, pady=12)
        
        self._name_label = tk.Label(
            info_frame,
            text=self.file_name,
            font=("Segoe UI", 11, "bold"),
            bg=colors.get("bg_secondary", "#16181F"),
            fg=colors.get("fg_primary", "#B2C2CD"),
            anchor="w"
        )
        self._name_label.pack(fill="x")
        
        date_str = self._format_date(self.modified_date)
        self._date_label = tk.Label(
            info_frame,
            text=date_str,
            font=("Segoe UI", 9),
            bg=colors.get("bg_secondary", "#16181F"),
            fg=colors.get("fg_secondary", "#8E9BAB"),
            anchor="w"
        )
        self._date_label.pack(fill="x", pady=(2, 0))
        
        self._auto_label = tk.Label(
            self._frame,
            text="⏱️",
            font=("Segoe UI", 12),
            bg=colors.get("bg_secondary", "#16181F"),
            fg=colors.get("accent", "#528BFF"),
            width=3
        )
        self._auto_label.pack(side="right", padx=12)
        
        self._bind_events()
        
    def _bind_events(self):
        self._frame.bind("<Button-1>", self._on_click)
        self._frame.bind("<Enter>", self._on_enter)
        self._frame.bind("<Leave>", self._on_leave)
        for widget in [self._frame, self._icon_label, self._name_label, self._date_label]:
            widget.bind("<Button-1>", self._on_click)
            widget.bind("<Enter>", self._on_enter)
            widget.bind("<Leave>", self._on_leave)
            
    def _on_click(self, event):
        if self.on_click:
            self.on_click(self.file_path, self.file_name)
            
    def _on_enter(self, event):
        colors = theme_manager.colors
        self._frame.configure(bg=colors.get("bg_tertiary", "#2D333B"))
        self._icon_label.configure(bg=colors.get("bg_tertiary", "#2D333B"))
        self._name_label.configure(bg=colors.get("bg_tertiary", "#2D333B"))
        self._date_label.configure(bg=colors.get("bg_tertiary", "#2D333B"))
        self._auto_label.configure(bg=colors.get("bg_tertiary", "#2D333B"))
        
    def _on_leave(self, event):
        colors = theme_manager.colors
        self._frame.configure(bg=colors.get("bg_secondary", "#16181F"))
        self._icon_label.configure(bg=colors.get("bg_secondary", "#16181F"))
        self._name_label.configure(bg=colors.get("bg_secondary", "#16181F"))
        self._date_label.configure(bg=colors.get("bg_secondary", "#16181F"))
        self._auto_label.configure(bg=colors.get("bg_secondary", "#16181F"))
        
    def _format_date(self, date: datetime) -> str:
        now = datetime.now()
        diff = now - date
        
        if diff.days == 0:
            return f"Hoy {date.strftime('%I:%M %p')}"
        elif diff.days == 1:
            return f"Ayer {date.strftime('%I:%M %p')}"
        elif diff.days < 7:
            return f"{date.strftime('%A %I:%M %p')}"
        else:
            return date.strftime('%d %b %Y')
            
    def update_theme(self):
        colors = theme_manager.colors
        self._frame.configure(bg=colors.get("bg_secondary", "#16181F"))
        
    def destroy(self):
        if self._frame:
            self._frame.destroy()


class RecentDocumentsManager:
    RECENT_FILE = Path.home() / ".xebec_pdf" / "recent.json"
    
    @classmethod
    def get_recent_documents(cls, limit: int = 10) -> List[Dict]:
        if not cls.RECENT_FILE.exists():
            return []
            
        try:
            with open(cls.RECENT_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('documents', [])[:limit]
        except Exception:
            return []
    
    @classmethod
    def add_document(cls, file_path: str, file_name: str):
        cls.RECENT_FILE.parent.mkdir(parents=True, exist_ok=True)
        
        documents = cls.get_recent_documents(limit=20)
        
        documents = [d for d in documents if d.get('path') != file_path]
        
        documents.insert(0, {
            'path': file_path,
            'name': file_name,
            'modified': datetime.now().isoformat()
        })
        
        with open(cls.RECENT_FILE, 'w', encoding='utf-8') as f:
            json.dump({'documents': documents[:20]}, f, indent=2)
    
    @classmethod
    def remove_document(cls, file_path: str):
        documents = cls.get_recent_documents(limit=20)
        documents = [d for d in documents if d.get('path') != file_path]
        
        cls.RECENT_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(cls.RECENT_FILE, 'w', encoding='utf-8') as f:
            json.dump({'documents': documents}, f, indent=2)
