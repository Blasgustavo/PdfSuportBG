---
name: skill-qt6-animations
description: Qt6 AAA Animations - Animaciones avanzadas estilo Dota 2 con QPropertyAnimation, partículas, transiciones cinematicas y micro-interacciones
---

## What I do

Diseñador de animaciones AAA en Qt6. Creo experiencias visuales de alto nivel inspiradas en Dota 2:

- **QPropertyAnimation experto**: Propiedades personalizadas, sequential/parallel groups
- **Easing Curves avanzadas**: Interpolaciones personalizadas, curvas bezier
- **Animaciones Dota 2**: fade-in, slide-in, scale-up, blur, glow, parallax
- **Sistemas de partículas**: Efectos visuales, transiciones fluidas
- **Micro-interacciones**: Hover, click, focus, drag reactivos
- **Integración WindowManager**: Animaciones sincronizadas con navegación
- **Optimización rendimiento**: Evitar stuttering, smooth 60fps

## When to use me

Usar cuando se necesite:
- Animaciones de entrada/salida de ventanas
- Transiciones entre pantallas
- Efectos hover/click avanzados
- Partículas y efectos visuales
- Animaciones de carga
- UI interactiva con feedback visual

## Arquitectura de Animaciones

```
src/gui/pyqt6/
├── animations/
│   ├── __init__.py
│   ├── base.py                   # Clases base de animación
│   ├── factory.py                # Factory de animaciones
│   ├── easings.py               # Curvas de easing personalizadas
│   ├── transitions/
│   │   ├── __init__.py
│   │   ├── window_transition.py # Transiciones de ventana
│   │   ├── page_transition.py   # Transiciones de página
│   │   └── dialog_transition.py # Transiciones de diálogo
│   ├── effects/
│   │   ├── __init__.py
│   │   ├── glow.py              # Efecto glow
│   │   ├── blur.py              # Efecto blur
│   │   ├── particles.py         # Sistema de partículas
│   │   └── reveal.py            # Efecto reveal
│   ├── micro/
│   │   ├── __init__.py
│   │   ├── hover.py             # Animaciones hover
│   │   ├── click.py             # Animaciones click
│   │   └── focus.py             # Animaciones focus
│   └── widgets/
│       ├── __init__.py
│       ├── animated_button.py    # Botón animado
│       ├── animated_card.py       # Tarjeta animada
│       └── loading_indicator.py  # Indicador de carga
```

## Sistema de Easing Personalizado

```python
from PyQt6.QtCore import QEasingCurve, qreal
from typing import Callable
from dataclasses import dataclass


class CustomEasing:
    """Curvas de easing personalizadas estilo Dota 2."""
    
    @staticmethod
    def dota2_enter() -> QEasingCurve:
        """Easing para entrada - estilo Dota 2."""
        curve = QEasingCurve(QEasingCurve.Type.Bezier)
        # Bezier curve para entrada rápida luego suave
        curve.setCustomPoint(0, 0.0, 0.0)
        curve.setCustomPoint(1, 0.4, 0.0)
        curve.setCustomPoint(2, 0.7, 0.0)
        curve.setCustomPoint(3, 1.0, 1.0)
        return curve
    
    @staticmethod
    def dota2_exit() -> QEasingCurve:
        """Easing para salida - estilo Dota 2."""
        curve = QEasingCurve(QEasingCurve.Type.Bezier)
        curve.setCustomPoint(0, 0.0, 0.0)
        curve.setCustomPoint(1, 0.3, 0.0)
        curve.setCustomPoint(2, 0.6, 0.0)
        curve.setCustomPoint(3, 1.0, 1.0)
        return curve
    
    @staticmethod
    def bounce_out() -> QEasingCurve:
        """Easing con rebote."""
        return QEasingCurve(QEasingCurve.Type.OutBounce)
    
    @staticmethod
    def elastic_out() -> QEasingCurve:
        """Easing elástico."""
        return QEasingCurve(QEasingCurve.Type.OutElastic)
    
    @staticmethod
    def smooth_step() -> QEasingCurve:
        """Smooth step interpolación."""
        return QEasingCurve(QEasingCurve.Type.SCurve)
    
    @staticmethod
    def exponential_in() -> QEasingCurve:
        """Exponencial de entrada."""
        return QEasingCurve(QEasingCurve.Type.InExpo)
    
    @staticmethod
    def exponential_out() -> QEasingCurve:
        """Exponencial de salida."""
        return QEasingCurve(QEasingCurve.Type.OutExpo)


class EasingFactory:
    """Factory para crear easing curves."""
    
    _curves = {
        "dota_enter": CustomEasing.dota2_enter,
        "dota_exit": CustomEasing.dota2_exit,
        "bounce": CustomEasing.bounce_out,
        "elastic": CustomEasing.elastic_out,
        "smooth": CustomEasing.smooth_step,
        "expo_in": CustomEasing.exponential_in,
        "expo_out": CustomEasing.exponential_out,
    }
    
    @classmethod
    def get(cls, name: str) -> QEasingCurve:
        if name in cls._curves:
            return cls._curves[name]()
        return QEasingCurve(QEasingCurve.Type.InOutQuad)
    
    @classmethod
    def register(cls, name: str, curve_fn: Callable) -> None:
        cls._curves[name] = curve_fn
```

