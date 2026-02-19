from typing import Any, Callable, Optional, cast

from src.orchestration.agents.base_agent import BaseAgent
from src.orchestration.agents.logic_agent import LogicAgent
from src.orchestration.agents.ui_agent import UIAgent
from src.orchestration.messages import (
    Action,
    AgentType,
    Message,
    MessageResponse,
    MessageType,
)


class Orchestrator:
    _instance: Optional["Orchestrator"] = None

    def __new__(cls) -> "Orchestrator":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._agents: dict[AgentType, BaseAgent] = {}
        self._event_listeners: dict[str, list[Callable[[Message], None]]] = {}
        self._initialized = True

    def register_agent(self, agent: BaseAgent) -> MessageResponse:
        if agent.agent_type in self._agents:
            return MessageResponse(
                success=False,
                error=f"Agent {agent.agent_type.name} already registered",
            )
        agent.orchestrator = self
        self._agents[agent.agent_type] = agent
        return MessageResponse(success=True, data={"registered": agent.agent_type.name})

    def unregister_agent(self, agent_type: AgentType) -> MessageResponse:
        if agent_type in self._agents:
            agent = self._agents.pop(agent_type)
            agent.orchestrator = None
            return MessageResponse(success=True, data={"unregistered": agent_type.name})
        return MessageResponse(
            success=False,
            error=f"Agent {agent_type.name} not found",
        )

    def get_agent(self, agent_type: AgentType) -> Optional[BaseAgent]:
        return self._agents.get(agent_type)

    @property
    def ui_agent(self) -> Optional[UIAgent]:
        return cast(Optional[UIAgent], self._agents.get(AgentType.UI))

    @property
    def logic_agent(self) -> Optional[LogicAgent]:
        return cast(Optional[LogicAgent], self._agents.get(AgentType.LOGIC))

    def route_message(self, message: Message) -> MessageResponse:
        if message.receiver == AgentType.ORCHESTRATOR:
            return self._handle_orchestrator_message(message)
        target_agent = self._agents.get(message.receiver)
        if target_agent is None:
            return MessageResponse(
                success=False,
                error=f"Agent {message.receiver.name} not found",
                correlation_id=message.correlation_id,
            )
        return target_agent.handle(message)

    def broadcast_event(self, message: Message) -> None:
        listeners = self._event_listeners.get(message.action, [])
        for listener in listeners:
            try:
                listener(message)
            except Exception:
                pass

    def add_event_listener(self, action: str, callback: Callable[[Message], None]) -> None:
        if action not in self._event_listeners:
            self._event_listeners[action] = []
        self._event_listeners[action].append(callback)

    def remove_event_listener(self, action: str, callback: Callable[[Message], None]) -> None:
        if action in self._event_listeners:
            self._event_listeners[action].remove(callback)

    def _handle_orchestrator_message(self, message: Message) -> MessageResponse:
        action_prefix = message.action.split(":")[0] if ":" in message.action else None
        
        if action_prefix:
            prefix_to_agent = {
                "ui": AgentType.UI,
                "logic": AgentType.LOGIC,
            }
            target_agent_type = prefix_to_agent.get(action_prefix)
            if target_agent_type and target_agent_type in self._agents:
                return self.route_message(Message(
                    msg_type=message.msg_type,
                    sender=message.sender,
                    receiver=target_agent_type,
                    action=message.action,
                    payload=message.payload,
                    correlation_id=message.correlation_id,
                ))

        if message.action == Action.ORCH_REGISTER_AGENT:
            agent_type = message.payload.get("agent_type")
            if agent_type:
                try:
                    agent_type_enum = AgentType[agent_type.upper()]
                    return MessageResponse(
                        success=False,
                        error="Use agent.register() instead",
                        correlation_id=message.correlation_id,
                    )
                except KeyError:
                    return MessageResponse(
                        success=False,
                        error=f"Invalid agent type: {agent_type}",
                        correlation_id=message.correlation_id,
                    )
        elif message.action == Action.ORCH_GET_STATUS:
            return MessageResponse(
                success=True,
                data={
                    "agents": [a.name for a in self._agents.keys()],
                    "event_listeners": list(self._event_listeners.keys()),
                },
                correlation_id=message.correlation_id,
            )
        return MessageResponse(
            success=False,
            error=f"Unknown orchestrator action: {message.action}",
            correlation_id=message.correlation_id,
        )

    def request(
        self,
        sender: AgentType,
        receiver: AgentType,
        action: str,
        payload: Optional[dict[str, Any]] = None,
    ) -> MessageResponse:
        message = Message(
            msg_type=MessageType.REQUEST,
            sender=sender,
            receiver=receiver,
            action=action,
            payload=payload or {},
        )
        return self.route_message(message)

    def send_response(
        self,
        original_message: Message,
        response: MessageResponse,
    ) -> None:
        pass

    def get_status(self) -> dict[str, Any]:
        return {
            "agents": {k.name: v.is_registered for k, v in self._agents.items()},
            "event_listeners": list(self._event_listeners.keys()),
        }


orchestrator = Orchestrator()
