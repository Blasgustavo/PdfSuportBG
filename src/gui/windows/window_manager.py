from typing import Optional, Dict, Any, Callable
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QApplication


class WindowManager(QObject):
    """
    WindowManager - Gestor centralizado de ventanas para Qt6.
    
    Implementa el patrón Singleton para mantener una única instancia
    que gestione todas las transiciones de ventanas de la aplicación.
    
    Señales:
        window_changed(str): Emite el tipo de ventana actual
        window_opened(str, dict): Emite cuando se abre una ventana
        window_closed(str): Emite cuando se cierra una ventana
    
    Uso:
        from src.gui.windows.window_manager import window_manager
        
        window_manager.show_main()
        window_manager.show_editor(document_type="blank")
        window_manager.go_back()
    """
    
    _instance: Optional['WindowManager'] = None
    
    window_changed = pyqtSignal(str)
    window_opened = pyqtSignal(str, dict)
    window_closed = pyqtSignal(str)
    
    def __new__(cls) -> 'WindowManager':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init()
        return cls._instance
    
    def _init(self) -> None:
        """Inicializa el WindowManager."""
        super().__init__()
        self._window_stack: list[Dict[str, Any]] = []
        self._current_window: Optional[Any] = None
        self._editor_window: Optional[Any] = None
        self._main_window: Optional[Any] = None
        self._app: Optional[QApplication] = None
    
    def set_app(self, app: QApplication) -> None:
        """Establece la referencia a la aplicación Qt."""
        self._app = app
    
    @property
    def current_window_type(self) -> str:
        """Retorna el tipo de ventana actual."""
        if self._editor_window is not None and self._editor_window.isVisible():
            return "editor"
        if self._main_window is not None and self._main_window.isVisible():
            return "main"
        return "none"
    
    @property
    def has_editor_open(self) -> bool:
        """Verifica si hay un editor abierto."""
        return self._editor_window is not None and self._editor_window.isVisible()
    
    @property
    def has_unsaved_changes(self) -> bool:
        """Verifica si hay cambios sin guardar en el editor."""
        if self._editor_window is not None:
            if hasattr(self._editor_window, 'editor'):
                return self._editor_window.editor._has_unsaved_changes
            if hasattr(self._editor_window, '_has_unsaved_changes'):
                return self._editor_window._has_unsaved_changes
        return False
    
    def show_splash(self, duration_ms: int = 2000) -> None:
        """
        Muestra la pantalla de splash.
        
        Args:
            duration_ms: Duración en milisegundos
        """
        from PyQt6.QtCore import QTimer
        from src.gui.screens.splash_screen import SplashScreen
        from src.gui.windows.main_window import MainWindow
        from src.gui.themes.theme_manager import theme_manager
        
        splash = SplashScreen()
        splash.show()
        
        if self._app:
            self._app.processEvents()
        
        # Crear la ventana principal en background (ya se oculta sola)
        self._main_window = MainWindow()
        
        def finish_splash():
            splash.finish(self._main_window)
            self._main_window.showMaximized()
            self.window_changed.emit("main")
            self.window_opened.emit("main", {})
        
        # Iniciar simulación de carga
        splash.simulate_loading(finish_splash)
    
    def show_main(self, **kwargs) -> None:
        """
        Muestra la ventana principal.
        
        Args:
            **kwargs: Argumentos adicionales para MainWindow
        """
        from src.gui.windows.main_window import MainWindow
        from src.gui.themes.theme_manager import theme_manager
        
        if self._main_window is not None:
            if hasattr(self._main_window, 'close'):
                self._main_window.close()
        
        self._main_window = MainWindow(**kwargs)
        self._main_window.showMaximized()
        theme_manager.emit_change()
        
        self.window_changed.emit("main")
        self.window_opened.emit("main", kwargs)
    
    def show_editor(self, document_type: str = "blank", **kwargs) -> None:
        """
        Muestra la ventana del editor.
        
        Args:
            document_type: Tipo de documento ("blank", "suggestion", "recent")
            **kwargs: Argumentos adicionales para EditorWindowContainer
        """
        from src.gui.windows.editor_window import EditorWindowContainer
        from src.gui.themes.theme_manager import theme_manager
        
        if self._main_window and self._main_window.isVisible():
            self._main_window.hide()
        
        self._editor_window = EditorWindowContainer(
            document_type=document_type,
            parent=self._main_window
        )
        self._editor_window.close_requested.connect(self._on_editor_close_requested)
        self._editor_window.showMaximized()
        
        theme_manager.emit_change()
        
        self.window_changed.emit("editor")
        self.window_opened.emit("editor", {"document_type": document_type, **kwargs})
    
    def _on_editor_close_requested(self) -> None:
        """Maneja el evento de cierre del editor."""
        self.close_editor()
    
    def close_editor(self, create_new_main: bool = True) -> None:
        """
        Cierra el editor y vuelve a la ventana principal.
        
        Args:
            create_new_main: Si True, crea una nueva instancia de MainWindow
        """
        if self._editor_window is not None:
            self._editor_window.close()
            self._editor_window.deleteLater()
            self._editor_window = None
            
            self.window_closed.emit("editor")
        
        if create_new_main:
            self.show_main()
        elif self._main_window:
            self._main_window.showMaximized()
            self.window_changed.emit("main")
    
    def navigate_to(self, window_type: str, **kwargs) -> None:
        """
        Navega a una ventana específica.
        
        Args:
            window_type: Tipo de ventana ("main", "editor", "splash")
            **kwargs: Argumentos para la ventana
        """
        if window_type == "main":
            self.show_main(**kwargs)
        elif window_type == "editor":
            self.show_editor(**kwargs)
        elif window_type == "splash":
            self.show_splash(**kwargs)
    
    def go_back(self) -> None:
        """Regresa a la ventana anterior en el stack."""
        if self._window_stack:
            previous = self._window_stack.pop()
            window_type = previous.get("type")
            window_data = previous.get("data", {})
            
            if window_type == "main":
                self.show_main(**window_data)
    
    def push_window(self, window_type: str, **data) -> None:
        """
        Guarda la ventana actual en el stack antes de navegar.
        
        Args:
            window_type: Tipo de ventana actual
            **data: Datos de la ventana actual
        """
        self._window_stack.append({
            "type": window_type,
            "data": data
        })
    
    def clear_stack(self) -> None:
        """Limpia el historial de navegación."""
        self._window_stack.clear()
    
    def close_all(self) -> None:
        """Cierra todas las ventanas y termina la aplicación."""
        if self._editor_window:
            self._editor_window.close()
            self._editor_window = None
        
        if self._main_window:
            self._main_window.close()
            self._main_window = None
        
        if self._app:
            self._app.quit()
    
    def confirm_close(self, has_unsaved_changes: bool = False) -> bool:
        """
        Muestra diálogo de confirmación de cierre.
        
        Args:
            has_unsaved_changes: Si hay cambios sin guardar
            
        Returns:
            True si el usuario confirma el cierre
        """
        if not has_unsaved_changes:
            return True
        
        from PyQt6.QtWidgets import QMessageBox
        
        if self._current_window is None:
            parent = self._editor_window if self._editor_window else self._main_window
        else:
            parent = self._current_window
        
        reply = QMessageBox.question(
            parent,
            "Cambios sin guardar",
            "¿Desea cerrar sin guardar los cambios?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        return reply == QMessageBox.StandardButton.Yes


window_manager = WindowManager()
