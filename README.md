# 🖥️ PROGRAMA COMPLETO – “Xebec PDF Fixer”

Branding: Corporación Xebec

Autor: BGNC

Versión: 0.0.1vs

---

Interfaz gráfica con Tkinter, branding y funciones completas, y falta completar

## Requisitos previos:

```bash
pip install -r requirements.txt
```

## 🟦 Convertirlo en un .EXE para tu escritorio

Cuando ya esté funcionando, puedes convertirlo en un ejecutable:
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=assets/icons/xebec_icon.png src/main.py
```
---

## 🎯 ¿Qué hace este programa?

Se abre como una ventana normal de Windows

- Tiene branding profesional
- Permite seleccionar cualquier carpeta
- Repara todos los PDFs automáticamente
- Guarda los reparados en /fixed

---

## 📁 Estructura del Proyecto

```
PdfSuport/
├── src/                    # Código fuente principal
│   ├── __init__.py
│   ├── main.py             # Punto de entrada
│   ├── gui/                # Interfaz gráfica
│   │   ├── __init__.py
│   │   ├── main_window.py
│   │   ├── widgets/        # Componentes reutilizables
│   │   └── themes/         # Temas (claro/oscuro)
│   ├── core/               # Lógica de negocio
│   │   ├── __init__.py
│   │   ├── pdf_repair.py   # Reparar PDFs
│   │   ├── pdf_merge.py    # Unir PDFs
│   │   ├── pdf_split.py    # Dividir PDFs
│   │   ├── pdf_extract.py  # Extraer páginas
│   │   └── pdf_delete.py   # Eliminar hojas
│   ├── utils/              # Utilidades
│   │   ├── __init__.py
│   │   ├── logger.py       # Logging
│   │   └── helpers.py
│   └── skills/             # Habilidades/Plugins (extensiones)
│       ├── __init__.py
│       └── base.py         # Clase base para skills
├── tests/                  # Tests unitarios
│   ├── __init__.py
│   └── test_core.py
├── assets/                 # Recursos estáticos
│   ├── icons/
│   └── splash/
├── docs/                   # Documentación
├── dist/                   # Builds generados
├── build/                  # Archivos de build
├── scripts/                # Scripts de utilidad
├── requirements.txt        # Dependencias
├── setup.py                # Configuración del paquete
├── pyproject.toml          # Configuración moderna
└── README.md
```

---

## agregar funcionalidades faltantes

Falta añadirle:

### Fase 1 - Estabilidad y UX
- [x] Barra de progreso durante el procesamiento
- [x] Reparar un solo PDF (botón adicional)
- [x] Tema oscuro
- [x] Logs detallados (ventana o archivo)
- [ ] Splash screen con logo de Xebec

### Fase 2 - Funcionalidades PDF
- [ ] Unir PDFs (combinar archivos)
- [ ] Separar/Dividir PDF (extraer páginas)
- [ ] Eliminar hojas específicas
- [ ] Rotar páginas
- [ ] Reordenar páginas (drag & drop)

### Fase 3 - Escalabilidad
- [ ] Sistema de plugins para extensiones
- [ ] Historial de operaciones
- [ ] Exportar a otros formatos (imágenes)
- [ ] Cifrado/Descifrado PDFs

### Mejoras Técnicas
- [x] Migrar de PyPDF2 (deprecated) a pypdf o pymupdf
- [ ] Añadir tests unitarios
- [ ] Configurar CI/CD para builds automáticos
- [ ] Crear installer profesional (Inno Setup, NSIS)

Solo dime qué más quieres que tenga.