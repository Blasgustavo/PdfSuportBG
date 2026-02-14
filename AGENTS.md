# Xebec Pdf - Project Agents

## Project Overview

**Xebec Pdf** - Aplicación de escritorio profesional para administrar PDFs en Windows con interfaz moderna inspirada en Microsoft Office.

## Technology Stack

- Python 3.8+
- Tkinter (GUI) con tema personalizado
- pypdf (procesamiento PDF)
- PyInstaller (build .exe)
- JetBrains Mono (fuente principal)

## Project Structure

```
PdfSuport/
├── src/
│   ├── main.py                    # Entry point
│   ├── core/                      # Lógica de negocio PDF
│   │   └── pdf_repair.py          # Reparar PDFs
│   ├── gui/                       # Interfaz gráfica
│   │   ├── main_window.py         # Ventana principal
│   │   ├── splash_screen.py       # Splash screen
│   │   ├── components/            # Componentes UI modulares
│   │   │   ├── sidebar.py         # Panel lateral
│   │   │   ├── header_templates.py # Header y plantillas
│   │   │   ├── recent_table.py    # Tabla de recientes
│   │   │   ├── start_panel.py     # Panel de inicio
│   │   │   ├── widgets.py         # Botones, inputs, etc.
│   │   │   ├── window_controls.py # Controles de ventana
│   │   │   └── theme_manager.py   # Gestor de temas
│   │   └── themes/                # Temas (One Dark Pro)
│   └── utils/                     # Utilidades
│       ├── logger.py              # Logging
│       └── font_manager.py        # Gestor de fuentes
├── .opencode/                     # Configuración OpenCode
│   ├── agents/                    # Agentes especializados
│   │   ├── orchestrator/
│   │   ├── pdf-engineer/
│   │   ├── gui-developer/
│   │   └── docs-writer/
│   └── skills/                    # Skills por dominio
│       ├── dev/                   # Desarrollo
│       ├── devops/                # DevOps (git, sync)
│       ├── docs/                  # Documentación
│       └── design/                # Diseño UI/UX
├── assets/                        # Recursos estáticos
│   ├── icons/                     # Iconos
│   ├── fonts/                     # Fuentes
│   └── design/                    # Mockups
└── README.md                      # Documentación
```

## Coding Patterns

### Python Modules
- Usar type hints completos
- Métodos estáticos para utilities
- Logging con `src.utils.logger`
- Retornar `Tuple[bool, Optional[str]]` para resultados

### GUI (Tkinter)
- **Tema oscuro One Dark Pro** por defecto
- Sistema de componentes UI modular
- Soporte para cambio dinámico de temas
- Fuente JetBrains Mono con fallback
- Usar threading para operaciones largas
- Manejo de errores con messagebox

### Componentes UI
- Heredar de clase base `Component`
- Soporte para `theme_manager` para colores dinámicos
- Métodos `update_theme()` para actualizar estilos
- Soporte para múltiples tamaños y variantes

### Commits
- Conventional Commits con iconos: `<tipo>(<alcance>): <descripción>`
- Tipos: ✨ feat, 🐛 fix, 📚 docs, ♻️ refactor, ✅ test, 🔧 chore
- Siempre hacer commit después de cada tarea completada

## Available Agents

| Agent | Purpose | Location |
|-------|---------|----------|
| orchestrator | Coordina desarrollo | `.opencode/agents/orchestrator/` |
| pdf-engineer | Funcionalidades PDF | `.opencode/agents/pdf-engineer/` |
| gui-developer | Interfaz gráfica | `.opencode/agents/gui-developer/` |
| docs-writer | Documentación | `.opencode/agents/docs-writer/` |

## Available Skills

### DevOps
| Skill | Purpose |
|-------|---------|
| skill-sinc | Sincronización y estado del repo |
| skill-commit | Convenciones de commits con iconos |

### Docs
| Skill | Purpose |
|-------|---------|
| skill-doc | Documentación y README |

### Dev
| Skill | Purpose |
|-------|---------|
| skill-generate | Generación de código y scaffolds |

### Design
| Skill | Purpose |
|-------|---------|
| skill-design | Diseño UI/UX completo |

## Flujo de Trabajo

1. **Splash Screen** → Muestra branding y carga recursos
2. **Panel de Inicio** → Documentos recientes + plantillas
3. **Selección** → Cargar PDF en visor principal
4. **Edición** → Herramientas PDF (reparar, unir, dividir, etc.)

## Funcionalidades Implementadas

✅ Splash screen con animación y progreso  
✅ Panel de inicio con sidebar, plantillas y recientes  
✅ Sistema de componentes UI modular  
✅ Tema oscuro One Dark Pro  
✅ Fuentes JetBrains Mono automáticas  
✅ Gestión de documentos recientes  
✅ Reparación de PDFs  

## Temas Soportados

- **One Dark Pro** (oscuro) - Tema principal
- **Atom One Light** (claro) - Alternativa

## Colores del Tema (One Dark Pro)

- Background: `#282A31`
- Foreground: `#B2C2CD`
- Accent: `#528BFF`
- Success: `#98C379`
- Warning: `#E5C07B`
- Error: `#E06C75`
