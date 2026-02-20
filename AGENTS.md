# AGENTS.md - Guidelines for AI Agents

This document provides guidelines for AI agents working in this repository.

## Project Overview

**Xebec Pdf Fixer** - A Windows desktop PDF management application built with Python and PyQt6.
- **Language**: Python 3.8+
- **GUI Framework**: PyQt6 (Qt6)
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
pytest tests/test_file.py         # Run specific test file
pytest tests/test_file.py::test_function  # Run specific test function
pytest -k "test_name"            # Run tests matching pattern
```

### Building Executable
```bash
# Compilar con icono
pyinstaller --onefile --windowed --icon=assets/icons/icono.png --add-data "assets;assets" --name "XebecPDF" src/main.py

# O versión con console (para debugging)
pyinstaller --onefile --console --icon=assets/icons/icono.png --add-data "assets;assets" --name "XebecPDF" src/main.py
```

### Installing Dependencies
```bash
pip install -r requirements.txt
pip install -e .                # Install in editable mode
```

## Architecture

### Window Management (WindowManager Pattern)

The project uses a centralized **WindowManager** (singleton) for handling all window transitions:

```
src/gui/pyqt6/window_manager.py  # WindowManager singleton
```

**Key methods:**
- `window_manager.show_main()` - Show main window
- `window_manager.show_editor(document_type)` - Show editor window
- `window_manager.close_editor()` - Close editor and return to main
- `window_manager.has_editor_open` - Check if editor is open
- `window_manager.push_window(type)` - Push current window to stack
- `window_manager.go_back()` - Return to previous window

**Signals:**
- `window_changed(str)` - Emitted when window changes
- `window_opened(str, dict)` - Emitted when a window opens
- `window_closed(str)` - Emitted when a window closes

### File Organization
```
src/
├── main.py                    # Entry point
├── core/                      # Business logic
│   └── pdf_repair.py
├── gui/
│   └── pyqt6/                 # PyQt6 GUI components
│       ├── main_window.py     # MainWindow (QMainWindow)
│       ├── editor_window.py   # EditorWindow + EditorWindowContainer
│       ├── splash_screen.py   # SplashScreen (QSplashScreen)
│       ├── window_manager.py  # WindowManager singleton
│       ├── theme_manager.py   # Theme management
│       └── components.py      # Reusable UI components
└── utils/                     # Utilities
    ├── logger.py
    ├── helpers.py
    └── recent_files.py
```

## Code Style Guidelines

### General Principles
- Use **type hints** for all function parameters and return types
- Use **pathlib.Path** instead of os.path strings
- Use **f-strings** for string formatting
- Use **absolute imports** (from src.package.module import ...)

### Naming Conventions
- **Classes**: PascalCase (e.g., `PDFRepairer`, `MainWindow`, `EditorWindowContainer`)
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
import sys
from pathlib import Path
from typing import Optional, Tuple

from PyQt6.QtWidgets import QMainWindow, QDialog, QWidget
from PyQt6.QtCore import Qt, pyqtSignal

from src.gui.pyqt6.window_manager import window_manager
from src.gui.pyqt6.theme_manager import theme_manager
from src.core.pdf_repair import PDFRepairer
from src.utils.logger import logger
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

### GUI Development (PyQt6)

#### Window Classes
- **QMainWindow**: Use for main application window (has built-in menu bar, toolbar)
- **QDialog**: Use for modal/modeless dialogs and secondary windows
- **QWidget**: Use for custom panels and components

#### Signals and Slots
```python
# Define signals in class
class MyWidget(QWidget):
    my_signal = pyqtSignal(str, int)
    
# Connect signals
self.my_signal.connect(self.handle_signal)

# Emit signals
self.my_signal.emit("value", 42)
```

#### Window Transitions
Always use WindowManager for window transitions:
```python
from src.gui.pyqt6.window_manager import window_manager

# Open editor
window_manager.show_editor(document_type="blank")

# Close editor and return to main
window_manager.close_editor()

# Check state
if window_manager.has_editor_open:
    ...
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

### Logging
Use the project's logger utility:
```python
from src.utils.logger import logger

log = logger.get_logger()
log.info("Message")
log.error("Error message")
```

