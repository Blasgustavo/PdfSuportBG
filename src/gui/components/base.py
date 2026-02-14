import tkinter as tk
from typing import Optional, Callable, Any
from abc import ABC, abstractmethod


class Component(ABC):
    def __init__(
        self,
        parent: tk.Widget,
        width: int = None,
        height: int = None,
        padding: int = 0,
        margin: int = 0,
        bg: str = None,
        fg: str = None,
        **kwargs
    ):
        self.parent = parent
        self.width = width
        self.height = height
        self.padding = padding
        self.margin = margin
        self._bg = bg
        self._fg = fg
        self._kwargs = kwargs
        self._widget = None
        self._theme_callback = None
        
    @property
    def widget(self) -> Optional[tk.Widget]:
        return self._widget
    
    @property
    def bg(self) -> str:
        return self._bg
    
    @bg.setter
    def bg(self, value: str):
        self._bg = value
        if self._widget:
            self._widget.configure(bg=value)
            
    @property
    def fg(self) -> str:
        return self._fg
    
    @fg.setter
    def fg(self, value: str):
        self._fg = value
        if self._widget:
            self._apply_fg(value)
    
    def _apply_fg(self, value: str):
        pass
    
    def configure(self, **kwargs):
        if self._widget:
            self._widget.configure(**kwargs)
    
    def bind(self, sequence: str, func: Callable, add: bool = None):
        if self._widget:
            self._widget.bind(sequence, func, add)
    
    def unbind(self, sequence: str):
        if self._widget:
            self._widget.unbind(sequence)
    
    def destroy(self):
        if self._widget:
            self._widget.destroy()
            self._widget = None
    
    def on_theme_change(self, callback: Callable):
        self._theme_callback = callback
        
    def update_theme(self):
        if self._theme_callback:
            self._theme_callback()


class ContainerComponent(Component):
    def __init__(self, parent: tk.Widget, **kwargs):
        super().__init__(parent, **kwargs)
        
    def _create_container(self, widget_class, **widget_kwargs):
        common_opts = {}
        if self.width:
            common_opts["width"] = self.width
        if self.height:
            common_opts["height"] = self.height
            
        common_opts.update(widget_kwargs)
        return widget_class(self.parent, **common_opts)
    
    def pack(self, **kwargs):
        if self._widget:
            self._widget.pack(**kwargs)
    
    def grid(self, **kwargs):
        if self._widget:
            self._widget.grid(**kwargs)
    
    def place(self, **kwargs):
        if self._widget:
            self._widget.place(**kwargs)
