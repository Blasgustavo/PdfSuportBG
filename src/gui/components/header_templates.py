import tkinter as tk
from typing import Callable, Optional, List, Dict
from .theme_manager import theme_manager
from datetime import datetime


class WelcomeHeader:
    def __init__(self, parent: tk.Widget, **kwargs):
        self.parent = parent
        self._frame = None
        self._label = None
        self._create_widget(**kwargs)
        
    def _create_widget(self, **kwargs):
        colors = theme_manager.colors
        
        self._frame = tk.Frame(
            self.parent,
            bg=colors.get("bg_primary", "#282A31"),
            **kwargs
        )
        
        greeting = self._get_greeting()
        
        self._label = tk.Label(
            self._frame,
            text=greeting,
            font=("Segoe UI Light", 28),
            bg=colors.get("bg_primary", "#282A31"),
            fg=colors.get("fg_primary", "#B2C2CD"),
            anchor="w"
        )
        self._label.pack(fill="x", pady=(20, 10), padx=30)
        
    def _get_greeting(self) -> str:
        hour = datetime.now().hour
        if hour < 12:
            return "Buenos días"
        elif hour < 18:
            return "Buenas tardes"
        else:
            return "Buenas noches"
            
    def update_theme(self):
        colors = theme_manager.colors
        self._frame.configure(bg=colors.get("bg_primary", "#282A31"))
        self._label.configure(
            bg=colors.get("bg_primary", "#282A31"),
            fg=colors.get("fg_primary", "#B2C2CD")
        )
        
    def get_widget(self):
        return self._frame


class TemplateCard:
    def __init__(
        self,
        parent: tk.Widget,
        title: str,
        icon: str = "📄",
        on_click: Optional[Callable] = None,
        **kwargs
    ):
        self.parent = parent
        self.title = title
        self.icon = icon
        self.on_click = on_click
        self._frame = None
        self._create_widget(**kwargs)
        
    def _create_widget(self, **kwargs):
        colors = theme_manager.colors
        
        self._frame = tk.Frame(
            self.parent,
            bg=colors.get("bg_tertiary", "#2D333B"),
            width=160,
            height=200,
            relief="flat",
            cursor="hand2",
            **kwargs
        )
        self._frame.pack(side="left", padx=8, pady=10)
        self._frame.pack_propagate(False)
        
        icon_label = tk.Label(
            self._frame,
            text=self.icon,
            font=("Segoe UI", 36),
            bg=colors.get("bg_tertiary", "#2D333B"),
            fg=colors.get("fg_secondary", "#8E9BAB")
        )
        icon_label.pack(pady=(30, 10))
        
        title_label = tk.Label(
            self._frame,
            text=self.title,
            font=("Segoe UI", 10),
            bg=colors.get("bg_tertiary", "#2D333B"),
            fg=colors.get("fg_primary", "#B2C2CD"),
            wraplength=140,
            justify="center"
        )
        title_label.pack(pady=10)
        
        self._frame.bind("<Button-1>", self._on_click)
        self._frame.bind("<Enter>", self._on_enter)
        self._frame.bind("<Leave>", self._on_leave)
        for widget in [icon_label, title_label]:
            widget.bind("<Button-1>", self._on_click)
            widget.bind("<Enter>", self._on_enter)
            widget.bind("<Leave>", self._on_leave)
            
    def _on_click(self, event):
        if self.on_click:
            self.on_click(self.title)
            
    def _on_enter(self, event):
        colors = theme_manager.colors
        hover_bg = colors.get("border", "#3E4451")
        self._frame.configure(bg=hover_bg)
        
    def _on_leave(self, event):
        colors = theme_manager.colors
        self._frame.configure(bg=colors.get("bg_tertiary", "#2D333B"))
            
    def update_theme(self):
        colors = theme_manager.colors
        self._frame.configure(bg=colors.get("bg_tertiary", "#2D333B"))


class TemplatesSection:
    def __init__(
        self,
        parent: tk.Widget,
        on_template_select: Optional[Callable[[str], None]] = None,
        **kwargs
    ):
        self.parent = parent
        self.on_template_select = on_template_select
        self._frame = None
        self._cards: List[TemplateCard] = []
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
            text="📐 Plantillas",
            font=("Segoe UI Semibold", 14),
            bg=colors.get("bg_primary", "#282A31"),
            fg=colors.get("fg_primary", "#B2C2CD"),
            anchor="w"
        )
        title.pack(fill="x", padx=30, pady=(20, 10))
        
        cards_frame = tk.Frame(
            self._frame,
            bg=colors.get("bg_primary", "#282A31")
        )
        cards_frame.pack(fill="x", padx=20)
        
        templates = [
            ("📄", "Documento en blanco"),
            ("📋", "Bienvenida"),
            ("📊", "Informe"),
            ("📝", "Notas"),
            ("✉️", "Carta"),
            ("📋", "Recibo"),
        ]
        
        for icon, title in templates:
            card = TemplateCard(
                cards_frame,
                title=title,
                icon=icon,
                on_click=lambda t=title: self._on_template_click(t)
            )
            self._cards.append(card)
            
    def _on_template_click(self, title: str):
        if self.on_template_select:
            self.on_template_select(title)
            
    def update_theme(self):
        colors = theme_manager.colors
        self._frame.configure(bg=colors.get("bg_primary", "#282A31"))
        for card in self._cards:
            card.update_theme()
            
    def get_widget(self):
        return self._frame
