import os
import urllib.request
import zipfile
from pathlib import Path
import shutil


class FontManager:
    FONTS_URL = "https://github.com/ryanoasis/nerd-fonts/releases/download/v3.0.2/JetBrainsMono.zip"
    
    @staticmethod
    def get_fonts_dir():
        base_path = Path(__file__).parent.parent.parent
        return base_path / "assets" / "fonts"
    
    @staticmethod
    def download_fonts():
        fonts_dir = FontManager.get_fonts_dir()
        fonts_dir.mkdir(parents=True, exist_ok=True)
        
        font_file = fonts_dir / "JetBrainsMono-Regular.ttf"
        bold_file = fonts_dir / "JetBrainsMono-Bold.ttf"
        
        if font_file.exists() and bold_file.exists():
            print("Fuentes ya descargadas")
            return True
            
        print("Descargando fuentes JetBrains Mono...")
        
        try:
            zip_path = fonts_dir / "fonts.zip"
            
            urllib.request.urlretrieve(
                "https://github.com/JetBrains/JetBrainsMono/releases/download/v2.304/JetBrainsMono-2.304.zip",
                zip_path
            )
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                for file in zip_ref.namelist():
                    if "JetBrainsMono-Regular.ttf" in file:
                        zip_ref.extract(file, fonts_dir)
                        extracted = list(fonts_dir.glob("**/JetBrainsMono-Regular.ttf"))[0]
                        extracted.rename(font_file)
                    elif "JetBrainsMono-Bold.ttf" in file:
                        zip_ref.extract(file, fonts_dir)
                        extracted = list(fonts_dir.glob("**/JetBrainsMono-Bold.ttf"))[0]
                        extracted.rename(bold_file)
            
            zip_path.unlink()
            
            for item in fonts_dir.glob("*"):
                if item.is_dir():
                    shutil.rmtree(item)
                    
            print(f"Fuentes descargadas en: {fonts_dir}")
            return True
            
        except Exception as e:
            print(f"Error descargando fuentes: {e}")
            return False
    
    @staticmethod
    def load_font(root, font_name="JetBrainsMono"):
        fonts_dir = FontManager.get_fonts_dir()
        font_file = fonts_dir / "JetBrainsMono-Regular.ttf"
        
        if font_file.exists():
            try:
                root.tk.call("font", "create", font_name, "-family", str(font_file))
                return font_name
            except Exception as e:
                print(f"Error cargando fuente: {e}")
                return None
        return None
