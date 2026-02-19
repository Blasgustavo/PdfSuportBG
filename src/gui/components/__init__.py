"""
GUI Components - Módulo de componentes de interfaz gráfica.
Contiene paneles, widgets y botones reutilizables.
"""

# Panels - importar desde panels
from .panels import (
    Sidebar,
    SidebarButton,
    RecentDocumentsWidget,
    StartPanel,
    NewPanel,
    RepairPanel,
    MergePanel,
    SplitPanel,
    SettingsPanel,
    NewDocumentPanel,
)

# Alias para compatibilidad
DocumentCard = RecentDocumentsWidget

# Buttons (temporal - usar QPushButton estándar)
BaseButton = None
IconButton = None

__all__ = [
    # Panels
    'Sidebar',
    'SidebarButton',
    'RecentDocumentsWidget',
    'StartPanel',
    'NewPanel',
    'RepairPanel', 
    'MergePanel',
    'SplitPanel',
    'SettingsPanel',
    'NewDocumentPanel',
    # Alias
    'DocumentCard',
    # Buttons
    'BaseButton',
    'IconButton',
]