## Animaciones Base

```python
from PyQt6.QtCore import QObject, QPropertyAnimation, QEasingCurve, pyqtSignal, QParallelAnimationGroup, QSequentialAnimationGroup
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QTransform, QColor, QGraphicsDropShadowEffect
from typing import Optional, Callable, List, Any
from dataclasses import dataclass
import math


@dataclass
class AnimationConfig:
    """Configuración de animación."""
    duration: int = 300  # ms
    easing: str = "dota_enter"
    delay: int = 0
    loop: bool = False
    reverse: bool = False


class AnimatedWidget(QWidget):
    """Widget base con capacidades de animación."""
    
    animation_started = pyqtSignal()
    animation_finished = pyqtSignal()
    
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._animations: List[QPropertyAnimation] = []
        self._is_animating = False
    
    def animate(
        self,
        property_name: bytes,
        start_value: Any,
        end_value: Any,
        config: Optional[AnimationConfig] = None
    ) -> QPropertyAnimation:
        """Crea y ejecuta una animación."""
        config = config or AnimationConfig()
        
        animation = QPropertyAnimation(self, property_name)
        animation.setDuration(config.duration)
        animation.setStartValue(start_value)
        animation.setEndValue(end_value)
        animation.setEasingCurve(EasingFactory.get(config.easing))
        
        if config.delay > 0:
            animation.setDelay(config.delay)
        
        animation.finished.connect(lambda: self.animation_finished.emit())
        
        self._animations.append(animation)
        
        if not self._is_animating:
            self.animation_started.emit()
            self._is_animating = True
        
        animation.start()
        
        return animation
    
    def animate_parallel(
        self,
        animations_config: List[dict],
        finished_callback: Optional[Callable] = None
    ) -> QParallelAnimationGroup:
        """Ejecuta múltiples animaciones en paralelo."""
        group = QParallelAnimationGroup()
        
        for config in animations_config:
            animation = self.animate(
                config["property"],
                config["start"],
                config["end"],
                config.get("animation_config")
            )
            group.addAnimation(animation)
        
        if finished_callback:
            group.finished.connect(finished_callback)
        
        group.start()
        return group
    
    def animate_sequential(
        self,
        animations_config: List[dict],
        finished_callback: Optional[Callable] = None
    ) -> QSequentialAnimationGroup:
        """Ejecuta animaciones en secuencia."""
        group = QSequentialAnimationGroup()
        
        for config in animations_config:
            animation = self.animate(
                config["property"],
                config["start"],
                config["end"],
                config.get("animation_config")
            )
            group.addAnimation(animation)
        
        if finished_callback:
            group.finished.connect(finished_callback)
        
        group.start()
        return group
    
    def stop_all_animations(self) -> None:
        """Detiene todas las animaciones."""
        for anim in self._animations:
            anim.stop()
        self._animations.clear()
        self._is_animating = False
```

## Transiciones de Ventana Estilo Dota 2

