"""
Sistema de animaciones Qt6 estilo Dota 2.
XEBEC CORPORATION - Premium Animations
"""

from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QParallelAnimationGroup, QSequentialAnimationGroup, QTimer, Qt, pyqtSignal, QObject
from PyQt6.QtWidgets import QWidget, QGraphicsDropShadowEffect
from PyQt6.QtGui import QColor, QPainter, QTransform
from typing import Optional, Callable, List, Dict, Any
from dataclasses import dataclass


# ==================== EASING CURVES ====================

class XebecEasing:
    """Curvas de easing personalizadas estilo XEBEC."""
    
    @staticmethod
    def smooth_enter() -> QEasingCurve:
        """Entrada suave."""
        curve = QEasingCurve(QEasingCurve.Type.OutCubic)
        return curve
    
    @staticmethod
    def smooth_exit() -> QEasingCurve:
        """Salida suave."""
        curve = QEasingCurve(QEasingCurve.Type.InCubic)
        return curve
    
    @staticmethod
    def bounce() -> QEasingCurve:
        """Rebote."""
        curve = QEasingCurve(QEasingCurve.Type.OutBounce)
        return curve
    
    @staticmethod
    def elastic() -> QEasingCurve:
        """Elástico."""
        curve = QEasingCurve(QEasingCurve.Type.OutElastic)
        return curve
    
    @staticmethod
    def exponential() -> QEasingCurve:
        """Exponencial."""
        curve = QEasingCurve(QEasingCurve.Type.OutExpo)
        return curve
    
    @staticmethod
    def bezier_smooth() -> QEasingCurve:
        """Bezier suave."""
        curve = QEasingCurve(QEasingCurve.Type.InOutQuad)
        return curve


# ==================== ANIMATION CONFIG ====================

@dataclass
class AnimationConfig:
    """Configuración de animación."""
    duration: int = 300
    easing: str = "smooth_enter"
    delay: int = 0


# ==================== BASE ANIMATED WIDGET ====================

class AnimatedWidget(QWidget):
    """Widget base con capacidades de animación."""
    
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._animations: List[QPropertyAnimation] = []
        self._is_animating = False
    
    def animate(
        self,
        property_name: bytes,
        start_value: Any,
        end_value: Any,
        duration: int = 300,
        easing: QEasingCurve = None
    ) -> QPropertyAnimation:
        """Crea y ejecuta una animación básica."""
        easing = easing or XebecEasing.smooth_enter()
        
        animation = QPropertyAnimation(self, property_name)
        animation.setDuration(duration)
        animation.setStartValue(start_value)
        animation.setEndValue(end_value)
        animation.setEasingCurve(easing)
        
        self._animations.append(animation)
        animation.start()
        
        return animation
    
    def fade_in(self, duration: int = 300, finished: Callable = None) -> QPropertyAnimation:
        """Animación fade-in."""
        self.setWindowOpacity(0)
        
        animation = QPropertyAnimation(self, b"windowOpacity")
        animation.setDuration(duration)
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        animation.setEasingCurve(XebecEasing.smooth_enter())
        
        if finished:
            animation.finished.connect(finished)
        
        self.show()
        animation.start()
        
        return animation
    
    def fade_out(self, duration: int = 300, finished: Callable = None) -> QPropertyAnimation:
        """Animación fade-out."""
        animation = QPropertyAnimation(self, b"windowOpacity")
        animation.setDuration(duration)
        animation.setStartValue(self.windowOpacity())
        animation.setEndValue(0.0)
        animation.setEasingCurve(XebecEasing.smooth_exit())
        
        if finished:
            animation.finished.connect(finished)
        
        animation.start()
        
        return animation


# ==================== BUTTON EFFECTS ====================

class AnimatedButtonMixin:
    """Mixin para botones animados."""
    
    def setup_button_animations(self):
        """Configura animaciones para botones."""
        self._hover_anim = None
        self._press_anim = None
        self._scale_normal = 1.0
        self._scale_hover = 1.05
        self._scale_press = 0.95
        
        self.setCursor(Qt.CursorShape.PointingHandCursor)
    
    def _on_hover_enter(self):
        """Animación al entrar el mouse."""
        if hasattr(self, '_animation_timer'):
            return
            
        self._animation_timer = QTimer()
        self._animation_timer.timeout.connect(self._animate_hover)
        self._animation_timer.start(16)
        self._hover_progress = 0
    
    def _on_hover_leave(self):
        """Animación al salir el mouse."""
        if hasattr(self, '_animation_timer'):
            self._animation_timer.stop()
            del self._animation_timer
    
    def _animate_hover(self):
        """Animación de hover."""
        pass  # Implementar en subclases


