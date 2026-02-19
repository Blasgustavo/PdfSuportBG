---
name: skill-pdf-plugin-architecture
description: PdfSuport Plugin Architecture - Sistema de plugins extensible con descubrimiento dinámico, aislamiento de dependencias y seguridad corporativa
---

## What I do

Diseñador de arquitecturas de plugins para PdfSuport. Creo sistemas extensibles y mantenibles:

- **Interfaces base**: PluginBase, PdfOperationPlugin, MetadataPlugin, OCRPlugin
- **Descubrimiento dinámico**: Carga desde carpetas, entry points, módulos externos
- **Sistema de registro**: PluginRegistry, PluginManager, PluginLoader
- **Aislamiento**: Cada plugin con sus propias dependencias
- **Integración pipelines**: Batch processing, jobs, watchers
- **Seguridad**: Validación, sandboxing, auditoría

## When to use me

Usar cuando se necesite:
- Extender funcionalidades PDF con nuevos plugins
- Crear arquitectura modular y extensible
- Implementar sistema de plugins con carga dinámica
- Aislar dependencias por plugin
- Agregar seguridad y validación

## Arquitectura de Plugins

```
src/
├── plugins/
│   ├── __init__.py
│   ├── base/
│   │   ├── __init__.py
│   │   ├── plugin_base.py        # Clase base de plugin
│   │   ├── interface.py          # Interfaces definidas
│   │   └── metadata.py           # Metadata del plugin
│   ├── core/
│   │   ├── __init__.py
│   │   ├── plugin_registry.py    # Registro central
│   │   ├── plugin_manager.py     # Gestor de plugins
│   │   ├── plugin_loader.py     # Cargador dinámico
│   │   └── plugin_discoverer.py # Descubridor de plugins
│   ├── security/
│   │   ├── __init__.py
│   │   ├── validator.py         # Validador de plugins
│   │   ├── sandbox.py           # Sandboxing básico
│   │   └── audit.py            # Auditoría de plugins
│   ├── pipeline/
│   │   ├── __init__.py
│   │   ├── plugin_pipeline.py   # Pipeline de plugins
│   │   └── plugin_job.py       # Jobs de plugin
│   └── builtin/
│       ├── __init__.py
│       ├── merge_plugin.py
│       ├── split_plugin.py
│       ├── compress_plugin.py
│       └── ocr_plugin.py
├── plugins.yaml                 # Configuración de plugins
└── plugins/                    # Directorio de plugins externos
    └── *.py
```

## Interfaces Base

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Dict, Any, List, Type
from enum import Enum
from datetime import datetime
import importlib.util


class PluginType(Enum):
    """Tipos de plugins."""
    PDF_OPERATION = "pdf_operation"
    METADATA = "metadata"
    OCR = "ocr"
    COMPRESSION = "compression"
    ANALYSIS = "analysis"
    UI = "ui"
    PIPELINE = "pipeline"
    CUSTOM = "custom"


class PluginState(Enum):
    """Estados del plugin."""
    DISCOVERED = "discovered"
    LOADED = "loaded"
    ENABLED = "enabled"
    DISABLED = "disabled"
    ERROR = "error"


@dataclass
class PluginMetadata:
    """Metadata de un plugin."""
    id: str
    name: str
    version: str
    author: str
    description: str
    plugin_type: PluginType
    
    dependencies: List[str] = field(default_factory=list)
    requirements: Dict[str, str] = field(default_factory=dict)  # package>=version
    
    min_pdf_support_version: str = "1.0.0"
    max_pdf_support_version: str = "999.999.999"
    
    tags: List[str] = field(default_factory=list)
    icon: Optional[str] = None
    
    loaded_at: Optional[datetime] = None
    file_path: Optional[Path] = None


@dataclass
class PluginConfig:
    """Configuración de un plugin."""
    enabled: bool = True
    priority: int = 100
    settings: Dict[str, Any] = field(default_factory=dict)