```python
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QParallelAnimationGroup, QRect, Qt
from PyQt6.QtWidgets import QWidget, QGraphicsScene, QGraphicsView, QGraphicsWidget
from PyQt6.QtGui import QTransform, QPainter, QColor, QBrush, QPen
from typing import Optional, Callable
from enum import Enum


class TransitionType(Enum):
    """Tipos de transición."""
    FADE = "fade"
    SLIDE_LEFT = "slide_left"
    SLIDE_RIGHT = "slide_right"
    SLIDE_UP = "slide_up"
    SLIDE_DOWN = "slide_down"
    SCALE = "scale"
    BLUR = "blur"
    GLOW = "glow"
    PIXELATE = "pixelate"
    GLITCH = "glitch"
    CINEMATIC = "cinematic"


class WindowTransition:
    """Sistema de transiciones de ventana estilo Dota 2."""
    
    @staticmethod
    def fade_in(
        widget: QWidget,
        duration: int = 400,
        easing: str = "dota_enter",
        finished: Optional[Callable] = None
    ) -> QPropertyAnimation:
        """Transición fade-in con efecto de aparición."""
        widget.setWindowOpacity(0)
        
        animation = QPropertyAnimation(widget, b"windowOpacity")
        animation.setDuration(duration)
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        animation.setEasingCurve(EasingFactory.get(easing))
        
        if finished:
            animation.finished.connect(finished)
        
        widget.show()
        animation.start()
        
        return animation
    
    @staticmethod
    def fade_out(
        widget: QWidget,
        duration: int = 300,
        easing: str = "dota_exit",
        finished: Optional[Callable] = None
    ) -> QPropertyAnimation:
        """Transición fade-out."""
        animation = QPropertyAnimation(widget, b"windowOpacity")
        animation.setDuration(duration)
        animation.setStartValue(widget.windowOpacity())
        animation.setEndValue(0.0)
        animation.setEasingCurve(EasingFactory.get(easing))
        
        if finished:
            animation.finished.connect(finished)
        
        animation.start()
        
        return animation
    
    @staticmethod
    def slide_in_from_right(
        widget: QWidget,
        parent_widget: QWidget,
        duration: int = 350,
        finished: Optional[Callable] = None
    ) -> QPropertyAnimation:
        """Slide desde la derecha estilo Dota 2."""
        end_rect = widget.geometry()
        
        start_rect = QRect(
            parent_widget.width(),
            end_rect.y(),
            end_rect.width(),
            end_rect.height()
        )
        
        widget.setGeometry(start_rect)
        widget.show()
        
        animation = QPropertyAnimation(widget, b"geometry")
        animation.setDuration(duration)
        animation.setStartValue(start_rect)
        animation.setEndValue(end_rect)
        animation.setEasingCurve(EasingFactory.get("dota_enter"))
        
        if finished:
            animation.finished.connect(finished)
        
        animation.start()
        
        return animation
    
    @staticmethod
    def scale_in(
        widget: QWidget,
        duration: int = 400,
        finished: Optional[Callable] = None
    ) -> QParallelAnimationGroup:
        """Scale + Fade in - efecto característico Dota 2."""
        widget.setWindowOpacity(0)
        widget.setScale(0.8)
        
        opacity = QPropertyAnimation(widget, b"windowOpacity")
        opacity.setDuration(duration)
        opacity.setStartValue(0.0)
        opacity.setEndValue(1.0)
        opacity.setEasingCurve(EasingFactory.get("expo_out"))
        
        scale_anim = QPropertyAnimation(widget, b"scale")
        scale_anim.setDuration(duration)
        scale_anim.setStartValue(0.8)
        scale_anim.setEndValue(1.0)
        scale_anim.setEasingCurve(EasingFactory.get("elastic"))
        
        group = QParallelAnimationGroup()
        group.addAnimation(opacity)
        group.addAnimation(scale_anim)
        
        if finished:
            group.finished.connect(finished)
        
        widget.show()
        group.start()
        
        return group
    
    @staticmethod
    def cinematic_enter(
        widget: QWidget,
        parent_widget: QWidget,
        duration: int = 600,
        finished: Optional[Callable] = None
    ) -> QParallelAnimationGroup:
        """Transición cinematográfica estilo Dota 2."""
        widget.setWindowOpacity(0)
        
        center_x = parent_widget.width() // 2 - widget.width() // 2
        center_y = parent_widget.height() // 2 - widget.height() // 2
        
        widget.setGeometry(center_x, center_y, widget.width(), widget.height())
        
        opacity = QPropertyAnimation(widget, b"windowOpacity")
        opacity.setDuration(duration)
        opacity.setStartValue(0.0)
        opacity.setEndValue(1.0)
        opacity.setEasingCurve(EasingFactory.get("dota_enter"))
        
        scale = QPropertyAnimation(widget, b"scale")
        scale.setDuration(duration)
        scale.setStartValue(0.5)
        scale.setEndValue(1.0)
        scale.setEasingCurve(EasingFactory.get("elastic"))
        
        group = QParallelAnimationGroup()
        group.addAnimation(opacity)
        group.addAnimation(scale)
        
        if finished:
            group.finished.connect(finished)
        
        widget.show()
        group.start()
        
        return group
    
    @staticmethod
    def dota2_style_transition(
        outgoing_widget: QWidget,
        incoming_widget: QWidget,
        direction: str = "left",
        duration: int = 400
    ) -> QSequentialAnimationGroup:
        """Transición estilo Dota 2 completa."""
        group = QSequentialAnimationGroup()
        
        # Fade out widget saliente
        fade_out = QPropertyAnimation(outgoing_widget, b"windowOpacity")
        fade_out.setDuration(duration // 2)
        fade_out.setStartValue(1.0)
        fade_out.setEndValue(0.0)
        fade_out.setEasingCurve(EasingFactory.get("dota_exit"))
        
        # Slide in widget entrante
        incoming_widget.setWindowOpacity(0)
        incoming_widget.show()
        
        fade_in = QPropertyAnimation(incoming_widget, b"windowOpacity")
        fade_in.setDuration(duration // 2)
        fade_in.setStartValue(0.0)
        fade_in.setEndValue(1.0)
        fade_in.setEasingCurve(EasingFactory.get("dota_enter"))
        
        group.addAnimation(fade_out)
        group.addAnimation(fade_in)
        
        group.start()
        
        return group
```

