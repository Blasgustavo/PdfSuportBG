---
name: skill-corporate-cli-v2
description: Corporate CLI Orchestrator v2 - Interfaces CLI profesionales con menús interactivos, múltiples modos, autocompletado y personalización avanzada
---

## What I do

Diseñador de CLI corporativas de alto nivel. Creo interfaces de línea de comandos profesionales:

- **Menús interactivos avanzados**: Navegación por teclado, selectores visuales, atajos
- **Branding XEBEC**: ASCII art, colores ANSI, banners dinámicos
- **Múltiples modos**: Normal, silencioso, experto, diagnóstico
- **Flujos profesionales**: Instalación, configuración, diagnóstico, automatización
- **Módulos integrados**: PDF operations, GUI launcher, system info, network tools
- **Autocompletado**: Tab completion, sugerencias inteligentes
- **Perfiles**: Configuraciones persistentes, múltiples entornos
- **Logs avanzados**: Rotación, niveles, exportación

## When to use me

Usar cuando se necesite:
- CLI avanzada con múltiples modos de operación
- Sistema de autocompletado
- Perfiles de usuario persistentes
- Diagnóstico profundo del sistema
- Automatización con scripts
- Integración completa con módulos internos

## Arquitectura CLI v2

```
src/cli/
├── __init__.py
├── main.py                     # Entry point
├── core/
│   ├── __init__.py
│   ├── menu.py                # Sistema de menús interactivos
│   ├── colors.py              # Colores y estilos ANSI
│   ├── input.py               # Input interactivo con validación
│   ├── table.py               # Tablas formateadas
│   ├── progress.py            # Barras de progreso
│   ├── completer.py           # Autocompletado
│   └── keyboard.py            # Manejo de teclas
├── commands/
│   ├── __init__.py
│   ├── base.py               # Clase base de comando
│   ├── pdf_commands.py       # Comandos PDF
│   ├── gui_commands.py       # Comandos GUI
│   ├── system_commands.py    # Comandos de sistema
│   ├── config_commands.py    # Configuración
│   └── diagnose_commands.py  # Diagnóstico
├── modes/
│   ├── __init__.py
│   ├── base.py               # Modo base
│   ├── normal_mode.py        # Modo normal
│   ├── quiet_mode.py         # Modo silencioso
│   ├── expert_mode.py        # Modo experto
│   └── diagnose_mode.py      # Modo diagnóstico
├── completion/
│   ├── __init__.py
│   ├── completer.py          # Motor de autocompletado
│   └── completions.py        # Completions predefinidos
├── profiles/
│   ├── __init__.py
│   ├── profile_manager.py    # Gestor de perfiles
│   └── profile.py            # Modelo de perfil
├── launcher.py               # Lanzador principal
└── runner.py                # Ejecutor de comandos
```

## Sistema de Menús v2

