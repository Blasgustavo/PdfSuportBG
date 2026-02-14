---
name: skill-design
description: Gestiona el diseño completo UI/UX de la aplicación incluyendo mockups, wireframes, paleta de colores, tipografía, iconografía y flujos de usuario
license: MIT
compatibility: opencode
metadata:
  audience: designers
  workflow: ui-ux
---

# 🎨 Xebec PDF Fixer - Sistema de Diseño

## Descripción General

**Xebec PDF Fixer** es una aplicación de escritorio para Windows enfocada en la administración de archivos PDF. El diseño debe ser profesional, limpio y funcional.

---

## 1. Identidad de Marca

### Nombre del Producto
- **Nombre:** Xebec PDF Fixer
- **Organización:** Corporación Xebec
- **Autor:** BGNC

### Logotipo
- Icono principal: Logo de Xebec
- Usado en: Splash screen, ventana principal, ejecutable

---

## 2. Temas - One Dark Pro & Atom One Light

### Tema Oscuro - One Dark Pro (Principal)
| Nombre | Hex | Uso |
|--------|-----|-----|
| Background | `#282A31` | Fondo principal |
| Background Alt | `#16181F` | Fondo secundario/sidebar |
| Background Current Line | `#2D333B` | Línea actual |
| Foreground | `#B2C2CD` | Texto principal |
| Foreground Dim | `#8E9BAB` | Texto secundario |
| Comment | `#5C6370` | Comentarios |
| Accent | `#528BFF` | Links, acentos |
| Red | `#E06C75` | Errores, eliminar |
| Green | `#98C379` | Éxito |
| Yellow | `#E5C07B` | Advertencias |
| Blue | `#61AFEF` | Información |
| Purple | `#C678DD` | Destacados |
| Cyan | `#56B6C2` | Estados |

### Tema Claro - Atom One Light
| Nombre | Hex | Uso |
|--------|-----|-----|
| Background | `#FAFAFA` | Fondo principal |
| Background Alt | `#F5F5F5` | Fondo secundario |
| Background Current Line | `#EFEFEF` | Línea actual |
| Foreground | `#383A42` | Texto principal |
| Foreground Dim | `#9DA5B4` | Texto secundario |
| Comment | `#A0A1A7` | Comentarios |
| Accent | `#526FFF` | Links, acentos |
| Red | `#E45649` | Errores, eliminar |
| Green | `#50A14F` | Éxito |
| Yellow | `#986801` | Advertencias |
| Blue | `#526FFF` | Información |
| Purple | `#A626A4` | Destacados |
| Cyan | `#0897B3` | Estados |

### Variables CSS del Tema (para referencia)
```css
/* One Dark Pro */
--bg-primary: #282A31;
--bg-secondary: #16181F;
--fg-primary: #B2C2CD;
--fg-secondary: #8E9BAB;
--accent: #528BFF;
--error: #E06C75;
--success: #98C379;
--warning: #E5C07B;

/* Atom One Light */
--bg-primary: #FAFAFA;
--bg-secondary: #F5F5F5;
--fg-primary: #383A42;
--fg-secondary: #9DA5B4;
--accent: #526FFF;
--error: #E45649;
--success: #50A14F;
--warning: #986801;
```

---

## 3. Tipografía

### Familia Principal
- **Sistema:** Segoe UI (Windows native)
- **Fallback:** Arial, sans-serif

### Escalera Tipográfica
| Elemento | Tamaño | Peso |
|----------|---------|------|
| Título Principal | 16px | Bold (700) |
| Subtítulo | 14px | SemiBold (600) |
| Cuerpo | 12px | Regular (400) |
| Pequeño/Labels | 10px | Regular (400) |
| Botones | 12px | SemiBold (600) |

---

## 4. Espaciado (8px Grid)

- **xs:** 4px
- **sm:** 8px
- **md:** 16px
- **lg:** 24px
- **xl:** 32px
- **xxl:** 48px

### Padding estándar
- Botones: 12px horizontal, 8px vertical
- Tarjetas: 16px
- Ventana: 20px

---

## 5. Componentes UI

### Botones
| Tipo | Estados | Uso |
|------|---------|-----|
| Primary | normal, hover, active, disabled | Acciones principales |
| Secondary | normal, hover, active, disabled | Acciones secundarias |
| Icon | normal, hover | Iconos con acción |

