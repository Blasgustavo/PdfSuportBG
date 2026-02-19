---
name: skill-pdf-automation-v2
description: PdfSuport Automation Engine v2 - Motor de automatización PDF avanzado con arquitectura modular, pipelines corporativos, OCR y procesamiento por lotes
---

## What I do

Diseñador y mantenedor del motor de automatización PDF. Creo arquitecturas limpias y modulares:

- **Operaciones PDF avanzadas**: merge, split, extract, repair, compress, OCR
- **Arquitectura modular**: core/, services/, pipelines/, adapters/, workers/
- **Pipelines corporativos**: batch processing, watchers, jobs, reportes
- **Integración moderna**: pypdf, pymupdf, pdfminer, tesseract OCR
- **Manejo de errores**: logs estructurados, auditoría, validación, fallback

## When to use me

Usar cuando se necesite:
- Nuevas operaciones PDF en el motor core
- Procesamiento por lotes avanzado
- Pipelines de automatización complejos
- Integración OCR
- Compresión avanzada de PDFs
- Reportes y auditoría

## Arquitectura Propuesta v2

```
src/
├── core/                          # Motor base
│   ├── __init__.py
│   ├── pdf_base.py               # Clase base abstracta
│   ├── pdf_factory.py            # Factory de operaciones
│   └── constants.py              # Constantes y configuraciones
│
├── services/                      # Servicios de negocio
│   ├── __init__.py
│   ├── merge/
│   │   ├── __init__.py
│   │   ├── merge_service.py      # Servicio de merge
│   │   └── merge_options.py     # Opciones de merge
│   ├── split/
│   │   ├── __init__.py
│   │   ├── split_service.py
│   │   └── split_options.py
│   ├── extract/
│   │   ├── __init__.py
│   │   ├── page_extractor.py
│   │   ├── text_extractor.py
│   │   └── metadata_extractor.py
│   ├── repair/
│   │   ├── __init__.py
│   │   └── repair_service.py
│   ├── compress/
│   │   ├── __init__.py
│   │   ├── compress_service.py
│   │   └── compression_strategy.py
│   └── batch/
│       ├── __init__.py
│       ├── batch_processor.py
│       └── batch_job.py
│
├── adapters/                      # Adaptadores de librerías
│   ├── __init__.py
│   ├── pypdf_adapter.py
│   ├── pymupdf_adapter.py
│   ├── pdfminer_adapter.py
│   └── ocr_adapter.py
│
├── pipelines/                     # Pipelines de automatización
│   ├── __init__.py
│   ├── base.py                   # Clase base de pipeline
│   ├── pipeline_builder.py       # Builder de pipelines
│   ├── watchers/
│   │   ├── __init__.py
│   │   ├── file_watcher.py
│   │   └── watcher_handler.py
│   └── reporters/
│       ├── __init__.py
│       ├── json_reporter.py
│       ├── html_reporter.py
│       └── pdf_reporter.py
│
├── workers/                       # Workers Qt
│   ├── __init__.py
│   ├── base_worker.py
│   ├── merge_worker.py
│   └── batch_worker.py
│
└── utils/
    ├── __init__.py
    ├── validators.py              # Validadores de archivos
    ├── audit.py                  # Sistema de auditoría
    └── cache.py                   # Cache de operaciones
```

## Clase Base y Factory

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple
from enum import Enum
import hashlib
import json
from datetime import datetime

from src.utils.logger import logger


class OperationType(Enum):
    """Tipos de operaciones PDF."""
    MERGE = "merge"
    SPLIT = "split"
    EXTRACT_PAGES = "extract_pages"
    EXTRACT_TEXT = "extract_text"
    EXTRACT_METADATA = "extract_metadata"
    REPAIR = "repair"
    COMPRESS = "compress"
    ENCRYPT = "encrypt"
    DECRYPT = "decrypt"
    ROTATE = "rotate"
    WATERMARK = "watermark"


