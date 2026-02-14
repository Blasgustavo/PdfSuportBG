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

## 2. Paleta de Colores

### Tema Oscuro (Principal)
| Nombre | Hex | Uso |
|--------|-----|-----|
| Background Primary | `#1e1e1e` | Fondo principal |
| Background Secondary | `#2d2d2d` | Fondo de tarjetas |
| Background Tertiary | `#3c3c3c` | Botones, inputs |
| Foreground Primary | `#ffffff` | Texto principal |
| Foreground Secondary | `#b0b0b0` | Texto secundario |
| Foreground Disabled | `#666666` | Texto deshabilitado |
| Accent Primary | `#0078d4` | Botones principales |
| Accent Hover | `#1084d8` | Hover de botones |
| Border | `#404040` | Bordes |
| Error | `#f44336` | Errores |
| Success | `#4caf50` | Éxito |
| Warning | `#ff9800` | Advertencias |

### Tema Claro
| Nombre | Hex | Uso |
|--------|-----|-----|
| Background Primary | `#ffffff` | Fondo principal |
| Background Secondary | `#f5f5f5` | Fondo de tarjetas |
| Background Tertiary | `#e0e0e0` | Botones, inputs |
| Foreground Primary | `#000000` | Texto principal |
| Foreground Secondary | `#666666` | Texto secundario |
| Accent Primary | `#0078d4` | Botones principales |

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

## 10. Assets Requeridos

### Imágenes
- [ ] xebec_icon.png (icono aplicación)
- [ ] splash_logo.png (splash screen)
- [ ] screenshot_main.png (demo)

### Iconos
- Iconos SVG preferidos
- Tamaño: 24x24 (UI), 48x48 (menú)
- Formato: PNG con transparencia

---

## 11. Guías de Implementación

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

## Commands disponibles

1. **Show palette**: Mostrar paleta de colores actual
2. **Show components**: Listar componentes disponibles
3. **Add mockup**: Agregar nuevo mockup/wireframe
4. **Update theme**: Actualizar colores del tema
5. **Export assets**: Exportar assets de diseño
6. **Validate design**: Validar diseño contra guías