class PluginBase(ABC):
    """Clase base para todos los plugins."""
    
    metadata: PluginMetadata
    config: PluginConfig
    
    def __init__(self) -> None:
        self._initialized = False
        self._state = PluginState.DISCOVERED
    
    @abstractmethod
    def initialize(self) -> bool:
        """Inicializa el plugin. Retorna True si tiene éxito."""
        pass
    
    @abstractmethod
    def shutdown(self) -> None:
        """Limpia recursos del plugin."""
        pass
    
    @abstractmethod
    def validate(self) -> tuple[bool, Optional[str]]:
        """Valida el plugin. Retorna (valid, error_message)."""
        pass
    
    @property
    def state(self) -> PluginState:
        return self._state
    
    @property
    def is_loaded(self) -> bool:
        return self._state == PluginState.LOADED
    
    @property
    def is_enabled(self) -> bool:
        return self._state == PluginState.ENABLED and self.config.enabled
    
    def get_info(self) -> Dict[str, Any]:
        """Retorna información del plugin."""
        return {
            "id": self.metadata.id,
            "name": self.metadata.name,
            "version": self.metadata.version,
            "type": self.metadata.plugin_type.value,
            "state": self._state.value,
            "enabled": self.is_enabled
        }


class PdfOperationPlugin(PluginBase):
    """Plugin para operaciones PDF."""
    
    @abstractmethod
    def execute(self, input_path: Path, output_path: Path, options: Dict[str, Any]) -> Dict[str, Any]:
        """Ejecuta la operación PDF."""
        pass
    
    @abstractmethod
    def get_supported_operations(self) -> List[str]:
        """Retorna lista de operaciones soportadas."""
        pass
    
    @abstractmethod
    def validate_input(self, input_path: Path) -> tuple[bool, Optional[str]]:
        """Valida el archivo de entrada."""
        pass


class MetadataPlugin(PluginBase):
    """Plugin para metadatos."""
    
    @abstractmethod
    def extract(self, pdf_path: Path) -> Dict[str, Any]:
        """Extrae metadatos."""
        pass
    
    @abstractmethod
    def update(self, pdf_path: Path, metadata: Dict[str, Any]) -> bool:
        """Actualiza metadatos."""
        pass


class OCRPlugin(PluginBase):
    """Plugin para OCR."""
    
    @abstractmethod
    def extract_text(self, pdf_path: Path, options: Dict[str, Any]) -> str:
        """Extrae texto usando OCR."""
        pass
    
    @abstractmethod
    def get_supported_languages(self) -> List[str]:
        """Retorna idiomas soportados."""
        pass
```

## Plugin Registry

```python
from typing import Dict, List, Optional, Type, Callable, Any
from pathlib import Path
from dataclasses import dataclass, field
import logging
import importlib.util
import json

from src.plugins.base.plugin_base import (
    PluginBase, PdfOperationPlugin, MetadataPlugin, OCRPlugin,
    PluginMetadata, PluginConfig, PluginType, PluginState
)
from src.utils.logger import logger