class OperationStatus(Enum):
    """Estados de operación."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class PDFOperationResult:
    """Resultado de una operación PDF."""
    success: bool
    message: str
    output_path: Optional[Path] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    duration_ms: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "message": self.message,
            "output_path": str(self.output_path) if self.output_path else None,
            "metadata": self.metadata,
            "error": self.error,
            "duration_ms": self.duration_ms
        }


@dataclass
class OperationOptions:
    """Opciones base para operaciones."""
    validate_input: bool = True
    create_backup: bool = False
    overwrite_output: bool = False
    preserve_metadata: bool = True


class PDFOperationBase(ABC):
    """Clase base abstracta para operaciones PDF."""
    
    operation_type: OperationType
    
    def __init__(self) -> None:
        self._logger = logger.get_logger()
    
    @abstractmethod
    def execute(
        self,
        input_path: Path,
        output_path: Path,
        options: Optional[OperationOptions] = None
    ) -> PDFOperationResult:
        """Ejecuta la operación PDF."""
        pass
    
    @abstractmethod
    def validate(self, input_path: Path) -> Tuple[bool, Optional[str]]:
        """Valida los archivos de entrada."""
        pass
    
    def _create_result(
        self,
        success: bool,
        message: str,
        output_path: Optional[Path] = None,
        error: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> PDFOperationResult:
        """Crea un resultado estandarizado."""
        return PDFOperationResult(
            success=success,
            message=message,
            output_path=output_path,
            error=error,
            metadata=metadata or {}
        )


class PDFFactory:
    """Factory para crear operaciones PDF."""
    
    _operations: Dict[OperationType, type] = {}
    
    @classmethod
    def register(cls, operation_type: OperationType, operation_class: type) -> None:
        """Registra una operación."""
        cls._operations[operation_type] = operation_class
        cls._logger.debug(f"Operación registrada: {operation_type.value}")
    
    @classmethod
    def create(cls, operation_type: OperationType) -> PDFOperationBase:
        """Crea una instancia de operación."""
        if operation_type not in cls._operations:
            raise ValueError(f"Operación no registrada: {operation_type}")
        
        return cls._operations[operation_type]()
    
    @classmethod
    def get_available_operations(cls) -> List[OperationType]:
        """Retorna lista de operaciones disponibles."""
        return list(cls._operations.keys())
```

## Servicio de Merge v2

```python
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Tuple
import time

from src.core.pdf_base import (
    PDFOperationBase, OperationType, OperationOptions,
    PDFOperationResult, PDFFactory
)
from src.utils.validators import PDFValidator


@dataclass
class MergeOptions(OperationOptions):
    """Opciones específicas para merge."""
    sort_by_name: bool = False
    add_bookmarks: bool = True
    flatten_forms: bool = False
    allow_duplicates: bool = True


@dataclass
class MergeProgress:
    """Progreso de operación merge."""
    current: int = 0
    total: int = 0
    current_file: str = ""
    percentage: float = 0.0


class MergeService(PDFOperationBase):
    """Servicio para unir múltiples PDFs."""
    
    operation_type = OperationType.MERGE
    
    def __init__(self) -> None:
        super().__init__()
        self._progress_callback: Optional[callable] = None
    
    def set_progress_callback(self, callback: callable) -> None:
        """Configura callback de progreso."""
        self._progress_callback = callback
    
    def execute(
        self,
        input_paths: List[Path],
        output_path: Path,
        options: Optional[MergeOptions] = None
    ) -> PDFOperationResult:
        """Une múltiples PDFs en uno solo."""
        start_time = time.time()
        
        options = options or MergeOptions()
        
        # Validar inputs
        if options.validate_input:
            valid, error = self.validate_inputs(input_paths)
            if not valid:
                return self._create_result(False, error, error=error)
        
        # Validar output
        if output_path.exists() and not options.overwrite_output:
            return self._create_result(
                False,
                f"El archivo ya existe: {output_path}",
                error="output_exists"
            )
        
        try:
            from pypdf import PdfWriter
            
            merger = PdfWriter()
            
            # Ordenar si es necesario
            if options.sort_by_name:
                input_paths = sorted(input_paths, key=lambda p: p.name)
            
            total = len(input_paths)
            
            for idx, path in enumerate(input_paths):
                # Callback de progreso
                if self._progress_callback:
                    self._progress_callback(MergeProgress(
                        current=idx + 1,
                        total=total,
                        current_file=path.name,
                        percentage=((idx + 1) / total) * 100
                    ))
                
                merger.append(str(path), import_outline=options.add_bookmarks)
                
                self._logger.info(f"Añadido {idx + 1}/{total}: {path.name}")
            
            # Opciones adicionales
            if options.flatten_forms:
                # flatten forms
                pass
            
            # Escribir resultado
            output_path.parent.mkdir(parents=True, exist_ok=True)
            merger.write(str(output_path))
            merger.close()
            
            duration_ms = (time.time() - start_time) * 1000
            
            original_size = sum(p.stat().st_size for p in input_paths)
            output_size = output_path.stat().st_size
            
            self._logger.info(
                f"Merge completado: {output_path.name} "
                f"({len(input_paths)} archivos, {duration_ms:.0f}ms)"
            )
            
            return self._create_result(
                True,
                f"PDFs combinados: {len(input_paths)} archivos",
                output_path=output_path,
                metadata={
                    "files_merged": len(input_paths),
                    "original_size": original_size,
                    "output_size": output_size,
                    "compression_ratio": 1 - (output_size / original_size) if original_size > 0 else 0
                }
            )
            
        except Exception as e:
            self._logger.error(f"Error en merge: {e}")
            return self._create_result(
                False,
                f"Error al combinar PDFs: {str(e)}",
                error=str(e)
            )
    
    def validate_inputs(self, input_paths: List[Path]) -> Tuple[bool, Optional[str]]:
        """Valida archivos de entrada."""
        if not input_paths:
            return False, "No se proporcionaron archivos"
        
        if len(input_paths) < 2:
            return False, "Se requieren al menos 2 archivos para merge"
        
        validator = PDFValidator()
        
        for path in input_paths:
            valid, error = validator.validate(path)
            if not valid:
                return False, f"Archivo inválido: {path.name} - {error}"
        
        return True, None
    
    def validate(self, input_path: Path) -> Tuple[bool, Optional[str]]:
        """Valida un solo archivo (implementación de base)."""
        validator = PDFValidator()
        return validator.validate(input_path)


# Registrar en factory
PDFFactory.register(OperationType.MERGE, MergeService)
```

## Servicio de Extracción de Texto v2

```python
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple
import re

from src.core.pdf_base import (
    PDFOperationBase, OperationType, OperationOptions,
    PDFOperationResult
)
from src.utils.validators import PDFValidator


@dataclass
class ExtractTextOptions(OperationOptions):
    """Opciones para extracción de texto."""
    method: str = "auto"  # auto, pypdf, pdfminer, ocr
    password: Optional[str] = None
    pages: Optional[List[int]] = None  # None = todas
    preserve_layout: bool = True
    strip_html: bool = True
    min_confidence: float = 0.5  # Para OCR


class TextExtractService(PDFOperationBase):
    """Servicio para extraer texto de PDFs."""
    
    operation_type = OperationType.EXTRACT_TEXT
    
    def __init__(self) -> None:
        super().__init__()
    
    def execute(
        self,
        input_path: Path,
        output_path: Optional[Path] = None,
        options: Optional[ExtractTextOptions] = None
    ) -> PDFOperationResult:
        """Extrae texto de un PDF."""
        options = options or ExtractTextOptions()
        
        valid, error = self.validate(input_path)
        if not valid:
            return self._create_result(False, error or "PDF inválido", error=error)
        
        try:
            text = ""
            
            # Seleccionar método
            if options.method == "auto":
                text = self._extract_auto(input_path, options)
            elif options.method == "pypdf":
                text = self._extract_with_pypdf(input_path, options)
            elif options.method == "pdfminer":
                text = self._extract_with_pdfminer(input_path, options)
            elif options.method == "ocr":
                text = self._extract_with_ocr(input_path, options)
            
            # Guardar si hay output path
            if output_path:
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_text(text, encoding="utf-8")
                
                return self._create_result(
                    True,
                    f"Texto extraído: {len(text)} caracteres",
                    output_path=output_path,
                    metadata={"characters": len(text), "words": len(text.split())}
                )
            
            return self._create_result(
                True,
                f"Texto extraído: {len(text)} caracteres",
                metadata={"characters": len(text), "words": len(text.split()), "text": text}
            )
            
        except Exception as e:
            self._logger.error(f"Error extrayendo texto: {e}")
            return self._create_result(False, str(e), error=str(e))
    
    def _extract_auto(self, input_path: Path, options: ExtractTextOptions) -> str:
        """Selecciona método automáticamente."""
        # Intentar pypdf primero (más rápido)
        try:
            text = self._extract_with_pypdf(input_path, options)
            if text.strip():
                return text
        except:
            pass
        
        # Intentar pdfminer
        try:
            text = self._extract_with_pdfminer(input_path, options)
            if text.strip():
                return text
        except:
            pass
        
        # Fallback a OCR
        if options.method != "ocr":
            self._logger.warning("Usando OCR como fallback")
        
        return self._extract_with_ocr(input_path, options)
    
    def _extract_with_pypdf(self, input_path: Path, options: ExtractTextOptions) -> str:
        """Extrae usando pypdf."""
        from pypdf import PdfReader
        
        reader = PdfReader(str(input_path))
        text_parts = []
        
        pages = options.pages or range(len(reader.pages))
        
        for page_num in pages:
            if page_num >= len(reader.pages):
                break
            
            page = reader.pages[page_num]
            text = page.extract_text()
            
            if text:
                text_parts.append(text)
        
        return "\n\n".join(text_parts)
    
    def _extract_with_pdfminer(self, input_path: Path, options: ExtractTextOptions) -> str:
        """Extrae usando pdfminer.six."""
        from pdfminer.high_level import extract_text
        
        page_numbers = options.pages
        text = extract_text(str(input_path), page_numbers=page_numbers)
        
        if options.strip_html:
            # Limpiar caracteres HTML
            text = re.sub(r'<[^>]+>', '', text)
        
        return text
    
    def _extract_with_ocr(self, input_path: Path, options: ExtractTextOptions) -> str:
        """Extrae usando OCR (Tesseract)."""
        try:
            import pytesseract
            from pypdf import PdfReader
            from PIL import Image
            import io
        except ImportError:
            return "OCR no disponible. Instala pytesseract y pillow."
        
        reader = PdfReader(str(input_path))
        text_parts = []
        
        pages = options.pages or range(len(reader.pages))
        
        for page_num in pages:
            if page_num >= len(reader.pages):
                break
            
            page = reader.pages[page_num]
            
            # Verificar si tiene texto
            if "/XObject" in page["/Resources"]:
                xobjects = page["/Resources"]["/XObject"].get_object()
                has_images = any(obj["/Subtype"] == "/Image" for obj in xobjects.values())
                
                if not has_images:
                    continue
            
            # OCR en la página
            try:
                pix = page.get_thumbnail(size=(2000, 2000))
                img = pix.to_image()
                
                text = pytesseract.image_to_string(
                    img,
                    lang='spa+eng',
                    config='--psm 6'
                )
                
                if text.strip():
                    text_parts.append(text)
                    
            except Exception as e:
                self._logger.warning(f"OCR falló en página {page_num + 1}: {e}")
        
        return "\n\n".join(text_parts)
    
    def validate(self, input_path: Path) -> Tuple[bool, Optional[str]]:
        """Valida el PDF."""
        validator = PDFValidator()
        return validator.validate(input_path)


# Registrar
PDFFactory.register(OperationType.EXTRACT_TEXT, TextExtractService)
```

## Batch Processor v2

```python
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Callable, Dict, Any
from datetime import datetime
from enum import Enum
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import shutil

from src.core.pdf_base import OperationType, PDFOperationResult
from src.services.merge.merge_service import MergeOptions
from src.utils.logger import logger


class BatchStrategy(Enum):
    """Estrategia de procesamiento por lotes."""
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    DISTRIBUTED = "distributed"


@dataclass
class BatchItem:
    """Elemento de un batch."""
    id: str
    input_path: Path
    output_path: Optional[Path] = None
    operation_type: OperationType = OperationType.MERGE
    options: Dict[str, Any] = field(default_factory=dict)
    status: str = "pending"
    result: Optional[PDFOperationResult] = None
    error: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


@dataclass
class BatchResult:
    """Resultado de un batch."""
    batch_id: str
    total_items: int
    successful: int
    failed: int
    cancelled: int
    items: List[BatchItem] = field(default_factory=list)
    started_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    total_duration_ms: float = 0.0


class BatchProcessor:
    """Procesador de lotes PDF."""
    
    def __init__(
        self,
        max_workers: int = 4,
        strategy: BatchStrategy = BatchStrategy.PARALLEL,
        progress_callback: Optional[Callable] = None
    ) -> None:
        self._max_workers = max_workers
        self._strategy = strategy
        self._progress_callback = progress_callback
        self._cancel_requested = False
        self._logger = logger.get_logger()
    
    def process(
        self,
        items: List[BatchItem],
        output_dir: Path,
        operation_type: OperationType,
        global_options: Optional[Dict[str, Any]] = None
    ) -> BatchResult:
        """Procesa un lote de items."""
        global_options = global_options or {}
        
        batch_id = self._generate_batch_id()
        result = BatchResult(batch_id=batch_id, total_items=len(items))
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        self._logger.info(f"Iniciando batch {batch_id}: {len(items)} items")
        
        if self._strategy == BatchStrategy.SEQUENTIAL:
            result = self._process_sequential(items, output_dir, operation_type, global_options, result)
        else:
            result = self._process_parallel(items, output_dir, operation_type, global_options, result)
        
        result.completed_at = datetime.now()
        result.total_duration_ms = (
            result.completed_at - result.started_at
        ).total_seconds() * 1000
        
        self._logger.info(
            f"Batch {batch_id} completado: "
            f"{result.successful} ok, {result.failed} errores"
        )
        
        return result
    
    def _process_sequential(
        self,
        items: List[BatchItem],
        output_dir: Path,
        operation_type: OperationType,
        global_options: Dict[str, Any],
        result: BatchResult
    ) -> BatchResult:
        """Procesa secuencialmente."""
        for idx, item in enumerate(items):
            if self._cancel_requested:
                item.status = "cancelled"
                result.cancelled += 1
                continue
            
            item = self._process_single(item, output_dir, operation_type, global_options)
            result.items.append(item)
            
            if item.status == "completed":
                result.successful += 1
            else:
                result.failed += 1
            
            if self._progress_callback:
                self._progress_callback(idx + 1, len(items), item)
        
        return result
    
    def _process_parallel(
        self,
        items: List[BatchItem],
        output_dir: Path,
        operation_type: OperationType,
        global_options: Dict[str, Any],
        result: BatchResult
    ) -> BatchResult:
        """Procesa en paralelo."""
        with ThreadPoolExecutor(max_workers=self._max_workers) as executor:
            futures = {}
            
            for item in items:
                if self._cancel_requested:
                    item.status = "cancelled"
                    result.cancelled += 1
                    result.items.append(item)
                    continue
                
                future = executor.submit(
                    self._process_single,
                    item,
                    output_dir,
                    operation_type,
                    global_options
                )
                futures[future] = item
            
            for future in as_completed(futures):
                item = futures[future]
                
                try:
                    processed_item = future.result()
                    result.items.append(processed_item)
                    
                    if processed_item.status == "completed":
                        result.successful += 1
                    else:
                        result.failed += 1
                        
                except Exception as e:
                    item.status = "failed"
                    item.error = str(e)
                    result.items.append(item)
                    result.failed += 1
                
                if self._progress_callback:
                    completed = result.successful + result.failed
                    self._progress_callback(completed, len(items), item)
        
        return result
    
    def _process_single(
        self,
        item: BatchItem,
        output_dir: Path,
        operation_type: OperationType,
        global_options: Dict[str, Any]
    ) -> BatchItem:
        """Procesa un solo item."""
        import uuid
        
        item.id = item.id or str(uuid.uuid4())[:8]
        item.started_at = datetime.now()
        item.status = "running"
        
        try:
            from src.core.pdf_factory import PDFFactory
            
            operation = PDFFactory.create(operation_type)
            
            # Determinar output path
            if not item.output_path:
                item.output_path = output_dir / f"{item.input_path.stem}_processed.pdf"
            
            # Merge opciones
            if operation_type == OperationType.MERGE:
                options = MergeOptions(**global_options)
                op_result = operation.execute(
                    item.input_path,
                    item.output_path,
                    options
                )
            else:
                op_result = operation.execute(
                    item.input_path,
                    item.output_path,
                    None
                )
            
            item.result = op_result
            
            if op_result.success:
                item.status = "completed"
                self._logger.debug(f"Item completado: {item.input_path.name}")
            else:
                item.status = "failed"
                item.error = op_result.message
                self._logger.warning(f"Item fallido: {item.input_path.name} - {op_result.message}")
            
        except Exception as e:
            item.status = "failed"
            item.error = str(e)
            self._logger.error(f"Error procesando {item.input_path.name}: {e}")
        
        item.completed_at = datetime.now()
        return item
    
    def _generate_batch_id(self) -> str:
        """Genera ID de batch."""
        import uuid
        return f"batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
    
    def cancel(self) -> None:
        """Solicita cancelación del batch."""
        self._cancel_requested = True
        self._logger.info("Cancelación solicitada")


class BatchReporter:
    """Generador de reportes de batch."""
    
    @staticmethod
    def to_json(result: BatchResult, output_path: Path) -> None:
        """Exporta a JSON."""
        report = {
            "batch_id": result.batch_id,
            "summary": {
                "total": result.total_items,
                "successful": result.successful,
                "failed": result.failed,
                "cancelled": result.cancelled,
                "duration_ms": result.total_duration_ms
            },
            "started_at": result.started_at.isoformat(),
            "completed_at": result.completed_at.isoformat() if result.completed_at else None,
            "items": [
                {
                    "id": item.id,
                    "input": str(item.input_path),
                    "output": str(item.output_path) if item.output_path else None,
                    "status": item.status,
                    "error": item.error,
                    "started_at": item.started_at.isoformat() if item.started_at else None,
                    "completed_at": item.completed_at.isoformat() if item.completed_at else None
                }
                for item in result.items
            ]
        }
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    
    @staticmethod
    def to_html(result: BatchResult, output_path: Path) -> None:
        """Exporta a HTML."""
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Batch Report - {result.batch_id}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1 {{ color: #1E3A5F; }}
        .summary {{ background: #f5f5f5; padding: 20px; border-radius: 8px; }}
        .item {{ padding: 10px; border-bottom: 1px solid #eee; }}
        .success {{ color: green; }}
        .failed {{ color: red; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }}
    </style>
</head>
<body>
    <h1>Batch Report: {result.batch_id}</h1>
    
    <div class="summary">
        <h2>Resumen</h2>
        <p><strong>Total:</strong> {result.total_items}</p>
        <p><strong>Exitosos:</strong> <span class="success">{result.successful}</span></p>
        <p><strong>Fallidos:</strong> <span class="failed">{result.failed}</span></p>
        <p><strong>Duración:</strong> {result.total_duration_ms:.0f}ms</p>
    </div>
    
    <h2>Detalles</h2>
    <table>
        <tr>
            <th>Archivo</th>
            <th>Estado</th>
            <th>Error</th>
        </tr>
"""
        
        for item in result.items:
            status_class = "success" if item.status == "completed" else "failed"
            html += f"""
        <tr>
            <td>{item.input_path.name}</td>
            <td class="{status_class}">{item.status}</td>
            <td>{item.error or '-'}</td>
        </tr>
"""
        
        html += """
    </table>
</body>
</html>
"""
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(html, encoding="utf-8")
```

## File Watcher

```python
from pathlib import Path
from typing import Callable, Optional, List
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent
import time

