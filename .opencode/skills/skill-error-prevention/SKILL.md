---
name: skill-error-prevention
description: Error Prevention System - Analiza errores LSP/runtime y genera validadores, reglas y patrones para evitar problemas futuros en Python, PyQt6 y Orquestación
---

## What I do

- **Analiza errores**: Examina errores LSP, runtime y excepciones para identificar patrones
- **Genera validadores**: Crea código de validación para prevenir errores recurrentes
- **Define reglas**: Establece patrones de codificación seguros
- **Previene problemas**: Añade checks, type hints, null guards automáticamente

## When to use me

- Cuando errores LSP aparecen frecuentemente en el código
- Cuando hay problemas de runtime recurrentes
- Para prevenir errores en PyQt6 (signals, memory leaks, lifecycle)
- Para validar comunicación entre agentes del orquestador
- Después de debugging para codificar la solución

## Arquitectura

```
src/utils/error_prevention/
├── __init__.py              # Exports
├── validators.py            # Validadores runtime
├── rules.py                 # Reglas de validación
└── error_tracker.py         # Analizador de errores
```

## Errores Comunes y Prevenciones

### Python General

| Error | Prevención |
|-------|------------|
| `NameError` | Usar type hints completos |
| `TypeError` | Validar tipos con `isinstance()` |
| `AttributeError` | hasattr() o Optional con null check |
| `ImportError` | Imports absolutos, try/except en imports |
| `FileNotFoundError` | Path.exists() antes de usar |
| `KeyError` | .get() o defaultdict |

### PyQt6

| Error | Prevención |
|-------|------------|
| `RuntimeError: wrapped C/C++ object` | Validar objeto existe antes de usar |
| Signal loop | disconnect() en closeEvent |
| Memory leak | Usar parent-child correctamente |
| Null parent | Validar parent no es None |

### Orquestación

| Error | Prevención |
|-------|------------|
| Agent not found | Verificar `agent.is_registered` antes de enviar |
| Message routing fail | Check `response.success` |
| TypeError in handler | Validar payload con schema |
| Circular dependency | Usar inyección de dependencias |

## Validadores

### BaseValidator

```python
from abc import ABC, abstractmethod
from typing import Any, Optional
from dataclasses import dataclass

@dataclass
class ValidationResult:
    valid: bool
    errors: list[str]
    warnings: list[str]

class BaseValidator(ABC):
    @abstractmethod
    def validate(self, target: Any) -> ValidationResult:
        pass

    def validate_or_raise(self, target: Any) -> None:
        result = self.validate(target)
        if not result.valid:
            raise ValueError(f"Validation failed: {result.errors}")
```

### PythonValidator

```python
from src.utils.error_prevention.validators import PythonValidator

validator = PythonValidator()

# Validar función
result = validator.validate_function(my_function)
# ValidationResult(valid=True, errors=[], warnings=['Missing return type hint'])

# Validar clase
result = validator.validate_class(MyClass)
# ValidationResult(valid=False, errors=['Missing type hint on attribute'], warnings=[])
```

### PyQt6Validator

```python
from src.utils.error_prevention.validators import PyQt6Validator

validator = PyQt6Validator()

# Validar widget
result = validator.validate_widget(my_button)
# ValidationResult(valid=True, errors=[], warnings=['Signal not disconnected in closeEvent'])

# Validar signal connection
result = validator.validate_signal_connection(my_button.clicked, handler)
# ValidationResult(valid=False, errors=['Missing disconnect in closeEvent'], warnings=[])
```

### OrchestrationValidator

```python
from src.utils.error_prevention.validators import OrchestrationValidator

validator = OrchestrationValidator()

# Validar mensaje
result = validator.validate_message(message)
# ValidationResult(valid=True, errors=[], warnings=[])

# Validar agente
result = validator.validate_agent(ui_agent)
# ValidationResult(valid=False, errors=['Agent not registered'], warnings=[])
```

## Reglas de Validación

### Type Hint Rules

```python
from src.utils.error_prevention.rules import TypeHintRule

# Regla: Type hints obligatorios en funciones públicas
rule = TypeHintRule(require_for_public=True, require_return=True)

# Verificar función
errors = rule.check_function(my_function)
# ['Parameter "x" missing type hint', 'Missing return type hint']
```

### Null Safety Rules

```python
from src.utils.error_prevention.rules import NullSafetyRule

rule = NullSafetyRule()

# Verificar código
errors = rule.check_code("obj.attr.method()")
# ['Potential AttributeError: "obj" may be None - use obj.attr?.method() or if obj:']

# Recomendación: Usar Optional y null checks
```

### PyQt6 Lifecycle Rules

```python
from src.utils.error_prevention.rules import PyQt6LifecycleRule

rule = PyQt6LifecycleRule()

# Verificar clase de ventana
errors = rule.check_window_class(MyWindow)
# ['Missing closeEvent with signal disconnection', 'Missing parent parameter in super().__init__']
```

## Error Tracker

```python
from src.utils.error_prevention.error_tracker import ErrorTracker, track_error

tracker = ErrorTracker()

# Registrar error
@track_error(tracker)
def risky_operation():
    try:
        # operation
    except Exception as e:
        tracker.track_error(type(e).__name__, str(e), {"context": "value"})

# Obtener estadísticas
stats = tracker.get_statistics()
# {'TypeError': 5, 'AttributeError': 3, 'FileNotFoundError': 2}

# Generar validador desde errores
validator_code = tracker.generate_validator()
# str - Código Python con validaciones basadas en errores vistos
```

## Decoradores de Prevención

```python
from src.utils.error_prevention.validators import safe_call, require_agent, validate_params

@safe_call(default_return=None, log_errors=True)
def risky_pdf_operation(path):
    """Decorador que previene errores runtime."""
    return pdf_reader.read(path)

@require_agent(agent_type=AgentType.LOGIC)
def send_to_logic(message):
    """Decorador que verifica agente registrado."""
    return agent.send_to_orchestrator(message)

@validate_params({"path": Path, "output": (str, Path)})
def repair_pdf(path, output):
    """Decorador que valida tipos de parámetros."""
    ...
```

## Integración con Skills

El skill se integra con:

- **skill-generate**: Genera código de validación automáticamente
- **skill-qt6-window-engineering**: Añade validaciones de lifecycle
- **skill-commit**: Valida quefix commits incluyan validación

## Ejemplo: Prevención Completa

```python
from src.utils.error_prevention import (
    PythonValidator,
    PyQt6Validator, 
    OrchestrationValidator,
    ErrorTracker,
)

# 1. Inicializar tracker
tracker = ErrorTracker()

# 2. Registrar errores observados
@track_error(tracker)
def operation_that_fails():
    ...

# 3. Generar validador desde errores
validator_code = tracker.generate_validator()

# 4. Aplicar validadores antes de ejecutar
py_validator = PythonValidator()
pyqt_validator = PyQt6Validator()

result = py_validator.validate_function(my_func)
if not result.valid:
    print(f"Fix: {result.errors}")

# 5. Usar decoradores en funciones críticas
@safe_call(default_return={"error": "Operation failed"})
def critical_operation():
    ...
```
