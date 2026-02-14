import tkinter as tk
from tkinter import ttk
from pathlib import Path
import time
import threading


class SplashScreen:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.configure(bg="#282A31")
        
        self._setup_window()
        self._build_ui()
        self._center_window()
        
        self.progress = 0
        self.status_text = "Iniciando..."
        
    def _setup_window(self):
        width = 500
        height = 300
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        x = (screen_w // 2) - (width // 2)
        y = (screen_h // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
    def _center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
    def _build_ui(self):
        self.root.configure(bg="#282A31")
        
        self.canvas = tk.Canvas(
            self.root,
            width=500,
            height=300,
            bg="#282A31",
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)
        
        logo_path = self._get_logo_path()
        
        if logo_path and logo_path.exists():
            try:
                from PIL import Image, ImageTk
                img = Image.open(logo_path)
                img = img.resize((120, 120), Image.Resampling.LANCZOS)
                self.logo_image = ImageTk.PhotoImage(img)
                self.canvas.create_image(250, 100, image=self.logo_image, anchor="center")
            except Exception:
                self._draw_default_logo()
        else:
            self._draw_default_logo()
            
        self.canvas.create_text(
            250, 180,
            text="Xebec PDF Fixer",
            font=("Segoe UI", 24, "bold"),
            fill="#B2C2CD",
            anchor="center"
        )
        
        self.canvas.create_text(
            250, 210,
            text="Corporación Xebec",
            font=("Segoe UI", 12),
            fill="#8E9BAB",
            anchor="center"
        )
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Splash.Horizontal.TProgressbar",
            thickness=6,
            background="#528BFF",
            troughcolor="#16181F"
        )
        
        self.progress_bar = ttk.Progressbar(
            self.root,
            mode="determinate",
            length=300,
            style="Splash.Horizontal.TProgressbar"
        )
        self.progress_bar.place(x=100, y=240)
        
        self.status_label = tk.Label(
            self.root,
            text="Iniciando...",
            font=("Segoe UI", 10),
            bg="#282A31",
            fg="#8E9BAB"
        )
        self.status_label.place(x=250, y=275, anchor="center")
        
    def _draw_default_logo(self):
        self.canvas.create_oval(200, 50, 300, 150, fill="#528BFF", outline="#528BFF")
        self.canvas.create_text(
            250, 100,
            text="X",
            font=("Segoe UI", 40, "bold"),
            fill="#282A31",
            anchor="center"
        )
        
    def _get_logo_path(self):
        possible_paths = [
            Path.cwd() / "assets" / "icons" / "logo.png",
            Path(__file__).parent.parent.parent / "assets" / "icons" / "logo.png",
        ]
        for path in possible_paths:
            if path.exists():
                return path
        return None
        
    def update_progress(self, value: int, status: str = ""):
        self.progress = value
        if status:
            self.status_text = status
        self.progress_bar["value"] = value
        self.status_label.config(text=status)
        self.root.update()
        
    def simulate_loading(self):
        steps = [
            (20, "Cargando configuración..."),
            (40, "Inicializando componentes..."),
            (60, "Cargando interfaz gráfica..."),
            (80, "Preparando herramientas PDF..."),
            (100, "¡Listo!")
        ]
        
        for progress, status in steps:
            self.update_progress(progress, status)
            time.sleep(0.5)
            
    def close(self):
        self.root.destroy()
        
    def run(self, main_app_callback):
        def loading_thread():
            self.simulate_loading()
            self.root.after(0, self._finish_loading, main_app_callback)
            
        thread = threading.Thread(target=loading_thread, daemon=True)
        thread.start()
        self.root.mainloop()
        
    def _finish_loading(self, main_app_callback):
        self.close()
        main_app_callback()
