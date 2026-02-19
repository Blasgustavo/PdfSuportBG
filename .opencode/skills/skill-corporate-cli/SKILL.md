---
name: skill-corporate-cli
description: Corporate CLI Orchestrator - Interfaces CLI profesionales, menús interactivos y herramientas de línea de comandos corporativas
---

## What I do

Diseñador de herramientas CLI corporativas. Creo interfaces de línea de comandos profesionales, interactivas y robustas:

- **Menús interactivos**: navegación por teclado, selección visual, atajos
- **Branding corporativo**: ASCII art, colores ANSI, banners personalizados
- **Flujos completos**: instalación, configuración, diagnóstico, automatización
- **Módulos integrados**: PDF operations, UI launcher, system info, network tools
- **Comandos inteligentes**: autocompletado, validación, sugerencias
- **Multiplataforma**: Windows, Linux, macOS con detección automática
- **Persistencia**: perfiles, configuraciones, logs, historial

## When to use me

Usar cuando se necesite:
- CLI interactiva para la aplicación
- Menú principal de navegación
- Herramientas de diagnóstico
- Lanzador de GUI
- Scripts de automatización
- Interfaz para usuarios no técnicos

## Arquitectura CLI Propuesta

```
src/
├── cli/
│   ├── __init__.py
│   ├── main.py                 # Punto de entrada
│   ├── core/
│   │   ├── menu.py             # Sistema de menús
│   │   ├── colors.py           # Colores ANSI
│   │   ├── input.py            # Input interactivo
│   │   ├── table.py            # Tablas formateadas
│   │   └── progress.py         # Barras de progreso
│   ├── commands/
│   │   ├── base.py             # Comando base
│   │   ├── pdf_commands.py     # Comandos PDF
│   │   ├── gui_commands.py     # Lanzador GUI
│   │   ├── system_commands.py  # Comandos sistema
│   │   └── config_commands.py  # Configuración
│   ├── launcher.py             # Lanzador principal
│   └── profile.py              # Perfiles de usuario
```

## Sistema de Menús Interactivos

```python
from typing import Callable, Optional, Any
from enum import Enum
from dataclasses import dataclass
import os
import sys


class Key(Enum):
    UP = "\x1b[A"
    DOWN = "\x1b[B"
    RIGHT = "\x1b[C"
    LEFT = "\x1b[D"
    ENTER = "\r"
    ESC = "\x1b"
    BACKSPACE = "\x7f"


@dataclass
class MenuItem:
    """Elemento de menú."""
    label: str
    action: Callable[[], Any]
    shortcut: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None


class InteractiveMenu:
    """Sistema de menús interactivos."""
    
    def __init__(
        self,
        title: str,
        items: list[MenuItem],
        subtitle: Optional[str] = None,
        banner: Optional[str] = None
    ) -> None:
        self.title = title
        self.items = items
        self.subtitle = subtitle
        self.banner = banner
        self.selected_index = 0
        self.running = False
    
    def _clear_screen(self) -> None:
        """Limpia la pantalla de forma multiplataforma."""
        os.system("cls" if os.name == "nt" else "clear")
    
    def _print_banner(self) -> None:
        """Imprime banner corporativo."""
        if self.banner:
            print(self.banner)
            print()
    
    def _print_menu(self) -> None:
        """Imprime el menú actual."""
        self._clear_screen()
        self._print_banner()
        
        from src.cli.core.colors import Colors
        
        # Título
        print(f"{Colors.BOLD}{Colors.CYAN}{'═' * 60}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}  {self.title}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'═' * 60}{Colors.RESET}")
        
        if self.subtitle:
            print(f"{Colors.DIM}{self.subtitle}{Colors.RESET}")
        
        print()
        
        # Items
        for idx, item in enumerate(self.items):
            is_selected = idx == self.selected_index
            prefix = f"{Colors.GREEN}▶{Colors.RESET} " if is_selected else "  "
            label_color = Colors.BOLD + Colors.GREEN if is_selected else Colors.WHITE
            shortcut_color = Colors.YELLOW
            
            line = f"{prefix}{label_color}{item.label}{Colors.RESET}"
            
            if item.shortcut:
                line += f"  {shortcut_color}[{item.shortcut}]{Colors.RESET}"
            
            print(line)
            
            if is_selected and item.description:
                print(f"     {Colors.DIM}{item.description}{Colors.RESET}")
        
        print()
        print(f"{Colors.DIM}↑↓ Navegar | Enter Seleccionar | ESC Volver | Q Salir{Colors.RESET}")
    
    def _handle_input(self) -> bool:
        """Maneja input del usuario. Retorna True para continuar."""
        try:
            key = self._get_key()
            
            if key == Key.UP:
                self.selected_index = (self.selected_index - 1) % len(self.items)
            elif key == Key.DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.items)
            elif key == Key.ENTER:
                self._clear_screen()
                self.items[self.selected_index].action()
                input(f"\n{Colors.YELLOW}Presiona Enter para continuar...{Colors.RESET}")
            elif key == Key.ESC or key.lower() == "q":
                return False
            
            return True
            
        except (KeyboardInterrupt, EOFError):
            return False
    
    def _get_key(self) -> str:
        """Obtiene una tecla sin eco."""
        import tty
        import termios
        
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
            
            if ch == "\x1b":
                # Secuencia de escape
                ch += sys.stdin.read(2)
                
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        
        return ch
    
    def run(self) -> None:
        """Ejecuta el menú interactivo."""
        self.running = True
        
        while self.running:
            self._print_menu()
            self.running = self._handle_input()
        
        self._clear_screen()
```