## Efectos Visuales (Glow, Blur, Partículas)

```python
from PyQt6.QtWidgets import QWidget, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem
from PyQt6.QtCore import QTimer, QPointF, Qt, QRectF, pyqtSignal
from PyQt6.QtGui import QColor, QBrush, QPen, QPainter, QPainterPath
from typing import List, Optional, Tuple
from dataclasses import dataclass
import random
import math


class GlowEffect:
    """Efecto glow estilo Dota 2."""
    
    @staticmethod
    def apply_glow(
        widget: QWidget,
        color: str = "#F6993F",
        blur_radius: int = 30,
        opacity: float = 0.8
    ) -> QGraphicsDropShadowEffect:
        """Aplica efecto glow a un widget."""
        from PyQt6.QtWidgets import QGraphicsDropShadowEffect
        
        effect = QGraphicsDropShadowEffect()
        effect.setBlurRadius(blur_radius)
        effect.setColor(QColor(color))
        effect.setOffset(0, 0)
        
        widget.setGraphicsEffect(effect)
        
        return effect
    
    @staticmethod
    def pulse_glow(
        widget: QWidget,
        color: str = "#F6993F",
        min_blur: int = 20,
        max_blur: int = 50,
        duration: int = 1000
    ) -> QPropertyAnimation:
        """Efecto glow pulsante."""
        effect = widget.graphicsEffect()
        
        if effect is None:
            effect = GlowEffect.apply_glow(widget, color)
        
        animation = QPropertyAnimation(effect, b"blurRadius")
        animation.setDuration(duration)
        animation.setStartValue(min_blur)
        animation.setEndValue(max_blur)
        animation.setEasingCurve(QEasingCurve.Type.InOutSine)
        animation.setLoopCount(-1)  # Infinite
        
        animation.start()
        
        return animation


class ParticleSystem:
    """Sistema de partículas estilo Dota 2."""
    
    particle_died = pyqtSignal(int)
    
    def __init__(self, parent: QWidget) -> None:
        super().__init__()
        self.parent = parent
        self.particles: List["Particle"] = []
        self.max_particles = 100
        self.active = False
        
        self._timer = QTimer()
        self._timer.timeout.connect(self._update_particles)
    
    def emit(
        self,
        x: float,
        y: float,
        count: int = 20,
        color: str = "#F6993F",
        velocity: float = 100,
        spread: float = 360
    ) -> None:
        """Emite partículas desde una posición."""
        for _ in range(count):
            if len(self.particles) >= self.max_particles:
                break
            
            angle = random.uniform(0, spread)
            speed = random.uniform(velocity * 0.5, velocity * 1.5)
            
            particle = Particle(
                x=x,
                y=y,
                vx=math.cos(math.radians(angle)) * speed,
                vy=math.sin(math.radians(angle)) * speed,
                color=color,
                life=random.uniform(0.5, 1.5),
                size=random.uniform(2, 6)
            )
            
            self.particles.append(particle)
        
        if not self.active:
            self.active = True
            self._timer.start(16)  # ~60fps
    
    def _update_particles(self) -> None:
        """Actualiza posiciones de partículas."""
        dt = 0.016  # 16ms
        
        for particle in self.particles[:]:
            particle.update(dt)
            
            if particle.is_dead():
                self.particles.remove(particle)
                self.particle_died.emit(1)
        
        if not self.particles:
            self.active = False
            self._timer.stop()
        
        self.parent.update()
    
    def render(self, painter: QPainter) -> None:
        """Dibuja las partículas."""
        for particle in self.particles:
            particle.render(painter)


@dataclass
class Particle:
    """Partícula individual."""
    x: float
    y: float
    vx: float
    vy: float
    color: str
    life: float
    max_life: float
    size: float
    
    def __init__(self, x, y, vx, vy, color, life, size):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.life = life
        self.max_life = life
        self.size = size
        self.gravity = 200
        self.fade_rate = 0.5
    
    def update(self, dt: float) -> None:
        """Actualiza posición y vida."""
        self.x += self.vx * dt
        self.y += self.vy * dt
        
        self.vy += self.gravity * dt
        
        self.life -= dt * self.fade_rate
    
    def is_dead(self) -> bool:
        return self.life <= 0
    
    def render(self, painter: QPainter) -> None:
        """Dibuja la partícula."""
        alpha = int(255 * (self.life / self.max_life))
        
        color = QColor(self.color)
        color.setAlpha(alpha)
        
        painter.setBrush(QBrush(color))
        painter.setPen(Qt.PenStyle.NoPen)
        
        size = self.size * (self.life / self.max_life)
        
        painter.drawEllipse(
            QPointF(self.x, self.y),
            size,
            size
        )


class BlurEffect:
    """Efecto blur (desenfoque)."""
    
    @staticmethod
    def apply_blur(widget: QWidget, radius: int = 5) -> None:
        """Aplica efecto blur."""
        from PyQt6.QtWidgets import QGraphicsBlurEffect
        
        effect = QGraphicsBlurEffect()
        effect.setBlurRadius(radius)
        effect.setBlurHints(QGraphicsBlurEffect.BlurHint.AnimationHint)
        
        widget.setGraphicsEffect(effect)
    
    @staticmethod
    def animate_blur(
        widget: QWidget,
        start_radius: int = 0,
        end_radius: int = 10,
        duration: int = 300
    ) -> QPropertyAnimation:
        """Anima el blur."""
        from PyQt6.QtWidgets import QGraphicsBlurEffect
        
        effect = widget.graphicsEffect()
        
        if effect is None:
            effect = QGraphicsBlurEffect()
            widget.setGraphicsEffect(effect)
        
        animation = QPropertyAnimation(effect, b"blurRadius")
        animation.setDuration(duration)
        animation.setStartValue(start_radius)
        animation.setEndValue(end_radius)
        animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        
        animation.start()
        
        return animation
```

