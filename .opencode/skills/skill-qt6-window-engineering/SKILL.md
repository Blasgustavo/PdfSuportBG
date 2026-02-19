---
name: skill-qt6-window-engineering
description: Qt6 Window Engineering - Arquitecturas avanzadas de ventanas PyQt6 con WindowManager, NavigationController, ViewModels y patrones profesionales
---

## What I do

Arquitecto de ventanas Qt6. Diseño e implemento arquitecturas complejas de ventanas en PyQt6:

- **WindowManager**: Singleton centralizado para navegación
- **NavigationController**: Controlador de flujo de ventanas
- **StackedNavigation**: Navegación con pila (adelante/atrás)
- **MultiWindow Orchestration**: Coordinación de múltiples ventanas
- **Signals-as-events**: Comunicación basada en señales
- **Controllers + ViewModels**: Separación de responsabilidades
- **Dependency Injection**: Inyección de dependencias
- **Ciclo de vida**: Evitar fugas de memoria y loops de señales
- **Animaciones**: Transiciones suaves entre ventanas

## When to use me

Usar cuando se necesite:
- Diseñar navegación entre ventanas
- Implementar WindowManager
- Crear flujos login → dashboard → módulos
- Manejar múltiples ventanas
- Depurar problemas de lifecycle
- Añadir animaciones/transiciones
- Estructurar código con MVC/MVVM

## Arquitectura de Ventanas

```
src/gui/pyqt6/
├── window_manager.py       # Gestor central de ventanas (singleton)
├── navigation_controller.py # Controlador de navegación
├── base_window.py         # Clase base para ventanas
├── views/                 # Vistas (UI)
│   ├── login_view.py
│   ├── dashboard_view.py
│   └── module_view.py
├── controllers/            # Controladores de lógica
│   ├── auth_controller.py
│   └── dashboard_controller.py
├── viewmodels/            # ViewModels (MVVM)
│   └── main_viewmodel.py
├── windows/               # Ventanas completas
│   ├── main_window.py
│   ├── editor_window.py
│   └── settings_window.py
├── transitions/           # Animaciones
│   └── window_transition.py
└── workers/              # Workers para operaciones async
```

## WindowManager (Core)

