from inspect import signature, isclass, isfunction
from typing import Any, Callable, Optional


class TypeHintRule:
    def __init__(
        self,
        require_for_public: bool = True,
        require_return: bool = True,
    ):
        self.require_for_public = require_for_public
        self.require_return = require_return

    def check_function(self, func: Callable) -> list[str]:
        errors: list[str] = []

        if not callable(func):
            return ["Not a callable"]

        try:
            hints = func.__annotations__
        except AttributeError:
            return ["No annotations available"]

        sig = signature(func)

        for param_name, param in sig.parameters.items():
            if param_name in ("self", "cls"):
                continue

            if self.require_for_public and not param_name.startswith("_"):
                if param_name not in hints:
                    errors.append(
                        f'Parameter "{param_name}" missing type hint'
                    )

        if self.require_return and "return" not in hints:
            errors.append("Missing return type hint")

        return errors


class NullSafetyRule:
    def __init__(self):
        self._dangerous_patterns = [
            ".",
            "[",
        ]

    def check_code(self, code: str) -> list[str]:
        warnings: list[str] = []

        if not code:
            return warnings

        tokens = code.split()
        for i, token in enumerate(tokens):
            if any(p in token for p in self._dangerous_patterns):
                if i > 0 and tokens[i - 1] in ("None", "null", "nothing"):
                    warnings.append(
                        f'Potential AttributeError: "{tokens[i-1]}" may be None'
                    )

        return warnings

    def check_attribute_access(self, obj_name: str, attr_name: str) -> list[str]:
        warnings: list[str] = []

        warnings.append(
            f'Potential AttributeError: check if "{obj_name}" is not None before accessing "{attr_name}"'
        )

        return warnings


class PyQt6LifecycleRule:
    def __init__(self):
        self._required_methods = ["closeEvent"]
        self._recommended_methods = ["showEvent"]

    def check_window_class(self, cls: type) -> list[str]:
        errors: list[str] = []
        warnings: list[str] = []

        if not isclass(cls):
            return ["Not a class"]

        methods = [m for m in dir(cls) if callable(getattr(cls, m, None))]

        for method in self._required_methods:
            if method not in methods:
                errors.append(f"Missing required method: {method}")

        for method in self._recommended_methods:
            if method not in methods:
                warnings.append(f"Missing recommended method: {method}")

        init = getattr(cls, "__init__", None)
        if init:
            sig = signature(init)
            params = list(sig.parameters.keys())
            if "parent" not in params:
                warnings.append('Missing "parent" parameter in __init__')

        return errors + warnings

    def check_signal_connection(
        self,
        signal_name: str,
        handler_name: Optional[str] = None,
    ) -> list[str]:
        warnings: list[str] = []

        warnings.append(
            f'Signal "{signal_name}" should be disconnected in closeEvent to prevent memory leaks'
        )

        if handler_name:
            warnings.append(
                f'Handler "{handler_name}" should be disconnected in closeEvent'
            )

        return warnings


class ImportRule:
    def __init__(self):
        self._allowed_modules = [
            "PyQt6",
            "pypdf",
            "PIL",
            "pathlib",
            "typing",
        ]

    def check_import(self, module_name: str) -> list[str]:
        errors: list[str] = []

        if module_name.startswith("."):
            errors.append(
                f'Use absolute imports instead of relative: "{module_name}"'
            )

        return errors


class PathRule:
    def __init__(self):
        pass

    def check_path_usage(self, func: Callable) -> list[str]:
        errors: list[str] = []
        warnings: list[str] = []

        if not callable(func):
            return ["Not callable"]

        try:
            hints = func.__annotations__
        except AttributeError:
            return ["No annotations"]

        sig = signature(func)

        for param_name, param in sig.parameters.items():
            if "path" in param_name.lower() or "file" in param_name.lower():
                if param_name not in hints:
                    warnings.append(
                        f'Parameter "{param_name}" suggests file/path - add type hint'
                    )
                elif hints.get(param_name) not in (str, Any):
                    pass

        return errors + warnings