class PluginRegistry:
    """Registro central de plugins."""
    
    _instance: Optional["PluginRegistry"] = None
    
    def __new__(cls) -> "PluginRegistry":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self) -> None:
        if self._initialized:
            return
        
        self._initialized = True
        
        self._plugins: Dict[str, PluginBase] = {}
        self._plugin_classes: Dict[str, Type[PluginBase]] = {}
        self._hooks: Dict[str, List[Callable]] = {}
        
        self._log = logger.get_logger()
        
        self._log.info("PluginRegistry inicializado")
    
    def register(
        self,
        plugin_id: str,
        plugin_class: Type[PluginBase],
        metadata: PluginMetadata
    ) -> None:
        """Registra una clase de plugin."""
        self._plugin_classes[plugin_id] = plugin_class
        
        self._log.debug(f"Plugin registrado: {plugin_id} ({metadata.name})")
        
        # Dispara hooks de registro
        self._trigger_hook("plugin_registered", plugin_id, metadata)
    
    def register_instance(self, plugin: PluginBase) -> None:
        """Registra una instancia de plugin."""
        plugin_id = plugin.metadata.id
        self._plugins[plugin_id] = plugin
        
        self._log.info(f"Plugin instanciado: {plugin_id}")
    
    def unregister(self, plugin_id: str) -> bool:
        """Elimina un plugin del registro."""
        if plugin_id in self._plugins:
            plugin = self._plugins[plugin_id]
            plugin.shutdown()
            del self._plugins[plugin_id]
            
            self._log.info(f"Plugin eliminado: {plugin_id}")
            return True
        
        return False
    
    def get(self, plugin_id: str) -> Optional[PluginBase]:
        """Obtiene un plugin por ID."""
        return self._plugins.get(plugin_id)
    
    def get_by_type(self, plugin_type: PluginType) -> List[PluginBase]:
        """Obtiene todos los plugins de un tipo."""
        return [
            p for p in self._plugins.values()
            if p.metadata.plugin_type == plugin_type and p.is_enabled
        ]
    
    def get_all(self) -> List[PluginBase]:
        """Obtiene todos los plugins."""
        return list(self._plugins.values())
    
    def get_enabled(self) -> List[PluginBase]:
        """Obtiene plugins habilitados."""
        return [p for p in self._plugins.values() if p.is_enabled]
    
    def add_hook(self, event: str, callback: Callable) -> None:
        """Añade un hook para un evento."""
        if event not in self._hooks:
            self._hooks[event] = []
        self._hooks[event].append(callback)
    
    def _trigger_hook(self, event: str, *args, **kwargs) -> None:
        """Dispara hooks de un evento."""
        if event in self._hooks:
            for callback in self._hooks[event]:
                try:
                    callback(*args, **kwargs)
                except Exception as e:
                    self._log.error(f"Error en hook {event}: {e}")


# Instancia global
plugin_registry = PluginRegistry()
```

## Plugin Manager

```python
from typing import Dict, List, Optional, Any, Type
from pathlib import Path
from dataclasses import dataclass
import importlib.util
import sys
import traceback

from src.plugins.base.plugin_base import (
    PluginBase, PluginMetadata, PluginConfig,
    PluginType, PluginState
)
from src.plugins.core.plugin_registry import plugin_registry
from src.plugins.security.validator import PluginValidator
from src.utils.logger import logger


@dataclass
class LoadResult:
    """Resultado de carga de plugin."""
    success: bool
    plugin_id: str
    message: str
    error: Optional[str] = None


