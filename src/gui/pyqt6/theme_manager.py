from typing import Dict, Any, Callable
import sys


# XEBEC CORPORATION - Paleta de colores corporativa
DARK_THEME = {
    "name": "XEBEC Dark",
    # Primary - Azul corporativo XEBEC
    "primary": "#1E3A5F",
    "primary_light": "#2E5A8F",
    "primary_dark": "#0E2A4F",
    # Backgrounds
    "bg_primary": "#1A202C",
    "bg_secondary": "#2D3748",
    "bg_tertiary": "#4A5568",
    "bg_current_line": "#2D333B",
    # Text
    "fg_primary": "#F7FAFC",
    "fg_secondary": "#E2E8F0",
    "fg_tertiary": "#A0AEC0",
    "fg_disabled": "#5C6370",
    # Accent - Naranja XEBEC
    "accent": "#F6993F",
    "accent_light": "#F6AD55",
    "accent_dark": "#DD6B20",
    "accent_hover": "#F6AD55",
    # Borders
    "border": "#4A5568",
    "border_light": "#718096",
    # Estados
    "success": "#38A169",
    "warning": "#D69E2E",
    "error": "#E53E3E",
    "info": "#3182CE",
    # Extra
    "purple": "#C678DD",
    "cyan": "#56B6C2",
    "close_btn": "#C0392B",
    "min_btn": "#7F8C8D",
    # Gradientes (para texturizado)
    "gradient_start": "#1E3A5F",
    "gradient_end": "#0E2A4F",
    # Metallic effects
    "metallic_light": "#E2E8F0",
    "metallic_mid": "#A0AEC0",
    "metallic_dark": "#718096",
}

LIGHT_THEME = {
    "name": "XEBEC Light",
    # Primary - Azul corporativo XEBEC
    "primary": "#1E3A5F",
    "primary_light": "#2E5A8F",
    "primary_dark": "#0E2A4F",
    # Backgrounds
    "bg_primary": "#FFFFFF",
    "bg_secondary": "#F7FAFC",
    "bg_tertiary": "#EDF2F7",
    "bg_current_line": "#EFEFEF",
    # Text
    "fg_primary": "#1A202C",
    "fg_secondary": "#4A5568",
    "fg_tertiary": "#718096",
    "fg_disabled": "#A0A1A7",
    # Accent - Naranja XEBEC
    "accent": "#F6993F",
    "accent_light": "#F6AD55",
    "accent_dark": "#DD6B20",
    "accent_hover": "#ED8936",
    # Borders
    "border": "#E2E8F0",
    "border_light": "#CBD5E0",
    # Estados
    "success": "#38A169",
    "warning": "#D69E2E",
    "error": "#E53E3E",
    "info": "#3182CE",
    # Extra
    "purple": "#A626A4",
    "cyan": "#0897B3",
    "close_btn": "#E45649",
    "min_btn": "#A0A1A7",
    # Gradientes
    "gradient_start": "#F7FAFC",
    "gradient_end": "#EDF2F7",
    # Metallic
    "metallic_light": "#F7FAFC",
    "metallic_mid": "#E2E8F0",
    "metallic_dark": "#A0AEC0",
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
        # Also update application stylesheet
        self._update_app_stylesheet()
    
    def _update_app_stylesheet(self):
        """Actualiza el stylesheet de la aplicación."""
        try:
            from PyQt6.QtWidgets import QApplication
            app = QApplication.instance()
            if app:
                app.setStyleSheet(self.get_stylesheet())
        except Exception:
            pass

    @property
    def theme(self) -> Dict[str, Any]:
        return DARK_THEME if self._current_theme == "dark" else LIGHT_THEME

    @property
    def colors(self) -> Dict[str, str]:
        return self.theme
    
    def toggle_theme(self) -> str:
        """Alterna entre tema oscuro y claro."""
        self._current_theme = "light" if self._current_theme == "dark" else "dark"
        self.emit_change()
        return self._current_theme
    
    def set_theme(self, theme_name: str) -> None:
        """Establece un tema específico."""
        if theme_name in ("dark", "light"):
            self._current_theme = theme_name
            self.emit_change()

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

    def get_stylesheet(self) -> str:
        """Genera stylesheet global para la aplicación."""
        colors = self.colors
        return f"""
            QWidget {{
                background-color: {colors['bg_primary']};
                color: {colors['fg_primary']};
                font-family: "Segoe UI", sans-serif;
                font-size: 14px;
            }}
            QMainWindow {{
                background-color: {colors['bg_primary']};
            }}
            QFrame {{
                background-color: {colors['bg_primary']};
                color: {colors['fg_primary']};
            }}
            QPushButton {{
                background-color: {colors['primary']};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: {colors['primary_light']};
            }}
            QPushButton:pressed {{
                background-color: {colors['primary_dark']};
            }}
            QLabel {{
                color: {colors['fg_primary']};
                background-color: transparent;
            }}
            QMenuBar {{
                background-color: {colors['bg_secondary']};
                color: {colors['fg_primary']};
            }}
            QMenuBar::item:selected {{
                background-color: {colors['bg_tertiary']};
            }}
            QMenu {{
                background-color: {colors['bg_secondary']};
                color: {colors['fg_primary']};
                border: 1px solid {colors['border']};
            }}
            QMenu::item:selected {{
                background-color: {colors['accent']};
            }}
            QScrollBar:vertical {{
                background-color: {colors['bg_secondary']};
                width: 12px;
                border: none;
            }}
            QScrollBar::handle:vertical {{
                background-color: {colors['bg_tertiary']};
                border-radius: 6px;
                min-height: 20px;
            }}
            QScrollBar::handle:vertical:hover {{
                background-color: {colors['accent']};
            }}
        """

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
