from typing import Any, Optional

from src.orchestration.agents.base_agent import BaseAgent
from src.orchestration.messages import (
    Action,
    AgentType,
    Message,
    MessageResponse,
    MessageType,
)


class UIAgent(BaseAgent):
    def __init__(
        self,
        orchestrator: Optional["Orchestrator"] = None,
        theme_manager=None,
        window_manager=None,
    ):
        super().__init__(AgentType.UI, orchestrator)
        self._theme_manager = theme_manager
        self._window_manager = window_manager

    def _register_handlers(self) -> None:
        self._handlers = {
            Action.UI_SHOW_WINDOW: self._handle_show_window,
            Action.UI_HIDE_WINDOW: self._handle_hide_window,
            Action.UI_UPDATE_THEME: self._handle_update_theme,
            Action.UI_SHOW_DIALOG: self._handle_show_dialog,
            Action.UI_SHOW_NOTIFICATION: self._handle_show_notification,
        }

    def handle(self, message: Message) -> MessageResponse:
        handler = self._handlers.get(message.action)
        if handler:
            return handler(message)
        return MessageResponse(
            success=False,
            error=f"Unknown action: {message.action}",
            correlation_id=message.correlation_id,
        )

    def _handle_show_window(self, message: Message) -> MessageResponse:
        window_type = message.payload.get("window_type", "main")
        try:
            if self._window_manager:
                if window_type == "main":
                    self._window_manager.show_main()
                elif window_type == "editor":
                    doc_type = message.payload.get("document_type", "blank")
                    self._window_manager.show_editor(document_type=doc_type)
                return MessageResponse(success=True, data={"window": window_type})
            return MessageResponse(
                success=False,
                error="Window manager not configured",
                correlation_id=message.correlation_id,
            )
        except Exception as e:
            return MessageResponse(
                success=False,
                error=str(e),
                correlation_id=message.correlation_id,
            )

    def _handle_hide_window(self, message: Message) -> MessageResponse:
        window_type = message.payload.get("window_type", "main")
        try:
            if self._window_manager:
                if window_type == "editor":
                    self._window_manager.close_editor()
                return MessageResponse(success=True, data={"hidden": window_type})
            return MessageResponse(
                success=False,
                error="Window manager not configured",
                correlation_id=message.correlation_id,
            )
        except Exception as e:
            return MessageResponse(
                success=False,
                error=str(e),
                correlation_id=message.correlation_id,
            )

    def _handle_update_theme(self, message: Message) -> MessageResponse:
        theme_name = message.payload.get("theme", "dark")
        try:
            if self._theme_manager:
                self._theme_manager.set_theme(theme_name)
                return MessageResponse(
                    success=True,
                    data={"theme": theme_name},
                    correlation_id=message.correlation_id,
                )
            return MessageResponse(
                success=False,
                error="Theme manager not configured",
                correlation_id=message.correlation_id,
            )
        except Exception as e:
            return MessageResponse(
                success=False,
                error=str(e),
                correlation_id=message.correlation_id,
            )

    def _handle_show_dialog(self, message: Message) -> MessageResponse:
        dialog_type = message.payload.get("dialog_type")
        title = message.payload.get("title", "")
        message_text = message.payload.get("message", "")
        try:
            from PyQt6.QtWidgets import QMessageBox
            from src.gui.pyqt6.window_manager import window_manager

            parent = window_manager.get_active_window()
            msg_box = QMessageBox(parent)
            msg_box.setWindowTitle(title)
            msg_box.setText(message_text)

            if dialog_type == "info":
                msg_box.setIcon(QMessageBox.Icon.Information)
            elif dialog_type == "warning":
                msg_box.setIcon(QMessageBox.Icon.Warning)
            elif dialog_type == "error":
                msg_box.setIcon(QMessageBox.Icon.Critical)
            elif dialog_type == "question":
                msg_box.setIcon(QMessageBox.Icon.Question)
                msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

            result = msg_box.exec()
            return MessageResponse(
                success=True,
                data={"result": result},
                correlation_id=message.correlation_id,
            )
        except Exception as e:
            return MessageResponse(
                success=False,
                error=str(e),
                correlation_id=message.correlation_id,
            )

    def _handle_show_notification(self, message: Message) -> MessageResponse:
        notification_type = message.payload.get("type", "info")
        title = message.payload.get("title", "")
        message_text = message.payload.get("message", "")
        duration = message.payload.get("duration", 3000)
        try:
            if self._window_manager:
                self._window_manager.show_notification(
                    title=title,
                    message=message_text,
                    notification_type=notification_type,
                    duration=duration,
                )
                return MessageResponse(
                    success=True,
                    data={"shown": True},
                    correlation_id=message.correlation_id,
                )
            return MessageResponse(
                success=False,
                error="Window manager not configured",
                correlation_id=message.correlation_id,
            )
        except Exception as e:
            return MessageResponse(
                success=False,
                error=str(e),
                correlation_id=message.correlation_id,
            )

    def set_theme_manager(self, theme_manager) -> None:
        self._theme_manager = theme_manager

    def set_window_manager(self, window_manager) -> None:
        self._window_manager = window_manager
