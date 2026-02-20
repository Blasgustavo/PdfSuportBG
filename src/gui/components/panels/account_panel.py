from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QFrame, QLineEdit, QFormLayout, QGroupBox, QMessageBox,
    QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSignal
from typing import Optional

from src.gui.themes.theme_manager import theme_manager
from src.utils.app_settings import app_settings


class AccountPanel(QWidget):
    """Panel de cuenta de usuario."""
    
    user_changed = pyqtSignal()
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._setup_ui()
        self._update_user_state()
        
        theme_manager.theme_changed.connect(self._apply_style)

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        title = QLabel("Cuenta")
        title.setObjectName("panelTitle")
        main_layout.addWidget(title)
        
        scroll = QScrollArea()
        scroll.setObjectName("accountScroll")
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(20)
        
        self.user_info_group = self._create_user_info_group()
        self.login_group = self._create_login_group()
        
        scroll_layout.addWidget(self.user_info_group)
        scroll_layout.addWidget(self.login_group)
        
        scroll_layout.addStretch()
        
        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)
    
    def _create_user_info_group(self) -> QGroupBox:
        group = QGroupBox("Información de Usuario")
        group.setObjectName("accountGroup")
        layout = QVBoxLayout(group)
        layout.setSpacing(15)
        
        self.user_avatar = QLabel("👤")
        self.user_avatar.setObjectName("userAvatar")
        self.user_avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.user_avatar)
        
        self.username_label = QLabel("")
        self.username_label.setObjectName("usernameLabel")
        self.username_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.username_label)
        
        self.email_label = QLabel("")
        self.email_label.setObjectName("emailLabel")
        self.email_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.email_label)
        
        self.last_login_label = QLabel("")
        self.last_login_label.setObjectName("lastLoginLabel")
        self.last_login_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.last_login_label)
        
        self.logout_btn = QPushButton("Cerrar Sesión")
        self.logout_btn.setObjectName("logoutButton")
        self.logout_btn.clicked.connect(self._on_logout)
        layout.addWidget(self.logout_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        return group
    
    def _create_login_group(self) -> QGroupBox:
        group = QGroupBox("Iniciar Sesión")
        group.setObjectName("loginGroup")
        layout = QFormLayout(group)
        layout.setSpacing(10)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Usuario")
        self.username_input.setObjectName("usernameInput")
        layout.addRow("Usuario:", self.username_input)
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Correo electrónico (opcional)")
        self.email_input.setObjectName("emailInput")
        layout.addRow("Correo:", self.email_input)
        
        self.login_btn = QPushButton("Iniciar Sesión")
        self.login_btn.setObjectName("loginButton")
        self.login_btn.clicked.connect(self._on_login)
        layout.addRow("", self.login_btn)
        
        info = QLabel("Ingresa tus credenciales para acceder a funcionalidades adicionales.")
        info.setObjectName("loginInfo")
        layout.addRow("", info)
        
        return group
    
    def _update_user_state(self):
        user_info = app_settings.get_user_info()
        
        if user_info["logged_in"]:
            self.user_info_group.setVisible(True)
            self.login_group.setVisible(False)
            self.username_label.setText(user_info["username"])
            self.email_label.setText(user_info["email"])
            if user_info["last_login"]:
                self.last_login_label.setText(f"Último ingreso: {user_info['last_login'][:10]}")
            else:
                self.last_login_label.setText("")
        else:
            self.user_info_group.setVisible(False)
            self.login_group.setVisible(True)
    
    def _on_login(self):
        username = self.username_input.text().strip()
        if not username:
            QMessageBox.warning(self, "Advertencia", "Por favor ingresa un nombre de usuario.")
            return
        
        email = self.email_input.text().strip()
        
        app_settings.login(username, email)
        self.username_input.clear()
        self.email_input.clear()
        self._update_user_state()
        self.user_changed.emit()
        
        QMessageBox.information(self, "Éxito", f"Bienvenido, {username}!")
    
    def _on_logout(self):
        reply = QMessageBox.question(
            self, 
            "Cerrar Sesión", 
            "¿Estás seguro que deseas cerrar sesión?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            app_settings.logout()
            self._update_user_state()
            self.user_changed.emit()

    def _apply_style(self):
        colors = theme_manager.colors
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {colors['bg_primary']};
            }}
            QLabel#panelTitle {{
                color: {colors['fg_primary']};
                font-size: 24px;
                font-weight: bold;
            }}
            QGroupBox#accountGroup, QGroupBox#loginGroup {{
                color: {colors['fg_primary']};
                font-weight: bold;
                border: 1px solid {colors['border']};
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 5px;
            }}
            QLabel#userAvatar {{
                font-size: 64px;
            }}
            QLabel#usernameLabel {{
                color: {colors['fg_primary']};
                font-size: 18px;
                font-weight: bold;
            }}
            QLabel#emailLabel {{
                color: {colors['fg_secondary']};
                font-size: 12px;
            }}
            QLabel#lastLoginLabel {{
                color: {colors['fg_secondary']};
                font-size: 11px;
            }}
            QLabel#loginInfo {{
                color: {colors['fg_secondary']};
                font-size: 11px;
                font-weight: normal;
            }}
            QLineEdit {{
                background-color: {colors['bg_tertiary']};
                color: {colors['fg_primary']};
                border: 1px solid {colors['border']};
                border-radius: 4px;
                padding: 8px;
            }}
            QLineEdit::placeholder {{
                color: {colors['fg_disabled']};
            }}
            QPushButton#loginButton, QPushButton#logoutButton {{
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {colors['accent']}, stop:1 {colors['accent_light']});
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
            }}
            QPushButton#loginButton:hover, QPushButton#logoutButton:hover {{
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {colors['accent_light']}, stop:1 {colors['accent']});
            }}
            QPushButton#loginButton:pressed, QPushButton#logoutButton:pressed {{
                background-color: {colors['accent_dark']};
            }}
            QScrollArea#accountScroll {{
                border: none;
                background-color: transparent;
            }}
            QScrollBar:vertical {{
                width: 8px;
                background: transparent;
            }}
            QScrollBar::handle:vertical {{
                background: {colors['bg_current_line']};
                border-radius: 4px;
                min-height: 40px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: {colors['accent']};
            }}
        """)