```python
from typing import Callable, Optional, Any, List, Dict
from enum import Enum
from dataclasses import dataclass, field
import os
import sys
import tty
import termios


class Key(Enum):
    UP = "\x1b[A"
    DOWN = "\x1b[B"
    RIGHT = "\x1b[C"
    LEFT = "\x1b[D"
    ENTER = "\r"
    ESC = "\x1b"
    TAB = "\t"
    SPACE = " "
    BACKSPACE = "\x7f"


class SelectionMode(Enum):
    SINGLE = "single"
    MULTIPLE = "multiple"
    TOGGLE = "toggle"


@dataclass
class MenuItem:
    """Elemento de menú."""
    label: str
    action: Callable[[], Any]
    shortcut: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    enabled: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MenuSection:
    """Sección de menú con título."""
    title: str
    items: List[MenuItem]
    collapsible: bool = False
    collapsed: bool = False


class InteractiveMenuV2:
    """Sistema de menús interactivos v2 con mejoras."""
    
    def __init__(
        self,
        title: str,
        items: List[MenuItem],
        sections: Optional[List[MenuSection]] = None,
        subtitle: Optional[str] = None,
        banner: Optional[str] = None,
        mode: str = "normal"
    ) -> None:
        self.title = title
        self.items = items
        self.sections = sections or []
        self.subtitle = subtitle
        self.banner = banner
        self.mode = mode
        
        self.selected_index = 0
        self.scroll_offset = 0
        self.running = False
        self.search_query = ""
        self.filtered_items = items
        
        self._max_visible = 20
    
    def _clear_screen(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")
    
    def _get_terminal_size(self) -> tuple:
        return os.get_terminal_size().lines, os.get_terminal_size().columns
    
    def _print_header(self) -> None:
        from src.cli.core.colors import Colors
        
        if self.banner:
            print(self.banner)
            print()
        
        print(f"{Colors.BOLD}{Colors.CYAN}{'═' * 60}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}  {self.title}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'═' * 60}{Colors.RESET}")
        
        if self.subtitle:
            print(f"{Colors.DIM}{self.subtitle}{Colors.RESET}")
        
        if self.search_query:
            print(f"{Colors.YELLOW}🔍 Búsqueda: {self.search_query}{Colors.RESET}")
        
        print()
    
    def _print_items(self) -> None:
        from src.cli.core.colors import Colors
        
        lines, _ = self._get_terminal_size()
        self._max_visible = lines - 15
        
        visible_items = self.filtered_items[
            self.scroll_offset:self.scroll_offset + self._max_visible
        ]
        
        for idx, item in enumerate(visible_items):
            actual_idx = idx + self.scroll_offset
            
            is_selected = actual_idx == self.selected_index
            is_disabled = not item.enabled
            
            prefix = f"{Colors.GREEN}▶{Colors.RESET} " if is_selected else "  "
            
            if is_disabled:
                label_color = Colors.DIM
            elif is_selected:
                label_color = Colors.BOLD + Colors.GREEN
            else:
                label_color = Colors.WHITE
            
            shortcut_str = ""
            if item.shortcut:
                shortcut_str = f"  {Colors.YELLOW}[{item.shortcut}]{Colors.RESET}"
            
            icon_str = f"{item.icon} " if item.icon else ""
            
            line = f"{prefix}{label_color}{icon_str}{item.label}{shortcut_str}{Colors.RESET}"
            
            # Truncar si es muy largo
            if len(line) > 50:
                line = line[:47] + "..."
            
            print(line)
            
            if is_selected and item.description and not is_disabled:
                desc_color = Colors.DIM
                print(f"     {desc_color}{item.description}{Colors.RESET}")
    
    def _print_footer(self) -> None:
        from src.cli.core.colors import Colors
        
        total = len(self.filtered_items)
        current = self.selected_index + 1
        
        print()
        print(f"{Colors.DIM}{'─' * 60}{Colors.RESET}")
        
        help_text = "↑↓ Navegar | Enter Seleccionar"
        
        if self.mode == "expert":
            help_text += " | / Buscar | * Favoritos"
        
        help_text += " | ESC Volver | Q Salir"
        
        print(f"{help_text}  {Colors.CYAN}[{current}/{total}]{Colors.RESET}")
    
    def _print_menu(self) -> None:
        self._clear_screen()
        self._print_header()
        self._print_items()
        self._print_footer()
    
    def _handle_input(self) -> bool:
        try:
            key = self._get_key()
            
            if key == Key.UP:
                self.selected_index = max(0, self.selected_index - 1)
                self._adjust_scroll()
                
            elif key == Key.DOWN:
                self.selected_index = min(
                    len(self.filtered_items) - 1,
                    self.selected_index + 1
                )
                self._adjust_scroll()
                
            elif key == Key.ENTER:
                if self.filtered_items:
                    self._clear_screen()
                    item = self.filtered_items[self.selected_index]
                    if item.enabled:
                        item.action()
                        input(f"\n{Colors.YELLOW}Presiona Enter para continuar...{Colors.RESET}")
            
            elif key == "/" and self.mode == "expert":
                self._handle_search()
            
            elif key.lower() == "q":
                return False
            
            elif key == Key.ESC:
                return False
            
            return True
            
        except (KeyboardInterrupt, EOFError):
            return False
    
    def _handle_search(self) -> None:
        from src.cli.core.colors import Colors
        
        print(f"\n{Colors.CYAN}Búsqueda: {Colors.RESET}", end="")
        self.search_query = input()
        
        if self.search_query:
            self.filtered_items = [
                item for item in self.items
                if self.search_query.lower() in item.label.lower()
            ]
            self.selected_index = 0
        else:
            self.filtered_items = self.items
            self.search_query = ""
    
    def _adjust_scroll(self) -> None:
        if self.selected_index >= self.scroll_offset + self._max_visible:
            self.scroll_offset = self.selected_index - self._max_visible + 1
        elif self.selected_index < self.scroll_offset:
            self.scroll_offset = self.selected_index
    
    def _get_key(self) -> str:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
            
            if ch == "\x1b":
                ch += sys.stdin.read(2)
                
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        
        return ch
    
    def run(self) -> None:
        self.running = True
        
        while self.running:
            self._print_menu()
            self.running = self._handle_input()
        
        self._clear_screen()


class CommandCompleter:
    """Autocompletado de comandos."""
    
    def __init__(self, commands: Dict[str, Any]) -> None:
        self.commands = commands
        self._build_completions()
    
    def _build_completions(self) -> None:
        self.completions = {}
        
        for name, cmd in self.commands.items():
            self.completions[name] = {
                "description": cmd.get("description", ""),
                "aliases": cmd.get("aliases", []),
                "args": cmd.get("args", []),
                "examples": cmd.get("examples", [])
            }
    
    def complete(self, text: str) -> List[str]:
        """Autocompleta texto."""
        if not text:
            return list(self.completions.keys())
        
        matches = [
            name for name in self.completions.keys()
            if name.startswith(text.lower())
        ]
        
        return sorted(matches)
    
    def get_suggestions(self, partial: str) -> List[Dict[str, str]]:
        """Obtiene sugerencias para autocompletado."""
        matches = self.complete(partial)
        
        suggestions = []
        for match in matches[:10]:
            info = self.completions[match]
            suggestions.append({
                "command": match,
                "description": info["description"],
                "preview": f"{match} {' '.join(info['args'])}"
            })
        
        return suggestions
```

