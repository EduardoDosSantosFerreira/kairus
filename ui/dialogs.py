"""Dialog windows for Kairus application"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QCheckBox, QComboBox,
    QMessageBox
)
from PySide6.QtCore import Qt


class FolderDialog(QDialog):
    """Dialog for creating new folders"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("New Folder")
        self.setModal(True)
        self.setFixedSize(380, 280)
        self.setStyleSheet("""
            QDialog { background-color: #0D0D0D; }
            QLabel { color: #F3F8F4; }
            QLineEdit, QCheckBox { 
                background-color: #1C2422; 
                color: #F3F8F4; 
                border: 1px solid #1A2422; 
                border-radius: 6px; 
                padding: 8px 12px;
            }
            QLineEdit:focus { border: 1px solid #244235; }
            QPushButton { 
                background-color: #244235; 
                border-radius: 6px; 
                padding: 8px 16px;
                color: #F3F8F4;
                font-weight: 600;
            }
            QPushButton:hover { background-color: #2E5A48; }
            QPushButton:disabled { background-color: #1C2422; color: #8A9A95; }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        
        # Title
        title = QLabel("Create New Folder")
        title.setStyleSheet("font-size: 16px; font-weight: 600;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Name input
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Folder name")
        self.name_input.textChanged.connect(self.validate)
        layout.addWidget(self.name_input)
        
        # Password checkbox
        self.protect_check = QCheckBox("Protect with password")
        self.protect_check.toggled.connect(self.toggle_password)
        layout.addWidget(self.protect_check)
        
        # Password inputs
        self.pwd_input = QLineEdit()
        self.pwd_input.setPlaceholderText("Password")
        self.pwd_input.setEchoMode(QLineEdit.Password)
        self.pwd_input.hide()
        self.pwd_input.textChanged.connect(self.validate)
        layout.addWidget(self.pwd_input)
        
        self.confirm_input = QLineEdit()
        self.confirm_input.setPlaceholderText("Confirm password")
        self.confirm_input.setEchoMode(QLineEdit.Password)
        self.confirm_input.hide()
        self.confirm_input.textChanged.connect(self.validate)
        layout.addWidget(self.confirm_input)
        
        # Feedback
        self.feedback = QLabel("")
        self.feedback.setStyleSheet("color: #8A9A95; font-size: 11px;")
        self.feedback.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.feedback)
        
        layout.addStretch()
        
        # Buttons
        btn_layout = QHBoxLayout()
        create_btn = QPushButton("Create")
        create_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(create_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)
    
    def toggle_password(self, checked):
        """Show/hide password fields"""
        self.pwd_input.setVisible(checked)
        self.confirm_input.setVisible(checked)
        if not checked:
            self.pwd_input.clear()
            self.confirm_input.clear()
        self.validate()
    
    def validate(self):
        """Validate form inputs"""
        name = self.name_input.text().strip()
        
        if len(name) < 2:
            self.feedback.setText("Name must be at least 2 characters")
            self.feedback.setStyleSheet("color: #ff6b6b; font-size: 11px;")
            return False
        
        if self.protect_check.isChecked():
            pwd = self.pwd_input.text()
            confirm = self.confirm_input.text()
            
            if len(pwd) < 4:
                self.feedback.setText("Password must be at least 4 characters")
                self.feedback.setStyleSheet("color: #ff6b6b; font-size: 11px;")
                return False
            
            if pwd != confirm:
                self.feedback.setText("Passwords do not match")
                self.feedback.setStyleSheet("color: #ff6b6b; font-size: 11px;")
                return False
        
        self.feedback.setText("✓ Ready to create")
        self.feedback.setStyleSheet("color: #6bc46d; font-size: 11px;")
        return True
    
    def get_result(self):
        """Get folder name and password"""
        name = self.name_input.text().strip()
        password = self.pwd_input.text() if self.protect_check.isChecked() else None
        return name, password


class MoveNoteDialog(QDialog):
    """Dialog for moving notes between folders"""
    
    def __init__(self, folders, current_folder=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Move Note")
        self.setModal(True)
        self.setFixedSize(350, 180)
        self.setStyleSheet("""
            QDialog { background-color: #0D0D0D; }
            QLabel { color: #F3F8F4; }
            QComboBox { 
                background-color: #1C2422; 
                color: #F3F8F4; 
                border: 1px solid #1A2422; 
                border-radius: 6px; 
                padding: 8px;
            }
            QComboBox::drop-down { border: none; }
            QComboBox QAbstractItemView {
                background-color: #1C2422;
                color: #F3F8F4;
                selection-background-color: #244235;
            }
            QPushButton { 
                background-color: #244235; 
                border-radius: 6px; 
                padding: 8px 16px;
                color: #F3F8F4;
                font-weight: 600;
            }
            QPushButton:hover { background-color: #2E5A48; }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        layout.addWidget(QLabel("Select destination folder:"))
        
        self.folder_combo = QComboBox()
        for folder in folders:
            if folder['name'] != current_folder:
                icon = "🔒 " if folder.get('protected') else "📁 "
                self.folder_combo.addItem(f"{icon}{folder['name']}", folder['name'])
        
        layout.addWidget(self.folder_combo)
        
        layout.addStretch()
        
        btn_layout = QHBoxLayout()
        move_btn = QPushButton("Move")
        move_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(move_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)
    
    def get_selected_folder(self):
        """Get selected folder name"""
        return self.folder_combo.currentData()


class PasswordDialog(QDialog):
    """Generic password input dialog"""
    
    def __init__(self, title: str, message: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setFixedSize(350, 160)
        self.setStyleSheet("""
            QDialog { background-color: #0D0D0D; }
            QLabel { color: #F3F8F4; }
            QLineEdit { 
                background-color: #1C2422; 
                color: #F3F8F4; 
                border: 1px solid #1A2422; 
                border-radius: 6px; 
                padding: 8px 12px;
            }
            QLineEdit:focus { border: 1px solid #244235; }
            QPushButton { 
                background-color: #244235; 
                border-radius: 6px; 
                padding: 8px 16px;
                color: #F3F8F4;
                font-weight: 600;
            }
            QPushButton:hover { background-color: #2E5A48; }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        
        layout.addWidget(QLabel(message))
        
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.returnPressed.connect(self.accept)
        layout.addWidget(self.password_input)
        
        layout.addStretch()
        
        btn_layout = QHBoxLayout()
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(ok_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)
    
    def get_password(self) -> str:
        """Get entered password"""
        return self.password_input.text()