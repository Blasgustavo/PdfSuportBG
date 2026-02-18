import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Redirect stderr to file
import io
sys.stderr = open("error_log.txt", "w")

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from src.gui.pyqt6.main_window import MainWindow
from src.gui.pyqt6.splash_screen import SplashScreen
from src.gui.pyqt6.theme_manager import theme_manager
from src.utils.logger import logger


def main():
    log_dir = Path.cwd() / "logs"
    logger.setup(log_dir=log_dir)
    log = logger.get_logger()
    log.info("Iniciando Xebec PDF Fixer con PyQt6")

    app = QApplication(sys.argv)
    app.setApplicationName("Xebec Pdf")
    app.setOrganizationName("Corporación Xebec")
    
    window = MainWindow()
    
    splash = SplashScreen()
    splash.show()
    
    def finish_splash():
        splash.finish(window)
        window.showMaximized()
        theme_manager.theme_changed.emit()
    
    QTimer.singleShot(100, finish_splash)
    splash.simulate_loading(lambda: None)
    
    window.close_requested.connect(app.quit)
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