## Modos de Operación v2

```python
from abc import ABC, abstractmethod
from typing import Optional, Any, Dict
from pathlib import Path
import argparse


class CLIMode(ABC):
    """Clase base para modos CLI."""
    
    name: str = "base"
    description: str = ""
    
    def __init__(self, cli: "CLILauncher") -> None:
        self.cli = cli
        self.config = cli.config
    
    @abstractmethod
    def execute(self, args: list) -> int:
        """Ejecuta el modo."""
        pass
    
    @abstractmethod
    def get_prompt(self) -> str:
        """Retorna el prompt del modo."""
        pass
    
    def before_execute(self) -> None:
        """Hook antes de ejecutar."""
        pass
    
    def after_execute(self, result: int) -> None:
        """Hook después de ejecutar."""
        pass


class NormalMode(CLIMode):
    """Modo normal - Interactivo con menús."""
    
    name = "normal"
    description = "Modo interactivo normal"
    
    def execute(self, args: list) -> int:
        return self.cli.run_interactive()
    
    def get_prompt(self) -> str:
        from src.cli.core.colors import Colors
        return f"{Colors.CYAN}xebec>{Colors.RESET} "


class QuietMode(CLIMode):
    """Modo silencioso - Sin output innecesario."""
    
    name = "quiet"
    description = "Modo silencioso para scripts"
    
    def execute(self, args: list) -> int:
        from src.cli.core.colors import Colors
        Colors.disable()
        
        return self.cli.execute_command(args)
    
    def get_prompt(self) -> str:
        return ""


class ExpertMode(CLIMode):
    """Modo experto - Más opciones y comandos."""
    
    name = "expert"
    description = "Modo experto con opciones avanzadas"
    
    def __init__(self, cli: "CLILauncher") -> None:
        super().__init__(cli)
        self._show_debug = True
        self._show_hidden = True
    
    def execute(self, args: list) -> int:
        self.cli.set_expert_mode(True)
        return self.cli.run_interactive()
    
    def get_prompt(self) -> str:
        from src.cli.core.colors import Colors
        return f"{Colors.RED}✦{Colors.RESET} {Colors.CYAN}xebec>{Colors.RESET} "
    
    def before_execute(self) -> None:
        from src.cli.core.colors import Colors
        Colors.enable()
        print(f"{Colors.YELLOW}Modo Experto activado{Colors.RESET}")


class DiagnoseMode(CLIMode):
    """Modo diagnóstico - Información detallada del sistema."""
    
    name = "diagnose"
    description = "Modo diagnóstico y debug"
    
    def execute(self, args: list) -> int:
        from src.cli.core.colors import Colors, StylizedPrinter
        
        StylizedPrinter.header("Diagnóstico del Sistema")
        
        diagnostics = self._run_diagnostics()
        
        for category, results in diagnostics.items():
            print(f"\n{Colors.BOLD}{Colors.CYAN}{category}{Colors.RESET}")
            print("─" * 40)
            
            for check, result in results.items():
                status = "✓" if result["status"] else "✗"
                status_color = Colors.GREEN if result["status"] else Colors.RED
                print(f"  {status_color}{status}{Colors.RESET} {check}")
                
                if result.get("details"):
                    print(f"      {Colors.DIM}{result['details']}{Colors.RESET}")
        
        return 0
    
    def get_prompt(self) -> str:
        from src.cli.core.colors import Colors
        return f"{Colors.YELLOW}diag>{Colors.RESET} "
    
    def _run_diagnostics(self) -> Dict[str, Dict[str, Any]]:
        """Ejecuta diagnósticos del sistema."""
        import sys
        import platform
        
        return {
            "Sistema": {
                "Python": {
                    "status": sys.version_info >= (3, 8),
                    "details": sys.version
                },
                "Plataforma": {
                    "status": True,
                    "details": f"{platform.system()} {platform.release()}"
                }
            },
            "Dependencias": {
                "PyQt6": self._check_module("PyQt6"),
                "pypdf": self._check_module("pypdf"),
                "pymupdf": self._check_module("fitz"),
                "Pillow": self._check_module("PIL")
            },
            "Archivos": {
                "Directorio de trabajo": {
                    "status": True,
                    "details": Path.cwd()
                }
            }
        }
    
    def _check_module(self, module_name: str) -> Dict[str, Any]:
        """Verifica si un módulo está instalado."""
        try:
            __import__(module_name)
            return {"status": True, "details": f"✓ {module_name} instalado"}
        except ImportError:
            return {"status": False, "details": f"✗ {module_name} no encontrado"}
```

