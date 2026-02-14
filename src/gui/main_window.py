import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
from typing import Optional

from src.core.pdf_repair import PDFRepairer
from src.utils.helpers import get_icon_path
from src.utils.logger import logger
from src.gui.components.theme_manager import theme_manager
from src.gui.components.window_controls import WindowControls
from src.gui.components.start_panel import StartPanel
from src.gui.components.document_card import RecentDocumentsManager


APP_NAME = "Xebec Pdf"
APP_VERSION = "0.0.1"
APP_AUTHOR = "BGNC"
APP_ORG = "Corporación Xebec"


class MainWindow:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(APP_NAME)
        
        self._setup_window()
        self._setup_theme()
        self._setup_icon()
        
        self.current_panel = "start"
        self._build_ui()
        
        self.log = logger.get_logger()
        theme_manager.register_callback(self._on_theme_change)
        
    def _setup_window(self):
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        
        window_width = 1200
        window_height = 700
        
        x = (screen_w - window_width) // 2
        y = (screen_h - window_height) // 2
        
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.minsize(900, 500)
        
    def _setup_theme(self):
        colors = theme_manager.colors
        self.root.configure(bg=colors.get("bg_primary", "#282A31"))
        
    def _setup_icon(self):
        icon_path = get_icon_path()
        if icon_path and icon_path.exists():
            try:
                from PIL import Image, ImageTk
                img = Image.open(icon_path)
                img = img.resize((32, 32), Image.Resampling.LANCZOS)
                icon = ImageTk.PhotoImage(img)
                self.root.iconphoto(True, icon)
            except Exception:
                pass
        
    def _build_ui(self):
        colors = theme_manager.colors
        
        self._main_container = tk.Frame(
            self.root,
            bg=colors.get("bg_primary", "#282A31")
        )
        self._main_container.pack(fill="both", expand=True)
        
        self._create_title_bar()
        
        self._start_panel = StartPanel(
            self._main_container,
            on_document_select=self._on_document_select,
            on_navigate=self._on_navigate
        )
        self._start_panel.get_widget().pack(fill="both", expand=True)
        
        self._window_controls = WindowControls(
            self.root,
            on_close=self._on_close,
            on_minimize=self._on_minimize
        )
        
    def _create_title_bar(self):
        colors = theme_manager.colors
        
        title_bar = tk.Frame(
            self._main_container,
            bg=colors.get("bg_primary", "#282A31"),
            height=40
        )
        title_bar.pack(fill="x")
        title_bar.pack_propagate(False)
        
        title_bar.bind("<Button-1>", self._start_move)
        title_bar.bind("<B1-Motion>", self._do_move)
        
        self._title_label = tk.Label(
            title_bar,
            text="Xebec Pdf",
            font=("Segoe UI", 12, "bold"),
            bg=colors.get("bg_primary", "#282A31"),
            fg=colors.get("fg_primary", "#B2C2CD")
        )
        self._title_label.pack(side="left", padx=20, pady=8)
        
    def _start_move(self, event):
        self.x = event.x
        self.y = event.y
        
    def _do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")
        
    def _on_document_select(self, file_path: str, file_name: str):
        self.log.info(f"Documento seleccionado: {file_name}")
        
        RecentDocumentsManager.add_document(file_path, file_name)
        
        if self._start_panel:
            self._start_panel.refresh_documents()
        
    def _on_navigate(self, nav_id: str):
        if nav_id == "nuevo":
            self._open_new_document()
        elif nav_id == "abrir":
            self._open_document()
            
    def _open_new_document(self):
        file_path = filedialog.askopenfilename(
            title="Abrir PDF",
            filetypes=[("PDF files", "*.pdf")]
        )
        if file_path:
            file_name = Path(file_path).name
            RecentDocumentsManager.add_document(file_path, file_name)
            if self._start_panel:
                self._start_panel.refresh_documents()
                
    def _open_document(self):
        file_path = filedialog.askopenfilename(
            title="Abrir PDF",
            filetypes=[("PDF files", "*.pdf")]
        )
        if file_path:
            file_name = Path(file_path).name
            self._on_document_select(file_path, file_name)
            
    def _on_close(self):
        self.root.destroy()
        
    def _on_minimize(self):
        self.root.state('iconic')
        
    def _on_theme_change(self):
        colors = theme_manager.colors
        
        self._main_container.configure(bg=colors.get("bg_primary", "#282A31"))
        self._title_label.configure(
            bg=colors.get("bg_primary", "#282A31"),
            fg=colors.get("fg_primary", "#B2C2CD")
        )
        
        if hasattr(self, '_start_panel'):
            self._start_panel.update_theme()
            
        if hasattr(self, '_window_controls'):
            self._window_controls.update_theme()
            
    def show_start_panel(self):
        self.current_panel = "start"
        if hasattr(self, '_start_panel'):
            self._start_panel.get_widget().pack(fill="both", expand=True)
