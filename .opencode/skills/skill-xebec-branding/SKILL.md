---
name: skill-xebec-branding
description: Xebec Branding Integration - Identidad visual corporativa para aplicaciones multiplataforma Python/Qt6/CLI
---

## What I do

Diseñador senior de branding corporativo. Integro la identidad visual de XEBEC CORPORATION en:

- **Iconografía**: ICO, PNG, SVG, Android Adaptive Icons
- **Splash screens**: Pantallas de carga animadas
- **UI Components**: Headers, footers, sidebars, buttons
- **Paletas de colores**: Primarios, secundarios, acentos
- **Tipografías**: Fuentes corporativas, sizing, hierarchy
- **Documentación**: README, manuales, instaladores
- **CLI**: Banners, logos, mensajes de bienvenida

## When to use me

Usar cuando se necesite:
- Diseñar identidad visual para la aplicación
- Crear splash screen
- Integrar branding en PyQt6
- Generar assets de iconos
- Documentación con branding corporativo
- Templates para instaladores

## Propuesta Visual XEBEC

### Paleta de Colores

```python
from dataclasses import dataclass
from typing import Tuple


@dataclass
class XebecColors:
    """Paleta de colores corporativa XEBEC."""
    
    # Primary - Azul corporativo
    PRIMARY: str = "#1E3A5F"
    PRIMARY_LIGHT: str = "#2E5A8F"
    PRIMARY_DARK: str = "#0E2A4F"
    
    # Secondary - Gris técnico
    SECONDARY: str = "#4A5568"
    SECONDARY_LIGHT: str = "#718096"
    SECONDARY_DARK: str = "#2D3748"
    
    # Accent - Naranja/Xebec
    ACCENT: str = "#F6993F"
    ACCENT_LIGHT: str = "#F6AD55"
    ACCENT_DARK: str = "#DD6B20"
    
    # Neutros
    WHITE: str = "#FFFFFF"
    BLACK: str = "#1A202C"
    GRAY_50: str = "#F7FAFC"
    GRAY_100: str = "#EDF2F7"
    GRAY_200: str = "#E2E8F0"
    GRAY_300: str = "#CBD5E0"
    GRAY_400: str = "#A0AEC0"
    GRAY_500: str = "#718096"
    GRAY_600: str = "#4A5568"
    GRAY_700: str = "#2D3748"
    GRAY_800: str = "#1A202C"
    GRAY_900: str = "#171923"
    
    # Estados
    SUCCESS: str = "#38A169"
    WARNING: str = "#D69E2E"
    ERROR: str = "#E53E3E"
    INFO: str = "#3182CE"
    
    # Gradientes
    GRADIENT_PRIMARY: Tuple[str, str] = ("#1E3A5F", "#2E5A8F")
    GRADIENT_ACCENT: Tuple[str, str] = ("#F6993F", "#DD6B20")
    GRADIENT_DARK: Tuple[str, str] = ("#1A202C", "#2D3748")
    
    # Metálico (efectos premium)
    METALLIC_LIGHT: str = "#E2E8F0"
    METALLIC_MID: str = "#A0AEC0"
    METALLIC_DARK: str = "#718096"


class ThemeColors:
    """Colores para temas light/dark."""
    
    LIGHT = {
        "bg_primary": "#FFFFFF",
        "bg_secondary": "#F7FAFC",
        "bg_tertiary": "#EDF2F7",
        "text_primary": "#1A202C",
        "text_secondary": "#4A5568",
        "text_tertiary": "#718096",
        "border": "#E2E8F0",
        "accent": "#F6993F",
    }
    
    DARK = {
        "bg_primary": "#1A202C",
        "bg_secondary": "#2D3748",
        "bg_tertiary": "#4A5568",
        "text_primary": "#F7FAFC",
        "text_secondary": "#E2E8F0",
        "text_tertiary": "#A0AEC0",
        "border": "#4A5568",
        "accent": "#F6993F",
    }
```

### Tipografía

