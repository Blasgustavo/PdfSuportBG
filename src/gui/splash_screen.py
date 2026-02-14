import tkinter as tk
from tkinter import ttk
from pathlib import Path
import time
import threading


class SplashScreen:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        
        self._setup_window()
        self._build_ui()
        self._center_window()
        
    def _setup_window(self):
        width = 600
        height = 400
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        x = (screen_w // 2) - (width // 2)
        y = (screen_h // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.configure(bg="#1E1E2E")
        
    def _center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
    def _build_ui(self):
        self.root.configure(bg="#1E1E2E")
        
        canvas = tk.Canvas(
            self.root,
            width=600,
            height=400,
            bg="#1E1E2E",
            highlightthickness=0
        )
        canvas.pack(fill="both", expand=True)
        
        splash_path = self._get_splash_path()
        
        if splash_path and splash_path.exists():
            try:
                from PIL import Image, ImageTk
                img = Image.open(splash_path)
                img = img.resize((600, 400), Image.Resampling.LANCZOS)
                self.splash_image = ImageTk.PhotoImage(img)
                canvas.create_image(300, 200, image=self.splash_image, anchor="center")
                self._create_progress_on_image()
            except Exception as e:
                print(f"Error loading splash: {e}")
                self._create_default_ui(canvas)
        else:
            self._create_default_ui(canvas)
            
    def _create_progress_on_image(self):
        self.progress = 0
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Splash.Horizontal.TProgressbar",
            thickness=4,
            background="#7C3AED",
            troughcolor="#313244"
        )
        
        self.progress_bar = ttk.Progressbar(
            self.root,
            mode="determinate",
            length=400,
            style="Splash.Horizontal.TProgressbar"
        )
        self.progress_bar.place(x=100, y=330)
        
        self.status_label = tk.Label(
            self.root,
            text="Cargando...",
            font=("Segoe UI", 10),
            bg="#1E1E2E",
            fg="#6C7086"
        )
        self.status_label.place(x=300, y=365, anchor="center")
        
    def _create_default_ui(self, canvas):
        canvas.configure(bg="#1E1E2E")
        
        logo_path = self._get_logo_path()
        
        if logo_path and logo_path.exists():
            try:
                from PIL import Image, ImageTk
                img = Image.open(logo_path)
                img = img.resize((100, 100), Image.Resampling.LANCZOS)
                self.logo_image = ImageTk.PhotoImage(img)
                canvas.create_image(300, 150, image=self.logo_image, anchor="center")
            except Exception:
                canvas.create_oval(250, 100, 350, 200, fill="#7C3AED", outline="#7C3AED")
                canvas.create_text(300, 150, text="X", font=("Segoe UI", 36, "bold"), fill="white", anchor="center")
        else:
            canvas.create_oval(250, 100, 350, 200, fill="#7C3AED", outline="#7C3AED")
            canvas.create_text(300, 150, text="X", font=("Segoe UI", 36, "bold"), fill="white", anchor="center")
            
        canvas.create_text(
            300, 240,
            text="Xebec Pdf",
            font=("Segoe UI", 28, "bold"),
            fill="#CDD6F4",
            anchor="center"
        )
        
        canvas.create_text(
            300, 275,
            text="Cargando...",
            font=("Segoe UI", 11),
            fill="#6C7086",
            anchor="center"
        )
        
        self.progress = 0
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Splash.Horizontal.TProgressbar",
            thickness=4,
            background="#7C3AED",
            troughcolor="#313244"
        )
        
        self.progress_bar = ttk.Progressbar(
            self.root,
            mode="determinate",
            length=400,
            style="Splash.Horizontal.TProgressbar"
        )
        self.progress_bar.place(x=100, y=330)
        
        self.status_label = tk.Label(
            self.root,
            text="Cargando...",
            font=("Segoe UI", 10),
            bg="#1E1E2E",
            fg="#6C7086"
        )
        self.status_label.place(x=300, y=365, anchor="center")
        
    def _get_splash_path(self):
        possible_paths = [
            Path.cwd() / "assets" / "splash" / "estart-cargando.png",
            Path(__file__).parent.parent.parent / "assets" / "splash" / "estart-cargando.png",
        ]
        for path in possible_paths:
            if path.exists():
                return path
        return None
        
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
            (20, "Iniciando..."),
            (40, "Cargando configuración..."),
            (60, "Preparando interfaz..."),
            (80, "Cargando herramientas..."),
            (100, "¡Listo!")
        ]
        
        for progress, status in steps:
            self.update_progress(progress, status)
            time.sleep(0.6)
            
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
