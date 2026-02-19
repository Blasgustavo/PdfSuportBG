---
name: skill-xebec-commit
description: XEBEC Commit Convention v1 - Convenciones corporativas para mensajes de commit con íconos semánticos, estructura consistente y estándares profesionales
---

## What I do

- Valido y genero mensajes de commit siguiendo el estándar XEBEC CORPORATION
- Utilizo íconos semánticos para identificar rápidamente el tipo de cambio
- Mantengo compatibilidad con Conventional Commits y herramientas de CI/CD
- Proporciono retroalimentación para mejorar los mensajes de commit

## When to use me

- Usar después de cada cambio de código para asegurar mensajes consistentes
- Cuando se necesita generar un mensaje de commit desde cero
- Para validar y mejorar mensajes de commit existentes

## Estructura del Commit

```
<icono> <tipo>(<área opcional>): <descripción breve>

[detalle opcional del cambio]

Refs: <tickets, issues, tareas>
```

## Íconos y Tipos Permitidos

| Ícono | Tipo | Descripción |
|-------|------|-------------|
| ✨ | feat | Nueva funcionalidad |
| 🐛 | fix | Corrección de errores |
| 📦 | build | Cambios en build, dependencias, empaquetado |
| 🧹 | chore | Tareas menores, limpieza, mantenimiento |
| 📝 | docs | Documentación |
| 🎨 | style | Formato, estilos, QSS, UI sin lógica |
| 🔧 | config | Configuración, settings, environment |
| 🚀 | perf | Mejoras de rendimiento |
| 🧪 | test | Pruebas unitarias o integraciones |
| ♻️ | refactor | Reestructuración sin cambiar comportamiento |
| 🔒 | security | Parches de seguridad |
| 🎬 | anim | Animaciones Qt6, transiciones, efectos |
| 🖼 | ui | Cambios visuales, layouts, dashboards |
| 🧩 | plugin | Cambios en plugins de PdfSuport |
| 📄 | pdf | Cambios en el motor PDF (PdfSuport) |
| 🛠 | cli | Cambios en herramientas CLI corporativas |
| 🎨 | vscode | Cambios en configuraciones VSCode |

## Reglas Corporativas

1. **Descripción breve**: Máximo 60 caracteres
2. **Atomicidad**: Un propósito, un cambio
3. **Detalles**: Explicar el "qué" y el "por qué"
4. **Refs**: Vincular tareas internas con `Refs: #123`
5. **Prohibido**: "update", "fixes", "changes", "stuff"

## Ejemplos

### Correctos
```
✨ feat(ui): agregar sidebar corporativa estilo Word

Adds XEBEC sidebar con navegación de módulos
y branding corporativo integrado

Refs: TASK-123
```

```
🎬 anim(dashboard): animación fade-in para panel principal

Transición suave con QPropertyAnimation
Duration: 300ms, QEasingCurve.InOutQuad
```

```
📄 pdf(core): mejorar extracción de metadatos en PdfSuport

Ahora extrae author, creator, producer fields
Usa pypdf para mejor compatibilidad
```

```
🧩 plugin(ocr): agregar plugin OCR con Tesseract

Plugin dinámico con discovery automático
Soporte para múltiples idiomas
```

```
🛠 cli: agregar menú interactivo para instalador

Usa click para CLI con autocompletado
Soporta modo silent para CI/CD
```

### Incorrectos
```
❌ update // Too generic
❌ fix things // No specifics  
❌ changes // What changes?
❌ asdflkj // Meaningless
❌ Fix bug #123 // Missing icon
```

## Validación

```python
def validate_commit(message: str) -> tuple[bool, list[str]]:
    """Valida mensaje de commit XEBEC."""
    errors = []
    
    # Check icon
    valid_prefixes = ['✨', '🐛', '📦', '🧹', '📝', '🎨', '🔧', '🚀', '🧪', '♻️', '🔒', '🎬', '🖼', '🧩', '📄', '🛠']
    if not any(message.startswith(p) for p in valid_prefixes):
        errors.append("Missing valid icon prefix")
    
    # Check format: <icon> <type>(<scope>): <desc>
    import re
    pattern = r'^[🎨✨🐛📦🧹📝🔧🚀🧪♻️🔒🎬🖼🧩📄🛠]\s+\w+(\(\w+\))?:'
    if not re.match(pattern, message):
        errors.append("Format: <icon> <type>(<area>): <description>")
    
    # Check description length
    desc = message.split('\n')[0]
    if len(desc) > 60:
        errors.append("Description max 60 characters")
    
    return len(errors) == 0, errors
```

## Áreas Opcionales

Para proyectos específicos:

### Qt6/PyQt6
- `ui`, `window`, `theme`, `anim`, `component`, `signal`

### PdfSuport
- `pdf`, `repair`, `merge`, `split`, `extract`, `plugin`

### CLI
- `cli`, `menu`, `installer`, `config`

### VSCode
- `vscode`, `settings`, `task`, `debug`, `extension`

## Formato de Respuesta

Al validar un commit:

1. **Explicación**: Tipo de commit y su propósito
2. **Ejemplo**: Commit correcto basado en los cambios
3. **Sugerencias**: Mejoras si no cumple el estándar

## Ejemplo de Uso

```
User: "commit para agregar botón de cerrar"

Validation:
- ❌ Falta ícono
- ❌ Falta tipo (feat/fix/style)

Suggested:
✨ feat(ui): agregar botón de cerrar en ventana principal

Refs
```
: TASK-456