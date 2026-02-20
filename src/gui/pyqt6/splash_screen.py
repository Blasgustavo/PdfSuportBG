from PyQt6.QtWidgets import QApplication, QSplashScreen, QProgressBar, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QRectF
from PyQt6.QtGui import QPixmap, QPainter, QColor, QFont, QLinearGradient, QPainterPath, QBrush, QPen
from pathlib import Path
import time
import math
import random


class AnimatedSplash(QSplashScreen):
    """Splash screen animado con branding XEBEC CORPORATION."""
    
    def __init__(self):
        self.logo_path = self._get_logo_path()
        
        self._width = 700
        self._height = 500
        
        self._opacity = 0.0
        self._progress = 0
        self._loading_text = "Inicializando..."
        self._pulse = 0
        self._star_positions = self._generate_star_positions()
        
        pixmap = QPixmap(self._width, self._height)
        super().__init__(pixmap)
        
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setEnabled(False)
        
        self._animation_timer = QTimer()
        self._animation_timer.timeout.connect(self._animate)
        self._animation_timer.start(50)
        
        self._draw_content(pixmap)
    
    def _generate_star_positions(self):
        """Genera posiciones fijas para las estrellas."""
        random.seed(42)
        stars = []
        for _ in range(50):
            stars.append({
                'x': random.randint(0, self._width),
                'y': random.randint(0, self._height),
                'size': random.uniform(0.5, 1.5),
                'alpha': random.randint(20, 60)
            })
        return stars
    
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
    
    def _animate(self):
        """Animación de pulso."""
        self._pulse += 0.1
        self._draw_content(self.pixmap())
        self.repaint()
        QApplication.processEvents()
    
    def _draw_content(self, pixmap: QPixmap):
        """Dibuja el contenido del splash con gradientes y efectos."""
        pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        
        # Fondo con gradiente diagonal XEBEC
        gradient = QLinearGradient(0, 0, self._width, self._height)
        gradient.setColorAt(0, QColor("#1E3A5F"))
        gradient.setColorAt(0.5, QColor("#0E2A4F"))
        gradient.setColorAt(1, QColor("#1A202C"))
        
        painter.fillRect(pixmap.rect(), gradient)
        
        # Efecto de partículas/estrellas sutiles
        self._draw_stars(painter)
        
        # Logo con efecto glow
        self._draw_logo(painter)
        
        # Título corporativo
        self._draw_title(painter)
        
        # Subtítulo
        self._draw_subtitle(painter)
        
        # Barra de progreso
        self._draw_progress_bar(painter)
        
        # Texto de carga
        self._draw_loading_text(painter)
        
        # Versión
        self._draw_version(painter)
        
        # Marca de agua corporativa
        self._draw_branding(painter)
        
        painter.end()
        
        self.setPixmap(pixmap)
    
    def _draw_stars(self, painter: QPainter):
        """Dibuja estrellas de fondo."""
        painter.save()
        
        for star in self._star_positions:
            color = QColor(255, 255, 255, star['alpha'])
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(color))
            painter.drawEllipse(star['x'], star['y'], int(star['size']), int(star['size']))
        
        painter.restore()
    
    def _draw_logo(self, painter: QPainter):
        """Dibuja el logo con efecto glow."""
        if self.logo_path and self.logo_path.exists():
            logo = QPixmap(str(self.logo_path))
            if not logo.isNull():
                pulse_scale = 1.0 + math.sin(self._pulse) * 0.02
                size = int(80 * pulse_scale)
                
                scaled_logo = logo.scaled(
                    size, size,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                
                x = (self._width - scaled_logo.width()) // 2
                y = 80
                
                # Glow effect
                for i in range(3):
                    glow_size = size + (i + 1) * 20
                    glow_alpha = 30 - i * 10
                    glow_color = QColor("#F6993F")
                    glow_color.setAlpha(glow_alpha)
                    painter.setPen(Qt.PenStyle.NoPen)
                    painter.setBrush(QBrush(glow_color))
                    center_x = self._width // 2 - glow_size // 2 + 10
                    painter.drawEllipse(center_x, y - 5, glow_size, glow_size)
                
                painter.drawPixmap(x + 10, y + 5, scaled_logo)
        else:
            # Logo de texto si no hay imagen
            pulse_scale = 1.0 + math.sin(self._pulse) * 0.05
            font_size = max(1, int(48 * pulse_scale))  # Ensure at least 1
            
            glow_color = QColor("#F6993F")
            glow_color.setAlpha(50)
            painter.setPen(glow_color)
            painter.setFont(QFont("Segoe UI", font_size, QFont.Weight.Bold))
            rect = QRectF(0, 100, self._width, 60)
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, "X")
    
    def _draw_title(self, painter: QPainter):
        """Dibuja el título corporativo."""
        # Sombra
        shadow_color = QColor(0, 0, 0, 100)
        painter.setPen(shadow_color)
        painter.setFont(QFont("Segoe UI", 36, QFont.Weight.Bold))
        rect = QRectF(0, 155, self._width, 45)
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, "XEBEC")
        
        # Texto principal
        painter.setPen(QColor("#FFFFFF"))
        painter.setFont(QFont("Segoe UI", 36, QFont.Weight.Bold))
        rect = QRectF(0, 153, self._width, 45)
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, "XEBEC")
        
        # PDF Fixer en accent
        accent_color = QColor("#F6993F")
        painter.setPen(accent_color)
        painter.setFont(QFont("Segoe UI", 22, QFont.Weight.Normal))
        rect = QRectF(0, 198, self._width, 30)
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, "PDF Fixer")
    
    def _draw_subtitle(self, painter: QPainter):
        """Dibuja el subtítulo."""
        painter.setPen(QColor("#A0AEC0"))
        painter.setFont(QFont("Segoe UI", 11))
        rect = QRectF(0, 230, self._width, 20)
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, "Corporación Xebec")
    
    def _draw_progress_bar(self, painter: QPainter):
        """Dibuja la barra de progreso."""
        bar_width = 400
        bar_height = 6
        bar_x = (self._width - bar_width) // 2
        bar_y = 310
        
        # Fondo de la barra
        bg_color = QColor(0, 0, 0, 80)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(bg_color))
        rect = QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRoundedRect(rect, 3, 3)
        
        # Progreso con gradiente
        if self._progress > 0:
            fill_width = int((self._progress / 100) * bar_width)
            
            progress_gradient = QLinearGradient(bar_x, 0, bar_x + bar_width, 0)
            progress_gradient.setColorAt(0, QColor("#F6993F"))
            progress_gradient.setColorAt(1, QColor("#F6AD55"))
            
            painter.setBrush(QBrush(progress_gradient))
            fill_rect = QRectF(bar_x, bar_y, fill_width, bar_height)
            painter.drawRoundedRect(fill_rect, 3, 3)
    
    def _draw_loading_text(self, painter: QPainter):
        """Dibuja el texto de carga."""
        alpha = 180 + int(math.sin(self._pulse * 2) * 50)
        text_color = QColor("#F6993F")
        text_color.setAlpha(alpha)
        
        painter.setPen(text_color)
        painter.setFont(QFont("Segoe UI", 10))
        
        dots = "." * (int(self._pulse * 3) % 4)
        text = f"{self._loading_text}{dots}"
        
        rect = QRectF(0, 325, self._width, 20)
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, text)
    
    def _draw_version(self, painter: QPainter):
        """Dibuja la versión."""
        painter.setPen(QColor("#4A5568"))
        painter.setFont(QFont("Segoe UI", 9))
        rect = QRectF(0, 405, self._width, 20)
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, "Autor: XEBEC CORPORATION  |  Versión: 1.0.0")
    
    def _draw_branding(self, painter: QPainter):
        """Dibuja marca de agua corporativa."""
        painter.setPen(QColor(255, 255, 255, 10))
        painter.setFont(QFont("Segoe UI", 60, QFont.Weight.Bold))
        
        painter.save()
        painter.translate(self._width // 2, self._height // 2)
        painter.rotate(-30)
        painter.drawText(QRectF(-200, -40, 400, 80), Qt.AlignmentFlag.AlignCenter, "XEBEC")
        painter.restore()

    def update_progress(self, value: int, status: str = ""):
        """Actualiza el progreso."""
        self._progress = value
        if status:
            self._loading_text = status
        
        self._draw_content(self.pixmap())
        QApplication.processEvents()

    def simulate_loading(self, callback):
        """Simula la carga con pasos."""
        steps = [
            (15, "Inicializando..."),
            (30, "Cargando configuración..."),
            (50, "Preparando interfaz..."),
            (70, "Cargando módulos PDF..."),
            (85, "Inicializando sistema..."),
            (100, "¡Listo!")
        ]
        
        for progress, status in steps:
            self.update_progress(progress, status)
            time.sleep(0.3)
        
        QTimer.singleShot(300, callback)


# Alias para compatibilidad
SplashScreen = AnimatedSplash
