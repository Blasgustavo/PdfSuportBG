from pathlib import Path
from typing import Tuple, Optional
from PyPDF2 import PdfReader, PdfWriter


class PDFRepairer:
    @staticmethod
    def repair(input_path: Path, output_path: Path) -> Tuple[bool, Optional[str]]:
        try:
            reader = PdfReader(str(input_path))
            writer = PdfWriter()

            for page in reader.pages:
                writer.add_page(page)

            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "wb") as f:
                writer.write(f)

            return True, None
        except Exception as e:
            return False, str(e)

    @staticmethod
    def repair_folder(folder: Path, output_subfolder: str = "fixed") -> dict:
        pdfs = list(folder.glob("*.pdf"))
        results = {"success": 0, "failed": 0, "errors": []}

        if not pdfs:
            results["error"] = "No se encontraron archivos PDF"
            return results

        output_folder = folder / output_subfolder
        output_folder.mkdir(parents=True, exist_ok=True)

        for pdf in pdfs:
            output_path = output_folder / pdf.name
            success, error = PDFRepairer.repair(pdf, output_path)
            if success:
                results["success"] += 1
            else:
                results["failed"] += 1
                results["errors"].append(f"{pdf.name}: {error}")

        return results