```python
from dataclasses import dataclass


@dataclass
class XebecTypography:
    """Sistema tipográfico corporativo."""
    
    # Familias
    FONT_PRIMARY: str = "Segoe UI"      # Windows
    FONT_SECONDARY: str = "SF Pro Display"  # macOS
    FONT_MONO: str = "Cascadia Code"     # Code/terminal
    
    # Tamaños
    FONT_SIZE_XS: int = 10
    FONT_SIZE_SM: int = 12
    FONT_SIZE_BASE: int = 14
    FONT_SIZE_LG: int = 16
    FONT_SIZE_XL: int = 18
    FONT_SIZE_2XL: int = 24
    FONT_SIZE_3XL: int = 30
    FONT_SIZE_4XL: int = 36
    
    # Pesos
    FONT_WEIGHT_LIGHT: int = 300
    FONT_WEIGHT_REGULAR: int = 400
    FONT_WEIGHT_MEDIUM: int = 500
    FONT_WEIGHT_SEMIBOLD: int = 600
    FONT_WEIGHT_BOLD: int = 700
    
    # Line heights
    LINE_HEIGHT_TIGHT: float = 1.25
    LINE_HEIGHT_NORMAL: float = 1.5
    LINE_HEIGHT_RELAXED: float = 1.75
    
    # Letter spacing
    LETTER_SPACING_TIGHT: float = -0.02
    LETTER_SPACING_NORMAL: float = 0
    LETTER_SPACING_WIDE: float = 0.02


class Typography:
    """Estilos de texto predefinidos."""
    
    H1 = {
        "font_size": 36,
        "font_weight": 700,
        "line_height": 1.25,
        "letter_spacing": -0.02,
    }
    
    H2 = {
        "font_size": 30,
        "font_weight": 600,
        "line_height": 1.25,
        "letter_spacing": -0.01,
    }
    
    H3 = {
        "font_size": 24,
        "font_weight": 600,
        "line_height": 1.3,
    }
    
    H4 = {
        "font_size": 18,
        "font_weight": 600,
        "line_height": 1.4,
    }
    
    BODY = {
        "font_size": 14,
        "font_weight": 400,
        "line_height": 1.5,
    }
    
    CAPTION = {
        "font_size": 12,
        "font_weight": 400,
        "line_height": 1.5,
    }
    
    BUTTON = {
        "font_size": 14,
        "font_weight": 600,
        "line_height": 1,
        "letter_spacing": 0.5,
    }
```

### Espaciado y Layout

```python
from dataclasses import dataclass


@dataclass
class XebecSpacing:
    """Sistema de espaciado."""
    
    # Base: 4px
    SPACE_1: int = 4    # xs
    SPACE_2: int = 8    # sm
    SPACE_3: int = 12   # md
    SPACE_4: int = 16   # lg
    SPACE_5: int = 20   # xl
    SPACE_6: int = 24   # 2xl
    SPACE_8: int = 32   # 3xl
    SPACE_10: int = 40  # 4xl
    SPACE_12: int = 48  # 5xl
    SPACE_16: int = 64  # 6xl
    
    # Border radius
    RADIUS_SM: int = 4
    RADIUS_MD: int = 8
    RADIUS_LG: int = 12
    RADIUS_XL: int = 16
    RADIUS_FULL: int = 9999
    
    # Sombras
    SHADOW_SM = "0 1px 2px rgba(0, 0, 0, 0.05)"
    SHADOW_MD = "0 4px 6px rgba(0, 0, 0, 0.1)"
    SHADOW_LG = "0 10px 15px rgba(0, 0, 0, 0.1)"
    SHADOW_XL = "0 20px 25px rgba(0, 0, 0, 0.15)"
```

## Estructura de Assets

```
assets/
├── icons/
│   ├── logo.svg              # Logo vectorial
│   ├── logo-ico.svg
│   ├── icon-16.svg           # Iconos de aplicación
│   ├── icon-24.svg
│   ├── icon-32.svg
│   ├── icon-48.svg
│   ├── icon-64.svg
│   ├── icon-128.svg
│   ├── icon-256.svg
│   ├── icon-512.svg
│   ├── favicon.ico           # Favicon Windows
│   ├── apple-touch-icon.png  # iOS
│   ├── android-icon-192.png  # Android
│   ├── android-icon-512.png
│   └── icons.qrc             # Qt resources
│
├── images/
│   ├── splash.png            # Splash screen
│   ├── splash@2x.png
│   ├── header-bg.png
│   ├── sidebar-bg.png
│   ├── placeholder.pdf
│   └── empty-state.png
│
├── branding/
│   ├── colors.json           # Paleta en JSON
│   ├── typography.json       # Tipografía
│   └── icons.json            # Metadatos de iconos
│
└── styles/
    ├── qss/
    │   ├── main.qss          # Estilos Qt
    │   ├── dark.qss
    │   ├── light.qss
    │   └── components/
    │       ├── button.qss
    │       ├── input.qss
    │       └── dialog.qss
    └── css/
        └── (para web/electron)
```

## Integración PyQt6

