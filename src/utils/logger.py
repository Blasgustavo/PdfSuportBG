import logging
import sys
from pathlib import Path
from datetime import datetime


class Logger:
    _instance = None
    _logger = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def setup(self, name: str = "XebecPDF", log_dir: Path = None, level: int = logging.INFO):
        if self._logger is not None:
            return self._logger

        self._logger = logging.getLogger(name)
        self._logger.setLevel(level)

        formatter = logging.Formatter(
            "%(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        self._logger.addHandler(console_handler)

        if log_dir:
            log_dir.mkdir(parents=True, exist_ok=True)
            log_file = log_dir / f"{name}_{datetime.now().strftime('%Y%m%d')}.log"
            file_handler = logging.FileHandler(log_file, encoding="utf-8")
            file_handler.setFormatter(formatter)
            self._logger.addHandler(file_handler)

        return self._logger

    def get_logger(self):
        if self._logger is None:
            return self.setup()
        return self._logger

    def app(self, message: str):
        self._logger.info(f"🚀 [APP] : {message}")

    def nav(self, message: str):
        self._logger.info(f"🧭 [NAV] : {message}")

    def action(self, message: str):
        self._logger.info(f"👆 [ACTION] : {message}")

    def ui(self, message: str):
        self._logger.info(f"🎨 [UI] : {message}")

    def config(self, message: str):
        self._logger.info(f"⚙️ [CONFIG] : {message}")

    def user(self, message: str):
        self._logger.info(f"👤 [USER] : {message}")

    def file(self, message: str):
        self._logger.info(f"📄 [FILE] : {message}")

    def warning(self, message: str):
        self._logger.warning(f"⚠️ [WARNING] : {message}")

    def error(self, message: str):
        self._logger.error(f"❌ [ERROR] : {message}")

    def debug(self, message: str):
        self._logger.debug(f"🔍 [DEBUG] : {message}")


logger = Logger()
