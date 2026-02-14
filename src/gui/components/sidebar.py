import tkinter as tk
from typing import Callable, Optional, List, Dict
from .theme_manager import theme_manager


class SidebarButton:
    def __init__(
        self,
        parent: tk.Widget,
        text: str,
        icon: str = "",
        command: Optional[Callable] = None,
        is_selected: bool = False,
        **kwargs
    ):
        self.parent = parent
        self.text = text
        self.icon = icon
        self.command = command
        self.is_selected = is_selected
        self._frame = None
        self._label = None
        self._create_widget(**kwargs)
        
    def _create_widget(self, **kwargs):
        colors = theme_manager.colors
        font = theme_manager.get_font
        
        self._frame = tk.Frame(
            self.parent,
            bg=colors.get("bg_secondary", "#1E1E1E"),
            cursor="hand2",
            pady=8,
            padx=16,
            **kwargs
        )
        
        display_text = f"  {self.icon}  {self.text}" if self.icon else f"  {self.text}"
        
        if self.is_selected:
            bg_color = colors.get("bg_tertiary", "#2D333B")
        else:
            bg_color = colors.get("bg_secondary", "#1E1E1E")
            
        self._label = tk.Label(
            self._frame,
            text=display_text,
            font=("Segoe UI", 11),
            bg=bg_color,
            fg=colors.get("fg_primary", "#B2C2CD"),
            anchor="w",
            padx=10,
            pady=6
        )
        self._label.pack(fill="x")
        
        self._frame.bind("<Button-1>", self._on_click)
        self._label.bind("<Button-1>", self._on_click)
        self._frame.bind("<Enter>", self._on_enter)
        self._frame.bind("<Leave>", self._on_leave)
        self._label.bind("<Enter>", self._on_enter)
        self._label.bind("<Leave>", self._on_leave)
        
    def _on_click(self, event):
        if self.command:
            self.command()
            
    def _on_enter(self, event):
        if not self.is_selected:
            colors = theme_manager.colors
            hover_bg = colors.get("bg_tertiary", "#2D333B")
            self._frame.configure(bg=hover_bg)
            self._label.configure(bg=hover_bg)
            
    def _on_leave(self, event):
        if not self.is_selected:
            colors = theme_manager.colors
            bg_color = colors.get("bg_secondary", "#1E1E1E")
            self._frame.configure(bg=bg_color)
            self._label.configure(bg=bg_color)
            
    def set_selected(self, selected: bool):
        self.is_selected = selected
        colors = theme_manager.colors
        if selected:
            bg = colors.get("bg_tertiary", "#2D333B")
        else:
            bg = colors.get("bg_secondary", "#1E1E1E")
        self._frame.configure(bg=bg)
        self._label.configure(bg=bg)
        
    def update_theme(self):
        colors = theme_manager.colors
        if self.is_selected:
            bg = colors.get("bg_tertiary", "#2D333B")
        else:
            bg = colors.get("bg_secondary", "#1E1E1E")
        self._frame.configure(bg=bg)
        self._label.configure(
            bg=bg,
            fg=colors.get("fg_primary", "#B2C2CD")
        )


class SidebarPanel:
    def __init__(
        self,
        parent: tk.Widget,
        on_navigate: Callable[[str], None] = None,
        width: int = 220,
        **kwargs
    ):
        self.parent = parent
        self.width = width
        self.on_navigate = on_navigate
        self._frame = None
        self._buttons: Dict[str, SidebarButton] = {}
        self._selected = "inicio"
        self._create_widget(**kwargs)
        
    def _create_widget(self, **kwargs):
        colors = theme_manager.colors
        
        self._frame = tk.Frame(
            self.parent,
            bg=colors.get("bg_secondary", "#1E1E1E"),
            width=self.width,
            **kwargs
        )
        self._frame.pack(side="left", fill="y")
        self._frame.pack_propagate(False)
        
        self._create_header()
        self._create_buttons()
        
    def _create_header(self):
        colors = theme_manager.colors
        
        header = tk.Frame(
            self._frame,
            bg=colors.get("bg_secondary", "#1E1E1E")
        )
        header.pack(fill="x", pady=(20, 10), padx=16)
        
        logo_label = tk.Label(
            header,
            text="🖥️",
            font=("Segoe UI", 24),
            bg=colors.get("bg_secondary", "#1E1E1E"),
            fg=colors.get("accent", "#528BFF")
        )
        logo_label.pack()
        
        org_label = tk.Label(
            header,
            text="XEBEC\nCORPORATION",
            font=("Segoe UI", 10, "bold"),
            bg=colors.get("bg_secondary", "#1E1E1E"),
            fg=colors.get("accent", "#528BFF"),
            justify="center"
        )
        org_label.pack(pady=(5, 0))
        
        separator = tk.Frame(
            self._frame,
            bg=colors.get("border", "#333333"),
            height=1
        )
        separator.pack(fill="x", padx=16, pady=15)
        
    def _create_buttons(self):
        buttons_config = [
            ("inicio", "🏠", "Inicio"),
            ("nuevo", "📄", "Nuevo"),
            ("abrir", "📂", "Abrir"),
        ]
        
        for btn_id, icon, text in buttons_config:
            is_selected = btn_id == self._selected
            btn = SidebarButton(
                self._frame,
                text=text,
                icon=icon,
                is_selected=is_selected,
                command=lambda id=btn_id: self._on_button_click(id)
            )
            self._buttons[btn_id] = btn
            
    def _on_button_click(self, btn_id: str):
        for old_id, btn in self._buttons.items():
            btn.set_selected(old_id == btn_id)
        self._selected = btn_id
        if self.on_navigate:
            self.on_navigate(btn_id)
            
    def select_button(self, btn_id: str):
        if btn_id in self._buttons:
            self._on_button_click(btn_id)
            
    def update_theme(self):
        colors = theme_manager.colors
        self._frame.configure(bg=colors.get("bg_secondary", "#1E1E1E"))
        for btn in self._buttons.values():
            btn.update_theme()
            
    def get_widget(self):
        return self._frame
