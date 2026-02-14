import tkinter as tk
from typing import Callable, Optional
from .theme_manager import theme_manager


class WindowControls:
    def __init__(
        self,
        parent: tk.Widget,
        on_close: Optional[Callable] = None,
        on_minimize: Optional[Callable] = None,
        on_maximize: Optional[Callable] = None,
        position: str = "top-right"
    ):
        self.parent = parent
        self.on_close = on_close
        self.on_minimize = on_minimize or self._default_minimize
        self.on_maximize = on_maximize
        self.position = position
        self._frame = None
        self._close_btn = None
        self._min_btn = None
        self._max_btn = None
        self._create_widgets()
        
    def _default_minimize(self):
        self.parent.withdraw()
        self.parent.after(100, self.parent.deiconify)
        
    def _create_widgets(self):
        colors = theme_manager.colors
        font = theme_manager.get_font(10)
        
        self._frame = tk.Frame(self.parent, bg=colors.get("bg_primary", "#282A31"))
        
        self._min_btn = tk.Button(
            self._frame,
            text="─",
            font=font,
            bg=colors.get("bg_primary", "#282A31"),
            fg=colors.get("min_btn", "#7F8C8D"),
            bd=0,
            width=2,
            pady=2,
            command=self.on_minimize,
            cursor="hand2",
            relief="flat",
            overrelief="flat",
            activebackground=colors.get("min_btn", "#7F8C8D"),
            activeforeground="white"
        )
        
        self._close_btn = tk.Button(
            self._frame,
            text="✕",
            font=font,
            bg=colors.get("bg_primary", "#282A31"),
            fg=colors.get("close_btn", "#C0392B"),
            bd=0,
            width=2,
            pady=2,
            command=self.on_close or self.parent.destroy,
            cursor="hand2",
            relief="flat",
            overrelief="flat",
            activebackground=colors.get("close_btn", "#C0392B"),
            activeforeground="white"
        )
        
        if self.on_maximize:
            self._max_btn = tk.Button(
                self._frame,
                text="☐",
                font=font,
                bg=colors.get("bg_primary", "#282A31"),
                fg="#F1C40F",
                bd=0,
                width=2,
                pady=2,
                command=self.on_maximize,
                cursor="hand2",
                relief="flat",
                overrelief="flat",
                activebackground="#F1C40F",
                activeforeground="white"
            )
            self._max_btn.pack(side="right", padx=2)
        
        self._min_btn.pack(side="right", padx=2)
        self._close_btn.pack(side="right", padx=2)
        
        self._place()
        
    def _place(self):
        if self.position == "top-right":
            self._frame.place(relx=1.0, x=-10, y=10, anchor="ne")
        elif self.position == "top-left":
            self._frame.place(x=10, y=10, anchor="nw")
            
    def update_theme(self):
        colors = theme_manager.colors
        font = theme_manager.get_font(10)
        
        self._frame.configure(bg=colors.get("bg_primary", "#282A31"))
        
        self._min_btn.configure(
            bg=colors.get("bg_primary", "#282A31"),
            fg=colors.get("min_btn", "#7F8C8D"),
            font=font,
            activebackground=colors.get("min_btn", "#7F8C8D")
        )
        
        self._close_btn.configure(
            bg=colors.get("bg_primary", "#282A31"),
            fg=colors.get("close_btn", "#C0392B"),
            font=font,
            activebackground=colors.get("close_btn", "#C0392B")
        )
        
        if self._max_btn:
            self._max_btn.configure(
                bg=colors.get("bg_primary", "#282A31"),
                fg="#F1C40F",
                font=font,
                activebackground="#F1C40F"
            )
            
    def destroy(self):
        if self._frame:
            self._frame.destroy()