## Gestor de Perfiles

```python
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Dict, Any, List
import json
from datetime import datetime


@dataclass
class Profile:
    """Perfil de usuario."""
    name: str
    description: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    last_used: Optional[datetime] = None
    
    config: Dict[str, Any] = field(default_factory=dict)
    aliases: Dict[str, str] = field(default_factory=dict)
    favorites: List[str] = field(default_factory=list)
    
    output_format: str = "text"  # text, json, xml
    color_enabled: bool = True
    verbose: bool = False
    
    default_output_dir: Optional[Path] = None
    default_pdf_operation: str = "merge"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "last_used": self.last_used.isoformat() if self.last_used else None,
            "config": self.config,
            "aliases": self.aliases,
            "favorites": self.favorites,
            "output_format": self.output_format,
            "color_enabled": self.color_enabled,
            "verbose": self.verbose,
            "default_output_dir": str(self.default_output_dir) if self.default_output_dir else None,
            "default_pdf_operation": self.default_pdf_operation
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Profile":
        data["created_at"] = datetime.fromisoformat(data["created_at"])
        if data.get("last_used"):
            data["last_used"] = datetime.fromisoformat(data["last_used"])
        if data.get("default_output_dir"):
            data["default_output_dir"] = Path(data["default_output_dir"])
        return cls(**data)


class ProfileManager:
    """Gestor de perfiles de usuario."""
    
    def __init__(self, config_dir: Optional[Path] = None) -> None:
        self.config_dir = config_dir or Path.home() / ".xebec"
        self.profiles_dir = self.config_dir / "profiles"
        self.profiles_dir.mkdir(parents=True, exist_ok=True)
        
        self._profiles: Dict[str, Profile] = {}
        self._current_profile: Optional[str] = None
        self._load_profiles()
    
    def _load_profiles(self) -> None:
        """Carga perfiles del directorio."""
        for profile_file in self.profiles_dir.glob("*.json"):
            try:
                data = json.loads(profile_file.read_text(encoding="utf-8"))
                profile = Profile.from_dict(data)
                self._profiles[profile.name] = profile
            except Exception:
                pass
    
    def create_profile(
        self,
        name: str,
        description: str = "",
        **kwargs
    ) -> Profile:
        """Crea un nuevo perfil."""
        profile = Profile(name=name, description=description, **kwargs)
        self._profiles[name] = profile
        self._save_profile(profile)
        return profile
    
    def switch_profile(self, name: str) -> bool:
        """Cambia al perfil especificado."""
        if name not in self._profiles:
            return False
        
        self._current_profile = name
        profile = self._profiles[name]
        profile.last_used = datetime.now()
        self._save_profile(profile)
        return True
    
    def delete_profile(self, name: str) -> bool:
        """Elimina un perfil."""
        if name not in self._profiles:
            return False
        
        if name == self._current_profile:
            self._current_profile = None
        
        del self._profiles[name]
        
        profile_file = self.profiles_dir / f"{name}.json"
        if profile_file.exists():
            profile_file.unlink()
        
        return True
    
    def get_profile(self, name: Optional[str] = None) -> Optional[Profile]:
        """Obtiene un perfil."""
        if name:
            return self._profiles.get(name)
        return self._profiles.get(self._current_profile)
    
    def list_profiles(self) -> List[Profile]:
        """Lista todos los perfiles."""
        return list(self._profiles.values())
    
    def _save_profile(self, profile: Profile) -> None:
        """Guarda un perfil."""
        profile_file = self.profiles_dir / f"{profile.name}.json"
        profile_file.write_text(
            json.dumps(profile.to_dict(), indent=2),
            encoding="utf-8"
        )


class CLIConfig:
    """Configuración global del CLI."""
    
    def __init__(self) -> None:
        self.config_dir = Path.home() / ".xebec"
        self.config_file = self.config_dir / "config.json"
        
        self.profile_manager = ProfileManager(self.config_dir)
        
        self._load_config()
    
    def _load_config(self) -> None:
        """Carga configuración global."""
        if self.config_file.exists():
            try:
                self._config = json.loads(self.config_file.read_text())
            except:
                self._config = self._default_config()
        else:
            self._config = self._default_config()
    
    def _default_config(self) -> Dict[str, Any]:
        return {
            "mode": "normal",
            "current_profile": "default",
            "log_level": "INFO",
            "log_file": str(self.config_dir / "cli.log"),
            "history_enabled": True,
            "completion_enabled": True,
            "confirm_destructive": True
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        self._config[key] = value
        self._save_config()
    
    def _save_config(self) -> None:
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.config_file.write_text(json.dumps(self._config, indent=2))
```

