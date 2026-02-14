import threading
from pathlib import Path
from tkinter import Tk, Label, Button, filedialog, messagebox, PhotoImage, ttk
from src.core.pdf_repair import PDFRepairer
from src.utils.helpers import center_window, get_icon_path
from src.utils.logger import logger
from src.gui.themes import DARK_THEME


APP_NAME = "Xebec Pdf"
APP_VERSION = "0.0.1vs"
APP_AUTHOR = "BGNC"
APP_ORG = "Corporación Xebec"


class MainWindow:
    def __init__(self, root: Tk):
        self.root = root
        self.root.title(APP_NAME)
        self.theme = DARK_THEME
        self._apply_theme()
        self._setup_icon()
        center_window(self.root, width=450, height=380)
        self._build_ui()
        self.log = logger.get_logger()

    def _apply_theme(self):
        self.root.configure(bg=self.theme["bg_primary"])
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "TProgressbar",
            thickness=20,
            background=self.theme["accent"],
            troughcolor=self.theme["bg_tertiary"],
        )

    def _setup_icon(self):
        icon_path = get_icon_path()
        if icon_path and icon_path.exists():
            try:
                icon = PhotoImage(file=str(icon_path))
                self.root.iconphoto(True, icon)
            except Exception:
                pass

    def _build_ui(self):
        Label(
            self.root,
            text=APP_NAME,
            font=("Segoe UI", 16, "bold"),
            bg=self.theme["bg_primary"],
            fg=self.theme["fg_primary"]
        ).pack(pady=10)

        Label(
            self.root,
            text=APP_ORG,
            font=("Segoe UI", 12),
            bg=self.theme["bg_primary"],
            fg=self.theme["fg_secondary"]
        ).pack()

        Label(
            self.root,
            text=f"Autor: {APP_AUTHOR} | Versión: {APP_VERSION}",
            font=("Segoe UI", 10),
            bg=self.theme["bg_primary"],
            fg=self.theme["fg_secondary"]
        ).pack(pady=5)

        Label(
            self.root,
            text="🧰 Reparador de PDFs para Vista Previa de Windows",
            font=("Segoe UI", 11),
            bg=self.theme["bg_primary"],
            fg=self.theme["fg_primary"]
        ).pack(pady=10)

        self.progress = ttk.Progressbar(
            self.root,
            mode="determinate",
            length=350,
            style="TProgressbar"
        )
        self.progress.pack(pady=10)
        self.progress["value"] = 0

        self.status_label = Label(
            self.root,
            text="Listo",
            font=("Segoe UI", 9),
            bg=self.theme["bg_primary"],
            fg=self.theme["fg_secondary"]
        )
        self.status_label.pack(pady=5)

        Button(
            self.root,
            text="📂 Seleccionar carpeta y reparar PDFs",
            font=("Segoe UI", 11),
            width=32,
            bg=self.theme["accent"],
            fg=self.theme["fg_primary"],
            activebackground=self.theme["accent_hover"],
            command=self._select_folder_threaded
        ).pack(pady=10)

        Button(
            self.root,
            text="📄 Reparar un solo PDF",
            font=("Segoe UI", 10),
            width=32,
            bg=self.theme["bg_tertiary"],
            fg=self.theme["fg_primary"],
            command=self._repair_single_pdf
        ).pack(pady=5)

        Button(
            self.root,
            text="Salir",
            font=("Segoe UI", 10),
            width=15,
            bg=self.theme["bg_tertiary"],
            fg=self.theme["fg_primary"],
            command=self.root.destroy
        ).pack(pady=15)

    def _select_folder_threaded(self):
        folder = filedialog.askdirectory(title="Selecciona una carpeta con PDFs")
        if not folder:
            return

        self.status_label.config(text="Procesando...")
        self.progress["value"] = 0
        thread = threading.Thread(target=self._process_folder, args=(Path(folder),))
        thread.daemon = True
        thread.start()

    def _process_folder(self, folder: Path):
        try:
            pdfs = list(folder.glob("*.pdf"))
            total = len(pdfs)

            if total == 0:
                self.root.after(0, lambda: messagebox.showinfo(
                    "Sin PDFs", "No se encontraron archivos PDF en esta carpeta."
                ))
                self.root.after(0, lambda: self.status_label.config(text="Listo"))
                return

            fixed_folder = folder / "fixed"
            ok = 0
            fail = 0

            for i, pdf in enumerate(pdfs):
                output_path = fixed_folder / pdf.name
                success, error = PDFRepairer.repair(pdf, output_path)
                if success:
                    ok += 1
                    self.log.info(f"Reparado: {pdf.name}")
                else:
                    fail += 1
                    self.log.error(f"Error en {pdf.name}: {error}")

                progress = ((i + 1) / total) * 100
                self.root.after(0, lambda p=progress: self.progress.config(value=p))

            self.root.after(0, lambda: messagebox.showinfo(
                "Proceso completado",
                f"PDFs reparados: {ok}\nFallidos: {fail}\n\nGuardados en:\n{fixed_folder}"
            ))
            self.root.after(0, lambda: self.progress.config(value=0))
            self.root.after(0, lambda: self.status_label.config(text="Listo"))

        except Exception as e:
            self.log.error(f"Error en proceso: {e}")
            self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
            self.root.after(0, lambda: self.status_label.config(text="Error"))

    def _repair_single_pdf(self):
        file_path = filedialog.askopenfilename(
            title="Selecciona un PDF",
            filetypes=[("PDF files", "*.pdf")]
        )
        if not file_path:
            return

        input_path = Path(file_path)
        output_path = input_path.parent / "fixed" / input_path.name

        success, error = PDFRepairer.repair(input_path, output_path)

        if success:
            self.log.info(f"PDF reparado: {input_path.name}")
            messagebox.showinfo(
                "Éxito",
                f"PDF reparado correctamente.\n\nGuardado en:\n{output_path}"
            )
        else:
            self.log.error(f"Error al reparar {input_path.name}: {error}")
            messagebox.showerror("Error", f"No se pudo reparar el PDF:\n{error}")
