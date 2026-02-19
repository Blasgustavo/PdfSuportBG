---
name: skill-pdf-automation
description: PdfSuport Automation Engine - Arquitectura y código para automatización PDF avanzada con Python
---

## What I do

Actúo como arquitecto senior en automatización PDF con Python 3.12+. Diseño y implemento:

- **Operaciones PDF robustas**: unir, dividir, extraer páginas, reparar, optimizar tamaño, extraer texto, metadatos, lotes
- **Arquitectura limpia**: core/, utils/, services/, pipelines/, adapters/
- **Pipelines de automatización**: batch processing, watchers, jobs, reportes
- **Integración con GUI PyQt6**: señales, WindowManager, estados reactivos

## When to use me

Usar cuando se necesite:
- Nuevas operaciones PDF en el motor core
- Procesamiento por lotes (batch processing)
- Pipelines de automatización
- Optimización de PDFs
- Extracción de texto/metadatos
- Integración con la GUI existente

## Arquitectura Propuesta

```
src/
├── core/                    # Motor PDF base
│   └── pdf_operations.py    # Operaciones fundamentales
├── services/                # Servicios de negocio
│   ├── pdf_merge.py         # Unir PDFs
│   ├── pdf_split.py         # Dividir PDFs
│   ├── pdf_repair.py        # Reparar PDFs
│   ├── pdf_compress.py      # Compresión
│   ├── pdf_text_extract.py  # Extracción de texto
│   ├── pdf_metadata.py      # Metadatos
│   └── pdf_batch.py         # Procesamiento por lotes
├── pipelines/               # Pipelines de automatización
│   ├── base.py              # Clase base
│   ├── batch_processor.py   # Procesador de lotes
│   ├── watcher.py           # File watcher
│   └── reporter.py          # Generación de reportes
├── adapters/                # Adaptadores de librerías
│   ├── pypdf_adapter.py     # pypdf wrapper
│   ├── pymupdf_adapter.py   # pymupdf wrapper
│   └── pdfminer_adapter.py  # pdfminer wrapper
└── gui/pyqt6/               # Integración GUI
    ├── operations/          # Widgets de operaciones
    └── workers/             # QThreads para operaciones
```

## Operaciones Disponibles

| Operación | Descripción | Librería principal |
|-----------|-------------|-------------------|
| merge | Unir múltiples PDFs | pypdf |
| split | Dividir PDF por páginas | pypdf |
| extract_pages | Extraer páginas específicas | pypdf |
| repair | Reparar PDF corrupto | pypdf |
| compress | Optimizar tamaño | pymupdf |
| extract_text | Extraer texto | pypdf / pdfminer |
| extract_metadata | Extraer metadatos | pypdf |
| batch | Procesar lote de archivos | todas |

## Patrones de Implementación

### 1. Servicio de Operación PDF

```python
from pathlib import Path
from typing import Optional, Tuple, List
from dataclasses import dataclass

from src.utils.logger import logger

log = logger.get_logger()


@dataclass
class OperationResult:
    success: bool
    message: str
    output_path: Optional[Path] = None
    data: Optional[dict] = None


class PDFMergeService:
    """Servicio para unir múltiples PDFs."""
    
    def __init__(self) -> None:
        self._supported_formats = [".pdf"]
    
    def validate_inputs(self, input_paths: List[Path]) -> Tuple[bool, Optional[str]]:
        """Valida archivos de entrada."""
        for path in input_paths:
            if not path.exists():
                return False, f"Archivo no encontrado: {path}"
            if path.suffix.lower() not in self._supported_formats:
                return False, f"Formato no soportado: {path.suffix}"
        return True, None
    
    def merge(
        self, 
        input_paths: List[Path], 
        output_path: Path
    ) -> OperationResult:
        """Une múltiples PDFs en uno solo."""
        try:
            valid, error = self.validate_inputs(input_paths)
            if not valid:
                return OperationResult(False, error)
            
            from pypdf import PdfWriter
            
            merger = PdfWriter()
            for path in input_paths:
                merger.append(str(path))
                log.info(f"Añadido: {path.name}")
            
            merger.write(str(output_path))
            merger.close()
            
            log.info(f"PDFs combinados exitosamente: {output_path}")
            return OperationResult(
                True, 
                f"PDFs combinados: {len(input_paths)} archivos",
                output_path
            )
            
        except Exception as e:
            log.error(f"Error al combinar PDFs: {e}")
            return OperationResult(False, str(e))
```

### 2. Pipeline de Batch Processing

