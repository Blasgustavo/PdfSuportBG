---
name: design
description: Gestiona el diseño completo UI/UX de la aplicación incluyendo mockups, wireframes, paleta de colores, tipografía, iconografía y flujos de usuario
license: MIT
compatibility: opencode
metadata:
  audience: designers
  workflow: ui-ux
---

# Xebec PDF Fixer - Sistema de Diseño

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

## Commands disponibles

1. **Show palette**: Mostrar paleta de colores actual
2. **Show components**: Listar componentes disponibles
3. **Add mockup**: Agregar nuevo mockup/wireframe
4. **Update theme**: Actualizar colores del tema
5. **Export assets**: Exportar assets de diseño
6. **Validate design**: Validar diseño contra guías
7. **List panels**: Mostrar estructura de paneles
8. **Show assets**: Listar assets disponibles