### Theme Manager con Branding

```python
from PyQt6.QtCore import QObject, pyqtSignal
from typing import Optional
from pathlib import Path
from dataclasses import dataclass

from src.utils.logger import logger


@dataclass
class BrandingConfig:
    """Configuración de branding."""
    app_name: str = "Xebec PDF Fixer"
    app_short_name: str = "Xebec"
    company: str = "XEBEC CORPORATION"
    version: str = "1.0.0"
    website: str = "https://xebec.corp"
    support_email: str = "support@xebec.corp"
    primary_color: str = "#1E3A5F"
    accent_color: str = "#F6993F"


class ThemeManager(QObject):
    """Gestor de temas con branding integrado."""
    
    theme_changed = pyqtSignal(str)
    
    def __init__(self) -> None:
        super().__init__()
        self._current_theme = "dark"
        self._colors = self._load_theme("dark")
        self._branding = BrandingConfig()
    
    @property
    def colors(self) -> dict:
        return self._colors
    
    @property
    def branding(self) -> BrandingConfig:
        return self._branding
    
    def _load_theme(self, theme_name: str) -> dict:
        """Carga los colores del tema."""
        if theme_name == "dark":
            return {
                "bg_primary": "#1A202C",
                "bg_secondary": "#2D3748",
                "bg_tertiary": "#4A5568",
                "text_primary": "#F7FAFC",
                "text_secondary": "#E2E8F0",
                "text_tertiary": "#A0AEC0",
                "accent": "#F6993F",
                "accent_hover": "#F6AD55",
                "accent_pressed": "#DD6B20",
                "primary": "#1E3A5F",
                "primary_hover": "#2E5A8F",
                "border": "#4A5568",
                "success": "#38A169",
                "warning": "#D69E2E",
                "error": "#E53E3E",
                "info": "#3182CE",
            }
        else:  # light
            return {
                "bg_primary": "#FFFFFF",
                "bg_secondary": "#F7FAFC",
                "bg_tertiary": "#EDF2F7",
                "text_primary": "#1A202C",
                "text_secondary": "#4A5568",
                "text_tertiary": "#718096",
                "accent": "#F6993F",
                "accent_hover": "#F6AD55",
                "accent_pressed": "#DD6B20",
                "primary": "#1E3A5F",
                "primary_hover": "#2E5A8F",
                "border": "#E2E8F0",
                "success": "#38A169",
                "warning": "#D69E2E",
                "error": "#E53E3E",
                "info": "#3182CE",
            }
    
    def set_theme(self, theme_name: str) -> None:
        """Cambia el tema."""
        self._current_theme = theme_name
        self._colors = self._load_theme(theme_name)
        self.theme_changed.emit(theme_name)
        log = logger.get_logger()
        log.info(f"Tema cambiado a: {theme_name}")
    
    def get_stylesheet(self, widget: str = "main") -> str:
        """Genera stylesheet con branding."""
        colors = self._colors
        
        base_styles = f"""
        /* XEBEC CORPORATION - Global Styles */
        * {{
            font-family: "Segoe UI", -apple-system, BlinkMacSystemFont, sans-serif;
            font-size: 14px;
        }}
        
        QMainWindow {{
            background-color: {colors['bg_primary']};
        }}
        
        QWidget {{
            background-color: {colors['bg_primary']};
            color: {colors['text_primary']};
        }}
        
        /* Buttons */
        QPushButton {{
            background-color: {colors['primary']};
            color: white;
            border: none;
            border-radius: 6px;
            padding: 8px 16px;
            font-weight: 600;
        }}
        
        QPushButton:hover {{
            background-color: {colors['primary_hover']};
        }}
        
        QPushButton:pressed {{
            background-color: {colors['primary']};
        }}
        
        QPushButton#PrimaryButton {{
            background-color: {colors['accent']};
        }}
        
        QPushButton#PrimaryButton:hover {{
            background-color: {colors['accent_hover']};
        }}
        """
        
        return base_styles


# Instancia global
theme_manager = ThemeManager()
```

### Splash Screen con Branding