```python
from pathlib import Path
from typing import List, Optional
from dataclasses import dataclass, field
from enum import Enum
import json
from datetime import datetime

from src.core.pdf_operations import PDFOperationBase


class BatchStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class BatchItem:
    input_path: Path
    output_path: Optional[Path] = None
    status: BatchStatus = BatchStatus.PENDING
    error: Optional[str] = None
    processed_at: Optional[datetime] = None


@dataclass
class BatchResult:
    total: int
    successful: int
    failed: int
    items: List[BatchItem] = field(default_factory=list)
    started_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None


class BatchProcessor:
    """Procesador de lotes PDF."""
    
    def __init__(
        self, 
        operation: PDFOperationBase,
        output_dir: Path
    ) -> None:
        self.operation = operation
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def process(
        self, 
        input_paths: List[Path],
        pattern: Optional[str] = None
    ) -> BatchResult:
        """Procesa un lote de archivos PDF."""
        result = BatchResult(total=len(input_paths), successful=0, failed=0)
        
        for input_path in input_paths:
            item = BatchItem(input_path=input_path)
            
            try:
                output_name = f"processed_{input_path.name}"
                output_path = self.output_dir / output_name
                
                op_result = self.operation.execute(input_path, output_path)
                
                if op_result.success:
                    item.status = BatchStatus.COMPLETED
                    item.output_path = output_path
                    item.processed_at = datetime.now()
                    result.successful += 1
                else:
                    item.status = BatchStatus.FAILED
                    item.error = op_result.message
                    result.failed += 1
                    
            except Exception as e:
                item.status = BatchStatus.FAILED
                item.error = str(e)
                result.failed += 1
                log.error(f"Error procesando {input_path.name}: {e}")
            
            result.items.append(item)
        
        result.completed_at = datetime.now()
        return result
    
    def save_report(self, result: BatchResult, report_path: Path) -> None:
        """Guarda reporte JSON del procesamiento."""
        report = {
            "summary": {
                "total": result.total,
                "successful": result.successful,
                "failed": result.failed,
                "duration_seconds": (
                    result.completed_at - result.started_at
                ).total_seconds() if result.completed_at else 0
            },
            "items": [
                {
                    "input": str(item.input_path),
                    "output": str(item.output_path) if item.output_path else None,
                    "status": item.status.value,
                    "error": item.error,
                    "processed_at": item.processed_at.isoformat() if item.processed_at else None
                }
                for item in result.items
            ]
        }
        
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
```

### 3. Integración con PyQt6 (Worker + Signals)

```python
from PyQt6.QtCore import QObject, QThread, pyqtSignal
from pathlib import Path
from typing import List, Optional

from src.services.pdf_merge import PDFMergeService, OperationResult
from src.utils.logger import logger

log = logger.get_logger()


class PDFMergeWorker(QThread):
    """Worker para operación merge en hilo separado."""
    
    finished = pyqtSignal(OperationResult)
    progress = pyqtSignal(int, str)  # percentage, message
    error = pyqtSignal(str)
    
    def __init__(
        self, 
        input_paths: List[Path], 
        output_path: Path
    ) -> None:
        super().__init__()
        self.input_paths = input_paths
        self.output_path = output_path
        self._service = PDFMergeService()
    
    def run(self) -> None:
        """Ejecuta la operación en hilo separado."""
        try:
            log.info(f"Iniciando merge de {len(self.input_paths)} archivos")
            self.progress.emit(10, "Validando archivos...")
            
            result = self._service.merge(self.input_paths, self.output_path)
            
            if result.success:
                self.progress.emit(100, "Completado")
                self.finished.emit(result)
            else:
                self.error.emit(result.message)
                
        except Exception as e:
            log.error(f"Error en worker merge: {e}")
            self.error.emit(str(e))
```

### 4. Widget de Operacion para GUI

