import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

# Redirect stdout and stderr to file
output_file = open("output_debug.txt", "w", buffering=1)
sys.stdout = output_file
sys.stderr = output_file

print("=" * 50, flush=True)
print("Iniciando aplicación...", flush=True)

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from src.gui.pyqt6.main_window import MainWindow
from src.gui.pyqt6.splash_screen import SplashScreen
from src.gui.pyqt6.theme_manager import theme_manager
from src.utils.logger import logger

def main():
    print("Creando QApplication...", flush=True)
    
    log_dir = Path.cwd() / "logs"
    logger.setup(log_dir=log_dir)
    log = logger.get_logger()
    log.info("Iniciando Xebec PDF Fixer con PyQt6")

    app = QApplication(sys.argv)
    app.setApplicationName("Xebec Pdf")
    app.setOrganizationName("Corporación Xebec")
    
    print("Creando MainWindow...", flush=True)
    window = MainWindow()
    
    splash = SplashScreen()
    splash.show()
    
    def finish_splash():
        print("finish_splash llamado", flush=True)
        splash.finish(window)
        window.showMaximized()
        theme_manager.theme_changed.emit()
        print("Splash terminado", flush=True)
    
    QTimer.singleShot(100, finish_splash)
    splash.simulate_loading(lambda: None)
    
    print("Conectando close_requested...", flush=True)
    window.close_requested.connect(app.quit)
    
    print("Ejecutando app.exec()...", flush=True)
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
