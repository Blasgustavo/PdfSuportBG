import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional
from .base import Component
from .theme_manager import theme_manager


class Button(Component):
    def __init__(
        self,
        parent: tk.Widget,
        text: str = "",
        command: Optional[Callable] = None,
        width: int = None,
        height: int = None,
        padding: int = 8,
        variant: str = "primary",
        **kwargs
    ):
        self.text = text
        self.command = command
        self.variant = variant
        super().__init__(parent, width=width, height=height, padding=padding, **kwargs)
        self._create_widget()
        self._apply_theme()
        
    def _create_widget(self):
        self._widget = tk.Button(
            self.parent,
            text=self.text,
            command=self.command,
            width=self.width,
            padx=self.padding,
            pady=self.padding // 2,
            relief="flat",
            cursor="hand2",
            **self._kwargs
        )
        
    def _apply_theme(self):
        colors = theme_manager.colors
        font = theme_manager.get_font(10)
        
        if self.variant == "primary":
            bg = colors.get("accent", "#528BFF")
            fg = "#FFFFFF"
            hover = colors.get("accent_hover", "#6FA3FF")
        elif self.variant == "secondary":
            bg = colors.get("bg_tertiary", "#2D333B")
            fg = colors.get("fg_primary", "#B2C2CD")
            hover = colors.get("border", "#3E4451")
        elif self.variant == "danger":
            bg = colors.get("error", "#E06C75")
            fg = "#FFFFFF"
            hover = "#C0392B"
        elif self.variant == "ghost":
            bg = colors.get("bg_primary", "#282A31")
            fg = colors.get("fg_primary", "#B2C2CD")
            hover = colors.get("bg_tertiary", "#2D333B")
        else:
            bg = colors.get("bg_tertiary", "#2D333B")
            fg = colors.get("fg_primary", "#B2C2CD")
            hover = colors.get("border", "#3E4451")
        
        self._widget.configure(
            bg=bg,
            fg=fg,
            font=font,
            activebackground=hover,
            activeforeground=fg
        )
        
    def configure(self, text: str = None, command: Callable = None, **kwargs):
        if text:
            self.text = text
            self._widget.configure(text=text)
        if command:
            self.command = command
            self._widget.configure(command=command)
        if kwargs:
            self._widget.configure(**kwargs)
            
    def update_theme(self):
        self._apply_theme()


class Label(Component):
    def __init__(
        self,
        parent: tk.Widget,
        text: str = "",
        width: int = None,
        height: int = None,
        font_size: int = 12,
        weight: str = "",
        align: str = "left",
        **kwargs
    ):
        self.text = text
        self.font_size = font_size
        self.weight = weight
        self.align = align
        super().__init__(parent, width=width, height=height, **kwargs)
        self._create_widget()
        self._apply_theme()
        
    def _create_widget(self):
        self._widget = tk.Label(
            self.parent,
            text=self.text,
            width=self.width,
            height=self.height,
            anchor=self.align[0].upper() if self.align else "w",
            **self._kwargs
        )
        
    def _apply_theme(self):
        colors = theme_manager.colors
        font = theme_manager.get_font(self.font_size, self.weight)
        
        self._widget.configure(
            bg=colors.get("bg_primary", "#282A31"),
            fg=colors.get("fg_primary", "#B2C2CD"),
            font=font
        )
        
    def configure(self, text: str = None, **kwargs):
        if text is not None:
            self.text = text
            self._widget.configure(text=text)
        if kwargs:
            self._widget.configure(**kwargs)
            
    def update_theme(self):
        self._apply_theme()


class Input(Component):
    def __init__(
        self,
        parent: tk.Widget,
        width: int = 30,
        height: int = None,
        placeholder: str = "",
        show: str = "",
        **kwargs
    ):
        self.placeholder = placeholder
        self.show = show
        self._placeholder_active = True
        super().__init__(parent, width=width, height=height, **kwargs)
        self._create_widget()
        self._apply_theme()
        self._bind_events()
        
    def _create_widget(self):
        self._widget = tk.Entry(
            self.parent,
            width=self.width,
            relief="flat",
            **self._kwargs
        )
        if self.show:
            self._widget.configure(show=self.show)
            
    def _apply_theme(self):
        colors = theme_manager.colors
        font = theme_manager.get_font(10)
        
        self._widget.configure(
            bg=colors.get("bg_tertiary", "#2D333B"),
            fg=colors.get("fg_primary", "#B2C2CD"),
            font=font,
            insertbackground=colors.get("fg_primary", "#B2C2CD"),
            disabledforeground=colors.get("fg_disabled", "#5C6370")
        )
        
    def _bind_events(self):
        self._widget.bind("<FocusIn>", self._on_focus_in)
        self._widget.bind("<FocusOut>", self._on_focus_out)
        
    def _on_focus_in(self, event):
        if self._placeholder_active and self.placeholder:
            self._widget.delete(0, tk.END)
            self._widget.configure(fg=theme_manager.colors.get("fg_primary", "#B2C2CD"))
            self._placeholder_active = False
            
    def _on_focus_out(self, event):
        if not self.get():
            self._set_placeholder()
            
    def _set_placeholder(self):
        self._widget.insert(0, self.placeholder)
        self._widget.configure(fg=theme_manager.colors.get("fg_disabled", "#5C6370"))
        self._placeholder_active = True
        
    def get(self) -> str:
        return self._widget.get()
    
    def set(self, value: str):
        self._widget.delete(0, tk.END)
        self._widget.insert(0, value)
        self._placeholder_active = False
        
    def clear(self):
        self._widget.delete(0, tk.END)
        if self.placeholder:
            self._set_placeholder()
            
    def update_theme(self):
        self._apply_theme()
        if self._placeholder_active:
            self._widget.configure(fg=theme_manager.colors.get("fg_disabled", "#5C6370"))


class ProgressBar(Component):
    def __init__(
        self,
        parent: tk.Widget,
        width: int = 300,
        height: int = 6,
        mode: str = "determinate",
        **kwargs
    ):
        self.mode = mode
        super().__init__(parent, width=width, height=height, **kwargs)
        self._create_widget()
        self._apply_theme()
        
    def _create_widget(self):
        style = ttk.Style()
        style.theme_use("clam")
        
        style.configure(
            "Custom.Horizontal.TProgressbar",
            thickness=self.height,
            background=theme_manager.colors.get("accent", "#528BFF"),
            troughcolor=theme_manager.colors.get("bg_tertiary", "#2D333B")
        )
        
        self._widget = ttk.Progressbar(
            self.parent,
            mode=self.mode,
            length=self.width,
            style="Custom.Horizontal.TProgressbar",
            **self._kwargs
        )
        
    def _apply_theme(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Custom.Horizontal.TProgressbar",
            thickness=self.height,
            background=theme_manager.colors.get("accent", "#528BFF"),
            troughcolor=theme_manager.colors.get("bg_tertiary", "#2D333B")
        )
        
    def set_value(self, value: float):
        self._widget["value"] = value
        
    def get_value(self) -> float:
        return self._widget["value"]
    
    def update_theme(self):
        self._apply_theme()