```python
from PyQt6.QtCore import QObject, pyqtSignal, QStack
from PyQt6.QtWidgets import QWidget, QStackedWidget
from typing import Optional, Dict, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
import logging

from src.utils.logger import logger


class WindowType(Enum):
    """Tipos de ventana."""
    MAIN = "main"
    EDITOR = "editor"
    SETTINGS = "settings"
    DIALOG = "dialog"
    SPLASH = "splash"


@dataclass
class WindowConfig:
    """Configuración de ventana."""
    window_type: WindowType
    widget: QWidget
    title: str = ""
    can_go_back: bool = True
    data: Dict[str, Any] = field(default_factory=dict)


class WindowManager(QObject):
    """Gestor centralizado de ventanas (Singleton)."""
    
    window_changed = pyqtSignal(str)
    window_opened = pyqtSignal(str, dict)
    window_closed = pyqtSignal(str)
    navigation_pushed = pyqtSignal(str)
    navigation_popped = pyqtSignal()
    
    _instance: Optional["WindowManager"] = None
    
    def __new__(cls) -> "WindowManager":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self) -> None:
        if self._initialized:
            return
        
        super().__init__()
        self._initialized = True
        
        self._windows: Dict[str, WindowConfig] = {}
        self._stack: QStack[str] = QStack()
        self._current_window: Optional[str] = None
        self._stacked_widget: Optional[QStackedWidget] = None
        self._main_window: Optional[QWidget] = None
        
        self._window_factory: Dict[WindowType, Callable] = {}
        
        log = logger.get_logger()
        log.info("WindowManager inicializado")
    
    def set_stacked_widget(self, stacked: QStackedWidget) -> None:
        """Configura el QStackedWidget para navegación."""
        self._stacked_widget = stacked
    
    def set_main_window(self, window: QWidget) -> None:
        """Configura la ventana principal."""
        self._main_window = window
    
    def register_window(self, name: str, config: WindowConfig) -> None:
        """Registra una ventana."""
        self._windows[name] = config
        log = logger.get_logger()
        log.debug(f"Ventana registrada: {name}")
    
    def register_factory(self, window_type: WindowType, factory: Callable) -> None:
        """Registra una fábrica de ventanas."""
        self._window_factory[window_type] = factory
    
    def show_window(self, name: str, data: Optional[Dict[str, Any]] = None) -> bool:
        """Muestra una ventana registrada."""
        if name not in self._windows:
            log = logger.get_logger()
            log.error(f"Ventana no encontrada: {name}")
            return False
        
        config = self._windows[name]
        
        if data:
            config.data.update(data)
        
        if self._stacked_widget:
            index = self._stacked_widget.addWidget(config.widget)
            self._stacked_widget.setCurrentIndex(index)
        
        self._current_window = name
        self._stack.push(name)
        
        config.widget.show()
        
        self.window_changed.emit(name)
        self.window_opened.emit(name, config.data)
        
        log = logger.get_logger()
        log.info(f"Ventana abierta: {name}")
        
        return True
    
    def close_window(self, name: Optional[str] = None) -> None:
        """Cierra una ventana."""
        target = name or self._current_window
        
        if not target or target not in self._windows:
            return
        
        config = self._windows[target]
        config.widget.hide()
        
        if self._stacked_widget and self._stacked_widget.indexOf(config.widget) >= 0:
            self._stacked_widget.removeWidget(config.widget)
        
        self._current_window = None
        self.window_closed.emit(target)
        
        log = logger.get_logger()
        log.info(f"Ventana cerrada: {target}")
    
    def go_back(self) -> bool:
        """Regresa a la ventana anterior."""
        if len(self._stack) <= 1:
            return False
        
        current = self._stack.pop()
        self.close_window(current)
        
        previous = self._stack[-1]
        self.show_window(previous)
        
        self.navigation_popped.emit()
        
        return True
    
    @property
    def current_window(self) -> Optional[str]:
        return self._current_window
    
    @property
    def has_windows(self) -> bool:
        return len(self._windows) > 0
    
    @property
    def stack_depth(self) -> int:
        return len(self._stack)


window_manager = WindowManager()
```

## NavigationController

```python
from PyQt6.QtCore import QObject, pyqtSignal
from typing import Optional, Callable, List, Any, Dict
from dataclasses import dataclass
from enum import Enum
import logging

from src.utils.logger import logger


class NavigationDirection(Enum):
    """Dirección de navegación."""
    FORWARD = "forward"
    BACKWARD = "backward"
    REPLACE = "replace"
    RESET = "reset"


@dataclass
class NavigationRoute:
    """Ruta de navegación."""
    name: str
    route: str
    component: str
    meta: Dict[str, Any]


class NavigationController(QObject):
    """Controlador de navegación entre pantallas."""
    
    navigate = pyqtSignal(str, dict)
    route_changed = pyqtSignal(str)
    
    def __init__(self, window_manager) -> None:
        super().__init__()
        self._window_manager = window_manager
        self._routes: Dict[str, NavigationRoute] = {}
        self._navigation_history: List[str] = []
        self._current_route: Optional[str] = None
    
    def add_route(self, route: NavigationRoute) -> None:
        """Añade una ruta."""
        self._routes[route.route] = route
        log = logger.get_logger()
        log.debug(f"Ruta registrada: {route.route}")
    
    def navigate_to(
        self,
        route: str,
        data: Optional[Dict[str, Any]] = None,
        direction: NavigationDirection = NavigationDirection.FORWARD
    ) -> bool:
        """Navega a una ruta."""
        if route not in self._routes:
            log = logger.get_logger()
            log.error(f"Ruta no encontrada: {route}")
            return False
        
        target_route = self._routes[route]
        
        if direction == NavigationDirection.RESET:
            self._navigation_history.clear()
        
        if direction in (NavigationDirection.FORWARD, NavigationDirection.REPLACE):
            self._navigation_history.append(route)
        
        self._current_route = route
        
        result = self._window_manager.show_window(
            target_route.name,
            data or target_route.meta
        )
        
        if result:
            self.route_changed.emit(route)
            self.navigate.emit(route, target_route.meta)
        
        return result
    
    def go_back(self) -> bool:
        """Regresa a la ruta anterior."""
        if len(self._navigation_history) <= 1:
            return False
        
        self._navigation_history.pop()
        
        previous = self._navigation_history[-1]
        return self.navigate_to(previous, direction=NavigationDirection.BACKWARD)
    
    def can_go_back(self) -> bool:
        """Verifica si puede regresar."""
        return len(self._navigation_history) > 1
    
    @property
    def current_route(self) -> Optional[str]:
        return self._current_route
    
    @property
    def history(self) -> List[str]:
        return self._navigation_history.copy()
```

