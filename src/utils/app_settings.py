import json
from pathlib import Path
from typing import Optional, Any, Dict
from datetime import datetime

from src.utils.logger import logger


class AppSettings:
    """Sistema de configuración persistente para la aplicación."""
    
    _instance: Optional['AppSettings'] = None
    _config_path: Path = None
    
    def __new__(cls) -> 'AppSettings':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init()
        return cls._instance
    
    def _init(self) -> None:
        """Inicializa la configuración."""
        self._config_dir = Path.home() / ".xebec-pdf-fixer"
        self._config_dir.mkdir(exist_ok=True)
        self._config_path = self._config_dir / "settings.json"
        self._load()
    
    def _load(self) -> None:
        """Carga la configuración desde el archivo."""
        if self._config_path.exists():
            try:
                with open(self._config_path, 'r', encoding='utf-8') as f:
                    self._data = json.load(f)
                logger.config(f"Configuración cargada desde {self._config_path}")
            except Exception as e:
                logger.warning(f"Error cargando configuración: {e}")
                self._data = self._default_settings()
        else:
            self._data = self._default_settings()
            logger.config(f"Usando configuración por defecto")
    
    def _default_settings(self) -> Dict[str, Any]:
        """Retorna la configuración por defecto."""
        return {
            "app": {
                "theme": "dark",
                "language": "es",
                "font_family": "Segoe UI",
                "font_size": 12,
                "startup_screen": "home",
                "show_splash": True,
                "splash_duration": 2000,
            },
            "modules": {
                "repair": True,
                "merge": True,
                "split": True,
                "extract": True,
                "compress": True,
                "encrypt": True,
            },
            "supported_files": {
                "pdf": True,
                "images_to_pdf": ["jpg", "jpeg", "png", "bmp", "gif", "tiff"],
                "max_file_size_mb": 500,
            },
            "user": {
                "logged_in": False,
                "username": "",
                "email": "",
                "last_login": None,
            },
            "recent_files": {
                "max_count": 20,
                "paths": []
            },
            "window": {
                "remember_size": True,
                "remember_position": True,
                "default_width": 1200,
                "default_height": 800,
            }
        }
    
    def save(self) -> None:
        """Guarda la configuración al archivo."""
        try:
            with open(self._config_path, 'w', encoding='utf-8') as f:
                json.dump(self._data, f, indent=4, ensure_ascii=False)
            logger.config(f"Configuración guardada")
        except Exception as e:
            logger.error(f"Error guardando configuración: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Obtiene un valor de configuración."""
        keys = key.split(".")
        value = self._data
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default
    
    def set(self, key: str, value: Any) -> None:
        """Establece un valor de configuración."""
        keys = key.split(".")
        data = self._data
        for k in keys[:-1]:
            if k not in data:
                data[k] = {}
            data = data[k]
        data[keys[-1]] = value
        self.save()
    
    def get_all(self) -> Dict[str, Any]:
        """Retorna toda la configuración."""
        return self._data.copy()
    
    @property
    def theme(self) -> str:
        return self.get("app.theme", "dark")
    
    @theme.setter
    def theme(self, value: str) -> None:
        self.set("app.theme", value)
    
    @property
    def font_family(self) -> str:
        return self.get("app.font_family", "Segoe UI")
    
    @font_family.setter
    def font_family(self, value: str) -> None:
        self.set("app.font_family", value)
    
    @property
    def font_size(self) -> int:
        value = self.get("app.font_size", 12)
        if value is None or not isinstance(value, int) or value < 1:
            return 12
        return value
    
    @font_size.setter
    def font_size(self, value: int) -> None:
        self.set("app.font_size", value)
    
    @property
    def is_logged_in(self) -> bool:
        return self.get("user.logged_in", False)
    
    @property
    def username(self) -> str:
        return self.get("user.username", "")
    
    def login(self, username: str, email: str = "") -> None:
        logger.user(f"Iniciando sesión: {username}")
        self.set("user.logged_in", True)
        self.set("user.username", username)
        self.set("user.email", email)
        self.set("user.last_login", datetime.now().isoformat())
        logger.user(f"Usuario logueado: {username}")
    
    def logout(self) -> None:
        username = self.username
        logger.user(f"Cerrando sesión: {username}")
        self.set("user.logged_in", False)
        self.set("user.username", "")
        self.set("user.email", "")
        logger.user(f"Sesión cerrada")
    
    def get_user_info(self) -> Dict[str, Any]:
        return {
            "logged_in": self.is_logged_in,
            "username": self.username,
            "email": self.get("user.email", ""),
            "last_login": self.get("user.last_login", None),
        }


app_settings = AppSettings()