## Colores y Estilo ANSI

```python
from typing import Optional
import os


class Colors:
    """Colores y estilos ANSI."""
    
    # Reset
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    
    # Colores foreground
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    
    # Colores bright
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"
    
    # Backgrounds
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"
    
    @classmethod
    def disable(cls) -> None:
        """Desactiva colores (modo silencioso)."""
        for attr in dir(cls):
            if not attr.startswith("_"):
                setattr(cls, attr, "")
    
    @classmethod
    def enable(cls) -> None:
        """Reactiva colores."""
        cls._init_colors()
    
    @classmethod
    def _init_colors(cls) -> None:
        """Inicializa colores detectando soporte."""
        if os.getenv("NO_COLOR") or os.getenv("TERM") == "dumb":
            cls.disable()
    
    # Detectar soporte automáticamente
    _init_colors()


class StylizedPrinter:
    """Printer con estilos predefinidos."""
    
    @staticmethod
    def success(message: str) -> None:
        print(f"{Colors.GREEN}✓ {message}{Colors.RESET}")
    
    @staticmethod
    def error(message: str) -> None:
        print(f"{Colors.RED}✗ {message}{Colors.RESET}")
    
    @staticmethod
    def warning(message: str) -> None:
        print(f"{Colors.YELLOW}⚠ {message}{Colors.RESET}")
    
    @staticmethod
    def info(message: str) -> None:
        print(f"{Colors.CYAN}ℹ {message}{Colors.RESET}")
    
    @staticmethod
    def header(message: str, width: int = 60) -> None:
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'═' * width}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}{message:^{width}}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'═' * width}{Colors.RESET}\n")
    
    @staticmethod
    def code(code: str, lang: str = "") -> None:
        print(f"{Colors.DIM}{Colors.BRIGHT_BLACK}{code}{Colors.RESET}")
```

## Banner Corporativo ASCII

