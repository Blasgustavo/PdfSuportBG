from pathlib import Path
from typing import Any, Optional

from src.core.pdf_repair import PDFRepairer
from src.orchestration.agents.base_agent import BaseAgent
from src.orchestration.messages import (
    Action,
    AgentType,
    Message,
    MessageResponse,
    MessageType,
)


class LogicAgent(BaseAgent):
    def __init__(
        self,
        orchestrator: Optional["Orchestrator"] = None,
        pdf_repairer: Optional[PDFRepairer] = None,
    ):
        super().__init__(AgentType.LOGIC, orchestrator)
        self._pdf_repairer = pdf_repairer or PDFRepairer()

    def _register_handlers(self) -> None:
        self._handlers = {
            Action.LOGIC_REPAIR_PDF: self._handle_repair_pdf,
            Action.LOGIC_VALIDATE_PDF: self._handle_validate_pdf,
            Action.LOGIC_LOAD_FILE: self._handle_load_file,
            Action.LOGIC_SAVE_FILE: self._handle_save_file,
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

    def _handle_repair_pdf(self, message: Message) -> MessageResponse:
        input_path = message.payload.get("input_path")
        output_path = message.payload.get("output_path")
        if not input_path:
            return MessageResponse(
                success=False,
                error="input_path is required",
                correlation_id=message.correlation_id,
            )
        try:
            input_path = Path(input_path)
            output_path = Path(output_path) if output_path else input_path.with_suffix(".fixed.pdf")
            success, error = self._pdf_repairer.repair(input_path, output_path)
            if success:
                return MessageResponse(
                    success=True,
                    data={
                        "repaired": True,
                        "output_path": str(output_path),
                    },
                    correlation_id=message.correlation_id,
                )
            return MessageResponse(
                success=False,
                error=error or "Repair failed",
                correlation_id=message.correlation_id,
            )
        except Exception as e:
            return MessageResponse(
                success=False,
                error=str(e),
                correlation_id=message.correlation_id,
            )

    def _handle_validate_pdf(self, message: Message) -> MessageResponse:
        file_path = message.payload.get("file_path")
        if not file_path:
            return MessageResponse(
                success=False,
                error="file_path is required",
                correlation_id=message.correlation_id,
            )
        try:
            from pypdf import PdfReader
            path = Path(file_path)
            if not path.exists():
                return MessageResponse(
                    success=False,
                    error="File does not exist",
                    correlation_id=message.correlation_id,
                )
            reader = PdfReader(str(path))
            page_count = len(reader.pages)
            is_encrypted = reader.is_encrypted
            return MessageResponse(
                success=True,
                data={
                    "valid": True,
                    "page_count": page_count,
                    "is_encrypted": is_encrypted,
                    "file_size": path.stat().st_size,
                },
                correlation_id=message.correlation_id,
            )
        except Exception as e:
            return MessageResponse(
                success=False,
                error=str(e),
                correlation_id=message.correlation_id,
            )

    def _handle_load_file(self, message: Message) -> MessageResponse:
        file_path = message.payload.get("file_path")
        if not file_path:
            return MessageResponse(
                success=False,
                error="file_path is required",
                correlation_id=message.correlation_id,
            )
        try:
            path = Path(file_path)
            if not path.exists():
                return MessageResponse(
                    success=False,
                    error="File does not exist",
                    correlation_id=message.correlation_id,
                )
            return MessageResponse(
                success=True,
                data={
                    "loaded": True,
                    "file_name": path.name,
                    "file_size": path.stat().st_size,
                    "file_path": str(path),
                },
                correlation_id=message.correlation_id,
            )
        except Exception as e:
            return MessageResponse(
                success=False,
                error=str(e),
                correlation_id=message.correlation_id,
            )

    def _handle_save_file(self, message: Message) -> MessageResponse:
        file_path = message.payload.get("file_path")
        content = message.payload.get("content")
        if not file_path:
            return MessageResponse(
                success=False,
                error="file_path is required",
                correlation_id=message.correlation_id,
            )
        try:
            path = Path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            if content:
                path.write_bytes(content)
            else:
                path.touch()
            return MessageResponse(
                success=True,
                data={
                    "saved": True,
                    "file_path": str(path),
                },
                correlation_id=message.correlation_id,
            )
        except Exception as e:
            return MessageResponse(
                success=False,
                error=str(e),
                correlation_id=message.correlation_id,
            )

    def set_pdf_repairer(self, pdf_repairer: PDFRepairer) -> None:
        self._pdf_repairer = pdf_repairer
