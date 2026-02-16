# Xebec Pdf - AGENTS.md

## Project Overview

**Xebec Pdf** - Aplicación de escritorio profesional para administrar PDFs en Windows con interfaz moderna inspirada en Microsoft Office.

- **Python**: 3.8+
- **GUI**: Tkinter con tema personalizado
- **PDF**: pypdf
- **Build**: PyInstaller

---

## Build, Lint, and Test Commands

### Running the Application

```bash
# Development mode
python src/main.py

# With debug logging
python -c "import logging; logging.basicConfig(level=logging.DEBUG); exec(open('src/main.py').read())"
```

### Running Tests

```bash
# Install test dependencies
pip install pytest>=7.0

# Run all tests
pytest

# Run all tests with verbose output
pytest -v

# Run a single test file
pytest tests/test_pdf_repair.py

# Run a single test function
pytest tests/test_pdf_repair.py::test_repair_single_pdf -v

# Run tests matching a pattern
pytest -k "repair"

# Run with coverage (if coverage is installed)
pip install pytest-cov
pytest --cov=src --cov-report=term-missing
```

### Building Executable

```bash
# Install PyInstaller
pip install pyinstaller>=5.0

# Build single-file executable
pyinstaller --onefile --windowed --icon=assets/icons/icono.png --name "XebecPdf" src/main.py

# Output located at: dist/XebecPdf.exe
```

### Code Quality (Linting)

```bash
# Install linting tools (recommended)
pip install ruff mypy

# Run ruff linter
ruff check src/

# Run ruff with auto-fix
ruff check --fix src/

# Run type checking
mypy src/

# Format code
ruff format src/
```

---

## Code Style Guidelines

### Imports

```python
# Standard library first, then third-party, then local
import logging
from pathlib import Path
from typing import Tuple, Optional, List

from pypdf import PdfReader, PdfWriter

from src.core.pdf_repair import PDFRepairer
from src.utils.logger import get_logger
```

- Use absolute imports from `src`
- Group imports with blank lines between groups
- Sort imports alphabetically within groups

### Type Hints

- **Always use type hints** for function parameters and return types
- Use `Optional[X]` instead of `X | None` (Python 3.8+ compatibility)
- Use `Tuple[X, Y]` for multiple return values

```python
# Good
def repair(input_path: Path, output_path: Path) -> Tuple[bool, Optional[str]]:
    ...

# Good
def process_files(files: List[Path]) -> dict:
    ...
```

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Classes | PascalCase | `PDFRepairer`, `Component` |
| Functions/methods | snake_case | `repair_pdf()`, `update_theme()` |
| Variables | snake_case | `input_path`, `output_folder` |
| Constants | UPPER_SNAKE_CASE | `MAX_PAGES = 1000` |
| Private methods | _snake_case | `_apply_fg()`, `_create_container()` |
| Files | snake_case | `pdf_repair.py`, `main_window.py` |

### Error Handling

- Return `Tuple[bool, Optional[str]]` for operations that can fail
- Use try/except for operations that need cleanup
- Log errors before returning failure

```python
# Pattern for operations that can fail
def operation(file_path: Path) -> Tuple[bool, Optional[str]]:
    try:
        # risky operation
        return True, None
    except Exception as e:
        logger.error(f"Operation failed: {e}")
        return False, str(e)
```

### GUI Components

- Inherit from `Component` base class (abc.ABC)
- Implement `update_theme()` method for theme changes
- Support `theme_manager` for dynamic colors
- Use threading for long-running operations

```python
class MyComponent(Component):
    def __init__(self, parent: tk.Widget, **kwargs):
        super().__init__(parent, **kwargs)
        self._create_widget()
    
    def update_theme(self):
        # Apply theme colors
        pass
```

### Class Structure

```python
class MyClass:
    def __init__(self, param: str):
        self.param = param
        self._private = None
    
    @property
    def value(self) -> str:
        return self._private
    
    @value.setter
    def value(self, val: str):
        self._private = val
    
    @staticmethod
    def utility_method(arg: str) -> bool:
        ...
    
    def instance_method(self) -> Tuple[bool, Optional[str]]:
        ...
```

### Logging

- Use the project's logger: `from src.utils.logger import get_logger`
- Log at appropriate levels: DEBUG, INFO, WARNING, ERROR
- Include context in log messages

```python
logger = get_logger(__name__)

logger.info("Starting PDF repair")
logger.error(f"Failed to repair {file}: {error}")
```

---

## Project Structure

```
PdfSuport/
├── src/
│   ├── main.py                    # Entry point
│   ├── core/                      # PDF business logic
│   │   └── pdf_repair.py
│   ├── gui/                       # GUI components
│   │   ├── main_window.py
│   │   ├── splash_screen.py
│   │   ├── components/
│   │   │   ├── base.py           # Component base class
│   │   │   ├── widgets.py
│   │   │   ├── theme_manager.py
│   │   │   └── ...
│   │   └── themes/
│   └── utils/
│       ├── logger.py
│       └── font_manager.py
├── tests/                         # Test files
│   └── test_*.py
├── assets/
│   ├── icons/
│   └── fonts/
├── pyproject.toml
├── requirements.txt
└── README.md
```

---

## Theme Colors (One Dark Pro)

| Name | Hex |
|------|-----|
| Background | `#282A31` |
| Foreground | `#B2C2CD` |
| Accent | `#528BFF` |
| Success | `#98C379` |
| Warning | `#E5C07B` |
| Error | `#E06C75` |

---

## Git Commit Conventions

Format: `<type>(<scope>): <description>`

Types:
- `feat` - New feature
- `fix` - Bug fix
- `refactor` - Code refactoring
- `test` - Tests
- `docs` - Documentation
- `chore` - Maintenance

Example: `feat(pdf): add PDF merge functionality`

---

## Testing Best Practices

1. Place tests in `tests/` directory
2. Name test files: `test_<module>.py`
3. Name test functions: `test_<description>()`
4. Use pytest fixtures for common setup
5. Mock external dependencies (file I/O, pypdf)
6. Test both success and failure paths

```python
# tests/test_pdf_repair.py
import pytest
from pathlib import Path
from src.core.pdf_repair import PDFRepairer

def test_repair_valid_pdf(tmp_path):
    input_file = tmp_path / "input.pdf"
    output_file = tmp_path / "output.pdf"
    # ... create test PDF ...
    
    success, error = PDFRepairer.repair(input_file, output_file)
    
    assert success is True
    assert error is None
    assert output_file.exists()
```

---

## Dependencies

### Runtime
- `pypdf>=3.0.0`
- `Pillow>=9.0.0`

### Development
- `pyinstaller>=5.0` - Build executable
- `pytest>=7.0` - Testing
- `ruff` - Linting/formatting
- `mypy` - Type checking
