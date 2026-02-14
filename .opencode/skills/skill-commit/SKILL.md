---
name: skill-commit
description: Gestiona conventciones de commits, crea mensajes siguen estándares y facilita el proceso de commit
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: git
---

## What I do

- Generar mensajes de commit siguiendo convención Conventional Commits
- Verificar cambios antes de commit
- Proponer tipo de cambio (feat, fix, docs, refactor, etc.)
- Crear commit atómico con cambios relacionados

## When to use me

Usa esta skill cuando:
- Hayas completado una tarea o bugfix
- Quieras hacer un commit limpio y bien documentado
- Necesites ayuda para formular el mensaje

## Commit Convention

Formato: `<tipo>(<alcance>): <descripción>`

### Tipos de commit

| Tipo | Descripción |
|------|-------------|
| `feat` | Nueva funcionalidad |
| `fix` | Bugfix |
| `docs` | Documentación |
| `style` | Formato/código |
| `refactor` | Refactorización |
| `test` | Tests |
| `chore` | Mantenimiento |
| `perf` | Performance |
| `build` | Build/CI |

### Ejemplos

```
feat(core): agregar función para unir PDFs
fix(gui): corregir error en tema oscuro
docs(readme): actualizar lista de funcionalidades
refactor(utils): simplificar logger
```

## Commands disponibles

1. **Prepare commit**: Revisar cambios y sugerir tipo
2. **Generate message**: Crear mensaje de commit
3. **Commit now**: Ejecutar git commit
4. **Amend**: Enmendar último commit (solo si es tuyo y no hecho push)