## Base Window con ViewModel

```python
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import pyqtSignal, QObject, Qt
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import logging

from src.utils.logger import logger


class ViewModel(QObject):
    """ViewModel base."""
    
    data_changed = pyqtSignal(dict)
    loading_changed = pyqtSignal(bool)
    error_occurred = pyqtSignal(str)
    
    def __init__(self) -> None:
        super().__init__()
        self._data: Dict[str, Any] = {}
        self._loading = False
    
    @property
    def data(self) -> Dict[str, Any]:
        return self._data
    
    @property
    def is_loading(self) -> bool:
        return self._loading
    
    def set_loading(self, loading: bool) -> None:
        self._loading = loading
        self.loading_changed.emit(loading)
    
    def update_data(self, key: str, value: Any) -> None:
        self._data[key] = value
        self.data_changed.emit(self._data)
    
    def set_error(self, message: str) -> None:
        self.error_occurred.emit(message)


class BaseWindow(QWidget, ABC):
    """Clase base para ventanas con patrón MVVM."""
    
    closed = pyqtSignal()
    
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._viewmodel: Optional[ViewModel] = None
        self._setup_base_ui()
        self._connect_signals()
    
    def _setup_base_ui(self) -> None:
        """Configura UI base."""
        self.setWindowFlags(
            Qt.WindowType.Window |
            Qt.WindowType.WindowTitleHint |
            Qt.WindowType.WindowCloseButtonHint
        )
    
    def _connect_signals(self) -> None:
        """Conecta señales del ViewModel."""
        if self._viewmodel:
            self._viewmodel.data_changed.connect(self._on_data_changed)
            self._viewmodel.loading_changed.connect(self._on_loading_changed)
            self._viewmodel.error_occurred.connect(self._on_error)
    
    def set_viewmodel(self, viewmodel: ViewModel) -> None:
        """Configura el ViewModel."""
        self._viewmodel = viewmodel
        self._connect_signals()
    
    @abstractmethod
    def _on_data_changed(self, data: dict) -> None:
        """Maneja cambios de datos."""
        pass
    
    def _on_loading_changed(self, loading: bool) -> None:
        """Maneja cambio de estado de carga."""
        pass
    
    def _on_error(self, message: str) -> None:
        """Maneja errores."""
        log = logger.get_logger()
        log.error(f"Error en ventana: {message}")
    
    def closeEvent(self, event) -> None:
        """Maneja cierre de ventana."""
        self.closed.emit()
        super().closeEvent(event)
```

## MultiWindow Orchestration