```python
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel,
    QProgressBar, QListWidget, QFileDialog, QMessageBox
)
from PyQt6.QtCore import pyqtSlot
from pathlib import Path
from typing import List

from src.gui.pyqt6.theme_manager import theme_manager
from src.gui.pyqt6.workers.pdf_merge_worker import PDFMergeWorker


class MergeOperationWidget(QWidget):
    """Widget para unir PDFs."""
    
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._worker: Optional[PDFMergeWorker] = None
        self._input_files: List[Path] = []
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        colors = theme_manager.colors
        
        layout = QVBoxLayout(self)
        
        self.title_label = QLabel("Unir PDFs")
        self.title_label.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {colors['text_primary']}")
        
        self.file_list = QListWidget()
        self.file_list.setStyleSheet(f"background: {colors['bg_secondary']}; color: {colors['text_primary']}")
        
        self.add_button = QPushButton("Agregar PDFs")
        self.add_button.clicked.connect(self._on_add_files)
        
        self.merge_button = QPushButton("Unir PDFs")
        self.merge_button.clicked.connect(self._on_merge)
        self.merge_button.setEnabled(False)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        
        layout.addWidget(self.title_label)
        layout.addWidget(self.file_list)
        layout.addWidget(self.add_button)
        layout.addWidget(self.merge_button)
        layout.addWidget(self.progress_bar)
    
    def _on_add_files(self) -> None:
        files, _ = QFileDialog.getOpenFileNames(
            self, 
            "Seleccionar PDFs", 
            "", 
            "PDF Files (*.pdf)"
        )
        
        for file_path in files:
            path = Path(file_path)
            self._input_files.append(path)
            self.file_list.addItem(path.name)
        
        self.merge_button.setEnabled(len(self._input_files) > 1)
    
    @pyqtSlot()
    def _on_merge(self) -> None:
        output_path, _ = QFileDialog.getSaveFileName(
            self, 
            "Guardar PDF combinado", 
            "", 
            "PDF Files (*.pdf)"
        )
        
        if not output_path:
            return
        
        self._run_merge(Path(output_path))
    
    def _run_merge(self, output_path: Path) -> None:
        self.merge_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        self._worker = PDFMergeWorker(self._input_files, output_path)
        self._worker.progress.connect(self._on_progress)
        self._worker.finished.connect(self._on_finished)
        self._worker.error.connect(self._on_error)
        self._worker.start()
    
    @pyqtSlot(int, str)
    def _on_progress(self, value: int, message: str) -> None:
        self.progress_bar.setValue(value)
    
    @pyqtSlot(OperationResult)
    def _on_finished(self, result: OperationResult) -> None:
        self.progress_bar.setVisible(False)
        self.merge_button.setEnabled(True)
        
        QMessageBox.information(
            self, 
            "Éxito", 
            result.message
        )
        
        self._input_files.clear()
        self.file_list.clear()
    
    @pyqtSlot(str)
    def _on_error(self, error: str) -> None:
        self.progress_bar.setVisible(False)
        self.merge_button.setEnabled(True)
        
        QMessageBox.critical(self, "Error", error)
```

## Manejo de Errores Corporativo

```python
from typing import Optional
from enum import Enum
from dataclasses import dataclass
import traceback


class ErrorSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class ErrorRecord:
    timestamp: str
    operation: str
    severity: ErrorSeverity
    message: str
    traceback: Optional[str] = None
    file_path: Optional[str] = None


class ErrorHandler:
    """Manejo centralizado de errores."""
    
    def __init__(self, audit_file: Path) -> None:
        self.audit_file = audit_file
        self.errors: list[ErrorRecord] = []
    
    def handle(
        self,
        operation: str,
        error: Exception,
        severity: ErrorSeverity = ErrorSeverity.MEDIUM,
        file_path: Optional[Path] = None
    ) -> ErrorRecord:
        """Registra y maneja un error."""
        record = ErrorRecord(
            timestamp=datetime.now().isoformat(),
            operation=operation,
            severity=severity,
            message=str(error),
            traceback=traceback.format_exc(),
            file_path=str(file_path) if file_path else None
        )
        
        self.errors.append(record)
        self._save_to_audit(record)
        
        log.error(f"[{severity.value}] {operation}: {error}")
        
        return record
    
    def _save_to_audit(self, record: ErrorRecord) -> None:
        """Guarda error en archivo de auditoría."""
        import json
        
        entry = {
            "timestamp": record.timestamp,
            "operation": record.operation,
            "severity": record.severity.value,
            "message": record.message,
            "file_path": record.file_path
        }
        
        with open(self.audit_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
```

## Variantes Avanzadas

### OCR con Tesseract

```python
class OCRProcessor:
    """Procesador OCR para PDFs escaneados."""
    
    def __init__(self, language: str = "spa+eng") -> None:
        self.language = language
        self._check_availability()
    
    def _check_availability(self) -> None:
        try:
            import pytesseract
            self._available = True
        except ImportError:
            self._available = False
            log.warning("Tesseract no disponible")
    
    def extract_with_ocr(self, pdf_path: Path) -> str:
        """Extrae texto usando OCR."""
        if not self._available:
            raise RuntimeError("OCR no disponible")
        
        import pytesseract
        from pypdf import PdfReader
        from PIL import Image
        
        reader = PdfReader(pdf_path)
        text_parts = []
        
        for page_num, page in enumerate(reader.pages):
            if "/XObject" in page["/Resources"]:
                continue  # Skip pages with text
            
            # Convert to image and OCR
            try:
                image = page.to_image()
                text = pytesseract.image_to_string(image, lang=self.language)
                text_parts.append(text)
            except Exception as e:
                log.warning(f"OCR falló en página {page_num}: {e}")
        
        return "\n".join(text_parts)
```

