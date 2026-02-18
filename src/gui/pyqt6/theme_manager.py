from typing import Dict, Any, Callable
import sys


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
    """Theme manager that works without QObject initially."""
    
    _instance = None
    _qobject = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._current_theme = "dark"
            cls._instance._font_family = "Segoe UI"
            cls._instance._font_size = 12
            cls._instance._callbacks = []
            cls._instance._signal_holder = None
        return cls._instance
    
    def _ensure_qobject(self):
        """Ensure QObject is created with signal."""
        if ThemeManager._qobject is None:
            try:
                from PyQt6.QtCore import QObject, pyqtSignal
                
                class SignalQObject(QObject):
                    theme_changed = pyqtSignal()
                
                ThemeManager._qobject = SignalQObject()
                self._signal_holder = ThemeManager._qobject
            except Exception:
                pass
    
    @property
    def theme_changed(self):
        """Return signal-like object for connecting."""
        self._ensure_qobject()
        if self._signal_holder:
            return self._signal_holder.theme_changed
        return None
    
    def connect(self, callback):
        """Connect a callback to theme changes."""
        self._ensure_qobject()
        self._callbacks.append(callback)
        if ThemeManager._qobject is not None:
            try:
                ThemeManager._qobject.theme_changed.connect(callback)
            except Exception:
                pass
    
    def disconnect(self, callback=None):
        """Disconnect a callback from theme changes."""
        if callback in self._callbacks:
            self._callbacks.remove(callback)
        if ThemeManager._qobject is not None and callback is not None:
            try:
                ThemeManager._qobject.theme_changed.disconnect(callback)
            except Exception:
                pass
    
    def emit_change(self):
        """Emit theme changed signal."""
        self._ensure_qobject()
        if ThemeManager._qobject is not None:
            try:
                ThemeManager._qobject.theme_changed.emit()
            except Exception:
                pass
        # Also call callbacks directly
        for callback in self._callbacks:
            try:
                callback()
            except Exception:
                pass

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

    def get_font(self, size: int = None, weight: str = "") -> str:
        size = size or self._font_size
        if weight:
            return f"{self._font_family} {size} {weight}"
        return f"{self._font_family} {size}"

    def get_qcolor(self, key: str):
        from PyQt6.QtGui import QColor
        color = self.theme.get(key, "#000000")
        return QColor(color)

    def get_palette(self):
        from PyQt6.QtGui import QPalette
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, self.get_qcolor("bg_primary"))
        palette.setColor(QPalette.ColorRole.WindowText, self.get_qcolor("fg_primary"))
        palette.setColor(QPalette.ColorRole.Base, self.get_qcolor("bg_secondary"))
        palette.setColor(QPalette.ColorRole.AlternateBase, self.get_qcolor("bg_tertiary"))
        palette.setColor(QPalette.ColorRole.ToolTipBase, self.get_qcolor("bg_secondary"))
        palette.setColor(QPalette.ColorRole.ToolTipText, self.get_qcolor("fg_primary"))
        palette.setColor(QPalette.ColorRole.Text, self.get_qcolor("fg_primary"))
        palette.setColor(QPalette.ColorRole.Button, self.get_qcolor("bg_tertiary"))
        palette.setColor(QPalette.ColorRole.ButtonText, self.get_qcolor("fg_primary"))
        palette.setColor(QPalette.ColorRole.BrightText, self.get_qcolor("fg_primary"))
        palette.setColor(QPalette.ColorRole.Highlight, self.get_qcolor("accent"))
        palette.setColor(QPalette.ColorRole.HighlightedText, self.get_qcolor("fg_primary"))
        return palette

    def set_theme(self, theme_name: str):
        if theme_name in ["dark", "light"]:
            self._current_theme = theme_name
            self.emit_change()

    def toggle_theme(self):
        self._current_theme = "light" if self._current_theme == "dark" else "dark"
        self.emit_change()

    def set_font(self, font_family: str, font_size: int = None):
        self._font_family = font_family
        if font_size:
            self._font_size = font_size
        self.emit_change()


theme_manager = ThemeManager()