```python
from typing import Optional


def get_banner(name: str = "Xebec", version: str = "1.0.0") -> str:
    """Genera banner corporativo."""
    
    return f"""
{Colors.BRIGHT_CYAN}
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║   ██████╗ ███████╗████████╗██████╗  ██████╗     ██████╗  ██████╗  ██████╗  ║
║   ██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██╔═══██╗    ██╔══██╗██╔═══██╗██╔═══██╗ ║
║   ██████╔╝█████╗     ██║   ██████╔╝██║   ██║    ██████╔╝██║   ██║██║   ██║ ║
║   ██╔══██╗██╔══╝     ██║   ██╔══██╗██║   ██║    ██╔══██╗██║   ██║██║   ██║ ║
║   ██║  ██║███████╗   ██║   ██║  ██║╚██████╔╝    ██████╔╝╚██████╔╝╚██████╔╝ ║
║   ╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝     ╚═════╝  ╚═════╝  ╚═════╝  ║
║                                                                      ║
║                          PDF Fixer Suite                            ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
{Colors.RESET}
{Colors.DIM}  Versión {version} | © 2024 Xebec Corporation | Enterprise Edition{Colors.RESET}
"""


def get_mini_banner() -> str:
    """Banner mini para submenús."""
    return f"""
{Colors.CYAN}╔═══════════════════════════════════╗
║     {Colors.BOLD}Xebec PDF Fixer{Colors.RESET}{Colors.CYAN}           ║
╚═══════════════════════════════════╝{Colors.RESET}
"""
```

## Árbol de Comandos

```
pdf-support CLI
├── main                    # Menú principal interactivo
│   ├── pdf                # Operaciones PDF
│   │   ├── merge          # Unir PDFs
│   │   ├── split          # Dividir PDF
│   │   ├── extract        # Extraer páginas/texto
│   │   ├── compress       # Comprimir PDF
│   │   ├── repair         # Reparar PDF
│   │   └── batch          # Procesamiento por lotes
│   ├── gui                # Lanzar GUI
│   │   ├── launch         # Abrir interfaz gráfica
│   │   └── preview        # Previsualizar PDF
│   ├── system             # Comandos de sistema
│   │   ├── info           # Información del sistema
│   │   ├── diagnostics   # Diagnósticos
│   │   ├── logs           # Ver logs
│   │   └── config         # Configuración
│   ├── profile            # Perfiles de usuario
│   │   ├── list           # Listar perfiles
│   │   ├── create         # Crear perfil
│   │   ├── switch         # Cambiar perfil
│   │   └── delete         # Eliminar perfil
│   └── help               # Ayuda
│
├── setup                  # Configuración inicial
├── diagnose               # Diagnóstico rápido
├── quick <command>        # Comando rápido sin menú
├── gui                    # Lanzar GUI directamente
├── version                # Mostrar versión
└── --help                 # Ayuda global
```

## Implementación de Comandos

