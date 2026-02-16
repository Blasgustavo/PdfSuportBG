---
name: generate
description: Genera código, scaffolds, plantillas y estructura para nuevas funcionalidades del proyecto
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: development
---

## What I do

- Generar estructura de carpetas según el proyecto
- Crear archivos Python con templates predefinidos
- Generar código base para nuevas funcionalidades PDF
- Crear tests unitarios básicos
- Generar configuración para nuevos módulos

## When to use me

Usa esta skill cuando:
- Necesites agregar una nueva funcionalidad PDF (unir, dividir, etc.)
- Quieras crear un nuevo módulo en src/core/
- Necesites generar tests para código existente
- Quieras crear un nuevo componente de UI

## Project Structure Reference

```
src/
├── main.py              # Entry point
├── core/                # Business logic
│   ├── pdf_repair.py    # ✅ Existe
│   ├── pdf_merge.py     # ⚠️ Por crear
│   ├── pdf_split.py     # ⚠️ Por crear
│   └── pdf_delete.py    # ⚠️ Por crear
├── gui/                 # Interface
├── utils/               # Utilities
└── skills/              # Plugins
```

## Commands disponibles

1. **Generate core module**: Crear nuevo módulo en src/core/
2. **Generate gui component**: Crear componente de UI
3. **Generate test**: Crear test unitario
4. **Generate skill**: Crear nueva skill/plugin

## Templates

Para nuevos módulos PDF usar:
- Clase con métodos estáticos
- Tipado con Type hints
- Manejo de excepciones
- Logging integrado