from src.core.pdf_base import OperationType
from src.services.batch.batch_processor import BatchProcessor, BatchItem
from src.utils.logger import logger


class PDFWatchHandler(FileSystemEventHandler):
    """Handler para monitorear archivos PDF."""
    
    def __init__(
        self,
        processor: BatchProcessor,
        output_dir: Path,
        operation_type: OperationType,
        options: dict,
        file_patterns: Optional[List[str]] = None
    ) -> None:
        super().__init__()
        
        self.processor = processor
        self.output_dir = output_dir
        self.operation_type = operation_type
        self.options = options
        self.file_patterns = file_patterns or [".pdf"]
        
        self._processed_files: set = set()
        self._pending_files: dict = {}
    
    def on_created(self, event: FileSystemEvent) -> None:
        """Detecta nuevos archivos."""
        if event.is_directory:
            return
        
        if not self._is_valid_file(event.src_path):
            return
        
        if event.src_path in self._processed_files:
            return
        
        self._logger.info(f"Archivo detectado: {event.src_path}")
        
        # Agendar procesamiento
        self._schedule_processing(event.src_path)
    
    def on_modified(self, event: FileSystemEvent) -> None:
        """Detecta modificaciones."""
        if event.is_directory:
            return
        
        if not self._is_valid_file(event.src_path):
            return
        
        # Solo procesar si no está pendiente
        if event.src_path not in self._pending_files:
            self._schedule_processing(event.src_path)
    
    def _is_valid_file(self, file_path: str) -> bool:
        """Verifica si es un archivo válido."""
        path = Path(file_path)
        
        if not path.suffix.lower() in self.file_patterns:
            return False
        
        if path.name.startswith("."):
            return False
        
        return True
    
    def _schedule_processing(self, file_path: str) -> None:
        """Agenda el procesamiento del archivo."""
        # Esperar a que el archivo esté completo
        time.sleep(1)
        
        path = Path(file_path)
        
        # Verificar que el archivo existe y tiene contenido
        if not path.exists() or path.stat().st_size == 0:
            return
        
        self._pending_files[file_path] = datetime.now()
        
        # Crear item de batch
        item = BatchItem(
            id="",
            input_path=path,
            operation_type=self.operation_type
        )
        
        # Procesar
        result = self.processor._process_single(
            item,
            self.output_dir,
            self.operation_type,
            self.options
        )
        
        if result.status == "completed":
            self._processed_files.add(file_path)
            self._logger.info(f"Procesado: {path.name}")
        else:
            self._logger.warning(f"Falló: {path.name} - {result.error}")
        
        del self._pending_files[file_path]


