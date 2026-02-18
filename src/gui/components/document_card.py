from pathlib import Path
from datetime import datetime
from typing import List, Dict
import json

from src.utils.recent_files import SystemRecentFiles


class RecentDocumentsManager:
    RECENT_FILE = Path.home() / ".xebec_pdf" / "recent.json"
    
    @classmethod
    def get_recent_documents(cls, limit: int = 10) -> List[Dict]:
        if not cls.RECENT_FILE.exists():
            return []
            
        try:
            with open(cls.RECENT_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('documents', [])[:limit]
        except Exception:
            return []
    
    @classmethod
    def add_document(cls, file_path: str, file_name: str):
        cls.RECENT_FILE.parent.mkdir(parents=True, exist_ok=True)
        
        documents = cls.get_recent_documents(limit=20)
        
        documents = [d for d in documents if d.get('path') != file_path]
        
        documents.insert(0, {
            'path': file_path,
            'name': file_name,
            'modified': datetime.now().isoformat()
        })
        
        with open(cls.RECENT_FILE, 'w', encoding='utf-8') as f:
            json.dump({'documents': documents[:20]}, f, indent=2)
    
    @classmethod
    def remove_document(cls, file_path: str):
        documents = cls.get_recent_documents(limit=20)
        documents = [d for d in documents if d.get('path') != file_path]
        
        cls.RECENT_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(cls.RECENT_FILE, 'w', encoding='utf-8') as f:
            json.dump({'documents': documents}, f, indent=2)
