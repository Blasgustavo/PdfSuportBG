"""
GUI Components - Módulo de componentes de interfaz gráfica.
Contiene paneles, widgets y botones reutilizables.
"""

# Importar desde panels (que tiene la implementación temporal)
from .panels import (
    Sidebar,
    RecentDocumentsWidget,
    StartPanel,
    NewPanel,
    RepairPanel,
    MergePanel,
    SplitPanel,
    SettingsPanel,
    NewDocumentPanel,
)

# DocumentCard es el mismo que RecentDocumentsWidget por ahora
DocumentCard = RecentDocumentsWidget

# Buttons (temporal - usar QPushButton estándar)
BaseButton = None
IconButton = None

__all__ = [
    # Panels
    'Sidebar',
    'RecentDocumentsWidget',
    'StartPanel',
    'NewPanel',
    'RepairPanel', 
    'MergePanel',
    'SplitPanel',
    'SettingsPanel',
    'NewDocumentPanel',
    # Widgets
    'DocumentCard',
    # Buttons
    'BaseButton',
    'IconButton',
]
