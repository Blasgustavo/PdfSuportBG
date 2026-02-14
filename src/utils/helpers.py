from pathlib import Path
from typing import Optional
from tkinter import Tk


def center_window(window: Tk, width: int = 420, height: int = 300) -> None:
    screen_w = window.winfo_screenwidth()
    screen_h = window.winfo_screenheight()
    x = (screen_w // 2) - (width // 2)
    y = (screen_h // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")


def get_app_data_dir() -> Path:
    if hasattr(__import__('sys'), 'frozen'):
        base = Path(__import__('sys')._MEIPASS)
    else:
        base = Path(__file__).parent.parent.parent
    return base


def get_icon_path(icon_name: str = "xebec_icon.png") -> Optional[Path]:
    possible_paths = [
        Path.cwd() / icon_name,
        get_app_data_dir() / "assets" / "icons" / icon_name,
    ]
    for path in possible_paths:
        if path.exists():
            return path
    return None