```python
from abc import ABC, abstractmethod
from typing import Optional, Any
from pathlib import Path
import sys


class Command(ABC):
    """Clase base para comandos."""
    
    name: str = ""
    description: str = ""
    aliases: list[str] = []
    options: dict[str, Any] = {}
    
    @abstractmethod
    def execute(self, args: list[str] = None) -> int:
        """Ejecuta el comando. Retorna código de salida."""
        pass
    
    def help(self) -> str:
        """Retorna ayuda del comando."""
        return f"{self.name}: {self.description}"


class PDFMergeCommand(Command):
    """Comando para unir PDFs."""
    
    name = "merge"
    description = "Une múltiples archivos PDF en uno"
    aliases = ["m", "join"]
    
    def execute(self, args: list[str] = None) -> int:
        from src.cli.core.colors import Colors, StylizedPrinter
        from src.services.pdf_merge import PDFMergeService
        
        if not args or len(args) < 2:
            StylizedPrinter.error("Uso: merge <archivo1> <archivo2> ... <output>")
            return 1
        
        input_files = [Path(f) for f in args[:-1]]
        output_file = Path(args[-1])
        
        service = PDFMergeService()
        result = service.merge(input_files, output_file)
        
        if result.success:
            StylizedPrinter.success(result.message)
            return 0
        else:
            StylizedPrinter.error(result.message)
            return 1


class GUILaunchCommand(Command):
    """Comando para lanzar la GUI."""
    
    name = "gui"
    description = "Lanza la interfaz gráfica"
    aliases = ["launch", "open"]
    
    def execute(self, args: list[str] = None) -> int:
        from src.cli.core.colors import Colors, StylizedPrinter
        
        StylizedPrinter.info("Iniciando interfaz gráfica...")
        
        try:
            from src.main import main as gui_main
            gui_main()
            return 0
        except Exception as e:
            StylizedPrinter.error(f"Error al iniciar GUI: {e}")
            return 1


class SystemInfoCommand(Command):
    """Comando para mostrar información del sistema."""
    
    name = "info"
    description = "Muestra información del sistema"
    aliases = ["system", "sys"]
    
    def execute(self, args: list[str] = None) -> int:
        from src.cli.core.colors import Colors
        from src.cli.core.table import Table
        
        StylizedPrinter.header("Información del Sistema")
        
        # Recopilar información
        info_data = [
            ("Sistema Operativo", os.name),
            ("Plataforma", sys.platform),
            ("Python Version", sys.version.split()[0]),
            ("Directorio de trabajo", os.getcwd()),
            ("CPU Count", str(os.cpu_count())),
        ]
        
        table = Table()
        table.add_rows(info_data)
        table.print()
        
        return 0
```

## Launcher Principal

```python
import sys
from pathlib import Path
from typing import Optional
import argparse


class CLILauncher:
    """Lanzador principal del CLI."""
    
    def __init__(self) -> None:
        self.commands: dict[str, Command] = {}
        self.parser = self._build_parser()
    
    def _build_parser(self) -> argparse.ArgumentParser:
        """Construye el parser de argumentos."""
        parser = argparse.ArgumentParser(
            prog="pdf-support",
            description="Xebec PDF Fixer - Herramienta CLI corporativa",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Ejemplos:
  pdf-support              # Menú interactivo
  pdf-support gui          # Lanzar GUI
  pdf-support merge a.pdf b.pdf output.pdf
  pdf-support diagnose     # Diagnóstico del sistema
  pdf-support --version    # Mostrar versión
            """
        )
        
        parser.add_argument(
            "command", 
            nargs="?", 
            help="Comando a ejecutar"
        )
        parser.add_argument(
            "args", 
            nargs=argparse.REMAINDER, 
            help="Argumentos del comando"
        )
        parser.add_argument(
            "--quiet", "-q", 
            action="store_true", 
            help="Modo silencioso"
        )
        parser.add_argument(
            "--expert", "-e", 
            action="store_true", 
            help="Modo experto (más opciones)"
        )
        parser.add_argument(
            "--version", "-v", 
            action="store_true", 
            help="Mostrar versión"
        )
        
        return parser
    
    def register_command(self, command: Command) -> None:
        """Registra un comando."""
        self.commands[command.name] = command
        for alias in command.aliases:
            self.commands[alias] = command
    
    def run(self, args: Optional[list[str]] = None) -> int:
        """Ejecuta el CLI."""
        parsed = self.parser.parse_args(args)
        
        # Modo silencioso
        if parsed.quiet:
            from src.cli.core.colors import Colors
            Colors.disable()
        
        # Mostrar versión
        if parsed.version:
            print(f"Xebec PDF Fixer v1.0.0")
            return 0
        
        # Sin comando - menú interactivo
        if not parsed.command:
            return self._run_interactive()
        
        # Ejecutar comando
        if parsed.command in self.commands:
            return self.commands[parsed.command].execute(parsed.args)
        else:
            print(f"Comando desconocido: {parsed.command}")
            print("Usa --help para ver comandos disponibles")
            return 1
    
    def _run_interactive(self) -> int:
        """Ejecuta el menú interactivo."""
        from src.cli.core.colors import Colors, StylizedPrinter
        from src.cli.core.menu import InteractiveMenu, MenuItem
        
        StylizedPrinter.header("Xebec PDF Fixer")
        
        def action_pdf():
            from src.cli.commands.pdf_commands import show_pdf_menu
            show_pdf_menu()
        
        def action_gui():
            from src.cli.commands.gui_commands import launch_gui
            launch_gui()
        
        def action_system():
            from src.cli.commands.system_commands import show_system_menu
            show_system_menu()
        
        def action_config():
            from src.cli.commands.config_commands import show_config_menu
            show_config_menu()
        
        def action_exit():
            print(f"\n{Colors.CYAN}¡Gracias por usar Xebec PDF Fixer!{Colors.RESET}")
            sys.exit(0)
        
        menu = InteractiveMenu(
            title="Menú Principal",
            subtitle="Selecciona una opción",
            items=[
                MenuItem("Operaciones PDF", action_pdf, "1", "Unir, dividir, comprimir, etc."),
                MenuItem("Interfaz Gráfica", action_gui, "2", "Abrir aplicación GUI"),
                MenuItem("Sistema", action_system, "3", "Info, diagnósticos, logs"),
                MenuItem("Configuración", action_config, "4", "Perfiles y opciones"),
                MenuItem("Salir", action_exit, "q", "Cerrar aplicación"),
            ],
            banner=get_banner()
        )
        
        menu.run()
        return 0


def main():
    """Punto de entrada principal."""
    from src.cli.core.colors import Colors
    
    # Verificar soporte de colores
    if not sys.stdout.isatty():
        Colors.disable()
    
    launcher = CLILauncher()
    
    # Registrar comandos
    from src.cli.commands.pdf_commands import (
        PDFMergeCommand, PDFSplitCommand, PDFCompressCommand
    )
    from src.cli.commands.gui_commands import GUILaunchCommand
    from src.cli.commands.system_commands import SystemInfoCommand
    
    launcher.register_command(PDFMergeCommand())
    launcher.register_command(PDFSplitCommand())
    launcher.register_command(PDFCompressCommand())
    launcher.register_command(GUILaunchCommand())
    launcher.register_command(SystemInfoCommand())
    
    sys.exit(launcher.run())


if __name__ == "__main__":
    main()
```

