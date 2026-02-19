from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from functools import wraps
from inspect import signature, isclass
from typing import Any, Callable, Optional, Type, Union, get_type_hints
import logging

from src.utils.error_prevention.rules import (
    TypeHintRule,
    NullSafetyRule,
    PyQt6LifecycleRule,
)

log = logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def __bool__(self) -> bool:
        return self.valid


class BaseValidator(ABC):
    @abstractmethod
    def validate(self, target: Any) -> ValidationResult:
        pass

    def validate_or_raise(self, target: Any) -> None:
        result = self.validate(target)
        if not result.valid:
            raise ValueError(f"Validation failed: {result.errors}")


class PythonValidator(BaseValidator):
    def __init__(
        self,
        require_type_hints: bool = True,
        require_return_hint: bool = True,
    ):
        self._type_rule = TypeHintRule(
            require_for_public=require_type_hints,
            require_return=require_return_hint,
        )
        self._null_rule = NullSafetyRule()

    def validate_function(self, func: Callable) -> ValidationResult:
        errors: list[str] = []
        warnings: list[str] = []

        if not callable(func):
            return ValidationResult(False, [f"Expected callable, got {type(func)}"])

        errors.extend(self._type_rule.check_function(func))

        try:
            hints = get_type_hints(func)
        except Exception as e:
            warnings.append(f"Could not get type hints: {e}")

        return ValidationResult(len(errors) == 0, errors, warnings)

    def validate_class(self, cls: type) -> ValidationResult:
        errors: list[str] = []
        warnings: list[str] = []

        if not isclass(cls):
            return ValidationResult(False, [f"Expected class, got {type(cls)}"])

        for name, attr in vars(cls).items():
            if callable(attr) and not name.startswith("_"):
                errors.extend(self._type_rule.check_function(attr))

        return ValidationResult(len(errors) == 0, errors, warnings)

    def validate(self, target: Any) -> ValidationResult:
        if callable(target):
            if isclass(target):
                return self.validate_class(target)
            return self.validate_function(target)
        return ValidationResult(False, [f"Cannot validate {type(target)}"])


class PyQt6Validator(BaseValidator):
    def __init__(self):
        self._lifecycle_rule = PyQt6LifecycleRule()

    def validate_widget(self, widget: Any) -> ValidationResult:
        errors: list[str] = []
        warnings: list[str] = []

        try:
            from PyQt6.QtWidgets import QWidget
            if not isinstance(widget, QWidget):
                warnings.append("Not a QWidget")
        except ImportError:
            errors.append("PyQt6 not installed")

        return ValidationResult(len(errors) == 0, errors, warnings)

    def validate_window_class(self, window_cls: type) -> ValidationResult:
        errors: list[str] = []
        warnings: list[str] = []

        errors.extend(self._lifecycle_rule.check_window_class(window_cls))

        return ValidationResult(len(errors) == 0, errors, warnings)

    def validate_signal_connection(
        self,
        signal: Any,
        handler: Callable,
    ) -> ValidationResult:
        errors: list[str] = []
        warnings: list[str] = []

        try:
            from PyQt6.QtCore import pyqtBoundSignal
            if not isinstance(signal, pyqtBoundSignal):
                warnings.append("Not a PyQt6 signal")
        except ImportError:
            errors.append("PyQt6 not installed")

        if not callable(handler):
            errors.append("Handler is not callable")

        return ValidationResult(len(errors) == 0, errors, warnings)

    def validate(self, target: Any) -> ValidationResult:
        if isclass(target):
            return self.validate_window_class(target)
        return self.validate_widget(target)


class OrchestrationValidator(BaseValidator):
    def validate_message(self, message: Any) -> ValidationResult:
        errors: list[str] = []
        warnings: list[str] = []

        required_attrs = ["msg_type", "sender", "receiver", "action"]
        for attr in required_attrs:
            if not hasattr(message, attr):
                errors.append(f"Message missing attribute: {attr}")

        return ValidationResult(len(errors) == 0, errors, warnings)

    def validate_agent(self, agent: Any) -> ValidationResult:
        errors: list[str] = []
        warnings: list[str] = []

        if not hasattr(agent, "agent_type"):
            errors.append("Missing agent_type attribute")

        if not hasattr(agent, "is_registered"):
            errors.append("Missing is_registered property")

        if hasattr(agent, "is_registered") and not agent.is_registered:
            warnings.append("Agent not registered - messages may fail")

        if hasattr(agent, "orchestrator") and agent.orchestrator is None:
            warnings.append("Orchestrator not set")

        return ValidationResult(len(errors) == 0, errors, warnings)

    def validate_response(self, response: Any) -> ValidationResult:
        errors: list[str] = []
        warnings: list[str] = []

        if not hasattr(response, "success"):
            errors.append("Response missing 'success' attribute")
            return ValidationResult(False, errors, warnings)

        if not response.success and not hasattr(response, "error"):
            warnings.append("Failed response without error message")

        return ValidationResult(True, errors, warnings)

    def validate(self, target: Any) -> ValidationResult:
        target_type = type(target).__name__

        if "Message" in target_type:
            return self.validate_message(target)
        elif "Agent" in target_type:
            return self.validate_agent(target)
        elif "Response" in target_type:
            return self.validate_response(target)

        return ValidationResult(False, [f"Unknown target type: {target_type}"])


def safe_call(
    default_return: Any = None,
    log_errors: bool = True,
    reraise: bool = False,
) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if log_errors:
                    log.error(f"Error in {func.__name__}: {e}")
                if reraise:
                    raise
                return default_return
        return wrapper
    return decorator


def require_agent(agent_type: Optional[Any] = None) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if not hasattr(self, "agent"):
                if log:
                    log.warning(f"{func.__name__}: self.agent not found")
                return {"success": False, "error": "Agent not available"}

            if not self.agent.is_registered:
                if log:
                    log.warning(f"{func.__name__}: Agent not registered")
                return {"success": False, "error": "Agent not registered"}

            return func(self, *args, **kwargs)
        return wrapper
    return decorator


def validate_params(**param_types: Any) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            sig = signature(func)
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()

            for param_name, expected_type in param_types.items():
                if param_name in bound.arguments:
                    value = bound.arguments[param_name]
                    if value is None:
                        continue

                    if isinstance(expected_type, tuple):
                        if not isinstance(value, expected_type):
                            raise TypeError(
                                f"{param_name}: expected {expected_type}, got {type(value)}"
                            )
                    else:
                        if not isinstance(value, expected_type):
                            raise TypeError(
                                f"{param_name}: expected {expected_type}, got {type(value)}"
                            )

            return func(*args, **kwargs)
        return wrapper
    return decorator
