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
from src.gui.components.recent_panel import RecentPanel
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
        
        self.current_panel = "recent"
        self._build_ui()
        
        self.log = logger.get_logger()
        theme_manager.register_callback(self._on_theme_change)
        
    def _setup_window(self):
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_w}x{screen_h}+0+0")
        self.root.state('zoomed')
        
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
        
        self._recent_panel = RecentPanel(
            self._main_container,
            on_document_select=self._on_document_select,
            on_new_document=self._on_new_document
        )
        self.recent_panel_widget = self._recent_panel.get_widget()
        self.recent_panel_widget.pack(fill="both", expand=True)
        
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
        
        messagebox.showinfo(
            "Documento seleccionado",
            f"Se abrirá: {file_name}\n\nRuta: {file_path}"
        )
        
    def _on_new_document(self):
        file_path = filedialog.askopenfilename(
            title="Abrir PDF",
            filetypes=[("PDF files", "*.pdf")]
        )
        if file_path:
            file_name = Path(file_path).name
            RecentDocumentsManager.add_document(file_path, file_name)
            self._recent_panel.load_documents()
            
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
        
        if hasattr(self, '_recent_panel'):
            self._recent_panel.update_theme()
            
        if hasattr(self, '_window_controls'):
            self._window_controls.update_theme()
            
    def show_main_panel(self):
        self.current_panel = "main"
        if hasattr(self, 'recent_panel_widget'):
            self.recent_panel_widget.pack_forget()
            
    def show_recent_panel(self):
        self.current_panel = "recent"
        if hasattr(self, 'recent_panel_widget'):
            self.recent_panel_widget.pack(fill="both", expand=True)
            
    def set_status(self, text: str):
        if hasattr(self, '_status_label'):
            self._status_label.configure(text=text)