class PDFWatcher:
    """Monitor de directorio para PDFs."""
    
    def __init__(
        self,
        watch_dir: Path,
        output_dir: Path,
        operation_type: OperationType = OperationType.COMPRESS,
        options: Optional[dict] = None,
        max_workers: int = 2
    ) -> None:
        self.watch_dir = watch_dir
        self.output_dir = output_dir
        self.operation_type = operation_type
        self.options = options or {}
        
        self._processor = BatchProcessor(max_workers=max_workers)
        self._observer: Optional[Observer] = None
        self._logger = logger.get_logger()
    
    def start(self) -> None:
        """Inicia el watcher."""
        self.watch_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        handler = PDFWatchHandler(
            self._processor,
            self.output_dir,
            self.operation_type,
            self.options
        )
        
        self._observer = Observer()
        self._observer.schedule(handler, str(self.watch_dir), recursive=False)
        self._observer.start()
        
        self._logger.info(f"Watcher iniciado: {self.watch_dir}")
    
    def stop(self) -> None:
        """Detiene el watcher."""
        if self._observer:
            self._observer.stop()
            self._observer.join()
            self._logger.info("Watcher detenido")
    
    def __enter__(self):
        """Context manager entry."""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop()
```

## Validadores y Auditoría

```python
from pathlib import Path
from typing import Tuple, Optional, List
from dataclasses import dataclass
import json
from datetime import datetime


