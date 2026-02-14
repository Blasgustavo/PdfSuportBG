# 🚀 Guía de Instalación - Xebec Pdf

Esta guía te ayudará a instalar y ejecutar Xebec Pdf en tu máquina.

---

## 📋 Requisitos del Sistema

### Sistema Operativo
- **Windows 10** o superior (64-bit)
- Windows 11 recomendado

### Hardware Mínimo
- **RAM**: 4 GB
- **Disco**: 500 MB de espacio libre
- **Resolución**: 1280x720 o superior

### Software Requerido
- **Python**: 3.8 o superior (3.10+ recomendado)
- **pip**: Gestor de paquetes de Python
- **Git**: Para clonar el repositorio (opcional)

---

## 🔧 Instalación Paso a Paso

### 1. Instalar Python

1. Descarga Python desde [python.org](https://www.python.org/downloads/)
2. **IMPORTANTE**: Marca la casilla "Add Python to PATH" durante la instalación
3. Verifica la instalación:
   ```cmd
   python --version
   ```

### 2. Clonar o Descargar el Proyecto

**Opción A: Usando Git (Recomendado)**
```cmd
git clone https://github.com/Blasgustavo/PdfSuportBG.git
cd PdfSuportBG
```

**Opción B: Descarga manual**
1. Ve a https://github.com/Blasgustavo/PdfSuportBG
2. Click en "Code" → "Download ZIP"
3. Extrae el archivo ZIP
4. Abre la carpeta `PdfSuportBG-main`

### 3. Instalar Dependencias

Abre una terminal (CMD o PowerShell) en la carpeta del proyecto y ejecuta:

```cmd
pip install -r requirements.txt
```

**Dependencias incluidas:**
- `pypdf>=3.0.0` - Procesamiento de PDFs
- `Pillow>=9.0.0` - Manejo de imágenes
- `pyinstaller>=5.0` - Para crear ejecutables

### 4. Verificar Instalación

Ejecuta el siguiente comando para verificar que todo está correcto:

```cmd
python src/main.py
```

Si ves el Splash Screen de Xebec Pdf, la instalación fue exitosa.

---

## 🎯 Ejecución del Proyecto

### Modo Desarrollo

Para ejecutar la aplicación en modo desarrollo:

```cmd
python src/main.py
```

El flujo de la aplicación será:
1. **Splash Screen** - Pantalla de carga con branding
2. **Panel de Inicio** - Documentos recientes y plantillas
3. **Herramientas PDF** - Reparar, unir, dividir PDFs

---

## 📦 Crear Ejecutable (.exe)

Para distribuir la aplicación sin necesidad de Python instalado:

### 1. Instalar PyInstaller (si no está instalado)

```cmd
pip install pyinstaller
```

### 2. Generar el Ejecutable

```cmd
pyinstaller --onefile --windowed --icon=assets/icons/icono.png --name "XebecPdf" src/main.py
```

### 3. Ubicación del Ejecutable

Después de compilar, el ejecutable estará en:
```
dist/XebecPdf.exe
```

### 4. Distribución

Para distribuir la aplicación:
1. Copia el archivo `dist/XebecPdf.exe`
2. Incluye la carpeta `assets` si es necesario

---

## 🐛 Solución de Problemas

### Error: "python no se reconoce como comando"

**Solución:**
1. Reinstala Python marcando "Add Python to PATH"
2. O agrega Python manualmente al PATH de Windows

### Error: "No module named 'pypdf'"

**Solución:**
```cmd
pip install pypdf Pillow pyinstaller
```

### Error: "Permission denied" al instalar paquetes

**Solución (Windows):**
```cmd
pip install -r requirements.txt --user
```

O ejecuta CMD como Administrador.

### Error: "No se encuentra el archivo icono.png"

**Solución:**
Asegúrate de estar en la carpeta raíz del proyecto (donde está `src/`):
```cmd
cd C:\ruta\al\proyecto\PdfSuportBG
python src/main.py
```

### Error: "ImportError: cannot import name 'Image' from 'PIL'"

**Solución:**
```cmd
pip uninstall Pillow
pip install Pillow
```

---

## 📝 Notas Adicionales

### Fuentes Personalizadas

La aplicación descarga automáticamente **JetBrains Mono** en la primera ejecución. Las fuentes se guardan en:
```
assets/fonts/
```

### Historial de Documentos

Los documentos recientes se guardan en:
```
%USERPROFILE%\.xebec_pdf\recent.json
```

### Logs

Los logs de la aplicación se guardan en:
```
logs/XebecPDF_YYYYMMDD.log
```

---

## 🆘 Soporte

Si encuentras algún problema:

1. Revisa que cumples con todos los requisitos
2. Verifica los mensajes de error en la terminal
3. Consulta los logs en la carpeta `logs/`
4. Abre un issue en GitHub: https://github.com/Blasgustavo/PdfSuportBG/issues

---

## ✅ Checklist de Instalación

- [ ] Python 3.8+ instalado y en PATH
- [ ] Proyecto descargado/clonado
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Aplicación ejecuta correctamente (`python src/main.py`)
- [ ] Splash screen visible
- [ ] Panel de inicio funciona

---

**Version**: 0.0.1  
**Last Updated**: 2026-02-14  
**Author**: BGNC - Corporación Xebec
