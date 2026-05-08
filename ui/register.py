"""Kairus Registration Window - Sem Outlines"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QFrame, QProgressBar,
    QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from storage.file_manager import FileManager
from security.crypto import CryptoManager
from utils.resources import get_icon_pixmap


class RegisterWindow(QWidget):
    """Registration window for creating new user accounts"""
    
    def __init__(self, app=None):
        super().__init__()
        self.app = app
        self.file_manager = FileManager()
        self.crypto = CryptoManager()
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Kairus - Create Account")
        self.resize(820, 550)
        self.setMinimumSize(700, 480)
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
            QPushButton:disabled {
                background-color: #1C2422;
                color: #8A9A95;
            }
            QFrame {
                border: none;
            }
            QProgressBar {
                background-color: #1C2422;
                border-radius: 2px;
                border: none;
            }
            QProgressBar::chunk {
                border-radius: 2px;
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
            scaled_pixmap = logo_pixmap.scaled(400, 400, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
        else:
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
        
        # ===== RIGHT PANEL - Registration Form =====
        right_panel = QFrame()
        right_panel.setStyleSheet("background-color: #111A17; border: none;")
        
        right_layout = QVBoxLayout(right_panel)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Card container
        card = QFrame()
        card.setMaximumWidth(380)
        card.setMinimumWidth(340)
        card.setStyleSheet("""
            QFrame {
                background-color: #161C1A;
                border-radius: 12px;
                border: 1px solid #1A2422;
            }
        """)
        
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(32, 32, 32, 32)
        card_layout.setSpacing(14)
        
        # Card title
        card_title = QLabel("Create Account")
        card_title.setStyleSheet("font-size: 18px; font-weight: 600; color: #F3F8F4; border: none;")
        card_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(card_title)
        
        # Card subtitle
        card_subtitle = QLabel("Start your secure journey")
        card_subtitle.setStyleSheet("font-size: 12px; color: #8A9A95; border: none;")
        card_subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(card_subtitle)
        
        card_layout.addSpacing(10)
        
        # Username input
        username_label = QLabel("Username")
        username_label.setStyleSheet("font-size: 12px; color: #F3F8F4; font-weight: 500; border: none;")
        card_layout.addWidget(username_label)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Choose a username (min. 3 characters)")
        self.username_input.textChanged.connect(self.validate_form)
        card_layout.addWidget(self.username_input)
        
        # Password input
        password_label = QLabel("Password")
        password_label.setStyleSheet("font-size: 12px; color: #F3F8F4; font-weight: 500; margin-top: 8px; border: none;")
        card_layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Create a strong password (min. 6 characters)")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.textChanged.connect(self.validate_form)
        card_layout.addWidget(self.password_input)
        
        # Password strength indicator
        self.strength_bar = QProgressBar()
        self.strength_bar.setMaximumHeight(4)
        self.strength_bar.setTextVisible(False)
        card_layout.addWidget(self.strength_bar)
        
        # Confirm password
        confirm_label = QLabel("Confirm Password")
        confirm_label.setStyleSheet("font-size: 12px; color: #F3F8F4; font-weight: 500; margin-top: 4px; border: none;")
        card_layout.addWidget(confirm_label)
        
        self.confirm_input = QLineEdit()
        self.confirm_input.setPlaceholderText("Confirm your password")
        self.confirm_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_input.textChanged.connect(self.validate_form)
        card_layout.addWidget(self.confirm_input)
        
        card_layout.addSpacing(10)
        
        # Feedback message
        self.feedback_label = QLabel("")
        self.feedback_label.setStyleSheet("font-size: 11px; border: none;")
        self.feedback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.feedback_label.setWordWrap(True)
        card_layout.addWidget(self.feedback_label)
        
        # Register button
        self.register_button = QPushButton("Create Account")
        self.register_button.setEnabled(False)
        self.register_button.clicked.connect(self.do_register)
        card_layout.addWidget(self.register_button)
        
        # Login link
        login_layout = QHBoxLayout()
        login_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        have_account_label = QLabel("Already have an account?")
        have_account_label.setStyleSheet("font-size: 11px; color: #8A9A95; border: none;")
        login_layout.addWidget(have_account_label)
        
        self.login_link = QPushButton("Login here")
        self.login_link.setStyleSheet("""
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
        self.login_link.clicked.connect(self.go_to_login)
        login_layout.addWidget(self.login_link)
        
        card_layout.addLayout(login_layout)
        
        right_layout.addWidget(card)
        
        # Add panels to main layout
        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(right_panel, 1)
    
    def validate_form(self):
        """Validate form fields and update UI"""
        username = self.username_input.text().strip()
        password = self.password_input.text()
        confirm = self.confirm_input.text()
        
        if len(username) < 3:
            self.feedback_label.setText("Username must be at least 3 characters")
            self.feedback_label.setStyleSheet("font-size: 11px; color: #ff6b6b; border: none;")
            self.register_button.setEnabled(False)
            return
        
        if self.file_manager.user_exists(username):
            self.feedback_label.setText("Username already taken")
            self.feedback_label.setStyleSheet("font-size: 11px; color: #ff6b6b; border: none;")
            self.register_button.setEnabled(False)
            return
        
        if len(password) < 6:
            self.feedback_label.setText("Password must be at least 6 characters")
            self.feedback_label.setStyleSheet("font-size: 11px; color: #ff6b6b; border: none;")
            self.register_button.setEnabled(False)
            self.update_strength(password)
            return
        
        if password != confirm:
            self.feedback_label.setText("Passwords do not match")
            self.feedback_label.setStyleSheet("font-size: 11px; color: #ff6b6b; border: none;")
            self.register_button.setEnabled(False)
            self.update_strength(password)
            return
        
        self.feedback_label.setText("✓ All good! Ready to create account")
        self.feedback_label.setStyleSheet("font-size: 11px; color: #6bc46d; border: none;")
        self.register_button.setEnabled(True)
        self.update_strength(password)
    
    def update_strength(self, password: str):
        score = 0
        if len(password) >= 6:
            score += 20
        if len(password) >= 10:
            score += 20
        if any(c.isupper() for c in password):
            score += 20
        if any(c.isdigit() for c in password):
            score += 20
        if any(c in "!@#$%^&*" for c in password):
            score += 20
        
        self.strength_bar.setValue(min(100, score))
        
        if score < 40:
            self.strength_bar.setStyleSheet("""
                QProgressBar { background-color: #1C2422; border-radius: 2px; border: none; }
                QProgressBar::chunk { background-color: #ff6b6b; border-radius: 2px; }
            """)
        elif score < 70:
            self.strength_bar.setStyleSheet("""
                QProgressBar { background-color: #1C2422; border-radius: 2px; border: none; }
                QProgressBar::chunk { background-color: #ffd93d; border-radius: 2px; }
            """)
        else:
            self.strength_bar.setStyleSheet("""
                QProgressBar { background-color: #1C2422; border-radius: 2px; border: none; }
                QProgressBar::chunk { background-color: #6bc46d; border-radius: 2px; }
            """)
    
    def do_register(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        password_hash = self.crypto.hash_password(password)
        
        success = self.file_manager.save_user(username, password_hash, "")
        
        if success:
            QMessageBox.information(
                self,
                "Account Created",
                f"Account '{username}' created successfully!\n\nYou can now login."
            )
            self.go_to_login()
        else:
            QMessageBox.critical(
                self,
                "Registration Failed",
                "Failed to create account. Please try again."
            )
    
    def go_to_login(self):
        from ui.login import LoginWindow
        self.login_window = LoginWindow(self.app if hasattr(self, 'app') else None)
        self.login_window.username_input.setText(self.username_input.text().strip())
        self.login_window.show()
        self.close()