from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from functools import wraps
from typing import Any, Callable, Optional
import logging


log = logging.getLogger(__name__)


@dataclass
class ErrorRecord:
    error_type: str
    message: str
    timestamp: datetime = field(default_factory=datetime.now)
    context: dict[str, Any] = field(default_factory=dict)
    count: int = 1


class ErrorTracker:
    def __init__(self, name: str = "default"):
        self.name = name
        self._errors: dict[str, list[ErrorRecord]] = defaultdict(list)
        self._error_counts: dict[str, int] = defaultdict(int)

    def track_error(
        self,
        error_type: str,
        message: str,
        context: Optional[dict[str, Any]] = None,
    ) -> None:
        record = ErrorRecord(
            error_type=error_type,
            message=message,
            context=context or {},
        )

        key = f"{error_type}:{message[:50]}"
        self._errors[key].append(record)
        self._error_counts[error_type] += 1

        log.debug(f"Tracked error: {error_type} - {message}")

    def get_errors(self, error_type: Optional[str] = None) -> list[ErrorRecord]:
        if error_type:
            result = []
            for key, records in self._errors.items():
                if key.startswith(error_type):
                    result.extend(records)
            return result

        result = []
        for records in self._errors.values():
            result.extend(records)
        return sorted(result, key=lambda r: r.timestamp, reverse=True)

    def get_statistics(self) -> dict[str, int]:
        return dict(self._error_counts)

    def get_top_errors(self, limit: int = 10) -> list[tuple[str, int]]:
        sorted_errors = sorted(
            self._error_counts.items(),
            key=lambda x: x[1],
            reverse=True,
        )
        return sorted_errors[:limit]

    def generate_validator(self) -> str:
        lines = [
            "# Auto-generated validator from error tracking",
            "# Generated: " + datetime.now().isoformat(),
            "",
            "from typing import Any, Optional",
            "from src.utils.error_prevention.validators import safe_call",
            "",
            "",
        ]

        type_hint_errors = [
            et for et in self._error_counts.keys()
            if "TypeError" in et or "NameError" in et
        ]
        if type_hint_errors:
            lines.append("# Type hint validations")
            for et in type_hint_errors[:3]:
                lines.append(f"# {et}: {self._error_counts[et]} occurrences")
            lines.append("")

        attribute_errors = [
            et for et in self._error_counts.keys()
            if "AttributeError" in et
        ]
        if attribute_errors:
            lines.append("# Null safety validations")
            for et in attribute_errors[:3]:
                lines.append(f"# {et}: {self._error_counts[et]} occurrences")
            lines.append("@safe_call(default_return=None, log_errors=True)")
            lines.append("def safe_attribute_access(obj: Any, attr: str) -> Any:")
            lines.append('    """Safe attribute access with null check."""')
            lines.append("    if obj is None:")
            lines.append("        return None")
            lines.append("    return getattr(obj, attr, None)")
            lines.append("")

        file_errors = [
            et for et in self._error_counts.keys()
            if "FileNotFoundError" in et or "NotFoundError" in et
        ]
        if file_errors:
            lines.append("# File/path validations")
            for et in file_errors[:3]:
                lines.append(f"# {et}: {self._error_counts[et]} occurrences")
            lines.append("from pathlib import Path")
            lines.append("")
            lines.append("def validate_path(path: str | Path) -> bool:")
            lines.append('    """Validate that path exists."""')
            lines.append("    return Path(path).exists()")
            lines.append("")

        return "\n".join(lines)

    def clear(self) -> None:
        self._errors.clear()
        self._error_counts.clear()

    def export_report(self) -> str:
        lines = [
            f"Error Tracker Report - {self.name}",
            "=" * 40,
            f"Generated: {datetime.now().isoformat()}",
            "",
            "Top Errors:",
        ]

        for error_type, count in self.get_top_errors():
            lines.append(f"  {error_type}: {count}")

        lines.append("")
        lines.append("Recent Errors:")
        for record in self.get_errors()[:10]:
            lines.append(
                f"  [{record.timestamp.isoformat()}] {record.error_type}: "
                f"{record.message[:60]}..."
            )

        return "\n".join(lines)


_global_tracker: Optional[ErrorTracker] = None


def get_tracker(name: str = "default") -> ErrorTracker:
    global _global_tracker
    if _global_tracker is None:
        _global_tracker = ErrorTracker(name)
    return _global_tracker


def track_error(tracker: Optional[ErrorTracker] = None) -> Callable:
    _tracker = tracker or get_tracker()

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                _tracker.track_error(
                    type(e).__name__,
                    str(e),
                    {"function": func.__name__, "args": str(args)[:100]},
                )
                raise
        return wrapper
    return decorator