```python
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QWidget, QDialog
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from enum import Enum
import logging

from src.utils.logger import logger


class WindowPriority(Enum):
    """Prioridad de ventana."""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    MODAL = 4


@dataclass
class WindowInfo:
    """Información de ventana."""
    id: str
    widget: QWidget
    priority: WindowPriority = WindowPriority.NORMAL
    is_modal: bool = False
    parent: Optional[str] = None


class MultiWindowOrchestrator(QObject):
    """Orquestador de múltiples ventanas."""
    
    window_registered = pyqtSignal(str)
    window_focused = pyqtSignal(str)
    all_windows_closed = pyqtSignal()
    
    def __init__(self) -> None:
        super().__init__()
        self._windows: Dict[str, WindowInfo] = {}
        self._focus_order: List[str] = []
        self._main_window_id: Optional[str] = None
    
    def register_window(
        self,
        window_id: str,
        widget: QWidget,
        priority: WindowPriority = WindowPriority.NORMAL,
        is_modal: bool = False,
        parent_id: Optional[str] = None
    ) -> None:
        """Registra una ventana."""
        info = WindowInfo(
            id=window_id,
            widget=widget,
            priority=priority,
            is_modal=is_modal,
            parent=parent_id
        )
        
        self._windows[window_id] = info
        self._focus_order.append(window_id)
        
        self.window_registered.emit(window_id)
        
        log = logger.get_logger()
        log.debug(f"Ventana registrada: {window_id}")
    
    def unregister_window(self, window_id: str) -> None:
        """Elimina una ventana."""
        if window_id in self._windows:
            del self._windows[window_id]
            if window_id in self._focus_order:
                self._focus_order.remove(window_id)
            
            log = logger.get_logger()
            log.debug(f"Ventana eliminada: {window_id}")
            
            if not self._windows:
                self.all_windows_closed.emit()
    
    def bring_to_front(self, window_id: str) -> None:
        """Trae una ventana al frente."""
        if window_id not in self._windows:
            return
        
        info = self._windows[window_id]
        
        if info.is_modal and info.parent:
            parent_info = self._windows.get(info.parent)
            if parent_info:
                info.widget.setWindowModality(Qt.WindowModality.WindowModal)
                info.widget.show()
                return
        
        info.widget.raise_()
        info.widget.activateWindow()
        
        if window_id in self._focus_order:
            self._focus_order.remove(window_id)
        self._focus_order.append(window_id)
        
        self.window_focused.emit(window_id)
    
    def close_all_windows(self, except_ids: Optional[List[str]] = None) -> None:
        """Cierra todas las ventanas."""
        exceptions = except_ids or []
        
        for window_id in list(self._windows.keys()):
            if window_id not in exceptions:
                self._windows[window_id].widget.close()
    
    def get_window(self, window_id: str) -> Optional[QWidget]:
        """Obtiene una ventana por ID."""
        info = self._windows.get(window_id)
        return info.widget if info else None
    
    @property
    def active_windows(self) -> List[str]:
        """Lista de ventanas activas."""
        return [
            wid for wid, info in self._windows.items()
            if info.widget.isVisible()
        ]
```

## Animaciones y Transiciones