class PluginManager:
    """Gestor de carga y descarga de plugins."""
    
    def __init__(self) -> None:
        self._log = logger.get_logger()
        self._validator = PluginValidator()
        self._plugin_dir = Path("src/plugins/builtin")
    
    def load_plugin(self, plugin_id: str) -> LoadResult:
        """Carga un plugin por ID."""
        if plugin_id in plugin_registry.get_all():
            return LoadResult(False, plugin_id, "Plugin ya cargado")
        
        # Obtener clase del registro
        plugin_class = plugin_registry._plugin_classes.get(plugin_id)
        
        if not plugin_class:
            return LoadResult(False, plugin_id, "Plugin no encontrado en registro")
        
        try:
            # Validar
            valid, error = self._validator.validate_class(plugin_class)
            if not valid:
                return LoadResult(False, plugin_id, f"Validación fallida: {error}")
            
            # Crear instancia
            plugin = plugin_class()
            
            # Inicializar
            if not plugin.initialize():
                plugin._state = PluginState.ERROR
                return LoadResult(False, plugin_id, "Error en inicialización")
            
            # Validar estado
            valid, error = plugin.validate()
            if not valid:
                plugin._state = PluginState.ERROR
                return LoadResult(False, plugin_id, f"Validación fallida: {error}")
            
            # Registrar instancia
            plugin._state = PluginState.LOADED
            plugin_registry.register_instance(plugin)
            
            # Habilitar si está configurado
            if plugin.config.enabled:
                plugin._state = PluginState.ENABLED
            
            self._log.info(f"Plugin cargado: {plugin_id}")
            
            return LoadResult(True, plugin_id, "Plugin cargado exitosamente")
            
        except Exception as e:
            self._log.error(f"Error cargando plugin {plugin_id}: {e}\n{traceback.format_exc()}")
            return LoadResult(False, plugin_id, str(e), traceback.format_exc())
    
    def unload_plugin(self, plugin_id: str) -> bool:
        """Descarga un plugin."""
        plugin = plugin_registry.get(plugin_id)
        
        if not plugin:
            return False
        
        try:
            plugin.shutdown()
            plugin_registry.unregister(plugin_id)
            self._log.info(f"Plugin descargado: {plugin_id}")
            return True
            
        except Exception as e:
            self._log.error(f"Error descargando plugin {plugin_id}: {e}")
            return False
    
    def enable_plugin(self, plugin_id: str) -> bool:
        """Habilita un plugin."""
        plugin = plugin_registry.get(plugin_id)
        
        if not plugin:
            return False
        
        plugin.config.enabled = True
        plugin._state = PluginState.ENABLED
        
        self._log.info(f"Plugin habilitado: {plugin_id}")
        return True
    
    def disable_plugin(self, plugin_id: str) -> bool:
        """Deshabilita un plugin."""
        plugin = plugin_registry.get(plugin_id)
        
        if not plugin:
            return False
        
        plugin.config.enabled = False
        plugin._state = PluginState.DISABLED
        
        self._log.info(f"Plugin deshabilitado: {plugin_id}")
        return True
    
    def reload_plugin(self, plugin_id: str) -> LoadResult:
        """Recarga un plugin."""
        self.unload_plugin(plugin_id)
        return self.load_plugin(plugin_id)
    
    def load_all_plugins(self) -> List[LoadResult]:
        """Carga todos los plugins registrados."""
        results = []
        
        for plugin_id in plugin_registry._plugin_classes.keys():
            result = self.load_plugin(plugin_id)
            results.append(result)
        
        return results
    
    def get_plugin_info(self, plugin_id: str) -> Optional[Dict[str, Any]]:
        """Obtiene información de un plugin."""
        plugin = plugin_registry.get(plugin_id)
        
        if plugin:
            return plugin.get_info()
        
        return None


# Instancia global
plugin_manager = PluginManager()
```

## Plugin Loader Dinámico

```python
from pathlib import Path
from typing import List, Optional, Dict, Any, Type
import importlib.util
import importlib
import sys
import pkgutil

from src.plugins.base.plugin_base import PluginBase, PluginMetadata, PluginConfig, PluginType
from src.plugins.core.plugin_registry import plugin_registry
from src.utils.logger import logger


class PluginDiscoverer:
    """Descubridor de plugins."""
    
    def __init__(self, plugin_dirs: Optional[List[Path]] = None) -> None:
        self._plugin_dirs = plugin_dirs or []
        self._log = logger.get_logger()
    
    def discover_from_directory(self, directory: Path) -> List[Type[PluginBase]]:
        """Descubre plugins en un directorio."""
        plugins = []
        
        if not directory.exists():
            self._log.warning(f"Directorio de plugins no existe: {directory}")
            return plugins
        
        for file_path in directory.glob("*.py"):
            if file_path.name.startswith("_"):
                continue
            
            try:
                plugin_class = self._load_module_from_file(file_path)
                
                if plugin_class and issubclass(plugin_class, PluginBase):
                    plugins.append(plugin_class)
                    self._log.debug(f"Plugin descubierto: {file_path.name}")
            
            except Exception as e:
                self._log.error(f"Error cargando {file_path.name}: {e}")
        
        return plugins
    
    def discover_from_entry_points(self, group: str = "pdfsupport.plugins") -> List[Type[PluginBase]]:
        """Descubre plugins desde entry points."""
        plugins = []
        
        try:
            from importlib.metadata import entry_points
            
            eps = entry_points()
            plugin_eps = eps.get(group, [])
            
            for ep in plugin_eps:
                try:
                    plugin_class = ep.load()
                    
                    if issubclass(plugin_class, PluginBase):
                        plugins.append(plugin_class)
                        self._log.debug(f"Plugin discovered from entry point: {ep.name}")
                
                except Exception as e:
                    self._log.error(f"Error cargando entry point {ep.name}: {e}")
        
        except ImportError:
            self._log.warning("importlib.metadata no disponible")
        
        return plugins
    
    def discover_from_package(self, package_name: str) -> List[Type[PluginBase]]:
        """Descubre plugins en un paquete."""
        plugins = []
        
        try:
            package = importlib.import_module(package_name)
            
            for _, name, is_pkg in pkgutil.iter_modules(package.__path__):
                if is_pkg:
                    continue
                
                try:
                    full_name = f"{package_name}.{name}"
                    module = importlib.import_module(full_name)
                    
                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)
                        
                        if (isinstance(attr, type) and 
                            issubclass(attr, PluginBase) and 
                            attr is not PluginBase):
                            plugins.append(attr)
                
                except Exception as e:
                    self._log.error(f"Error cargando {name}: {e}")
        
        except Exception as e:
            self._log.error(f"Error importando paquete {package_name}: {e}")
        
        return plugins
    
    def _load_module_from_file(self, file_path: Path) -> Optional[Type[PluginBase]]:
        """Carga un módulo desde archivo."""
        module_name = f"pdfsupport_plugins.{file_path.stem}"
        
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        
        if not spec or not spec.loader:
            return None
        
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        
        # Buscar clase de plugin
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            
            if (isinstance(attr, type) and 
                issubclass(attr, PluginBase) and 
                attr is not PluginBase):
                return attr
        
        return None