### Compresión Avanzada

```python
class PDFCompressor:
    """Compresor de PDFs con múltiples estrategias."""
    
    def __init__(self) -> None:
        self._strategies = [
            self._compress_images,
            self._remove_metadata,
            self._flatten_forms,
            self._optimize_objects
        ]
    
    def compress(
        self, 
        input_path: Path, 
        output_path: Path,
        quality: str = "medium"  # low, medium, high
    ) -> OperationResult:
        """Comprime PDF usando múltiples estrategias."""
        try:
            import fitz  # pymupdf
            
            doc = fitz.open(str(input_path))
            
            for strategy in self._strategies:
                strategy(doc, quality)
            
            doc.save(str(output_path), garbage=4, deflate=True)
            doc.close()
            
            original_size = input_path.stat().st_size
            compressed_size = output_path.stat().st_size
            ratio = (1 - compressed_size / original_size) * 100
            
            return OperationResult(
                True,
                f"Comprimido: {ratio:.1f}% reducción",
                output_path,
                {"original_size": original_size, "compressed_size": compressed_size}
            )
            
        except Exception as e:
            return OperationResult(False, str(e))
    
    def _compress_images(self, doc: fitz.Document, quality: str) -> None:
        """Comprime imágenes en el documento."""
        dpi_settings = {
            "low": 72,
            "medium": 150,
            "high": 300
        }
        dpi = dpi_settings.get(quality, 150)
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            images = page.get_images()
            
            for img_index, img in enumerate(images):
                xref = img[0]
                base_image = doc.extract_image(xref)
                
                # Recompress if needed
                # (Implementation depends on requirements)
```

### File Watcher para Automatización

```python
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent


class PDFWatcherHandler(FileSystemEventHandler):
    """Handler para monitorear directorio de PDFs."""
    
    def __init__(
        self, 
        processor: BatchProcessor,
        output_dir: Path
    ) -> None:
        self.processor = processor
        self.output_dir = output_dir
        self._processed: set[str] = set()
    
    def on_created(self, event: FileSystemEvent) -> None:
        """Detecta nuevos archivos PDF."""
        if event.is_directory:
            return
        
        if not event.src_path.lower().endswith(".pdf"):
            return
        
        if event.src_path in self._processed:
            return
        
        path = Path(event.src_path)
        
        # Wait for file to be fully written
        time.sleep(1)
        
        log.info(f"Nuevo PDF detectado: {path.name}")
        
        result = self.processor.process([path])
        
        if result.successful > 0:
            self._processed.add(event.src_path)
            log.info(f"Procesado: {path.name}")


class PDFWatcher:
    """Monitorea directorio y procesa PDFs automáticamente."""
    
    def __init__(
        self, 
        watch_dir: Path,
        processor: BatchProcessor,
        output_dir: Path
    ) -> None:
        self.watch_dir = watch_dir
        self.processor = processor
        self.output_dir = output_dir
        self._observer: Optional[Observer] = None
    
    def start(self) -> None:
        """Inicia el watcher."""
        event_handler = PDFWatcherHandler(self.processor, self.output_dir)
        
        self._observer = Observer()
        self._observer.schedule(
            event_handler, 
            str(self.watch_dir), 
            recursive=False
        )
        self._observer.start()
        
        log.info(f"Watcher iniciado: {self.watch_dir}")
    
    def stop(self) -> None:
        """Detiene el watcher."""
        if self._observer:
            self._observer.stop()
            self._observer.join()
            log.info("Watcher detenido")
```

## Buenas Prácticas

1. **Validación temprana**: Verificar archivos antes de procesar
2. **Logs estructurados**: Usar el logger del proyecto
3. **Errores específicos**: Capturar excepciones específicas, no genéricas
4. **Rutas con pathlib**: Siempre usar Path, no os.path
5. **Type hints completos**: Tipar todo el código
6. **Workers para GUI**: Operaciones largas en QThread
7. **Validación de resultados**: Verificar archivos generados
8. **Limpieza de recursos**: Cerrar archivos y conexiones
9. **Reportes de operación**: Guardar logs de auditoría
10. **Tests unitarios**: Probar cada servicio independientemente