```python
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QRect, QParallelAnimationGroup
from PyQt6.QtWidgets import QWidget
from typing import Optional


class WindowTransition:
    """Transiciones de ventanas."""
    
    @staticmethod
    def fade_in(widget: QWidget, duration: int = 300) -> QPropertyAnimation:
        """Animación de aparición con fundido."""
        widget.setWindowOpacity(0)
        
        animation = QPropertyAnimation(widget, b"windowOpacity")
        animation.setDuration(duration)
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        
        return animation
    
    @staticmethod
    def slide_in_from_right(widget: QWidget, parent: QWidget, duration: int = 300) -> QPropertyAnimation:
        """Animación de deslizamiento desde la derecha."""
        end_geometry = widget.geometry()
        start_geometry = QRect(
            parent.width(),
            end_geometry.y(),
            end_geometry.width(),
            end_geometry.height()
        )
        
        widget.setGeometry(start_geometry)
        
        animation = QPropertyAnimation(widget, b"geometry")
        animation.setDuration(duration)
        animation.setStartValue(start_geometry)
        animation.setEndValue(end_geometry)
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        return animation
    
    @staticmethod
    def scale_in(widget: QWidget, duration: int = 250) -> QParallelAnimationGroup:
        """Animación de escala."""
        widget.setWindowOpacity(0)
        widget.setScale(0.8)
        
        opacity = QPropertyAnimation(widget, b"windowOpacity")
        opacity.setDuration(duration)
        opacity.setStartValue(0.0)
        opacity.setEndValue(1.0)
        
        scale_anim = QPropertyAnimation(widget, b"scale")
        scale_anim.setDuration(duration)
        scale_anim.setStartValue(0.8)
        scale_anim.setEndValue(1.0)
        scale_anim.setEasingCurve(QEasingCurve.Type.OutBack)
        
        group = QParallelAnimationGroup()
        group.addAnimation(opacity)
        group.addAnimation(scale_anim)
        
        return group


class AnimatedWindowMixin:
    """Mixin para ventanas con animaciones."""
    
    def __init__(self) -> None:
        self._transition_enabled = True
    
    def show_with_animation(self, animation_type: str = "fade") -> None:
        """Muestra ventana con animación."""
        if not self._transition_enabled:
            self.show()
            return
        
        if animation_type == "fade":
            self.show()
            anim = WindowTransition.fade_in(self)
            anim.start()
        elif animation_type == "slide":
            parent = self.parent()
            if parent:
                self.show()
                anim = WindowTransition.slide_in_from_right(self, parent)
                anim.start()
        elif animation_type == "scale":
            self.show()
            anim = WindowTransition.scale_in(self)
            anim.start()
    
    def close_with_animation(self, animation_type: str = "fade") -> None:
        """Cierra ventana con animación."""
        if not self._transition_enabled:
            self.close()
            return
        
        animation = QPropertyAnimation(self, b"windowOpacity")
        animation.setDuration(200)
        animation.setStartValue(1.0)
        animation.setEndValue(0.0)
        animation.finished.connect(self.close)
        animation.start()
```

## Flujo Login → Dashboard → Módulos

