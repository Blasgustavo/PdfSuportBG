from PyQt6.QtCore import pyqtSignal, QObject

DARK_THEME = {
    "name": "One Dark Pro",
    "bg_primary": "#282A31",
}

class ThemeManager(QObject):
    theme_changed = pyqtSignal()

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        super().__init__()
        self._initialized = True
        self._current_theme = "dark"

theme_manager = ThemeManager()
print("theme_manager created")
