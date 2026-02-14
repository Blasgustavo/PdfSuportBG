import os
import sys
from pathlib import Path
from tkinter import Tk, Label, Button, filedialog, messagebox, PhotoImage
from PyPDF2 import PdfReader, PdfWriter

APP_NAME = "Xebec PDF Fixer"
APP_VERSION = "0.0.1vs"
APP_AUTHOR = "BGNC"
APP_ORG = "Corporación Xebec"

def repair_pdf(input_path: Path, output_path: Path):
    try:
        reader = PdfReader(str(input_path))
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "wb") as f:
            writer.write(f)

        return True
    except Exception as e:
        print(f"Error reparando {input_path.name}: {e}")
        return False

def repair_folder(folder: Path):
    pdfs = list(folder.glob("*.pdf"))
    if not pdfs:
        messagebox.showinfo("Sin PDFs", "No se encontraron archivos PDF en esta carpeta.")
        return

    fixed_folder = folder / "fixed"
    ok = 0
    fail = 0

    for pdf in pdfs:
        out = fixed_folder / pdf.name
        if repair_pdf(pdf, out):
            ok += 1
        else:
            fail += 1

    messagebox.showinfo(
        "Proceso completado",
        f"PDFs reparados: {ok}\nFallidos: {fail}\n\nGuardados en:\n{fixed_folder}"
    )

def select_folder():
    folder = filedialog.askdirectory(title="Selecciona una carpeta con PDFs")
    if folder:
        repair_folder(Path(folder))

def center_window(window, width=420, height=300):
    screen_w = window.winfo_screenwidth()
    screen_h = window.winfo_screenheight()
    x = (screen_w // 2) - (width // 2)
    y = (screen_h // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

def main():
    root = Tk()
    root.title(APP_NAME)

    try:
        icon_path = Path("xebec_icon.png")
        if icon_path.exists():
            icon = PhotoImage(file=str(icon_path))
            root.iconphoto(True, icon)
    except:
        pass

    center_window(root)

    Label(root, text=f"{APP_NAME}", font=("Segoe UI", 16, "bold")).pack(pady=10)
    Label(root, text=f"{APP_ORG}", font=("Segoe UI", 12)).pack()
    Label(root, text=f"Autor: {APP_AUTHOR} | Versión: {APP_VERSION}", font=("Segoe UI", 10)).pack(pady=5)

    Label(root, text="🧰 Reparador de PDFs para Vista Previa de Windows", font=("Segoe UI", 11)).pack(pady=10)

    Button(
        root,
        text="📂 Seleccionar carpeta y reparar PDFs",
        font=("Segoe UI", 12),
        width=30,
        command=select_folder
    ).pack(pady=20)

    Button(
        root,
        text="Salir",
        font=("Segoe UI", 10),
        width=15,
        command=root.destroy
    ).pack()

    root.mainloop()

if __name__ == "__main__":
    main()
