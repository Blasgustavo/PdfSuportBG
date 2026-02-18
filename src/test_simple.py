import sys
from pathlib import Path
import traceback

sys.path.insert(0, str(Path.cwd()))

print("1. Starting script...")

try:
    print("2. Importing PyQt6.QtWidgets...")
    from PyQt6.QtWidgets import QApplication
    print("3. PyQt6.QtWidgets imported")
    
    print("4. Creating QApplication...")
    app = QApplication(sys.argv)
    print("5. QApplication created")
    
    print("6. Importing theme_manager...")
    from src.gui.pyqt6.theme_manager import theme_manager
    print("7. theme_manager imported")
    
    print("8. Setting theme...")
    theme_manager.set_theme('dark')
    print("9. Theme set")
    
    print("10. Importing MainWindow...")
    from src.gui.pyqt6.main_window import MainWindow
    print("11. MainWindow imported")
    
    print("12. Creating MainWindow...")
    window = MainWindow()
    print("13. MainWindow created")
    
    print("14. Showing window...")
    window.show()
    print("15. Window shown")
    
    print("16. Running app.exec()...")
    sys.exit(app.exec())
    
except Exception as e:
    print(f"ERROR: {e}")
    traceback.print_exc()
