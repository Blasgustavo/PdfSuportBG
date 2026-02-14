import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from tkinter import Tk
from src.gui.main_window import MainWindow
from src.utils.logger import logger


def main():
    log_dir = Path.cwd() / "logs"
    logger.setup(log_dir=log_dir)
    log = logger.get_logger()
    log.info("Iniciando Xebec PDF Fixer")

    root = Tk()
    app = MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
