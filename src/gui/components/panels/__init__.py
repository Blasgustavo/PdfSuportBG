"""
GUI Components - Panels
Contiene los paneles de la interfaz.
"""

from .sidebar import Sidebar, SidebarButton
from .document_card import RecentDocumentsWidget
from .start_panel import StartPanel
from .new_panel import NewPanel
from .repair_panel import RepairPanel
from .merge_panel import MergePanel
from .split_panel import SplitPanel
from .settings_panel import SettingsPanel
from .new_document_panel import NewDocumentPanel
from .account_panel import AccountPanel

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
    'AccountPanel',
]