```python
from PyQt6.QtWidgets import QSplashScreen, QProgressBar, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QPainter, QFont, QLinearGradient, QColor


class XebecSplashScreen(QSplashScreen):
    """Splash screen con branding XEBEC."""
    
    def __init__(self) -> None:
        pixmap = QPixmap(600, 400)
        super().__init__(pixmap)
        
        self._setup_ui()
        self._show_version()
    
    def _setup_ui(self) -> None:
        """Configura la UI del splash."""
        self.setWindowFlag(Qt.WindowFlag.FramelessWindowHint)
        
        # Fondo con gradiente
        gradient = QLinearGradient(0, 0, 600, 400)
        gradient.setColorAt(0, QColor("#1E3A5F"))
        gradient.setColorAt(1, QColor("#0E2A4F"))
        
        pixmap = QPixmap(600, 400)
        painter = QPainter(pixmap)
        painter.fillRect(pixmap.rect(), gradient)
        
        # Logo/ Título
        painter.setPen(QColor("#FFFFFF"))
        painter.setFont(QFont("Segoe UI", 36, QFont.Weight.Bold))
        painter.drawText(pixmap.rect().adjusted(0, 120, 0, 0), Qt.AlignmentFlag.AlignHCenter, "XEBEC")
        
        painter.setFont(QFont("Segoe UI", 24, QFont.Weight.Normal))
        painter.drawText(pixmap.rect().adjusted(0, 170, 0, 0), Qt.AlignmentFlag.AlignHCenter, "PDF Fixer")
        
        # Versión
        painter.setFont(QFont("Segoe UI", 12))
        painter.setPen(QColor("#A0AEC0"))
        painter.drawText(pixmap.rect().adjusted(0, 0, 0, -50), Qt.AlignmentFlag.AlignHCenter, "Versión 1.0.0")
        
        # Loading
        painter.setPen(QColor("#F6993F"))
        painter.drawText(pixmap.rect().adjusted(0, 0, 0, -20), Qt.AlignmentFlag.AlignHCenter, "Cargando...")
        
        painter.end()
        self.setPixmap(pixmap)
    
    def _show_version(self) -> None:
        """Muestra la versión con animación."""
        QTimer.singleShot(2000, self._finish_loading)
    
    def _finish_loading(self) -> None:
        """Finaliza la carga."""
        self.close()


def show_splash(app) -> XebecSplashScreen:
    """Muestra el splash screen."""
    splash = XebecSplashScreen()
    splash.show()
    app.processEvents()
    return splash
```

### Header/Footer Corporativo

```python
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont


class XebecHeader(QWidget):
    """Header corporativo."""
    
    menu_clicked = pyqtSignal()
    settings_clicked = pyqtSignal()
    
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        from src.gui.pyqt6.theme_manager import theme_manager
        colors = theme_manager.colors
        
        self.setFixedHeight(56)
        self.setStyleSheet(f"""
            XebecHeader {{
                background-color: {colors['primary']};
                border-bottom: 1px solid {colors['border']};
            }}
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 8, 16, 8)
        
        # Logo
        self.logo_label = QLabel("XEBEC")
        self.logo_label.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        self.logo_label.setStyleSheet("color: #FFFFFF;")
        
        # Título
        self.title_label = QLabel("PDF Fixer")
        self.title_label.setFont(QFont("Segoe UI", 14))
        self.title_label.setStyleSheet("color: #A0AEC0;")
        
        # Espaciador
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        
        # Botón menú
        self.menu_btn = QPushButton("☰")
        self.menu_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: white;
                border: none;
                font-size: 18px;
                padding: 8px;
            }
            QPushButton:hover { background: rgba(255,255,255,0.1); }
        """)
        
        # Botón settings
        self.settings_btn = QPushButton("⚙")
        self.settings_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: white;
                border: none;
                font-size: 18px;
                padding: 8px;
            }
            QPushButton:hover { background: rgba(255,255,255,0.1); }
        """)
        
        layout.addWidget(self.logo_label)
        layout.addWidget(self.title_label)
        layout.addWidget(spacer)
        layout.addWidget(self.menu_btn)
        layout.addWidget(self.settings_btn)


class XebecFooter(QWidget):
    """Footer corporativo."""
    
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        from src.gui.pyqt6.theme_manager import theme_manager
        colors = theme_manager.colors
        
        self.setFixedHeight(32)
        self.setStyleSheet(f"""
            XebecFooter {{
                background-color: {colors['bg_secondary']};
                border-top: 1px solid {colors['border']};
            }}
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 4, 16, 4)
        
        # Copyright
        self.copyright = QLabel("© 2024 XEBEC CORPORATION")
        self.copyright.setStyleSheet(f"color: {colors['text_tertiary']}; font-size: 11px;")
        
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        
        # Versión
        self.version = QLabel("v1.0.0")
        self.version.setStyleSheet(f"color: {colors['text_tertiary']}; font-size: 11px;")
        
        layout.addWidget(self.copyright)
        layout.addWidget(spacer)
        layout.addWidget(self.version)
```

