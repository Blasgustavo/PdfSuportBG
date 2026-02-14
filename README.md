# 🖥️ Xebec Pdf

**Gestor de documentos PDF para Windows**

Branding: Corporación Xebec  
Autor: BGNC  
Versión: 0.0.1

---

Aplicación de escritorio profesional para administrar, visualizar y editar archivos PDF con interfaz moderna inspirada en Microsoft Office.

## ✨ Características

- 🎨 **Interfaz moderna** con tema oscuro One Dark Pro
- 📄 **Panel de inicio** con documentos recientes y plantillas
- 🖼️ **Splash screen** animado con branding corporativo
- 🔧 **Herramientas PDF**: Reparar, unir, dividir, extraer páginas
- 🎭 **Sistema de componentes UI** modular y reutilizable
- 📝 **Gestión de documentos** con historial y auto-guardado
- 🔍 **Búsqueda integrada** de documentos

## Requisitos previos:

```bash
pip install -r requirements.txt
```

## 🚀 Ejecutar la aplicación

```bash
python src/main.py
```

## 🟦 Convertirlo en un .EXE para tu escritorio

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=assets/icons/icono.png src/main.py
```

---

## 📁 Estructura del Proyecto

```
PdfSuport/
├── src/                           # Código fuente principal
│   ├── main.py                    # Punto de entrada
│   ├── core/                      # Lógica de negocio PDF
│   │   └── pdf_repair.py          # Reparar PDFs
│   ├── gui/                       # Interfaz gráfica
│   │   ├── main_window.py         # Ventana principal
│   │   ├── splash_screen.py       # Pantalla de carga
│   │   ├── components/            # Componentes UI
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
├── assets/                        # Recursos estáticos
│   ├── icons/                     # Iconos (logo.png, icono.png)
│   ├── fonts/                     # Fuentes (JetBrains Mono)
│   └── design/                    # Mockups de diseño
├── .opencode/                     # Configuración OpenCode
│   ├── agents/                    # Agentes especializados
│   └── skills/                    # Skills por dominio
├── requirements.txt               # Dependencias
└── README.md                      # Este archivo
```

---

## 📋 Funcionalidades Implementadas

### ✅ Completadas
- [x] Splash screen animado con progreso
- [x] Panel de inicio con sidebar, plantillas y documentos recientes
- [x] Sistema de componentes UI modular
- [x] Tema oscuro One Dark Pro
- [x] Fuentes JetBrains Mono descargadas automáticamente
- [x] Gestión de documentos recientes (JSON)
- [x] Reparación de PDFs
- [x] Logging detallado
- [x] Skills de OpenCode configuradas

### 🔄 En desarrollo
- [ ] Unir PDFs
- [ ] Separar/Dividir PDF
- [ ] Eliminar hojas específicas
- [ ] Rotar páginas
- [ ] Reordenar páginas

### 📋 Pendientes
- [ ] Tests unitarios
- [ ] CI/CD para builds automáticos
- [ ] Installer profesional (Inno Setup)
- [ ] Exportar a otros formatos
- [ ] Cifrado/Descifrado de PDFs

---

## 🎨 Sistema de Diseño

### Paleta de Colores (One Dark Pro)
- **Background**: `#282A31`
- **Foreground**: `#B2C2CD`
- **Accent**: `#528BFF`
- **Success**: `#98C379`
- **Warning**: `#E5C07B`
- **Error**: `#E06C75`

### Tipografía
- **Primaria**: JetBrains Mono (descargada automáticamente)
- **Secundaria**: Segoe UI (sistema)

---

## 🤖 OpenCode Configuration

El proyecto está configurado para usar OpenCode con:

### Agentes
- `orchestrator`: Coordina el desarrollo
- `pdf-engineer`: Funcionalidades PDF
- `gui-developer`: Interfaz gráfica

### Skills
- `skill-sinc`: Sincronización del proyecto
- `skill-doc`: Documentación
- `skill-generate`: Generación de código
- `skill-commit`: Convenciones de commits
- `skill-design`: Diseño UI/UX

---

## 📝 Licencia

MIT License - Corporación Xebec

## 👨‍💻 Autor

BGNC - Desarrollador Principal

---

¿Tienes alguna sugerencia o encuentras algún bug? ¡Abre un issue en GitHub!