## Launcher Principal v2

```python
import sys
import argparse
from pathlib import Path
from typing import Optional, Dict, Any
import shlex

from src.cli.core.colors import Colors
from src.cli.modes.normal_mode import NormalMode
from src.cli.modes.quiet_mode import QuietMode
from src.cli.modes.expert_mode import ExpertMode
from src.cli.modes.diagnose_mode import DiagnoseMode
from src.cli.profiles.profile_manager import ProfileManager, CLIConfig
from src.cli.commands.base import Command


class CLILauncher:
    """Lanzador principal del CLI v2."""
    
    def __init__(self) -> None:
        self.config = CLIConfig()
        self.profile_manager = self.config.profile_manager
        
        self.modes = {
            "normal": NormalMode(self),
            "quiet": QuietMode(self),
            "expert": ExpertMode(self),
            "diagnose": DiagnoseMode(self)
        }
        
        self.commands: Dict[str, Command] = {}
        self.completer: Optional[CommandCompleter] = None
        
        self.expert_mode = False
        self.parser = self._build_parser()
    
    def _build_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            prog="xebec",
            description="XEBEC PDF Fixer - CLI Corporativo",
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        
        parser.add_argument("command", nargs="?", help="Comando a ejecutar")
        parser.add_argument("args", nargs=argparse.REMAINDER, help="Argumentos")
        
        parser.add_argument("--mode", "-m", choices=["normal", "quiet", "expert", "diagnose"],
                          help="Modo de operación")
        parser.add_argument("--profile", "-p", help="Perfil a usar")
        parser.add_argument("--quiet", "-q", action="store_true", help="Modo silencioso")
        parser.add_argument("--expert", "-e", action="store_true", help="Modo experto")
        parser.add_argument("--diagnose", "-d", action="store_true", help="Modo diagnóstico")
        parser.add_argument("--version", "-v", action="store_true", help="Versión")
        parser.add_argument("--completion", action="store_true", help="Generar scripts de autocompletado")
        
        return parser
    
    def register_command(self, command: Command) -> None:
        self.commands[command.name] = command
        for alias in command.aliases:
            self.commands[alias] = command
        
        self.completer = CommandCompleter({
            cmd.name: cmd.get_info() for cmd in self.commands.values()
        })
    
    def set_expert_mode(self, enabled: bool) -> None:
        self.expert_mode = enabled
    
    def run(self, args: Optional[list] = None) -> int:
        parsed = self.parser.parse_args(args)
        
        # Versión
        if parsed.version:
            print("XEBEC PDF Fixer v1.0.0")
            return 0
        
        # Completado de shell
        if parsed.completion:
            self._generate_completion()
            return 0
        
        # Determinar modo
        mode_name = parsed.mode
        
        if parsed.quiet:
            mode_name = "quiet"
        elif parsed.expert:
            mode_name = "expert"
        elif parsed.diagnose:
            mode_name = "diagnose"
        
        mode = self.modes.get(mode_name, self.modes["normal"])
        
        # Cambiar perfil si se especificó
        if parsed.profile:
            self.profile_manager.switch_profile(parsed.profile)
        
        # Ejecutar modo
        return mode.execute(parsed.args)
    
    def run_interactive(self) -> int:
        """Ejecuta el modo interactivo."""
        from src.cli.core.menu import InteractiveMenuV2, MenuItem
        from src.cli.core.colors import StylizedPrinter
        
        StylizedPrinter.header("XEBEC PDF Fixer")
        
        items = [
            MenuItem("Operaciones PDF", self._show_pdf_menu, "1", "Unir, dividir, comprimir"),
            MenuItem("Interfaz Gráfica", self._launch_gui, "2", "Abrir aplicación GUI"),
            MenuItem("Diagnóstico", self._run_diagnose, "3", "Verificar sistema"),
            MenuItem("Configuración", self._show_config, "4", "Perfiles y opciones"),
            MenuItem("Ayuda", self._show_help, "h", "Ver ayuda"),
        ]
        
        if self.expert_mode:
            items.insert(0, MenuItem("Modo Experto", lambda: None, "*", "Opciones avanzadas"))
        
        menu = InteractiveMenuV2(
            title="Menú Principal",
            subtitle="Selecciona una opción",
            items=items,
            mode="expert" if self.expert_mode else "normal"
        )
        
        menu.run()
        return 0
    
    def execute_command(self, args: list) -> int:
        """Ejecuta un comando directamente."""
        if not args:
            return 1
        
        cmd_name = args[0]
        cmd_args = args[1:]
        
        if cmd_name in self.commands:
            return self.commands[cmd_name].execute(cmd_args)
        
        print(f"Comando desconocido: {cmd_name}")
        return 1
    
    def _generate_completion(self) -> None:
        """Genera scripts de autocompletado."""
        from src.cli.core.colors import Colors
        
        bash_complete = """
_xebec() {
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    
    opts="merge split compress extract repair gui diagnose help"
    
    COMPREPLY=($(compgen -W "${opts}" -- ${cur}))
    return 0
}
complete -F _xebec xebec
"""
        print(bash_complete)
    
    # Placeholder methods
    def _show_pdf_menu(self) -> None:
        print("Menú de operaciones PDF")
    
    def _launch_gui(self) -> None:
        print("Lanzando GUI...")
    
    def _run_diagnose(self) -> None:
        self.modes["diagnose"].execute([])
    
    def _show_config(self) -> None:
        print("Configuración del CLI")
    
    def _show_help(self) -> None:
        print("Ayuda del CLI")


def main():
    launcher = CLILauncher()
    
    # Registrar comandos
    from src.cli.commands.pdf_commands import MergeCommand, SplitCommand
    from src.cli.commands.gui_commands import GUILaunchCommand
    from src.cli.commands.system_commands import SystemInfoCommand
    
    launcher.register_command(MergeCommand())
    launcher.register_command(SplitCommand())
    launcher.register_command(GUILaunchCommand())
    launcher.register_command(SystemInfoCommand())
    
    sys.exit(launcher.run())


if __name__ == "__main__":
    main()
```

