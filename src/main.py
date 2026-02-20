import sys
import os
from pathlib import Path

# Enable High DPI scaling before Qt is imported
os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
os.environ["QT_SCALE_FACTOR_ROUNDING_POLICY"] = "PassThrough"

# Windows High DPI support
if sys.platform == "win32":
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(2)
    except Exception:
        pass

sys.path.insert(0, str(Path(__file__).parent.parent))

# Install Qt message handler BEFORE any Qt imports to suppress font warnings
from PyQt6.QtCore import qInstallMessageHandler, QtMsgType, QMessageLogContext

def suppress_font_warnings(msg_type: QtMsgType, context: QMessageLogContext, message: str):
    if "setPointSize" in message or "Point size" in message:
        return

qInstallMessageHandler(suppress_font_warnings)

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon

from src.gui.windows.window_manager import window_manager
from src.gui.themes.theme_manager import theme_manager
from src.config import APP_NAME, APP_VERSION
from src.utils.logger import logger


def main():
    log_dir = Path.cwd() / "logs"
    logger.setup(log_dir=log_dir)
    log = logger.get_logger()
    
    logger.app(f"Iniciando {APP_NAME} v{APP_VERSION}")
    logger.config(f"Cargando configuración desde ~/.xebec-pdf-fixer")
    logger.ui(f"Aplicando tema: {theme_manager.theme}")

    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setOrganizationName("Corporación Xebec")
    
    # Set application icon
    icon_path = Path(__file__).parent.parent / "assets" / "icons" / "icono.png"
    if not icon_path.exists():
        icon_path = Path.cwd() / "assets" / "icons" / "icono.png"
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))
    
    app.setStyleSheet(theme_manager.get_stylesheet())
    
    window_manager.set_app(app)
    logger.nav(f"Mostrando splash screen")
    window_manager.show_splash(duration_ms=1500)
    
    logger.app(f"Aplicación iniciada correctamente")
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