## Micro-interacciones (Hover, Click, Focus)

```python
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QPoint, Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit
from PyQt6.QtGui import QColor, QBrush, QPainter, QPainterPath
from typing import Optional, Callable


class HoverAnimation:
    """Animaciones hover estilo Dota 2."""
    
    @staticmethod
    def scale_on_hover(
        widget: QWidget,
        scale_factor: float = 1.05,
        duration: int = 150
    ) -> Callable:
        """Crea función para animación scale en hover."""
        def on_hover(event):
            animation = QPropertyAnimation(widget, b"scale")
            animation.setDuration(duration)
            animation.setStartValue(widget.scale())
            animation.setEndValue(scale_factor)
            animation.setEasingCurve(QEasingCurve.Type.OutCubic)
            animation.start()
        
        def on_leave(event):
            animation = QPropertyAnimation(widget, b"scale")
            animation.setDuration(duration)
            animation.setStartValue(widget.scale())
            animation.setEndValue(1.0)
            animation.setEasingCurve(QEasingCurve.Type.OutCubic)
            animation.start()
        
        return on_hover, on_leave
    
    @staticmethod
    def glow_on_hover(widget: QWidget, color: str = "#F6993F") -> Callable:
        """Crea función para glow en hover."""
        effect = GlowEffect.apply_glow(widget, color, blur_radius=15, opacity=0.5)
        
        def on_hover(event):
            animation = QPropertyAnimation(effect, b"blurRadius")
            animation.setDuration(200)
            animation.setStartValue(15)
            animation.setEndValue(30)
            animation.setEasingCurve(QEasingCurve.Type.OutQuad)
            animation.start()
        
        def on_leave(event):
            animation = QPropertyAnimation(effect, b"blurRadius")
            animation.setDuration(200)
            animation.setStartValue(effect.blurRadius())
            animation.setEndValue(15)
            animation.setEasingCurve(QEasingCurve.Type.OutQuad)
            animation.start()
        
        return on_hover, on_leave
    
    @staticmethod
    def color_shift_on_hover(
        widget: QWidget,
        start_color: str = "#1E3A5F",
        end_color: str = "#2E5A8F",
        property_name: bytes = b"cursor"
    ) -> Callable:
        """Animación de cambio de color en hover."""
        # Requires custom property or styling
        pass


class ClickAnimation:
    """Animaciones de click estilo Dota 2."""
    
    @staticmethod
    def press_effect(
        widget: QWidget,
        duration: int = 100
    ) -> Callable:
        """Efecto de presión al hacer click."""
        original_geometry = widget.geometry()
        
        def on_click(event):
            # Shrink
            shrink = QPropertyAnimation(widget, b"geometry")
            shrink.setDuration(duration)
            shrink.setStartValue(original_geometry)
            
            shrunk = type(original_geometry)(
                original_geometry.x() + 5,
                original_geometry.y() + 5,
                original_geometry.width() - 10,
                original_geometry.height() - 10
            )
            
            shrink.setEndValue(shrunk)
            shrink.setEasingCurve(QEasingCurve.Type.InOutQuad)
            shrink.start()
            
            # Restore after
            shrink.finished.connect(lambda: _restore())
        
        def _restore():
            restore = QPropertyAnimation(widget, b"geometry")
            restore.setDuration(duration)
            restore.setStartValue(widget.geometry())
            restore.setEndValue(original_geometry)
            restore.setEasingCurve(QEasingCurve.Type.OutBack)
            restore.start()
        
        return on_click
    
    @staticmethod
    def ripple_effect(
        widget: QWidget,
        color: str = "#F6993F"
    ) -> Callable:
        """Efecto ripple al hacer click."""
        def on_click(event):
            pos = widget.mapFromGlobal(event.globalPosition().toPoint())
            
            # Create ripple (visual effect)
            painter = QPainter(widget)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            
            path = QPainterPath()
            path.addEllipse(pos.x() - 50, pos.y() - 50, 100, 100)
            
            painter.fillPath(path, QBrush(QColor(color)))
            painter.end()
        
        return on_click
    
    @staticmethod
    def bounce_on_click(widget: QWidget) -> Callable:
        """Efecto rebote al hacer click."""
        original_y = widget.y()
        
        def on_click(event):
            # Up
            up = QPropertyAnimation(widget, b"y")
            up.setDuration(100)
            up.setStartValue(original_y)
            up.setEndValue(original_y - 10)
            up.setEasingCurve(QEasingCurve.Type.OutQuad)
            up.start()
            
            # Down
            up.finished.connect(lambda: _bounce_down())
        
        def _bounce_down():
            down = QPropertyAnimation(widget, b"y")
            down.setDuration(150)
            down.setStartValue(widget.y())
            down.setEndValue(original_y)
            down.setEasingCurve(QEasingCurve.Type.OutBounce)
            down.start()
        
        return on_click


class AnimatedButton(QPushButton):
    """Botón animado estilo Dota 2."""
    
    def __init__(
        self,
        text: str = "",
        parent=None,
        hover_effect: str = "scale",
        click_effect: str = "bounce"
    ) -> None:
        super().__init__(text, parent)
        
        self._hover_effect = hover_effect
        self._click_effect = click_effect
        
        self._setup_animations()
        self._setup_styles()
    
    def _setup_animations(self) -> None:
        """Configura las animaciones."""
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        if self._hover_effect == "scale":
            self._hover_enter, self._hover_leave = HoverAnimation.scale_on_hover(
                self, scale_factor=1.08
            )
        elif self._hover_effect == "glow":
            self._hover_enter, self._hover_leave = HoverAnimation.glow_on_hover(self)
        
        if self._click_effect == "bounce":
            self._on_click = ClickAnimation.bounce_on_click(self)
        elif self._click_effect == "press":
            self._on_click = ClickAnimation.press_effect(self)
    
    def _setup_styles(self) -> None:
        """Configura estilos base."""
        self.setStyleSheet("""
            AnimatedButton {
                background-color: #1E3A5F;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px 24px;
                font-weight: 600;
                font-size: 14px;
            }
            AnimatedButton:hover {
                background-color: #2E5A8F;
            }
            AnimatedButton:pressed {
                background-color: #0E2A4F;
            }
        """)
    
    def enterEvent(self, event) -> None:
        if hasattr(self, '_hover_enter'):
            self._hover_enter(event)
        super().enterEvent(event)
    
    def leaveEvent(self, event) -> None:
        if hasattr(self, '_hover_leave'):
            self._hover_leave(event)
        super().leaveEvent(event)
    
    def mousePressEvent(self, event) -> None:
        if hasattr(self, '_on_click'):
            self._on_click(event)
        super().mousePressEvent(event)
```

