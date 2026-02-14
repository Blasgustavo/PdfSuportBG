import tkinter as tk
from tkinter import ttk
from pathlib import Path
import time
import threading


class SplashScreen:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        
        self.font_name = "Segoe UI"
        
        self._setup_window()
        self._download_and_load_fonts()
        self._build_ui()
        self._center_window()
        
    def _download_and_load_fonts(self):
        try:
            from src.utils.font_manager import FontManager
            
            print("Verificando fuentes...")
            FontManager.download_fonts()
            
            loaded_font = FontManager.load_font(self.root, "JetBrainsMono")
            if loaded_font:
                self.font_name = "JetBrainsMono"
                print(f"Fuente cargada: {self.font_name}")
            else:
                self.font_name = self._get_system_font()
        except Exception as e:
            print(f"Error cargando fuentes: {e}")
            self.font_name = self._get_system_font()
            
    def _get_system_font(self):
        fonts = self.root.tk.call("font", "names")
        font_list = list(fonts) if fonts else []
        
        preferred_fonts = [
            "Cascadia Code",
            "JetBrains Mono", 
            "Fira Code",
            "Hack",
            "Ubuntu Mono",
            "Consolas",
            "Courier New",
        ]
        
        for font_name in preferred_fonts:
            if font_name in font_list:
                return font_name
                
        return "Segoe UI"
        
    def _setup_window(self):
        width = 600
        height = 400
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
        print(f"Usando fuente: {self.font_name}")
        
        canvas = tk.Canvas(
            self.root,
            width=600,
            height=400,
            bg="#0F0F0F",
            highlightthickness=0
        )
        canvas.pack(fill="both", expand=True)
        
        icon_path = self._get_icon_path()
        
        if icon_path and icon_path.exists():
            try:
                from PIL import Image, ImageTk
                img = Image.open(icon_path)
                img = img.resize((80, 80), Image.Resampling.LANCZOS)
                self.icon_image = ImageTk.PhotoImage(img)
                canvas.create_image(230, 160, image=self.icon_image, anchor="center")
            except Exception as e:
                print(f"Error loading icon: {e}")
                self._draw_default_icon(canvas)
        else:
            self._draw_default_icon(canvas)
            
        canvas.create_text(
            320, 160,
            text="Xebec Pdf",
            font=(self.font_name, 28, "bold"),
            fill="#FFFFFF",
            anchor="center"
        )
        
        canvas.create_text(
            300, 290,
            text="Corporación Xebec",
            font=(self.font_name, 11),
            fill="#666666",
            anchor="center"
        )
        
        canvas.create_text(
            300, 315,
            text="Autor: BGNC  |  Versión: 0.0.1",
            font=(self.font_name, 10),
            fill="#444444",
            anchor="center"
        )
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Splash.Horizontal.TProgressbar",
            thickness=4,
            background="#FFFFFF",
            troughcolor="#333333"
        )
        
        self.progress_bar = ttk.Progressbar(
            self.root,
            mode="determinate",
            length=400,
            style="Splash.Horizontal.TProgressbar"
        )
        self.progress_bar.place(x=100, y=350)
        
        self.status_label = tk.Label(
            self.root,
            text="Cargando...",
            font=(self.font_name, 9),
            bg="#0F0F0F",
            fg="#666666"
        )
        self.status_label.place(x=300, y=380, anchor="center")
        
    def _draw_default_icon(self, canvas):
        canvas.create_oval(240, 100, 360, 220, fill="#333333", outline="#555555")
        canvas.create_text(300, 160, text="X", font=(self.font_name, 40, "bold"), fill="white", anchor="center")
        
    def _get_icon_path(self):
        possible_paths = [
            Path.cwd() / "assets" / "icons" / "icono.png",
            Path.cwd() / "assets" / "icons" / "logo.png",
            Path(__file__).parent.parent.parent / "assets" / "icons" / "icono.png",
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
            time.sleep(1.5)
            
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
