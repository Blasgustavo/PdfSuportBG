import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from PyQt6.QtWidgets import QApplication

# Nuevos imports modularizados
from src.gui.windows.window_manager import window_manager
from src.gui.themes.theme_manager import theme_manager
from src.config import APP_NAME, APP_VERSION
from src.utils.logger import logger


def main():
    log_dir = Path.cwd() / "logs"
    logger.setup(log_dir=log_dir)
    log = logger.get_logger()
    log.info(f"Iniciando {APP_NAME} v{APP_VERSION}")

    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setOrganizationName("Corporación Xebec")
    
    # Aplicar tema a nivel de aplicación ANTES de crear ventanas
    app.setStyleSheet(theme_manager.get_stylesheet())
    
    window_manager.set_app(app)
    window_manager.show_splash(duration_ms=1500)
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
