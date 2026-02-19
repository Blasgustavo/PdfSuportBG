"""
GUI Components - Panels
Contiene los paneles de la interfaz.
"""

# Importar desde archivos separados
from .sidebar import Sidebar, SidebarButton

# RecentDocumentsWidget está en document_card.py
try:
    from .document_card import RecentDocumentsWidget
except ImportError:
    from .components_temp import RecentDocumentsWidget

# Importar paneles restantes desde temporal
try:
    from .components_temp import (
        StartPanel,
        NewPanel,
        RepairPanel,
        MergePanel,
        SplitPanel,
        SettingsPanel,
        NewDocumentPanel,
    )
except ImportError:
    pass

__all__ = [
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
]