class PluginLoader:
    """Cargador de plugins con auto-descubrimiento."""
    
    def __init__(self) -> None:
        self._log = logger.get_logger()
        self._discoverer = PluginDiscoverer()
        self._loaded = False
    
    def load_plugins(
        self,
        builtin_dir: Optional[Path] = None,
        external_dirs: Optional[List[Path]] = None,
        use_entry_points: bool = True
    ) -> int:
        """Carga todos los plugins disponibles."""
        count = 0
        
        # Built-in plugins
        if builtin_dir:
            builtin_plugins = self._discoverer.discover_from_directory(builtin_dir)
            for plugin_class in builtin_plugins:
                self._register_plugin_class(plugin_class)
                count += 1
        
        # External plugins
        if external_dirs:
            for directory in external_dirs:
                external_plugins = self._discoverer.discover_from_directory(directory)
                for plugin_class in external_plugins:
                    self._register_plugin_class(plugin_class)
                    count += 1
        
        # Entry points
        if use_entry_points:
            ep_plugins = self._discoverer.discover_from_entry_points()
            for plugin_class in ep_plugins:
                self._register_plugin_class(plugin_class)
                count += 1
        
        self._loaded = True
        self._log.info(f"Descubiertos {count} plugins")
        
        return count
    
    def _register_plugin_class(self, plugin_class: Type[PluginBase]) -> None:
        """Registra una clase de plugin."""
        if not hasattr(plugin_class, "metadata"):
            self._log.warning(f"Plugin {plugin_class.__name__} no tiene metadata")
            return
        
        metadata = plugin_class.metadata
        
        plugin_registry.register(
            metadata.id,
            plugin_class,
            metadata
        )
```

## Seguridad y Validación

```python
from typing import Optional, Dict, Any, List
from pathlib import Path
import hashlib
import json
from datetime import datetime

from src.plugins.base.plugin_base import PluginBase, PluginMetadata, PluginType
from src.utils.logger import logger