class GlowEffectMixin:
    """Mixin para efecto glow."""
    
    def apply_glow(
        self,
        color: str = "#F6993F",
        blur_radius: int = 20,
        opacity: float = 0.6
    ):
        """Aplica efecto glow."""
        effect = QGraphicsDropShadowEffect()
        effect.setBlurRadius(blur_radius)
        effect.setColor(QColor(color))
        effect.setOffset(0, 0)
        self.setGraphicsEffect(effect)
        return effect
    
    def pulse_glow(
        self,
        color: str = "#F6993F",
        min_blur: int = 15,
        max_blur: int = 35,
        duration: int = 1000
    ) -> QPropertyAnimation:
        """Efecto glow pulsante."""
        effect = self.graphicsEffect() or self.apply_glow(color)
        
        animation = QPropertyAnimation(effect, b"blurRadius")
        animation.setDuration(duration)
        animation.setStartValue(min_blur)
        animation.setEndValue(max_blur)
        animation.setEasingCurve(QEasingCurve.Type.InOutSine)
        animation.setLoopCount(-1)
        
        animation.start()
        
        return animation


# ==================== WINDOW TRANSITIONS ====================

class WindowTransitions:
    """Transiciones de ventana estilo XEBEC."""
    
    @staticmethod
    def fade_slide(
        outgoing: QWidget,
        incoming: QWidget,
        direction: str = "right",
        duration: int = 350
    ) -> QParallelAnimationGroup:
        """Transición fade + slide."""
        group = QParallelAnimationGroup()
        
        # Fade out
        fade_out = QPropertyAnimation(outgoing, b"windowOpacity")
        fade_out.setDuration(duration // 2)
        fade_out.setStartValue(1.0)
        fade_out.setEndValue(0.0)
        fade_out.setEasingCurve(XebecEasing.smooth_exit())
        
        # Fade in
        incoming.setWindowOpacity(0)
        incoming.show()
        
        fade_in = QPropertyAnimation(incoming, b"windowOpacity")
        fade_in.setDuration(duration // 2)
        fade_in.setStartValue(0.0)
        fade_in.setEndValue(1.0)
        fade_in.setEasingCurve(XebecEasing.smooth_enter())
        
        group.addAnimation(fade_out)
        group.addAnimation(fade_in)
        
        group.start()
        
        return group
    
    @staticmethod
    def scale_fade(
        widget: QWidget,
        direction: str = "in",
        duration: int = 400
    ) -> QParallelAnimationGroup:
        """Transición scale + fade."""
        group = QParallelAnimationGroup()
        
        if direction == "in":
            widget.setWindowOpacity(0)
            widget.setScale(0.8)
            
            opacity = QPropertyAnimation(widget, b"windowOpacity")
            opacity.setDuration(duration)
            opacity.setStartValue(0.0)
            opacity.setEndValue(1.0)
            opacity.setEasingCurve(XebecEasing.exponential())
            
            scale = QPropertyAnimation(widget, b"scale")
            scale.setDuration(duration)
            scale.setStartValue(0.8)
            scale.setEndValue(1.0)
            scale.setEasingCurve(XebecEasing.elastic())
        else:
            widget.setScale(1.0)
            
            opacity = QPropertyAnimation(widget, b"windowOpacity")
            opacity.setDuration(duration)
            opacity.setStartValue(1.0)
            opacity.setEndValue(0.0)
            opacity.setEasingCurve(XebecEasing.smooth_exit())
            
            scale = QPropertyAnimation(widget, b"scale")
            scale.setDuration(duration)
            scale.setStartValue(1.0)
            scale.setEndValue(0.8)
            scale.setEasingCurve(XebecEasing.smooth_exit())
        
        group.addAnimation(opacity)
        group.addAnimation(scale)
        
        widget.show()
        group.start()
        
        return group


# ==================== CARD ANIMATIONS ====================

class CardAnimator:
    """Animaciones para tarjetas."""
    
    @staticmethod
    def hover_scale(
        widget: QWidget,
        scale_factor: float = 1.03,
        duration: int = 200
    ):
        """Animación de hover en tarjeta."""
        animation = QPropertyAnimation(widget, b"scale")
        animation.setDuration(duration)
        animation.setStartValue(widget.scale())
        animation.setEndValue(scale_factor)
        animation.setEasingCurve(XebecEasing.smooth_enter())
        animation.start()
    
    @staticmethod
    def entrance_slide(
        widget: QWidget,
        direction: str = "up",
        delay: int = 0,
        duration: int = 400
    ):
        """Animación de entrada."""
        # Guardar posición original
        orig_x = widget.x()
        orig_y = widget.y()
        
        # Posición inicial
        if direction == "up":
            start_y = orig_y + 50
        elif direction == "down":
            start_y = orig_y - 50
        else:
            start_y = orig_y
        
        widget.setWindowOpacity(0)
        widget.move(orig_x, start_y)
        
        # Animaciones
        group = QParallelAnimationGroup()
        
        opacity = QPropertyAnimation(widget, b"windowOpacity")
        opacity.setDuration(duration)
        opacity.setStartValue(0.0)
        opacity.setEndValue(1.0)
        opacity.setEasingCurve(XebecEasing.smooth_enter())
        
        if delay > 0:
            opacity.setDelay(delay)
        
        group.addAnimation(opacity)
        
        widget.show()
        group.start()
        
        return group


# ==================== LOADING INDICATOR ====================

class XebecLoadingIndicator(QWidget):
    """Indicador de carga estilo XEBEC."""
    
    def __init__(self, parent=None, color: str = "#F6993F"):
        super().__init__(parent)
        self._color = QColor(color)
        self._angle = 0
        self._timer = QTimer()
        self._timer.timeout.connect(self._rotate)
        
        self.setFixedSize(50, 50)
    
    def start(self):
        self._timer.start(30)
    
    def stop(self):
        self._timer.stop()
    
    def _rotate(self):
        self._angle = (self._angle + 15) % 360
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        center = self.rect().center()
        radius = 18
        
        # Fondo
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(0, 0, 0, 30))
        painter.drawEllipse(center, radius, radius)
        
        # Arco
        pen = QPen(self._color)
        pen.setWidth(4)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        
        rect = self.rect().adjusted(8, 8, -8, -8)
        painter.drawArc(rect, self._angle * 16, 240 * 16)


# ==================== HOVER BUTTON ====================

class HoverButton(QWidget):
    """Botón con efectos hover animados."""
    
    clicked = pyqtSignal()
    
    def __init__(
        self,
        text: str = "",
        parent=None,
        bg_color: str = "#2D3748",
        hover_color: str = "#F6993F",
        text_color: str = "#FFFFFF"
    ):
        super().__init__(parent)
        self._text = text
        self._bg_color = QColor(bg_color)
        self._hover_color = QColor(hover_color)
        self._text_color = QColor(text_color)
        self._is_hovered = False
        
        self.setFixedHeight(40)
        self.setMinimumWidth(100)
        
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Animación de color
        self._color_anim = QPropertyAnimation(self, b"scale")
        self._color_anim.setDuration(150)
    
    def enterEvent(self, event):
        self._is_hovered = True
        self.update()
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        self._is_hovered = False
        self.update()
        super().leaveEvent(event)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Color de fondo
        bg = self._hover_color if self._is_hovered else self._bg_color
        
        # Efecto hover
        if self._is_hovered:
            # Efecto de brillo
            gradient = QLinearGradient(0, 0, 0, self.height())
            gradient.setColorAt(0, bg.lighter(110))
            gradient.setColorAt(0.5, bg)
            gradient.setColorAt(1, bg.darker(110))
            painter.setBrush(gradient)
        else:
            painter.setBrush(bg)
        
        painter.setPen(Qt.PenStyle.NoPen)
        
        # Dibujar rectángulo redondeado
        from PyQt6.QtCore import QRectF
        rect = QRectF(0, 0, self.width(), self.height())
        painter.drawRoundedRect(rect, 8, 8)
        
        # Texto
        painter.setPen(self._text_color)
        font = painter.font()
        font.setBold(True)
        painter.setFont(font)
        
        painter.drawText(
            self.rect(),
            Qt.AlignmentFlag.AlignCenter,
            self._text
        )


# ==================== EXPORTS ====================

__all__ = [
    'XebecEasing',
    'AnimationConfig', 
    'AnimatedWidget',
    'AnimatedButtonMixin',
    'GlowEffectMixin',
    'WindowTransitions',
    'CardAnimator',
    'XebecLoadingIndicator',
    'HoverButton',
]