## Widgets Animados

```python
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QParallelAnimationGroup, QSize, QTimer
from PyQt6.QtGui import QColor, QBrush, QPainter, QPainterPath, QLinearGradient
from typing import Optional


class AnimatedCard(QWidget):
    """Tarjeta animada estilo Dota 2."""
    
    def __init__(
        self,
        title: str = "",
        content: str = "",
        parent=None
    ) -> None:
        super().__init__(parent)
        
        self._title = title
        self._content = content
        
        self._setup_ui()
        self._setup_animations()
    
    def _setup_ui(self) -> None:
        self.setMinimumWidth(250)
        self.setMaximumWidth(350)
        
        self.setStyleSheet("""
            AnimatedCard {
                background-color: #2D3748;
                border-radius: 12px;
                border: 1px solid #4A5568;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        self.title_label = QLabel(self._title)
        self.title_label.setStyleSheet("""
            color: white;
            font-size: 18px;
            font-weight: bold;
        """)
        
        self.content_label = QLabel(self._content)
        self.content_label.setStyleSheet("""
            color: #A0AEC0;
            font-size: 14px;
        """)
        self.content_label.setWordWrap(True)
        
        layout.addWidget(self.title_label)
        layout.addWidget(self.content_label)
    
    def _setup_animations(self) -> None:
        """Configura animaciones de entrada."""
        self.setWindowOpacity(0)
        self.setScale(0.9)
    
    def animate_in(self, delay: int = 0) -> QParallelAnimationGroup:
        """Animación de entrada."""
        group = QParallelAnimationGroup()
        
        opacity = QPropertyAnimation(self, b"windowOpacity")
        opacity.setDuration(400)
        opacity.setStartValue(0.0)
        opacity.setEndValue(1.0)
        opacity.setEasingCurve(EasingFactory.get("expo_out"))
        
        scale = QPropertyAnimation(self, b"scale")
        scale.setDuration(400)
        scale.setStartValue(0.9)
        scale.setEndValue(1.0)
        scale.setEasingCurve(EasingFactory.get("elastic"))
        
        if delay > 0:
            opacity.setDelay(delay)
            scale.setDelay(delay)
        
        group.addAnimation(opacity)
        group.addAnimation(scale)
        
        group.start()
        
        return group


class LoadingIndicator(QWidget):
    """Indicador de carga estilo Dota 2."""
    
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        
        self._angle = 0
        self._timer = QTimer()
        self._timer.timeout.connect(self._rotate)
        
        self.setFixedSize(60, 60)
    
    def _rotate(self) -> None:
        self._angle = (self._angle + 10) % 360
        self.update()
    
    def start(self) -> None:
        self._timer.start(30)
    
    def stop(self) -> None:
        self._timer.stop()
    
    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        center = self.rect().center()
        radius = 20
        
        # Background circle
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor("#4A5568")))
        painter.drawEllipse(center, radius, radius)
        
        # Arc
        pen = QPen(QColor("#F6993F"))
        pen.setWidth(4)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        
        rect = self.rect().adjusted(10, 10, -10, -10)
        
        painter.drawArc(rect, self._angle * 16, 270 * 16)
```

