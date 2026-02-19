from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Any, Optional
from uuid import UUID, uuid4


class MessageType(Enum):
    REQUEST = auto()
    RESPONSE = auto()
    EVENT = auto()
    ERROR = auto()


class AgentType(Enum):
    ORCHESTRATOR = auto()
    UI = auto()
    LOGIC = auto()


@dataclass
class Message:
    msg_type: MessageType
    sender: AgentType
    receiver: AgentType
    action: str
    payload: dict[str, Any] = field(default_factory=dict)
    correlation_id: UUID = field(default_factory=uuid4)
    timestamp: datetime = field(default_factory=datetime.now)
    reply_to: Optional[UUID] = None

    def __str__(self) -> str:
        return f"[{self.msg_type.name}] {self.sender.name} -> {self.receiver.name}: {self.action}"


@dataclass
class MessageResponse:
    success: bool
    data: Optional[dict[str, Any]] = None
    error: Optional[str] = None
    correlation_id: UUID = field(default_factory=uuid4)
    timestamp: datetime = field(default_factory=datetime.now)


class Action:
    UI_SHOW_WINDOW = "ui:show_window"
    UI_HIDE_WINDOW = "ui:hide_window"
    UI_UPDATE_THEME = "ui:update_theme"
    UI_SHOW_DIALOG = "ui:show_dialog"
    UI_SHOW_NOTIFICATION = "ui:show_notification"

    LOGIC_REPAIR_PDF = "logic:repair_pdf"
    LOGIC_VALIDATE_PDF = "logic:validate_pdf"
    LOGIC_LOAD_FILE = "logic:load_file"
    LOGIC_SAVE_FILE = "logic:save_file"

    ORCH_REGISTER_AGENT = "orch:register_agent"
    ORCH_UNREGISTER_AGENT = "orch:unregister_agent"
    ORCH_GET_STATUS = "orch:get_status"
