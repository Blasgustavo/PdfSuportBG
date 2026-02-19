from abc import ABC, abstractmethod
from typing import Any, Callable, Optional

from src.orchestration.messages import (
    Action,
    AgentType,
    Message,
    MessageResponse,
    MessageType,
)


class BaseAgent(ABC):
    def __init__(self, agent_type: AgentType, orchestrator: Optional["Orchestrator"] = None):
        self.agent_type = agent_type
        self.orchestrator = orchestrator
        self._handlers: dict[str, Callable[[Message], MessageResponse]] = {}
        self._is_registered = False
        self._register_handlers()

    @abstractmethod
    def _register_handlers(self) -> None:
        pass

    @abstractmethod
    def handle(self, message: Message) -> MessageResponse:
        pass

    def send_to_orchestrator(
        self,
        action: str,
        payload: Optional[dict[str, Any]] = None,
    ) -> MessageResponse:
        if self.orchestrator is None:
            return MessageResponse(
                success=False,
                error="Orchestrator not set",
            )
        message = Message(
            msg_type=MessageType.REQUEST,
            sender=self.agent_type,
            receiver=AgentType.ORCHESTRATOR,
            action=action,
            payload=payload or {},
        )
        return self.orchestrator.route_message(message)

    def request_to_agent(
        self,
        receiver: AgentType,
        action: str,
        payload: Optional[dict[str, Any]] = None,
    ) -> MessageResponse:
        if self.orchestrator is None:
            return MessageResponse(
                success=False,
                error="Orchestrator not set",
            )
        message = Message(
            msg_type=MessageType.REQUEST,
            sender=self.agent_type,
            receiver=receiver,
            action=action,
            payload=payload or {},
        )
        return self.orchestrator.route_message(message)

    def emit_event(
        self,
        action: str,
        payload: Optional[dict[str, Any]] = None,
    ) -> None:
        if self.orchestrator is None:
            return
        message = Message(
            msg_type=MessageType.EVENT,
            sender=self.agent_type,
            receiver=AgentType.ORCHESTRATOR,
            action=action,
            payload=payload or {},
        )
        self.orchestrator.broadcast_event(message)

    def register(self) -> None:
        if self.orchestrator and not self._is_registered:
            self.orchestrator.register_agent(self)
            self._is_registered = True

    def unregister(self) -> None:
        if self.orchestrator and self._is_registered:
            self.orchestrator.unregister_agent(self.agent_type)
            self._is_registered = False

    @property
    def is_registered(self) -> bool:
        return self._is_registered
