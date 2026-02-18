from PyQt6.QtWidgets import QApplication, QSplashScreen, QProgressBar, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QPainter, QColor, QFont, QLinearGradient
from pathlib import Path
import time


class SplashScreen(QSplashScreen):
    def __init__(self):
        self.logo_path = self._get_logo_path()
        
        pixmap = QPixmap(600, 400)
        pixmap.fill(QColor("#0F0F0F"))
        
        super().__init__(pixmap)
        
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setEnabled(False)
        
        self._draw_content(pixmap)
        
    def _get_logo_path(self):
        possible_paths = [
            Path.cwd() / "assets" / "icons" / "logo.png",
            Path.cwd() / "assets" / "icons" / "icono.png",
            Path(__file__).parent.parent.parent / "assets" / "icons" / "logo.png",
            Path(__file__).parent.parent.parent / "assets" / "icons" / "icono.png",
        ]
        for path in possible_paths:
            if path.exists():
                return path
        return None

    def _draw_content(self, pixmap: QPixmap):
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        if self.logo_path and self.logo_path.exists():
            logo = QPixmap(str(self.logo_path))
            if not logo.isNull():
                scaled_logo = logo.scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                x = (pixmap.width() - scaled_logo.width()) // 2
                painter.drawPixmap(x, 100, scaled_logo)
        
        painter.setPen(QColor("#FFFFFF"))
        painter.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        painter.drawText(pixmap.rect().adjusted(0, 190, 0, -100), Qt.AlignmentFlag.AlignCenter, "Xebec Pdf")
        
        painter.setPen(QColor("#666666"))
        painter.setFont(QFont("Segoe UI", 11))
        painter.drawText(pixmap.rect().adjusted(0, 230, 0, -80), Qt.AlignmentFlag.AlignCenter, "Corporación Xebec")
        
        painter.setPen(QColor("#444444"))
        painter.setFont(QFont("Segoe UI", 10))
        painter.drawText(pixmap.rect().adjusted(0, 255, 0, -50), Qt.AlignmentFlag.AlignCenter, "Autor: BGNC  |  Versión: 0.0.1")
        
        gradient = QLinearGradient(0, 330, 400, 330)
        gradient.setColorAt(0, QColor("#333333"))
        gradient.setColorAt(0.5, QColor("#FFFFFF"))
        gradient.setColorAt(1, QColor("#333333"))
        
        painter.setPen(QColor("#333333"))
        painter.drawRect(100, 340, 400, 4)
        
        painter.setPen(QColor("#666666"))
        painter.setFont(QFont("Segoe UI", 9))
        self._status_text = "Cargando..."
        painter.drawText(pixmap.rect().adjusted(0, 365, 0, -20), Qt.AlignmentFlag.AlignCenter, self._status_text)
        
        painter.end()
        
        self.setPixmap(pixmap)

    def update_progress(self, value: int, status: str = ""):
        if status:
            self._status_text = status
            
            pixmap = QPixmap(600, 400)
            pixmap.fill(QColor("#0F0F0F"))
            
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            
            if self.logo_path and self.logo_path.exists():
                logo = QPixmap(str(self.logo_path))
                if not logo.isNull():
                    scaled_logo = logo.scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                    x = (pixmap.width() - scaled_logo.width()) // 2
                    painter.drawPixmap(x, 100, scaled_logo)
            
            painter.setPen(QColor("#FFFFFF"))
            painter.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
            painter.drawText(pixmap.rect().adjusted(0, 190, 0, -100), Qt.AlignmentFlag.AlignCenter, "Xebec Pdf")
            
            painter.setPen(QColor("#666666"))
            painter.setFont(QFont("Segoe UI", 11))
            painter.drawText(pixmap.rect().adjusted(0, 230, 0, -80), Qt.AlignmentFlag.AlignCenter, "Corporación Xebec")
            
            painter.setPen(QColor("#444444"))
            painter.setFont(QFont("Segoe UI", 10))
            painter.drawText(pixmap.rect().adjusted(0, 255, 0, -50), Qt.AlignmentFlag.AlignCenter, "Autor: BGNC  |  Versión: 0.0.1")
            
            painter.setPen(QColor("#333333"))
            painter.drawRect(100, 340, 400, 4)
            
            fill_width = int((value / 100) * 400)
            if fill_width > 0:
                painter.setBrush(QColor("#FFFFFF"))
                painter.setPen(Qt.PenStyle.NoPen)
                painter.drawRect(100, 340, fill_width, 4)
            
            painter.setPen(QColor("#666666"))
            painter.setFont(QFont("Segoe UI", 9))
            painter.drawText(pixmap.rect().adjusted(0, 365, 0, -20), Qt.AlignmentFlag.AlignCenter, status)
            
            painter.end()
            
            self.setPixmap(pixmap)
        
        QApplication.processEvents()

    def simulate_loading(self, callback):
        steps = [
            (20, "Iniciando..."),
            (40, "Cargando configuración..."),
            (60, "Preparando interfaz..."),
            (80, "Cargando herramientas..."),
            (100, "¡Listo!")
        ]
        
        for progress, status in steps:
            self.update_progress(progress, status)
            time.sleep(0.15)
        
        QTimer.singleShot(100, callback)