## Integración con WindowManager

```python
from PyQt6.QtCore import QPropertyAnimation, QParallelAnimationGroup
from typing import Optional, Callable


class AnimatedWindowManager:
    """WindowManager con animaciones integradas."""
    
    def __init__(self, window_manager) -> None:
        self._wm = window_manager
        self._transition_type = "fade"
        self._transition_duration = 400
    
    def set_transition(
        self,
        transition_type: str,
        duration: int = 400
    ) -> None:
        """Configura tipo de transición."""
        self._transition_type = transition_type
        self._transition_duration = duration
    
    def show_window_animated(
        self,
        window_name: str,
        data: Optional[dict] = None,
        finished: Optional[Callable] = None
    ) -> bool:
        """Muestra ventana con animación."""
        if self._transition_type == "fade":
            return self._show_with_fade(window_name, data, finished)
        elif self._transition_type == "scale":
            return self._show_with_scale(window_name, data, finished)
        elif self._transition_type == "slide":
            return self._show_with_slide(window_name, data, finished)
        else:
            return self._wm.show_window(window_name, data)
    
    def _show_with_fade(
        self,
        window_name: str,
        data: Optional[dict],
        finished: Optional[Callable]
    ) -> bool:
        """Muestra con transición fade."""
        widget = self._wm._windows.get(window_name)
        
        if not widget:
            return self._wm.show_window(window_name, data)
        
        result = self._wm.show_window(window_name, data)
        
        if result and finished:
            WindowTransition.fade_in(widget, self._transition_duration, finished=finished)
        
        return result
    
    def _show_with_scale(
        self,
        window_name: str,
        data: Optional[dict],
        finished: Optional[Callable]
    ) -> bool:
        """Muestra con transición scale."""
        widget = self._wm._windows.get(window_name)
        
        result = self._wm.show_window(window_name, data)
        
        if result and widget:
            WindowTransition.scale_in(widget, self._transition_duration, finished=finished)
        
        return result
    
    def _show_with_slide(
        self,
        window_name: str,
        data: Optional[dict],
        finished: Optional[Callable]
    ) -> bool:
        """Muestra con transición slide."""
        # Implementation
        return self._wm.show_window(window_name, data)
```