## Development Workflow

1. **Before writing code**: Understand the existing component structure
2. **Window Management**: Use WindowManager for all window transitions
3. **Testing**: Add tests for new features in `tests/` directory
4. **Error handling**: Always handle exceptions gracefully with user feedback
5. **Theme**: Use `theme_manager.colors` for consistent styling

## Project Configuration

### pyproject.toml Settings
- Package name: `xebec-pdf-fixer`
- Test path: `tests/`
- Build: PyInstaller onefile windowed

## Known Limitations

- Tests directory exists but may be empty - add tests for new features
- No CI/CD configured yet
- No linter/formatter configured (consider adding ruff)

## Skills

Available skills are defined in `.opencode/skills/<name>/SKILL.md`. To use a skill, load it with the `skill` tool:

```python
skill(name: "skill-name")
```

### Available Skills

| Skill | Description |
|-------|-------------|
| skill-commit | Conventional commits (format: `type(scope): description`) |
| skill-sinc | Project synchronization |
| skill-doc | Documentation generation |
| skill-generate | Code generation (tests, components) |
| skill-design | UI/UX design assistance |

### Creating New Skills

When creating a new skill, follow this pattern:

**Folder structure:**
```
.opencode/skills/<skill-name>/
└── SKILL.md
```

**SKILL.md format:**
```markdown
---
name: <skill-name>
description: <description (1-1024 chars)>
---

## What I do
- Describe capabilities

## When to use me
- Describe usage context
```

**Naming rules:**
- 1-64 characters
- Lowercase alphanumeric with single hyphens
- Cannot start or end with hyphen
- Must match folder name

Example for a new skill:
```markdown
---
name: skill-pdf-optimize
description: Optimize PDF files by reducing size
---

## What I do
- Compress images in PDF
- Remove unnecessary metadata
- Flatten forms

## When to use me
Use this when a PDF file is too large and needs to be reduced in size.
```

### Verifying Skills

To verify all skills are properly configured, run:

```
/verify-skills
```

Or manually run the verification script:
```bash
python .opencode/scripts/verify_skills.py
```

**Auto-verification:** A git pre-commit hook (`.git/hooks/pre-commit`) automatically verifies skills when changes are committed to `.opencode/skills/`.

### Qt6WindowEngineering Skill

This skill provides advanced window management capabilities for Qt6 applications:

**Capabilities:**
- WindowManager, NavigationController, StackedNavigation, MultiWindow Orchestration
- Signals-as-events, Dependency Injection, Controllers, ViewModels
- Login → Dashboard → Módulos → Subventanas flows
- Memory & lifecycle: evitar ventanas huérfanas, cierres incorrectos, signal loops
- Animaciones y transiciones modernas de Qt6

**Location:** `src/skills/qt6_window_engineering.py`

**Usage Example:**
```python
from src.gui.pyqt6.window_manager import window_manager

# Advanced navigation patterns
window_manager.push_window("main", data={"user": current_user})
window_manager.go_back()

# Multi-window orchestration
window_manager.open_modal(parent=self, dialog_type="settings")
window_manager.open_detached_window("log_viewer")
```

### Conventional Commits Format
```
<type>(<scope>): <description>

Types: feat, fix, docs, style, refactor, test, chore
Examples:
  feat(pdf): add merge functionality
  fix(gui): resolve theme toggle crash
  feat(window): add WindowManager for navigation
  docs: update README with new commands
```

## Quick Reference

### Importing WindowManager
```python
from src.gui.pyqt6.window_manager import window_manager
```

### Common Patterns
```python
# Create new window
window_manager.show_main()
window_manager.show_editor(document_type="blank")

# Navigate back
window_manager.go_back()

# Check state
if window_manager.has_editor_open:
    if window_manager.has_unsaved_changes:
        # Show confirmation dialog
```

### Theme Management
```python
from src.gui.pyqt6.theme_manager import theme_manager

# Get colors
colors = theme_manager.colors
bg = colors['bg_primary']
accent = colors['accent']

# Change theme
theme_manager.set_theme("dark")  # or "light"

# Listen for changes
theme_manager.theme_changed.connect(self.update_theme)
```