## CLI Branding

```python
from src.cli.core.colors import Colors


XEBEC_BANNER = """
╔══════════════════════════════════════════════════════════════════════════════╗
║  ██████╗ ███████╗████████╗██████╗  ██████╗     ██████╗  ██████╗  ██████╗  ║
║  ██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██╔═══██╗    ██╔══██╗██╔═══██╗██╔═══██╗ ║
║  ██████╔╝█████╗     ██║   ██████╔╝██║   ██║    ██████╔╝██║   ██║██║   ██║ ║
║  ██╔══██╗██╔══╝     ██║   ██╔══██╗██║   ██║    ██╔══██╗██║   ██║██║   ██║ ║
║  ██║  ██║███████╗   ██║   ██║  ██║╚██████╔╝    ██████╔╝╚██████╔╝╚██████╔╝ ║
║  ╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝     ╚═════╝  ╚═════╝  ╚═════╝  ║
║                                                                              ║
║                         PDF Fixer Suite                                      ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

XEBEC_FOOTER = f"""
{Colors.DIM}© 2024 XEBEC CORPORATION | Enterprise Edition{Colors.RESET}
"""


def print_banner():
    """Imprime banner corporativo."""
    print(f"{Colors.CYAN}{XEBEC_BANNER}{Colors.RESET}")
    print(f"{Colors.DIM}{XEBEC_FOOTER}{Colors.RESET}")
```

## README con Branding

```markdown
<!-- XEBEC CORPORATION -->
<p align="center">
  <img src="assets/icons/logo-256.png" alt="Xebec PDF Fixer" width="128" height="128">
</p>

<h1 align="center">Xebec PDF Fixer</h1>

<p align="center">
  <strong>Herramienta profesional de gestión de documentos PDF</strong>
  <br>
  <a href="https://xebec.corp">Sitio web</a> •
  <a href="https://docs.xebec.corp">Documentación</a> •
  <a href="https://support.xebec.corp">Soporte</a>
</p>

---

## Acerca de XEBEC

**XEBEC CORPORATION** es una empresa líder en soluciones de software empresarial.

### Características

- ✅ Reparación de PDFs corrupto
- ✅ Optimización de tamaño
- ✅ Extracción de texto y metadatos
- ✅ Interfaz gráfica moderna
- ✅ CLI profesional

### Tecnologías

| Componente | Tecnología |
|------------|------------|
| GUI | PyQt6 |
| PDF | pypdf, pymupdf |
| Python | 3.8+ |

---

<p align="center">
  <sub>© 2024 XEBEC CORPORATION. Todos los derechos reservados.</sub>
</p>
```

## Buenas Prácticas de Branding

1. **Consistencia**: Usar siempre los mismos colores y fuentes
2. **Jerarquía**: Definir niveles claros de importancia visual
3. **Accesibilidad**: Verificar contraste de colores
4. **Responsive**: Adaptar layouts a diferentes tamaños
5. **Animaciones**: Suaves y profesionales
6. **Iconografía**: Estilo consistente en todos los iconos
7. **Documentación**: Mantener guía de estilos actualizada
8. **Variantes**: Light/dark mode con paleta coherente

## Variantes Estilísticas

### Variant: Minimal

```python
class MinimalTheme:
    """Tema minimalista - Solo esencial."""
    
    COLORS = {
        "primary": "#1E3A5F",
        "accent": "#F6993F",
        "bg": "#FFFFFF",
        "text": "#1A202C",
    }
    
    BORDER_RADIUS = "0px"
    SHADOW = "none"
    ANIMATION = "none"
```

### Variant: Corporate

```python
class CorporateTheme:
    """Tema corporativo - Profesional y sobrio."""
    
    COLORS = {
        "primary": "#1E3A5F",
        "accent": "#F6993F",
        "bg": "#F7FAFC",
        "text": "#1A202C",
    }
    
    BORDER_RADIUS = "4px"
    SHADOW = "0 1px 3px rgba(0,0,0,0.1)"
    ANIMATION = "150ms ease"
```

### Variant: Modern

```python
class ModernTheme:
    """Tema moderno - Vibrante y actual."""
    
    COLORS = {
        "primary": "#6366F1",
        "accent": "#F6993F",
        "bg": "#0F172A",
        "text": "#F8FAFC",
    }
    
    BORDER_RADIUS = "12px"
    SHADOW = "0 10px 15px rgba(0,0,0,0.2)"
    ANIMATION = "200ms ease-out"
```