```python
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QStackedWidget
)
from PyQt6.QtCore import pyqtSignal, Qt
from typing import Optional
import logging

from src.gui.pyqt6.window_manager import window_manager
from src.gui.pyqt6.base_window import BaseWindow, ViewModel
from src.utils.logger import logger


class LoginViewModel(ViewModel):
    """ViewModel para login."""
    
    login_successful = pyqtSignal(dict)
    
    def __init__(self) -> None:
        super().__init__()
        self.update_data("username", "")
        self.update_data("password", "")
    
    def login(self, username: str, password: str) -> bool:
        """Intenta iniciar sesión."""
        self.set_loading(True)
        
        try:
            # Simular autenticación
            if username and password:
                user_data = {
                    "username": username,
                    "role": "admin",
                    "token": "abc123"
                }
                self.update_data("user", user_data)
                self.login_successful.emit(user_data)
                self.set_loading(False)
                return True
            
            self.set_loading(False)
            self.set_error("Credenciales inválidas")
            return False
            
        except Exception as e:
            self.set_loading(False)
            self.set_error(str(e))
            return False


class LoginView(BaseWindow):
    """Vista de login."""
    
    login_success = pyqtSignal(dict)
    
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._viewmodel = LoginViewModel()
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        self.setWindowTitle("Xebec PDF Fixer - Login")
        self.setFixedSize(400, 300)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        
        title = QLabel("XEBEC PDF Fixer")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #1E3A5F;")
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Usuario")
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        self.login_button = QPushButton("Iniciar Sesión")
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #F6993F;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 6px;
                font-weight: 600;
            }
            QPushButton:hover { background-color: #F6AD55; }
        """)
        self.login_button.clicked.connect(self._on_login)
        
        layout.addWidget(title)
        layout.addSpacing(20)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addSpacing(20)
        layout.addWidget(self.login_button)
    
    def _on_login(self) -> None:
        username = self.username_input.text()
        password = self.password_input.text()
        
        if self._viewmodel.login(username, password):
            self.login_success.emit(self._viewmodel.data.get("user", {}))
    
    def _on_data_changed(self, data: dict) -> None:
        pass


class DashboardWindow(BaseWindow):
    """Ventana de dashboard principal."""
    
    def __init__(self, user_data: dict, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._user_data = user_data
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        self.setWindowTitle("Xebec PDF Fixer - Dashboard")
        self.setMinimumSize(800, 600)
        
        layout = QVBoxLayout(self)
        
        header = QLabel(f"Bienvenido, {self._user_data.get('username', 'Usuario')}")
        header.setStyleSheet("font-size: 20px; font-weight: bold; padding: 20px;")
        
        btn_pdf = QPushButton("Operaciones PDF")
        btn_pdf.clicked.connect(lambda: window_manager.show_editor("pdf"))
        
        btn_settings = QPushButton("Configuración")
        
        layout.addWidget(header)
        layout.addWidget(btn_pdf)
        layout.addWidget(btn_settings)
    
    def _on_data_changed(self, data: dict) -> None:
        pass


class AuthController(QObject):
    """Controlador de autenticación."""
    
    auth_changed = pyqtSignal(bool, dict)
    
    def __init__(self) -> None:
        super().__init__()
        self._current_user: Optional[dict] = None
    
    def login(self, username: str, password: str) -> bool:
        """Procesa login."""
        # Lógica de autenticación
        if username and password:
            self._current_user = {
                "username": username,
                "role": "admin"
            }
            self.auth_changed.emit(True, self._current_user)
            return True
        return False
    
    def logout(self) -> None:
        """Cierra sesión."""
        self._current_user = None
        self.auth_changed.emit(False, {})
    
    @property
    def is_authenticated(self) -> bool:
        return self._current_user is not None
    
    @property
    def current_user(self) -> Optional[dict]:
        return self._current_user
```

## Diagrama de Flujo de Ventanas

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           APPLICATION FLOW                              │
└─────────────────────────────────────────────────────────────────────────┘

    ┌──────────┐
    │  SPLASH  │ ──────► ┌──────────┐
    │  SCREEN  │          │   LOGIN  │
    └──────────┘          └────┬─────┘
                               │
                    ┌──────────┴──────────┐
                    │   AUTH SUCCESS     │
                    └──────────┬──────────┘
                               │
                               ▼
    ┌─────────────────────────────────────────────────────────────┐
    │                      DASHBOARD                              │
    │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐       │
    │  │   PDF   │  │  TOOLS  │  │  BATCH  │  │  CONFIG │       │
    │  │   Ops   │  │         │  │         │  │         │       │
    │  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘       │
    └───────┼────────────┼────────────┼────────────┼──────────────┘
            │            │            │            │
            ▼            ▼            ▼            ▼
    ┌─────────────────────────────────────────────────────────────┐
    │                     EDITOR WINDOW                           │
    │  ┌──────────────────────────────────────────────────────┐ │
    │  │  Toolbar │              Canvas                     │ │
    │  │          │                                          │ │
    │  │  Tools   │         Document Preview                 │ │
    │  │          │                                          │ │
    │  └──────────┴──────────────────────────────────────────┘ │
    └─────────────────────────────────────────────────────────────┘

    WINDOW MANAGER (Singleton)
    ┌────────────────────────────────────────────────────────────┐
    │  stack: [splash, login, dashboard, editor]                │
    │  current: "editor"                                        │
    │  windows: {login, dashboard, editor, settings}            │
    └────────────────────────────────────────────────────────────┘

    NAVIGATION: show_editor() ──► go_back() ──► close_editor()