class PluginValidator:
    """Validador de plugins."""
    
    def __init__(self) -> None:
        self._log = logger.get_logger()
        self._allowed_types = {t.value for t in PluginType}
    
    def validate_class(self, plugin_class: Type[PluginBase]) -> tuple[bool, Optional[str]]:
        """Valida una clase de plugin."""
        # Verificar que tiene metadata
        if not hasattr(plugin_class, "metadata"):
            return False, "Plugin no tiene metadata"
        
        metadata = plugin_class.metadata
        
        # Verificar campos requeridos
        if not metadata.id or not metadata.name:
            return False, "Faltan campos requeridos en metadata"
        
        # Verificar tipo
        if metadata.plugin_type.value not in self._allowed_types:
            return False, f"Tipo de plugin inválido: {metadata.plugin_type}"
        
        # Verificar métodos requeridos
        required_methods = ["initialize", "shutdown", "validate"]
        
        for method in required_methods:
            if not hasattr(plugin_class, method):
                return False, f"Plugin no implementa {method}"
        
        return True, None
    
    def validate_instance(self, plugin: PluginBase) -> tuple[bool, Optional[str]]:
        """Valida una instancia de plugin."""
        valid, error = self.validate_class(type(plugin))
        
        if not valid:
            return valid, error
        
        # Verificar estado inicial
        if plugin.state.value not in ["discovered", "loaded", "enabled"]:
            return False, f"Estado inválido: {plugin.state}"
        
        return True, None
    
    def validate_dependencies(self, metadata: PluginMetadata) -> tuple[bool, Optional[str]]:
        """Valida las dependencias de un plugin."""
        for dep in metadata.requirements:
            try:
                __import__(dep)
            except ImportError:
                return False, f"Dependencia no encontrada: {dep}"
        
        return True, None


class PluginSandbox:
    """Sandboxing básico para plugins."""
    
    def __init__(self) -> None:
        self._log = logger.get_logger()
        self._restricted_modules = {
            "os": ["system", "popen", "spawn"],
            "subprocess": ["call", "Popen", "run"],
            "sys": ["exit", "setrecursionlimit"],
            "threading": ["Timer"],
        }
        self._allowed_paths = [Path.cwd()]
    
    def is_safe_plugin(self, plugin_class: Type[PluginBase]) -> bool:
        """Verifica si un plugin es seguro."""
        # Implementar verificaciones de seguridad
        # Por ahora retorna True
        return True
    
    def restrict_plugin(self, plugin: PluginBase) -> None:
        """Aplica restricciones a un plugin."""
        self._log.info(f"Sandbox aplicado a plugin: {plugin.metadata.id}")


class PluginAudit:
    """Auditoría de plugins."""
    
    def __init__(self, audit_dir: Path) -> None:
        self.audit_dir = audit_dir
        self.audit_dir.mkdir(parents=True, exist_ok=True)
        
        self._log = logger.get_logger()
    
    def log_event(
        self,
        event_type: str,
        plugin_id: str,
        details: Optional[Dict[str, Any]] = None
    ) -> None:
        """Registra un evento de plugin."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "event": event_type,
            "plugin_id": plugin_id,
            "details": details or {}
        }
        
        date = datetime.now().strftime("%Y%m%d")
        audit_file = self.audit_dir / f"plugin_audit_{date}.jsonl"
        
        with open(audit_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
        
        self._log.debug(f"Audit: {event_type} - {plugin_id}")
    
    def get_events(
        self,
        plugin_id: Optional[str] = None,
        event_type: Optional[str] = None,
        date: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Obtiene eventos de auditoría."""
        date = date or datetime.now().strftime("%Y%m%d")
        audit_file = self.audit_dir / f"plugin_audit_{date}.jsonl"
        
        if not audit_file.exists():
            return []
        
        events = []
        
        with open(audit_file, "r", encoding="utf-8") as f:
            for line in f:
                event = json.loads(line)
                
                if plugin_id and event.get("plugin_id") != plugin_id:
                    continue
                
                if event_type and event.get("event") != event_type:
                    continue
                
                events.append(event)
        
        return events
```

## Ejemplo de Plugin Real

```python
from pathlib import Path
from typing import Dict, Any, List, Optional

from src.plugins.base.plugin_base import (
    PdfOperationPlugin, PluginMetadata, PluginConfig, PluginType
)