class PDFValidator:
    """Validador de archivos PDF."""
    
    MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB
    ALLOWED_EXTENSIONS = [".pdf"]
    
    def validate(self, file_path: Path) -> Tuple[bool, Optional[str]]:
        """Valida un archivo PDF."""
        
        # Verificar existencia
        if not file_path.exists():
            return False, "El archivo no existe"
        
        # Verificar extensión
        if file_path.suffix.lower() not in self.ALLOWED_EXTENSIONS:
            return False, f"Extensión no permitida. Usar: {', '.join(self.ALLOWED_EXTENSIONS)}"
        
        # Verificar tamaño
        if file_path.stat().st_size == 0:
            return False, "El archivo está vacío"
        
        if file_path.stat().st_size > self.MAX_FILE_SIZE:
            return False, f"Archivo demasiado grande. Máximo: {self.MAX_FILE_SIZE // (1024*1024)}MB"
        
        # Verificar header PDF
        try:
            with open(file_path, "rb") as f:
                header = f.read(5)
                if not header.startswith(b"%PDF-"):
                    return False, "No es un archivo PDF válido"
        except Exception as e:
            return False, f"No se puede leer el archivo: {e}"
        
        return True, None
    
    def validate_multiple(self, file_paths: List[Path]) -> Tuple[bool, Optional[str], List[Path]]:
        """Valida múltiples archivos."""
        valid_paths = []
        
        for path in file_paths:
            valid, error = self.validate(path)
            if valid:
                valid_paths.append(path)
            else:
                return False, error, valid_paths
        
        return True, None, valid_paths


