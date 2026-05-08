"""Kairus Login Window - Versão Corrigida sem outlines"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QFrame, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QColor
from storage.file_manager import FileManager
from security.crypto import CryptoManager
from utils.resources import get_icon_pixmap


class LoginWindow(QWidget):
    """Login window for Kairus application"""
    
    def __init__(self, app=None):
        super().__init__()
        self.app = app
        self.file_manager = FileManager()
        self.crypto = CryptoManager()
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Kairus - Login")
        self.resize(820, 500)
        self.setMinimumSize(700, 420)
        self.setStyleSheet("""
            QWidget {
                background-color: #0D0D0D;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLineEdit {
                background-color: #1C2422;
                border: 1px solid #1A2422;
                border-radius: 6px;
                padding: 10px 12px;
                color: #F3F8F4;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 1px solid #244235;
            }
            QPushButton {
                background-color: #244235;
                border: none;
                border-radius: 6px;
                padding: 10px;
                color: #F3F8F4;
                font-size: 13px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #2E5A48;
            }
            QPushButton:pressed {
                background-color: #1A3A2E;
            }
            QFrame {
                border: none;
            }
        """)
        
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # ===== LEFT PANEL - Branding =====
        left_panel = QFrame()
        left_panel.setStyleSheet("background-color: #0D0D0D; border: none;")
        
        left_layout = QVBoxLayout(left_panel)
        left_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_layout.setSpacing(15)
        
        # Logo (from embedded resource)
        logo_label = QLabel()
        logo_pixmap = get_icon_pixmap()
        if logo_pixmap and not logo_pixmap.isNull():
            # Scale logo to reasonable size
            scaled_pixmap = logo_pixmap.scaled(400, 400, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
        else:
            # Fallback if icon not found
            logo_label.setText("🔒")
            logo_label.setStyleSheet("font-size: 48px; color: #244235; font-weight: bold; border: none;")
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_layout.addWidget(logo_label)
        
        # Title
        title_label = QLabel("KAIRUS")
        title_label.setStyleSheet("font-size: 28px; color: #F3F8F4; font-weight: 600; letter-spacing: 2px; border: none;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_layout.addWidget(title_label)
        
        # Subtitle
        subtitle_label = QLabel("Secure Notes")
        subtitle_label.setStyleSheet("font-size: 12px; color: #8A9A95; border: none;")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_layout.addWidget(subtitle_label)
        
        # ===== RIGHT PANEL - Login Form =====
        right_panel = QFrame()
        right_panel.setStyleSheet("background-color: #111A17; border: none;")
        
        right_layout = QVBoxLayout(right_panel)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Card container
        card = QFrame()
        card.setMaximumWidth(360)
        card.setMinimumWidth(320)
        card.setStyleSheet("""
            QFrame {
                background-color: #161C1A;
                border-radius: 12px;
                border: 1px solid #1A2422;
            }
        """)
        
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(32, 32, 32, 32)
        card_layout.setSpacing(16)
        
        # Card title
        card_title = QLabel("Welcome Back")
        card_title.setStyleSheet("font-size: 18px; font-weight: 600; color: #F3F8F4; border: none;")
        card_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(card_title)
        
        # Card subtitle
        card_subtitle = QLabel("Login to access your vault")
        card_subtitle.setStyleSheet("font-size: 12px; color: #8A9A95; border: none;")
        card_subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(card_subtitle)
        
        card_layout.addSpacing(10)
        
        # Username input
        username_label = QLabel("Username")
        username_label.setStyleSheet("font-size: 12px; color: #F3F8F4; font-weight: 500; border: none;")
        card_layout.addWidget(username_label)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.returnPressed.connect(self.do_login)
        card_layout.addWidget(self.username_input)
        
        # Password input
        password_label = QLabel("Password")
        password_label.setStyleSheet("font-size: 12px; color: #F3F8F4; font-weight: 500; margin-top: 8px; border: none;")
        card_layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.returnPressed.connect(self.do_login)
        card_layout.addWidget(self.password_input)
        
        card_layout.addSpacing(10)
        
        # Status message
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("font-size: 11px; color: #ff6b6b; border: none;")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setWordWrap(True)
        card_layout.addWidget(self.status_label)
        
        # Login button
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.do_login)
        card_layout.addWidget(self.login_button)
        
        # Register link
        register_layout = QHBoxLayout()
        register_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        no_account_label = QLabel("Don't have an account?")
        no_account_label.setStyleSheet("font-size: 11px; color: #8A9A95; border: none;")
        register_layout.addWidget(no_account_label)
        
        self.register_link = QPushButton("Create one")
        self.register_link.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                color: #244235;
                font-size: 11px;
                font-weight: 600;
                text-decoration: underline;
                padding: 0px;
            }
            QPushButton:hover {
                color: #2E5A48;
            }
        """)
        self.register_link.clicked.connect(self.go_to_register)
        register_layout.addWidget(self.register_link)
        
        card_layout.addLayout(register_layout)
        
        right_layout.addWidget(card)
        
        # Add panels to main layout
        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(right_panel, 1)
    
    def do_login(self):
        """Perform login authentication"""
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not username or not password:
            self.status_label.setText("Please fill in all fields")
            return
        
        # Check if user exists
        if not self.file_manager.user_exists(username):
            self.status_label.setText("User not found")
            self.password_input.clear()
            return
        
        # Load user data
        user_data = self.file_manager.load_user(username)
        if not user_data:
            self.status_label.setText("Error loading user data")
            return
        
        # Verify password
        if self.crypto.verify_password(password, user_data["password_hash"]):
            self.status_label.setText("")
            
            # Login successful - open main window
            from ui.main_window import MainWindow
            self.main_window = MainWindow(self.app, username, password)
            self.main_window.show()
            self.close()
        else:
            self.status_label.setText("Invalid password")
            self.password_input.clear()
            self.password_input.setFocus()
    
    def go_to_register(self):
        """Switch to registration window"""
        from ui.register import RegisterWindow
        self.register_window = RegisterWindow(self.app)
        self.register_window.show()
        self.close()