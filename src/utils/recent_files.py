import ctypes
from ctypes import wintypes
from pathlib import Path
from typing import List, Dict
import os
from datetime import datetime


CSIDL_RECENT = 0x0008
CSIDL_PERSONAL = 0x0005
CSIDL_DESKTOP = 0x0010
CSIDL_DOWNLOAD = 0x0035
SHGFP_TYPE_CURRENT = 0
SHARD_PATHW = 0x0003


def get_recent_folder() -> Path:
    """Obtiene la ruta de la carpeta Recent de Windows."""
    buf = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_RECENT, None, SHGFP_TYPE_CURRENT, buf)
    return Path(buf.value)


def get_special_folder(csidl: int) -> Path:
    """Obtiene una carpeta especial de Windows."""
    buf = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(None, csidl, None, SHGFP_TYPE_CURRENT, buf)
    return Path(buf.value)


def resolve_shortcut(lnk_path: Path) -> Path:
    """Resuelve un archivo .lnk y devuelve la ruta real."""
    try:
        import pythoncom
        from win32com.shell import shell, shellcon
        
        shortcut = pythoncom.CoCreateInstance(shell.CLSID_ShellLink, None, pythoncom.CLSCTX_INPROC_SERVER, shell.IShellLinkW)
        shortcut.QueryInterface(shell.IID_IPersistFile).Load(lnk_path)
        
        buf = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
        shortcut.GetPath(buf, wintypes.MAX_PATH)
        
        return Path(buf.value)
    except Exception:
        pass
    
    try:
        from winshell import shell_link
        return Path(shell_link(str(lnk_path)))
    except Exception:
        pass
    
    return lnk_path


def get_pdfs_from_folder(folder: Path, max_results: int = 100) -> List[Path]:
    """Obtiene PDFs de una carpeta."""
    if not folder.exists():
        return []
    try:
        return list(folder.glob("*.pdf"))[:max_results]
    except Exception:
        return []


def get_recent_pdfs(limit: int = 20) -> List[Dict]:
    """Obtiene PDFs recientes del sistema buscando en carpetas comunes."""
    user_home = Path.home()
    
    search_folders = [
        user_home / "Documents",
        user_home / "Desktop",
        user_home / "Downloads",
    ]
    
    all_pdfs = []
    for folder in search_folders:
        if folder.exists():
            try:
                for pdf in folder.glob("*.pdf"):
                    try:
                        if pdf.exists():
                            all_pdfs.append(pdf)
                    except Exception:
                        continue
            except Exception:
                continue
    
    pdfs_with_time = []
    for pdf in all_pdfs:
        try:
            stat = pdf.stat()
            pdfs_with_time.append({
                "path": str(pdf),
                "name": pdf.name,
                "modified_timestamp": stat.st_mtime,
                "size": stat.st_size
            })
        except Exception:
            continue
    
    pdfs_with_time.sort(key=lambda x: x["modified_timestamp"], reverse=True)
    
    result = []
    for pdf in pdfs_with_time[:limit]:
        modified_date = datetime.fromtimestamp(pdf["modified_timestamp"])
        result.append({
            "path": pdf["path"],
            "name": pdf["name"],
            "modified": modified_date.strftime("%d/%m/%Y %H:%M"),
            "modified_timestamp": pdf["modified_timestamp"],
            "size": pdf["size"]
        })
    
    return result


def add_to_recent_docs(file_path: str) -> None:
    """Agrega un archivo a los documentos recientes de Windows."""
    ctypes.windll.shell32.SHAddToRecentDocs(SHARD_PATHW, file_path)


class SystemRecentFiles:
    """Clase para gestionar los archivos PDF recientes del sistema."""
    
    @staticmethod
    def get_pdfs(limit: int = 20) -> List[Dict]:
        """Obtiene la lista de PDFs recientes."""
        return get_recent_pdfs(limit)
    
    @staticmethod
    def add_file(file_path: str) -> None:
        """Agrega un archivo a documentos recientes de Windows."""
        add_to_recent_docs(file_path)