## Árbol de Comandos v2

```
xebec CLI
│
├── MODOS DE OPERACIÓN
│   ├── normal          # Menú interactivo estándar
│   ├── quiet (-q)      # Sin output, para scripts
│   ├── expert (-e)     # Opciones avanzadas, debug
│   └── diagnose (-d)   # Diagnóstico del sistema
│
├── COMANDOS PRINCIPALES
│   ├── pdf
│   │   ├── merge <files> <output>    # Unir PDFs
│   │   ├── split <file> <pages>      # Dividir PDF
│   │   ├── compress <file> [options]  # Comprimir
│   │   ├── extract
│   │   │   ├── pages <file> <range>
│   │   │   ├── text <file>
│   │   │   └── metadata <file>
│   │   ├── repair <file>              # Reparar
│   │   ├── info <file>                # Información
│   │   └── batch <directory>          # Procesamiento por lotes
│   │
│   ├── gui
│   │   ├── launch                      # Abrir GUI
│   │   ├── preview <file>              # Previsualizar
│   │   └── recent                      # Archivos recientes
│   │
│   ├── system
│   │   ├── info                        # Info del sistema
│   │   ├── check                       # Verificar dependencias
│   │   ├── logs                        # Ver logs
│   │   └── clean                       # Limpiar caché
│   │
│   ├── config
│   │   ├── show                        # Mostrar config
│   │   ├── set <key> <value>           # Establecer valor
│   │   ├── profile
│   │   │   ├── list                    # Listar perfiles
│   │   │   ├── create <name>           # Crear perfil
│   │   │   ├── switch <name>           # Cambiar perfil
│   │   │   └── delete <name>           # Eliminar perfil
│   │   └── reset                       # Resetear config
│   │
│   └── help [command]                   # Ayuda
│
├── OPCIONES GLOBALES
│   ├── --mode, -m <mode>    # Seleccionar modo
│   ├── --profile, -p <name> # Perfil a usar
│   ├── --completion         # Generar autocompletado
│   └── --version, -v        # Versión
│
└── EJEMPLOS
    xebec pdf merge a.pdf b.pdf out.pdf
    xebec -e pdf compress huge.pdf --quality=high
    xebec diagnose
    xebec --expert config profile create miperfil
```

## Variantes de Modo

### Modo Silencioso (Quiet)
```bash
xebec -q pdf merge a.pdf b.pdf c.pdf  # Solo código de retorno
echo $?  # 0 = éxito, 1 = error
```

### Modo Experto (Expert)
```bash
xebec -e                              # Menú extendido
xebec -e pdf compress --debug         # Con debug
xebec -e config set log_level DEBUG  # Configuración avanzada
```

### Modo Diagnóstico
```bash
xebec diagnose                        # Diagnóstico completo
xebec -d system check                # Verificar dependencias
xebec -d pdf info documento.pdf      # Info detallada de PDF
```

## Buenas Prácticas CLI v2

1. **Modularidad**: Separar modos en clases independientes
2. **Perfiles**: Guardar configuraciones de usuario
3. **Autocompletado**: Implementar para todos los comandos
4. **Validación**: Verificar argumentos antes de procesar
5. **Logs**: Niveles configurables y rotación
6. **Código de salida**: 0=éxito, 1=error, 2=ayuda
7. **Colors**: Detectar terminal不支持时自动禁用
8. **Historial**: Guardar comandos ejecutados
9. **Sugerencias**: Ofrecer correcciones automáticas
10. **Documentación**: Help integrado en cada comando