## Modos de Operación

### Modo Silencioso (Quiet Mode)

```python
def quiet_mode_example():
    """Ejemplo de modo silencioso."""
    
    # Desactivar salida
    from src.cli.core.colors import Colors
    Colors.disable()
    
    # Ejecutar sin output
    result = service.merge(files, output)
    
    # Solo código de retorno
    return 0 if result.success else 1
```

### Modo Experto (Expert Mode)

```python
def expert_menu():
    """Menú con opciones avanzadas."""
    
    if not expert_mode:
        return  # Solo mostrar en modo experto
    
    StylizedPrinter.header("Opciones de Experto")
    
    print("  1. Configurar memoria máxima")
    print("  2. Habilitar debug mode")
    print("  3. Cambiar nivel de logging")
    print("  4. Directorio temporal personalizado")
    print("  5. Configurar proxy")
    print("  6. Regenerar índice de búsqueda")
```

### Modo GUI Launcher

```python
def launch_gui_direct():
    """Lanza GUI directamente sin CLI."""
    
    # Verificar Qt disponible
    try:
        from PyQt6.QtWidgets import QApplication
    except ImportError:
        print("Error: Qt no disponible")
        return 1
    
    # Crear aplicación
    app = QApplication(sys.argv)
    app.setApplicationName("Xebec PDF Fixer")
    
    # Importar y mostrar ventana principal
    from src.gui.pyqt6.main_window import MainWindow
    
    window = MainWindow()
    window.show()
    
    return app.exec()
```

## Tablas Formateadas