## Buenas Prácticas de Rendimiento

```python
# Optimizaciones para 60fps smooth

class AnimationOptimizer:
    """Optimizador de animaciones."""
    
    @staticmethod
    def enable_smooth_animation() -> None:
        """Habilita animaciones suaves."""
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtCore import Qt
        
        # Enable VSYNC
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)
    
    @staticmethod
    def disable_animations_for_performance() -> None:
        """Desactiva animaciones para bajo rendimiento."""
        # Disable para sistemas lentos
        pass
    
    @staticmethod
    def schedule_animations(animations: list) -> None:
        """Agenda animaciones para evitar bloqueos."""
        # Usar QTimer.singleShot para distribuir
        pass
```

## Variantes

### QML Version
```qml
// Para QtQuick/QML
import QtQuick 2.15
import QtGraphicalEffects 1.15

Rectangle {
    id: card
    
    Behavior on opacity { NumberAnimation { duration: 300; easing.type: Easing.OutCubic } }
    Behavior on scale { NumberAnimation { duration: 300; easing.type: Easing.OutElastic } }
}
```

### Hybrid (Qt + QML)
```python
# Combinar PyQt6 con QML para efectos avanzados
```

## Ejemplo de Uso Completo

```python
# Ejemplo de uso de sistema de animaciones

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton
from src.gui.pyqt6.animations import WindowTransition, AnimatedButton, LoadingIndicator
from src.gui.pyqt6.animations.easings import EasingFactory

# Crear ventana principal
main_window = QMainWindow()

# Botón animado
btn = AnimatedButton("Click Me", hover_effect="scale", click_effect="bounce")

# Indicador de carga
loader = LoadingIndicator()
loader.start()

# Transición de ventana
def on_show():
    WindowTransition.cinematic_enter(new_window, main_window)

# Animación de entrada de tarjeta
card = AnimatedCard("Título", "Contenido")
card.animate_in(delay=200)
```
