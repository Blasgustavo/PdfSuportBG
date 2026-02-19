from PyQt6.QtWidgets import QApplication, QSplashScreen, QProgressBar, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QPixmap, QPainter, QColor, QFont, QLinearGradient, QPainterPath, QBrush
from pathlib import Path
import time
import math


class AnimatedSplash(QSplashScreen):
    """Splash screen animado con branding XEBEC CORPORATION."""
    
    def __init__(self):
        self.logo_path = self._get_logo_path()
        
        # Tamaño del splash
        self._width = 700
        self._height = 500
        
        # Estado de animación
        self._opacity = 0.0
        self._progress = 0
        self._loading_text = "Inicializando..."
        self._pulse = 0
        
        pixmap = QPixmap(self._width, self._height)
        super().__init__(pixmap)
        
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setEnabled(False)
        
        # Timer para animación de pulso
        self._animation_timer = QTimer()
        self._animation_timer.timeout.connect(self._animate)
        self._animation_timer.start(50)  # 20fps
        
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
        gradient.setColorAt(0, QColor("#1E3A5F"))  # Primary XEBEC
        gradient.setColorAt(0.5, QColor("#0E2A4F"))  # Primary dark
        gradient.setColorAt(1, QColor("#1A202C"))  # Dark bg
        
        # Fondo principal
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
        
        # Usar una semilla fija para que las estrellas no parpadeen
        import random
        random.seed(42)
        
        for _ in range(50):
            x = random.randint(0, self._width)
            y = random.randint(0, self._height)
            size = random.uniform(0.5, 1.5)
            
            # Color con transparencia
            alpha = random.randint(20, 60)
            color = QColor(255, 255, 255, alpha)
            
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(color))
            painter.drawEllipse(x, y, size, size)
        
        painter.restore()
    
    def _draw_logo(self, painter: QPainter):
        """Dibuja el logo con efecto glow."""
        if self.logo_path and self.logo_path.exists():
            logo = QPixmap(str(self.logo_path))
            if not logo.isNull():
                # Efecto de escala con pulso
                pulse_scale = 1.0 + math.sin(self._pulse) * 0.02
                size = int(80 * pulse_scale)
                
                scaled_logo = logo.scaled(
                    size, size,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                
                x = (self._width - scaled_logo.width()) // 2
                y = 80
                
                # Glow effect (círculos concéntricos difusos)
                for i in range(3):
                    glow_size = size + (i + 1) * 20
                    glow_alpha = 30 - i * 10
                    glow_color = QColor("#F6993F", glow_alpha)  # Accent color
                    painter.setPen(Qt.PenStyle.NoPen)
                    painter.setBrush(QBrush(glow_color))
                    center_x = self._width // 2 - glow_size // 2 + 10
                    painter.drawEllipse(center_x, y - 5, glow_size, glow_size)
                
                painter.drawPixmap(x + 10, y + 5, scaled_logo)
        else:
            # Logo de texto si no hay imagen
            pulse_scale = 1.0 + math.sin(self._pulse) * 0.05
            
            # Glow
            glow_color = QColor("#F6993F", 50)
            painter.setPen(glow_color)
            painter.setFont(QFont("Segoe UI", int(48 * pulse_scale), QFont.Weight.Bold))
            painter.drawText(self._width // 2, 130, Qt.AlignmentFlag.AlignCenter, "X")
    
    def _draw_title(self, painter: QPainter):
        """Dibuja el título corporativo."""
        # Sombra
        shadow_color = QColor(0, 0, 0, 100)
        painter.setPen(shadow_color)
        painter.setFont(QFont("Segoe UI", 36, QFont.Weight.Bold))
        painter.drawText(self._width // 2 + 2, 192, Qt.AlignmentFlag.AlignCenter, "XEBEC")
        
        # Texto principal
        painter.setPen(QColor("#FFFFFF"))
        painter.setFont(QFont("Segoe UI", 36, QFont.Weight.Bold))
        painter.drawText(self._width // 2, 190, Qt.AlignmentFlag.AlignCenter, "XEBEC")
        
        # PDF Fixer en accent
        accent_color = QColor("#F6993F")
        painter.setPen(accent_color)
        painter.setFont(QFont("Segoe UI", 22, QFont.Weight.Normal))
        painter.drawText(self._width // 2, 220, Qt.AlignmentFlag.AlignCenter, "PDF Fixer")
    
    def _draw_subtitle(self, painter: QPainter):
        """Dibuja el subtítulo."""
        painter.setPen(QColor("#A0AEC0"))
        painter.setFont(QFont("Segoe UI", 11))
        painter.drawText(self._width // 2, 245, Qt.AlignmentFlag.AlignCenter, "Corporación Xebec")
    
    def _draw_progress_bar(self, painter: QPainter):
        """Dibuja la barra de progreso."""
        bar_width = 400
        bar_height = 6
        bar_x = (self._width - bar_width) // 2
        bar_y = 310
        
        # Fondo de la barra (oscuro)
        bg_color = QColor(0, 0, 0, 80)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(bg_color))
        painter.drawRoundedRect(bar_x, bar_y, bar_width, bar_height, 3, 3)
        
        # Progreso con gradiente
        if self._progress > 0:
            fill_width = int((self._progress / 100) * bar_width)
            
            progress_gradient = QLinearGradient(bar_x, 0, bar_x + bar_width, 0)
            progress_gradient.setColorAt(0, QColor("#F6993F"))  # Accent
            progress_gradient.setColorAt(1, QColor("#F6AD55"))  # Accent light
            
            painter.setBrush(QBrush(progress_gradient))
            painter.drawRoundedRect(bar_x, bar_y, fill_width, bar_height, 3, 3)
    
    def _draw_loading_text(self, painter: QPainter):
        """Dibuja el texto de carga."""
        # Efecto de parpadeo sutil
        alpha = 180 + int(math.sin(self._pulse * 2) * 50)
        text_color = QColor("#F6993F")
        text_color.setAlpha(alpha)
        
        painter.setPen(text_color)
        painter.setFont(QFont("Segoe UI", 10))
        
        # Indicador de carga animado
        dots = "." * (int(self._pulse * 3) % 4)
        text = f"{self._loading_text}{dots}"
        
        painter.drawText(self._width // 2, 340, Qt.AlignmentFlag.AlignCenter, text)
    
    def _draw_version(self, painter: QPainter):
        """Dibuja la versión."""
        painter.setPen(QColor("#4A5568"))
        painter.setFont(QFont("Segoe UI", 9))
        painter.drawText(self._width // 2, 420, Qt.AlignmentFlag.AlignCenter, "Autor: XEBEC CORPORATION  |  Versión: 1.0.0")
    
    def _draw_branding(self, painter: QPainter):
        """Dibuja marca de agua corporativa."""
        painter.setPen(QColor(255, 255, 255, 10))
        painter.setFont(QFont("Segoe UI", 60, QFont.Weight.Bold))
        
        # Texto diagonal de fondo
        painter.save()
        painter.translate(self._width // 2, self._height // 2)
        painter.rotate(-30)
        painter.drawText(0, 0, Qt.AlignmentFlag.AlignCenter, "XEBEC")
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
