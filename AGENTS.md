# Xebec PDF Fixer - Project Agents

## Project Overview

**Xebec PDF Fixer** - Aplicación de escritorio para administrar PDFs en Windows.

## Technology Stack

- Python 3.8+
- Tkinter (GUI)
- pypdf (procesamiento PDF)
- PyInstaller (build .exe)

## Project Structure

```
PdfSuport/
├── src/
│   ├── main.py              # Entry point
│   ├── core/                # Lógica de negocio PDF
│   ├── gui/                 # Interfaz gráfica
│   ├── utils/               # Utilidades
│   └── skills/              # Plugins
├── .opencode/               # Configuración OpenCode
│   ├── agents/              # Agentes especializados
│   │   ├── orchestrator/
│   │   ├── pdf-engineer/
│   │   ├── gui-developer/
│   │   └── docs-writer/
│   └── skills/              # Skills por dominio
│       ├── dev/             # Desarrollo
│       ├── devops/          # DevOps (git, sync)
│       └── docs/            # Documentación
├── tests/                   # Tests unitarios
├── assets/                  # Recursos estáticos
└── README.md                # Documentación
```

## Coding Patterns

### Python Modules
- Usar type hints completos
- Métodos estáticos para utilities
- Logging con `src.utils.logger`
- Retornar `Tuple[bool, Optional[str]]` para resultados

### GUI (Tkinter)
- Tema oscuro por defecto
- Usar threading para operaciones largas
- Barra de progreso obligatoria
- Manejo de errores con messagebox

### Commits
- Conventional Commits: `<tipo>(<alcance>): <descripción>`
- Tipos: feat, fix, docs, refactor, test, chore

## Available Agents

| Agent | Purpose |
|-------|---------|
| orchestrator | Coordina desarrollo |
| pdf-engineer | Funcionalidades PDF |
| gui-developer | Interfaz gráfica |
| docs-writer | Documentación |

## Available Skills

### DevOps
| Skill | Purpose |
|-------|---------|
| skill-sinc | Sincronización y estado del repo |
| skill-commit | Convenciones de commits |

### Docs
| Skill | Purpose |
|-------|---------|
| skill-doc | Documentación y README |

### Dev
| Skill | Purpose |
|-------|---------|
| skill-generate | Generación de código y scaffolds |
