"""
Legacy import file - panels have been moved to individual files.
This file exists for backward compatibility.
"""

from src.gui.components.panels.sidebar import Sidebar, SidebarButton
from src.gui.components.panels.document_card import RecentDocumentsWidget
from src.gui.components.panels.start_panel import StartPanel
from src.gui.components.panels.new_panel import NewPanel
from src.gui.components.panels.repair_panel import RepairPanel
from src.gui.components.panels.merge_panel import MergePanel
from src.gui.components.panels.split_panel import SplitPanel
from src.gui.components.panels.settings_panel import SettingsPanel
from src.gui.components.panels.new_document_panel import NewDocumentPanel

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