### Campos de Entrada
- Bordes redondeados: 4px
- Focus: Borde accent
- Error: Borde rojo + mensaje

### Barras de Progreso
- Altura: 20px
- Color: Accent Primary
- Fondo: Background Tertiary

### Diálogos
- Modal con overlay
- Título + contenido + acciones
- Botones: Cancelar (secondary) + Aceptar (primary)

---

## 6. Estructura de Ventanas

### Ventana Principal (420x380)
```
┌─────────────────────────────────┐
│  🖥️ Xebec PDF Fixer            │  ← Título + branding
│     Corporación Xebec          │  ← Subtítulo
│  Autor: BGNC | Versión: 0.0.1  │  ← Info
├─────────────────────────────────┤
│                                 │
│  🧰 Reparador de PDFs para    │  ← Descripción
│     Vista Previa de Windows    │
│                                 │
│  ┌─────────────────────────┐   │
│  │ ████████████░░░░░░░░░░░ │   │  ← Progress bar
│  └─────────────────────────┘   │
│        Procesando...            │  ← Status
│                                 │
│  [📂 Seleccionar carpeta...]   │  ← Botón primary
│  [📄 Reparar un solo PDF]      │  ← Botón secondary
│  [Salir]                       │  ← Botón secondary
│                                 │
└─────────────────────────────────┘
```

### Diálogos Futuros
- **Unir PDFs:** Selector múltiples archivos + preview
- **Dividir PDF:** Selector página inicio/fin
- **Eliminar Hojas:** Grid de páginas + checkboxes
- **Configuración:** Theme toggle, path configuración

---

## 7. Iconografía

### Iconos principales
| Icono | Significado |
|-------|--------------|
| 📂 | Seleccionar carpeta |
| 📄 | PDF/Archivo |
| 🔧 | Herramientas |
| ⚙️ | Configuración |
| ✅ | Éxito |
| ❌ | Error |
| ⚠️ | Advertencia |
| 🔄 | Procesando |

### Iconos de Acciones PDF
| Icono | Acción |
|-------|--------|
| 🔗 | Unir PDFs |
| ✂️ | Dividir PDF |
| 🗑️ | Eliminar hojas |
| 🔄 | Rotar páginas |
| ↔️ | Reordenar |

---

## 8. Flujos de Usuario

### Flujo 1: Reparar PDFs
1. Usuario abre app
2. Selecciona "Seleccionar carpeta"
3. Sistema escanea PDFs
4. Barra de progreso muestra estado
5. Sistema guarda en /fixed
6. Mensaje de resultado

### Flujo 2: Herramientas PDF
1. Usuario hace clic en menú herramientas
2. Selecciona operación (unir/dividir/eliminar)
3. Ingresa parámetros
4. Preview si aplica
5. Ejecuta operación
6. Resultado + opción de abrir carpeta

---

## 9. Animaciones y Transiciones

| Elemento | Animación | Duración |
|----------|-----------|----------|
| Botones | Background fade | 150ms |
| Progress bar | Width transition | 200ms |
| Diálogos | Fade + scale | 200ms |
| Splash | Fade in/out | 500ms |

---

## 10. Assets de Diseño

### Imágenes del Proyecto
```
assets/
├── icons/
│   ├── icono.png          # Icono de aplicación (197KB)
│   └── logo.png           # Logo corporativo (1.2MB)
├── splash/
│   └── estart-cargando.png    # Splash screen
└── design/
    ├── estart-cargando.png           # Diseño splash
    ├── 2 panel despues del start.png # Panel principal
    ├── arbol de archivos.png         # Navegador archivos
    ├── panel de busqueda.png         # Panel búsqueda
    ├── panel de lectura.png          # Visor PDF
    ├── panel de edicion lateral.png  # Panel edición
    ├── panel de opciones en formato cinta.png  # Ribbon toolbar
    ├── paenel de configuracion.png  # Configuración
    └── panel de ayuda de teclas.png  # Atajos teclado
```

### Assets Implementados
| Asset | Estado | Ubicación |
|-------|--------|-----------|
| Logo | ✅ Listo | `assets/icons/logo.png` |
| Icono app | ✅ Listo | `assets/icons/icono.png` |
| Splash | ✅ Listo | `assets/splash/estart-cargando.png` |