```python
class Table:
    """Tablas formateadas para CLI."""
    
    def __init__(self, headers: list[str] = None) -> None:
        self.headers = headers or []
        self.rows: list[list[str]] = []
        self.column_widths: list[int] = []
    
    def add_row(self, row: list[str]) -> None:
        self.rows.append(row)
    
    def add_rows(self, data: list[tuple]) -> None:
        for row in data:
            self.add_row(list(row))
    
    def _calculate_widths(self) -> None:
        if self.headers:
            self.column_widths = [len(h) for h in self.headers]
        
        for row in self.rows:
            for idx, cell in enumerate(row):
                width = len(str(cell))
                if idx < len(self.column_widths):
                    self.column_widths[idx] = max(self.column_widths[idx], width)
                else:
                    self.column_widths.append(width)
    
    def print(self) -> None:
        from src.cli.core.colors import Colors
        
        self._calculate_widths()
        
        # Encabezados
        if self.headers:
            header_row = "│ " + " │ ".join(
                h.ljust(w) for h, w in zip(self.headers, self.column_widths)
            ) + " │"
            
            separator = "├─" + "─┼─".join("─" * w for w in self.column_widths) + "─┤"
            
            print(f"{Colors.BOLD}{Colors.CYAN}{separator}{Colors.RESET}")
            print(f"{Colors.BOLD}{Colors.CYAN}{header_row}{Colors.RESET}")
            print(f"{Colors.BOLD}{Colors.CYAN}{separator}{Colors.RESET}")
        
        # Filas
        for row in self.rows:
            row_str = "│ " + " │ ".join(
                str(cell).ljust(w) for cell, w in zip(row, self.column_widths)
            ) + " │"
            print(row_str)
        
        # Footer
        if self.headers:
            print(f"{Colors.BOLD}{Colors.CYAN}{separator}{Colors.RESET}")
```

## Input Interactivo

```python
def ask_yes_no(question: str, default: bool = None) -> bool:
    """Pregunta sí/no interactiva."""
    from src.cli.core.colors import Colors
    
    options = ""
    if default is True:
        options = "[S/n]"
    elif default is False:
        options = "[s/N]"
    else:
        options = "[s/n]"
    
    while True:
        response = input(f"{Colors.CYAN}{question} {options}: {Colors.RESET}").lower().strip()
        
        if not response and default is not None:
            return default
        
        if response in ("s", "si", "sí", "y", "yes"):
            return True
        if response in ("n", "no"):
            return False
        
        print(f"{Colors.YELLOW}Por favor ingresa 's' o 'n'{Colors.RESET}")


def ask_choice(question: str, options: list[str], default: int = None) -> str:
    """Pregunta con opciones múltiples."""
    from src.cli.core.colors import Colors
    
    print(f"\n{Colors.BOLD}{question}{Colors.RESET}\n")
    
    for idx, option in enumerate(options):
        marker = "→" if default == idx else " "
        print(f"  {marker} {idx + 1}. {option}")
    
    while True:
        try:
            response = input(f"\n{Colors.CYAN}Selecciona [1-{len(options)}]: {Colors.RESET}")
            
            if not response and default is not None:
                return options[default]
            
            idx = int(response) - 1
            if 0 <= idx < len(options):
                return options[idx]
                
        except ValueError:
            pass
        
        print(f"{Colors.YELLOW}Opción inválida{Colors.RESET}")
```

## Buenas Prácticas CLI

1. **Código de salida**: Usar 0 para éxito, 1+ para errores
2. **Colores**: Detectar terminal不支持时自动禁用
3. **Atajos**: Implementar navegación por teclado
4. **Ayuda**: Siempre documentar comandos
5. **Logs**: Guardar operaciones en archivo
6. **Perfiles**: Persistir configuración de usuario
7. **Validación**: Verificar argumentos antes de procesar
8. **Mensajes claros**: Error/warning/info diferenciados
9. **Modo batch**: Soportar ejecución no interactiva
10. **Progres bar**: Mostrar progreso en operaciones largas