```

## Manejo de Lifecycle

```python
from PyQt6.QtCore import QObject, QTimer
from typing import Optional, Set
import logging
from gc import collect


class WindowLifecycleManager(QObject):
    """Gestor de ciclo de vida de ventanas."""
    
    def __init__(self) -> None:
        super().__init__()
        self._tracked_windows: Set[int] = set()
        self._cleanup_timer = QTimer()
        self._cleanup_timer.timeout.connect(self._cleanup_windows)
        self._cleanup_timer.start(60000)  # Cada minuto
    
    def track_window(self, window: QWidget) -> None:
        """Registra una ventana para seguimiento."""
        window_id = id(window)
        self._tracked_windows.add(window_id)
        
        window.destroyed.connect(lambda: self._untrack_window(window_id))
        
        log = logger.get_logger()
        log.debug(f"Ventana registrada para lifecycle: {window_id}")
    
    def _untrack_window(self, window_id: int) -> None:
        """Elimina ventana del seguimiento."""
        self._tracked_windows.discard(window_id)
        
        log = logger.get_logger()
        log.debug(f"Ventana eliminada del lifecycle: {window_id}")
    
    def _cleanup_windows(self) -> None:
        """Limpia recursos de ventanas cerradas."""
        collected = collect()
        
        log = logger.get_logger()
        if collected > 0:
            log.debug(f"Garbage collector: {collected} objetos liberados")
    
    def force_cleanup(self) -> None:
        """Fuerza limpieza inmediata."""
        collect()
        self._cleanup_windows()


class SignalLoopPrevention:
    """Previene loops de señales."""
    
    def __init__(self) -> None:
        self._signals_blocked: Set[str] = set()
    
    def block_signal(self, signal_id: str) -> None:
        """Bloquea una señal temporalmente."""
        self._signals_blocked.add(signal_id)
    
    def unblock_signal(self, signal_id: str) -> None:
        """Desbloquea una señal."""
        self._signals_blocked.discard(signal_id)
    
    def is_blocked(self, signal_id: str) -> bool:
        """Verifica si una señal está bloqueada."""
        return signal_id in self._signals_blocked
```

## Buenas Prácticas Qt6

1. **Singletons**: Usar para WindowManager y ThemeManager
2. **Señales**: Preferir signals sobre callbacks
3. **Parents**: Siempre asignar parent correcto
4. **Cleanup**: Cerrar conexiones en closeEvent
5. **Threading**: Operaciones largas en QThread
6. **Memory**: Usar parent-child para auto-limpieza
7. **UI Logic**: Separar UI de lógica (MVVM)
8. **Error Handling**: Try/except en operaciones críticas
9. **Logging**: Registrar acciones importantes
10. **Testing**: Probar transiciones de ventana

## Variantes Arquitectónicas

### Variante 1: QML/QtQuick

```python
# Para aplicaciones con QtQml
from PyQt6.QtQml import QQmlApplicationEngine

class QmlWindowManager:
    """WindowManager para QML."""
    
    def __init__(self) -> None:
        self._engine = QQmlApplicationEngine()
    
    def load_view(self, qml_file: str) -> None:
        self._engine.load(qml_file)
```

### Variante 2: C++/Qt6

```cpp
// Para rendimiento máximo
class WindowManager : public QObject {
    Q_OBJECT
    
public:
    static WindowManager& instance();
    void showWindow(const QString& name);
    void goBack();
    
signals:
    void windowChanged(const QString& name);
    
private:
    QStack<QString> m_stack;
    QMap<QString, QWidget*> m_windows;
};
```

### Variante 3: Plugin-based

```python
class PluginWindowManager(WindowManager):
    """WindowManager con soporte de plugins."""
    
    def register_plugin(self, plugin) -> None:
        self._plugins[plugin.name] = plugin
        plugin.register_windows(self)
```
