"""
Qt6WindowEngineering Skill

This skill provides advanced window management capabilities for Qt6 applications.
It helps design, optimize, and debug complex window navigation systems.

Usage:
    This skill is invoked when working with:
    - WindowManager implementation
    - Multi-window applications
    - Navigation patterns
    - Window lifecycle management
    - PyQt6/C++ Qt6 development
"""

SKILL_NAME = "Qt6WindowEngineering"
SKILL_DESCRIPTION = "Ingeniero senior especializado en arquitectura de ventanas Qt6 (PyQt6 y C++/Qt6)"
SKILL_VERSION = "1.0.0"

# Skill capabilities
CAPABILITIES = [
    "Crear arquitecturas de navegación: WindowManager, NavigationController, StackedNavigation, MultiWindow Orchestration",
    "Implementar patrones modernos: Signals-as-events, Dependency Injection, Controllers, ViewModels",
    "Diseñar flujos avanzados: login → dashboard → módulos → subventanas",
    "Manejar memoria y lifecycle: evitar ventanas huérfanas, cierres incorrectos, loops de señales, fugas",
    "Integrar animaciones, transiciones y efectos modernos de Qt6",
    "Generar código completo en PyQt6 o C++/Qt6",
]

# Example patterns provided by this skill
EXAMPLE_PATTERNS = {
    "window_manager": {
        "description": "Singleton pattern for centralized window management",
        "file": "src/gui/pyqt6/window_manager.py",
    },
    "signals": {
        "description": "PyQt6 signals for window communication",
        "pattern": "pyqtSignal, pyqtSlot",
    },
    "lifecycle": {
        "description": "Proper window lifecycle management",
        "methods": ["show()", "hide()", "close()", "deleteLater()"],
    },
}


def get_skill_info():
    """Return skill information dictionary."""
    return {
        "name": SKILL_NAME,
        "description": SKILL_DESCRIPTION,
        "version": SKILL_VERSION,
        "capabilities": CAPABILITIES,
        "examples": EXAMPLE_PATTERNS,
    }
