# AGENTS.md - Guidelines for AI Agents

This document provides guidelines for AI agents working in this repository.

## Project Overview

**Xebec Pdf Fixer** - A Windows desktop PDF management application built with Python and tkinter.
- **Language**: Python 3.8+
- **GUI Framework**: tkinter (built-in)
- **PDF Library**: pypdf>=3.0.0
- **Image Library**: Pillow>=9.0.0

## Build, Test, and Run Commands

### Running the Application
```bash
python src/main.py
```

### Running Tests
```bash
pytest tests/                    # Run all tests
pytest tests/test_file.py        # Run specific test file
pytest tests/test_file.py::test_function  # Run specific test function
pytest -k "test_name"           # Run tests matching pattern
```

### Building Executable
```bash
pyinstaller --onefile --windowed --icon=assets/icons/icono.png src/main.py
```

### Installing Dependencies
```bash
pip install -r requirements.txt
pip install -e .                # Install in editable mode
```

## Code Style Guidelines

### General Principles
- Use **type hints** for all function parameters and return types
- Use **pathlib.Path** instead of os.path strings
- Use **f-strings** for string formatting
- Use **absolute imports** (from src.package.module import ...)

### Naming Conventions
- **Classes**: PascalCase (e.g., `PDFRepairer`, `MainWindow`)
- **Functions/methods**: snake_case (e.g., `repair_pdf`, `_setup_window`)
- **Private methods**: prefix with underscore (e.g., `_on_close`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `APP_NAME`, `APP_VERSION`)
- **Files**: snake_case (e.g., `pdf_repair.py`, `main_window.py`)

### Import Order
1. Standard library imports
2. Third-party imports
3. Local application imports

Group with blank line between groups:
```python
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
from typing import Optional, Tuple

from pypdf import PdfReader, PdfWriter

from src.core.pdf_repair import PDFRepairer
from src.utils.logger import logger
from src.gui.components.theme_manager import theme_manager
```

### Type Hints
Use type hints for all functions:
```python
def repair(input_path: Path, output_path: Path) -> Tuple[bool, Optional[str]]:
    ...

def _on_document_select(self, file_path: str, file_name: str) -> None:
    ...
```

### Error Handling
- Use try/except blocks with specific exception types
- Return error information rather than raising for recoverable errors
- Log errors appropriately:
```python
try:
    # operation
except Exception as e:
    return False, str(e)
```

### Docstrings
Use Google-style docstrings for public methods:
```python
def repair(input_path: Path, output_path: Path) -> Tuple[bool, Optional[str]]:
    """Repair a PDF file by reading and rewriting it.

    Args:
        input_path: Path to the input PDF file.
        output_path: Path where the repaired PDF will be saved.

    Returns:
        Tuple of (success: bool, error_message: Optional[str])
    """
```

### GUI Development
- Use tkinter Frame widgets as containers
- Follow component-based architecture (see `src/gui/components/`)
- Use theme_manager for colors (One Dark Pro theme)
- Use descriptive names for UI elements (e.g., `_main_container`, `_start_panel`)

### File Organization
```
src/
├── main.py              # Entry point
├── core/                # Business logic
│   └── pdf_repair.py
├── gui/                 # GUI components
│   ├── main_window.py
│   ├── splash_screen.py
│   └── components/     # Reusable UI components
└── utils/               # Utilities
    ├── logger.py
    └── helpers.py
```

### Logging
Use the project's logger utility:
```python
from src.utils.logger import logger

log = logger.get_logger()
log.info("Message")
log.error("Error message")
```

## Project Configuration

### pyproject.toml Settings
- Package name: `xebec-pdf-fixer`
- Test path: `tests/`
- Build: PyInstaller onefile windowed

## Development Workflow

1. **Before writing code**: Understand the existing component structure
2. **Testing**: Add tests for new features in `tests/` directory
3. **Error handling**: Always handle exceptions gracefully with user feedback
4. **Theme**: Use `theme_manager.colors` for consistent styling

## Known Limitations
- Tests directory exists but may be empty - add tests for new features
- No CI/CD configured yet
- No linter/formatter configured (consider adding ruff)

## Agent Structure

### Orchestrator
- **orchestrator**: Main agent that coordinates all development tasks. Delegates to specialized sub-agents.

### Sub-agents
- **pdf-engineer**: Specialized for PDF operations (repair, merge, split, extract, rotate, encrypt)
- **gui-developer**: Specialized for tkinter GUI development (windows, panels, components, themes)

## Skills

| Skill | Description | Auto-invoke |
|-------|-------------|--------------|
| skill-commit | Conventional commits (format: `type(scope): description`) | Yes (on_code_change) |
| skill-sinc | Project synchronization | No |
| skill-doc | Documentation generation | No |
| skill-generate | Code generation (tests, components) | No |
| skill-design | UI/UX design assistance | No |

### Conventional Commits Format
```
<type>(<scope>): <description>

Types: feat, fix, docs, style, refactor, test, chore
Examples:
  feat(pdf): add merge functionality
  fix(gui): resolve theme toggle crash
  docs: update README with new commands
```