class AuditLogger:
    """Sistema de auditoría de operaciones."""
    
    def __init__(self, audit_dir: Path) -> None:
        self.audit_dir = audit_dir
        self.audit_dir.mkdir(parents=True, exist_ok=True)
        
        self.current_session = datetime.now().strftime("%Y%m%d")
        self._audit_file = self.audit_dir / f"audit_{self.current_session}.jsonl"
    
    def log(
        self,
        operation: str,
        input_files: List[str],
        output_file: Optional[str],
        success: bool,
        error: Optional[str] = None,
        metadata: Optional[dict] = None
    ) -> None:
        """Registra una operación."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "input_files": input_files,
            "output_file": output_file,
            "success": success,
            "error": error,
            "metadata": metadata or {}
        }
        
        with open(self._audit_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
    
    def get_session_logs(self, session: Optional[str] = None) -> List[dict]:
        """Obtiene logs de una sesión."""
        session = session or self.current_session
        audit_file = self.audit_dir / f"audit_{session}.jsonl"
        
        if not audit_file.exists():
            return []
        
        logs = []
        with open(audit_file, "r", encoding="utf-8") as f:
            for line in f:
                logs.append(json.loads(line))
        
        return logs
```

## Buenas Prácticas

1. **Validación temprana**: Verificar archivos antes de procesar
2. **Operaciones atómicas**: Cada operación es independiente
3. **Logs estructurados**: Usar el logger del proyecto
4. **Manejo de errores**: Try/except con fallback
5. **Rutas pathlib**: Siempre usar Path
6. **Type hints**: Tipar todo el código
7. **Workers async**: Operaciones largas en threads
8. **Progreso**: Callbacks de progreso para UI
9. **Reportes**: Generar reportes de operaciones
10. **Auditoría**: Registrar todas las operaciones

## Variantes Avanzadas

### Compresión con pymupdf

```python
class CompressService(PDFOperationBase):
    """Servicio de compresión de PDFs."""
    
    operation_type = OperationType.COMPRESS
    
    def __init__(self) -> None:
        super().__init__()
    
    def execute(self, input_path, output_path, options=None) -> PDFOperationResult:
        import fitz  # pymupdf
        
        doc = fitz.open(str(input_path))
        
        # Comprimir imágenes
        for page_num in range(len(doc)):
            page = doc[page_num]
            images = page.get_images()
            
            for img_index, img in enumerate(images):
                xref = img[0]
                base_image = doc.extract_image(xref)
                
                # Recompress if needed
                # Implementation...
        
        # Guardar con compresión
        doc.save(
            str(output_path),
            garbage=4,  # Recolectar objetos no usados
            deflate=True,
            clean=True
        )
        
        doc.close()
        
        return self._create_result(True, "PDF comprimido", output_path)
```

### Pipeline Builder

```python
class PipelineBuilder:
    """Builder para pipelines de operaciones."""
    
    def __init__(self) -> None:
        self._steps: List[tuple] = []
    
    def add_step(
        self,
        operation: OperationType,
        options: dict
    ) -> "PipelineBuilder":
        self._steps.append((operation, options))
        return self
    
    def build(self) -> List[tuple]:
        return self._steps.copy()
```