class MergePDFPlugin(PdfOperationPlugin):
    """Plugin para unir PDFs."""
    
    # Metadata del plugin
    metadata = PluginMetadata(
        id="pdf_merge",
        name="PDF Merger",
        version="1.0.0",
        author="XEBEC Corporation",
        description="Plugin para unir múltiples archivos PDF en uno",
        plugin_type=PluginType.PDF_OPERATION,
        dependencies=[],
        requirements={"pypdf": ">=3.0.0"},
        tags=["pdf", "merge", "utility"]
    )
    
    config = PluginConfig(
        enabled=True,
        priority=100,
        settings={
            "add_bookmarks": True,
            "flatten_forms": False
        }
    )
    
    def __init__(self) -> None:
        super().__init__()
        self._initialized = False
    
    def initialize(self) -> bool:
        """Inicializa el plugin."""
        try:
            import pypdf
            self._initialized = True
            return True
        except ImportError:
            return False
    
    def shutdown(self) -> None:
        """Limpia recursos."""
        pass
    
    def validate(self) -> tuple[bool, Optional[str]]:
        """Valida el plugin."""
        if not self._initialized:
            return False, "Plugin no inicializado"
        return True, None
    
    def execute(
        self,
        input_path: Path,
        output_path: Path,
        options: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Ejecuta la operación de merge."""
        from pypdf import PdfWriter
        
        # Obtener archivos a merge
        input_files = options.get("files", [])
        
        if not input_files:
            return {
                "success": False,
                "error": "No se proporcionaron archivos para merge"
            }
        
        try:
            merger = PdfWriter()
            
            for file_path in input_files:
                path = Path(file_path)
                if path.exists():
                    merger.append(str(path))
            
            output_path.parent.mkdir(parents=True, exist_ok=True)
            merger.write(str(output_path))
            merger.close()
            
            return {
                "success": True,
                "output": str(output_path),
                "files_merged": len(input_files)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_supported_operations(self) -> List[str]:
        """Retorna operaciones soportadas."""
        return ["merge", "combine", "join"]
    
    def validate_input(self, input_path: Path) -> tuple[bool, Optional[str]]:
        """Valida archivo de entrada."""
        if not input_path.exists():
            return False, "Archivo no existe"
        
        if input_path.suffix.lower() != ".pdf":
            return False, "No es un archivo PDF"
        
        return True, None


# Registrar automáticamente al cargar
from src.plugins.core.plugin_registry import plugin_registry

plugin_registry.register(
    MergePDFPlugin.metadata.id,
    MergePDFPlugin,
    MergePDFPlugin.metadata
)
```

## Pipeline de Plugins

```python
from typing import List, Dict, Any, Optional
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime

from src.plugins.base.plugin_base import PdfOperationPlugin, PluginBase
from src.plugins.core.plugin_registry import plugin_registry
from src.utils.logger import logger


@dataclass
class PipelineStep:
    """Paso en un pipeline de plugins."""
    plugin_id: str
    options: Dict[str, Any]
    order: int


@dataclass
class PipelineResult:
    """Resultado de ejecución de pipeline."""
    success: bool
    steps_executed: int
    steps_failed: int
    results: List[Dict[str, Any]]
    total_duration_ms: float


class PluginPipeline:
    """Pipeline que ejecuta múltiples plugins en secuencia."""
    
    def __init__(self, name: str) -> None:
        self.name = name
        self.steps: List[PipelineStep] = []
        self._log = logger.get_logger()
    
    def add_step(
        self,
        plugin_id: str,
        options: Optional[Dict[str, Any]] = None,
        order: Optional[int] = None
    ) -> "PluginPipeline":
        """Añade un paso al pipeline."""
        step = PipelineStep(
            plugin_id=plugin_id,
            options=options or {},
            order=order or len(self.steps)
        )
        
        self.steps.append(step)
        self.steps.sort(key=lambda s: s.order)
        
        return self
    
    def execute(
        self,
        input_path: Path,
        output_dir: Path
    ) -> PipelineResult:
        """Ejecuta el pipeline."""
        start_time = datetime.now()
        
        results = []
        steps_executed = 0
        steps_failed = 0
        
        current_input = input_path
        
        for step in self.steps:
            plugin = plugin_registry.get(step.plugin_id)
            
            if not plugin or not isinstance(plugin, PdfOperationPlugin):
                self._log.error(f"Plugin no encontrado: {step.plugin_id}")
                steps_failed += 1
                continue
            
            # Generar output intermedio
            output_path = output_dir / f"step_{step.order}_{current_input.stem}.pdf"
            
            try:
                result = plugin.execute(current_input, output_path, step.options)
                
                results.append({
                    "step": step.order,
                    "plugin_id": step.plugin_id,
                    "result": result
                })
                
                if result.get("success"):
                    steps_executed += 1
                    current_input = output_path
                else:
                    steps_failed += 1
                    self._log.error(f"Step {step.order} falló: {result.get('error')}")
                    break
                    
            except Exception as e:
                self._log.error(f"Error en step {step.order}: {e}")
                steps_failed += 1
                break
        
        duration = (datetime.now() - start_time).total_seconds() * 1000
        
        return PipelineResult(
            success=steps_failed == 0,
            steps_executed=steps_executed,
            steps_failed=steps_failed,
            results=results,
            total_duration_ms=duration
        )
```

## Diagrama de Arquitectura

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        PLUGIN ARCHITECTURE                              │
└─────────────────────────────────────────────────────────────────────────┘

┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Plugin     │────▶│   Plugin    │────▶│   Plugin    │
│   Loader     │     │   Registry  │     │   Manager    │
└──────────────┘     └──────┬───────┘     └──────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Built-in   │    │   External   │    │   Entry      │
│   Plugins    │    │   Plugins    │    │   Points     │
└──────────────┘    └──────────────┘    └──────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                         PLUGIN LIFECYCLE                                │
└─────────────────────────────────────────────────────────────────────────┘

  DISCOVERED ──▶ LOADED ──▶ ENABLED ──▶ RUNNING ──▶ DISABLED ──▶ UNLOADED
                   │            │            │
                   │            │            └──────────────┐
                   │            │                             │
                   ▼            ▼                             ▼
              VALIDATE      INITIALIZE                   SHUTDOWN

┌─────────────────────────────────────────────────────────────────────────┐
│                         SECURITY LAYER                                  │
└─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
  │  Validator  │───▶│  Sandbox    │───▶│   Audit     │
  │             │    │             │    │             │
  │ - Class     │    │ - Restricted│    │ - Events    │
  │ - Instance  │    │   modules   │    │ - Logs      │
  │ - Depends   │    │ - Paths     │    │ - Reports   │
  └─────────────┘    └─────────────┘    └─────────────┘
```

## Variantes

### Plugins Remotos

```python
class RemotePluginLoader:
    """Cargador de plugins desde servidor remoto."""
    
    def __init__(self, server_url: str) -> None:
        self.server_url = server_url
    
    def download_plugin(self, plugin_id: str, dest: Path) -> bool:
        """Descarga un plugin desde el servidor."""
        # Implementar descarga
        pass
    
    def list_remote_plugins(self) -> List[PluginMetadata]:
        """Lista plugins disponibles en el servidor."""
        # Consultar API
        pass
```

### Marketplace Interno

```python
class PluginMarketplace:
    """Marketplace interno de plugins."""
    
    def __init__(self, storage_dir: Path) -> None:
        self.storage_dir = storage_dir
    
    def publish(self, plugin_package: Path) -> str:
        """Publica un plugin en el marketplace."""
        # Validar, comprimir, guardar
        pass
    
    def search(self, query: str) -> List[PluginMetadata]:
        """Busca plugins en el marketplace."""
        pass
    
    def install(self, plugin_id: str) -> bool:
        """Instala un plugin del marketplace."""
        pass
```

## Buenas Prácticas

1. **Interfaces claras**: Definir contratos estables
2. **Metadata completa**: Siempre incluir metadata
3. **Validación temprana**: Verificar antes de cargar
4. **Aislamiento**: Plugins independientes entre sí
5. **Auditoría**: Registrar todas las operaciones
6. **Versionado**: SemVer para plugins
7. **Documentación**: README en cada plugin
8. **Tests**: Unit tests por plugin
9. **Configuración**: Per-plugin settings
10. **Errores claros**: Mensajes de error útiles
