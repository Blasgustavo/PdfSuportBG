import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from PyQt6.QtWidgets import QApplication
from src.gui.pyqt6.window_manager import window_manager
from src.utils.logger import logger


def main():
    log_dir = Path.cwd() / "logs"
    logger.setup(log_dir=log_dir)
    log = logger.get_logger()
    log.info("Iniciando Xebec PDF Fixer con PyQt6")

    app = QApplication(sys.argv)
    app.setApplicationName("Xebec Pdf")
    app.setOrganizationName("Corporación Xebec")
    
    window_manager.set_app(app)
    window_manager.show_splash(duration_ms=1500)
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
