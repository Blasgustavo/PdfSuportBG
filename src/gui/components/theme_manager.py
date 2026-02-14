from typing import Dict, Any, Callable, Optional
from pathlib import Path
import tkinter as tk


DARK_THEME = {
    "name": "One Dark Pro",
    "bg_primary": "#282A31",
    "bg_secondary": "#16181F",
    "bg_tertiary": "#2D333B",
    "bg_current_line": "#2D333B",
    "fg_primary": "#B2C2CD",
    "fg_secondary": "#8E9BAB",
    "fg_disabled": "#5C6370",
    "accent": "#528BFF",
    "accent_hover": "#6FA3FF",
    "border": "#3E4451",
    "comment": "#5C6370",
    "error": "#E06C75",
    "success": "#98C379",
    "warning": "#E5C07B",
    "info": "#61AFEF",
    "purple": "#C678DD",
    "cyan": "#56B6C2",
    "close_btn": "#C0392B",
    "min_btn": "#7F8C8D",
}

LIGHT_THEME = {
    "name": "Atom One Light",
    "bg_primary": "#FAFAFA",
    "bg_secondary": "#F5F5F5",
    "bg_tertiary": "#EFEFEF",
    "bg_current_line": "#EFEFEF",
    "fg_primary": "#383A42",
    "fg_secondary": "#9DA5B4",
    "fg_disabled": "#A0A1A7",
    "accent": "#526FFF",
    "accent_hover": "#6B80FF",
    "border": "#E5E5E6",
    "comment": "#A0A1A7",
    "error": "#E45649",
    "success": "#50A14F",
    "warning": "#986801",
    "info": "#526FFF",
    "purple": "#A626A4",
    "cyan": "#0897B3",
    "close_btn": "#E45649",
    "min_btn": "#A0A1A7",
}


class ThemeManager:
    _instance = None
    _callbacks: list[Callable] = []
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._current_theme = "dark"
        self._font_family = "Segoe UI"
        self._font_size = 12
        
    @property
    def theme(self) -> Dict[str, Any]:
        return DARK_THEME if self._current_theme == "dark" else LIGHT_THEME
    
    @property
    def colors(self) -> Dict[str, str]:
        return self.theme
    
    @property
    def font_family(self) -> str:
        return self._font_family
    
    @property
    def font_size(self) -> int:
        return self._font_size
    
    @property
    def font(self) -> tuple:
        return (self._font_family, self._font_size)
    
    def get_font(self, size: int = None, weight: str = "") -> tuple:
        if weight:
            return (self._font_family, size or self._font_size, weight)
        return (self._font_family, size or self._font_size)
    
    def set_theme(self, theme_name: str):
        if theme_name in ["dark", "light"]:
            self._current_theme = theme_name
            self._notify()
    
    def toggle_theme(self):
        self._current_theme = "light" if self._current_theme == "dark" else "dark"
        self._notify()
    
    def set_font(self, font_family: str, font_size: int = None):
        self._font_family = font_family
        if font_size:
            self._font_size = font_size
        self._notify()
    
    def register_callback(self, callback: Callable):
        if callback not in self._callbacks:
            self._callbacks.append(callback)
    
    def unregister_callback(self, callback: Callable):
        if callback in self._callbacks:
            self._callbacks.remove(callback)
    
    def _notify(self):
        for callback in self._callbacks:
            try:
                callback()
            except Exception:
                pass


theme_manager = ThemeManager()