---

## 11. Estructura de Paneles (UI Modular)

### Layout Principal
```
┌─────────────────────────────────────────────────────────────┐
│  [Logo] Xebec PDF Fixer        [─] [□] [×]                │  ← Title Bar
├─────────────────────────────────────────────────────────────┤
│  [Archivo] [Editar] [Ver] [Herramientas] [Ayuda]          │  ← Ribbon Menu
├──────────┬─────────────────────────────────┬──────────────┤
│          │                                 │              │
│  Sidebar │       Panel Principal           │  Panel       │
│  (Árbol) │       (Visor/Lectura)          │  Lateral     │
│          │                                 │  (Edición)   │
│  - PDFs  │   ┌─────────────────────┐       │              │
│  - Recientes│   │                   │       │  - Propiedades│
│  - Favoritos│  │    Vista PDF     │       │  - Herramientas│
│          │   │                   │       │              │
│          │   └─────────────────────┘       │              │
├──────────┴─────────────────────────────────┴──────────────┤
│  [Barra de estado: página actual | zoom | archivos]       │
└─────────────────────────────────────────────────────────────┘
```

### Descripción de Paneles

| Panel | Componente | Archivo Mockup |
|-------|------------|----------------|
| Splash | Pantalla carga | `assets/design/estart-cargando.png` |
| Principal | Post inicio | `assets/design/2 panel despues del start.png` |
| Sidebar | Árbol archivos | `assets/design/arbol de archivos.png` |
| Búsqueda | Buscador | `assets/design/panel de busqueda.png` |
| Lectura | Visor PDF | `assets/design/panel de lectura.png` |
| Lateral | Edición | `assets/design/panel de edicion lateral.png` |
| Ribbon | Menú cinta | `assets/design/panel de opciones en formato cinta.png` |
| Configuración | Ajustes | `assets/design/paenel de configuracion.png` |
| Ayuda | Atajos | `assets/design/panel de ayuda de teclas.png` |

---

## 12. Flujos de Usuario

### Para Desarrolladores GUI
1. Usar variables de colors del tema
2. Mantener espaciado 8px grid
3. Todos los botones deben tener hover
4. Operaciones largas = barra progreso + threading
5. Errores = messagebox.error
6. Éxitos = messagebox.showinfo

### Para Diseñadores
1. Mantener consistencia con paleta
2. Priorizar usabilidad sobre estética
3. Testing en Windows nativo
4. Accesibilidad: contraste mínimo 4.5:1

---

## 13. Guías de Implementación

### Para Desarrolladores GUI
1. Usar variables de colores del tema (One Dark Pro / Atom One Light)
2. Mantener espaciado 8px grid
3. Todos los botones deben tener hover
4. Operaciones largas = barra progreso + threading
5. Errores = messagebox.error
6. Éxitos = messagebox.showinfo
7. Implementar navegación entre paneles

### Para Diseñadores
1. Mantener consistencia con paleta One Dark/One Light
2. Priorizar usabilidad sobre estética
3. Testing en Windows nativo
4. Accesibilidad: contraste mínimo 4.5:1

---

## 14. Estructura de Código GUI

```
src/gui/
├── main_window.py           # Contenedor principal con panels
├── splash_screen.py         # Splash animado
├── widgets/
│   ├── __init__.py
│   ├── sidebar.py           # Árbol de archivos
│   ├── viewer.py            # Panel de lectura/viso
│   ├── editor.py            # Panel de edición lateral
│   ├── ribbon.py            # Toolbar tipo cinta
│   ├── search.py            # Panel de búsqueda
│   └── settings.py          # Diálogo de configuración
└── themes/
    └── __init__.py          # DARK_THEME, LIGHT_THEME
```

---

## Commands disponibles

1. **Show palette**: Mostrar paleta de colores actual
2. **Show components**: Listar componentes disponibles
3. **Add mockup**: Agregar nuevo mockup/wireframe
4. **Update theme**: Actualizar colores del tema
5. **Export assets**: Exportar assets de diseño
6. **Validate design**: Validar diseño contra guías
7. **List panels**: Mostrar estructura de paneles
8. **Show assets**: Listar assets disponibles
