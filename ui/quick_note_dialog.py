"""Quick Note Dialog - Popup para escrita rápida"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTextEdit, 
    QLabel, QPushButton, QMessageBox
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction, QKeySequence
from datetime import datetime


class QuickNoteDialog(QDialog):
    """Dialog for quick note taking - opens directly for writing"""
    
    note_saved = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("✨ Quick Note")
        self.setModal(False)
        self.setMinimumSize(500, 400)
        self.resize(550, 450)
        
        # Center on parent
        if parent:
            parent_geo = parent.geometry()
            x = parent_geo.x() + (parent_geo.width() - 550) // 2
            y = parent_geo.y() + (parent_geo.height() - 450) // 2
            self.move(x, y)
        
        self.init_ui()
        self.setup_shortcuts()
        
    def init_ui(self):
        """Initialize the dialog"""
        self.setStyleSheet("""
            QDialog {
                background-color: #0D0D0D;
                border: 1px solid #244235;
                border-radius: 8px;
            }
            QLabel {
                color: #F3F8F4;
            }
            QTextEdit {
                background-color: #1C2422;
                border: 1px solid #1A2422;
                border-radius: 6px;
                color: #F3F8F4;
                font-family: monospace;
                font-size: 13px;
                padding: 8px;
            }
            QTextEdit:focus {
                border: 1px solid #244235;
            }
            QPushButton {
                background-color: #244235;
                border-radius: 6px;
                padding: 8px 16px;
                color: #F3F8F4;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #2E5A48;
            }
            QPushButton#cancel {
                background-color: #1C2422;
            }
            QPushButton#cancel:hover {
                background-color: #2C3432;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # Header
        header = QHBoxLayout()
        title_label = QLabel("📝 Quick Note")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #244235;")
        header.addWidget(title_label)
        
        header.addStretch()
        
        hint_label = QLabel("Save to Vault • Ctrl+Enter to save")
        hint_label.setStyleSheet("color: #8A9A95; font-size: 10px;")
        header.addWidget(hint_label)
        
        layout.addLayout(header)
        
        # Separator
        sep = QLabel("─" * 50)
        sep.setStyleSheet("color: #1A2422;")
        layout.addWidget(sep)
        
        # Editor
        self.editor = QTextEdit()
        self.editor.setPlaceholderText("""
Write your note here...

• Press Ctrl+Enter to save
• Press Esc to cancel
• Note will be saved to Vault automatically
        """.strip())
        self.editor.setFocus()
        layout.addWidget(self.editor)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        
        self.save_btn = QPushButton("💾 Save to Vault (Ctrl+Enter)")
        self.save_btn.clicked.connect(self.save_and_close)
        
        self.cancel_btn = QPushButton("Cancel (Esc)")
        self.cancel_btn.setObjectName("cancel")
        self.cancel_btn.clicked.connect(self.reject)
        
        btn_layout.addStretch()
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(btn_layout)
    
    def setup_shortcuts(self):
        """Setup keyboard shortcuts"""
        save_action = QAction(self)
        save_action.setShortcut(QKeySequence("Ctrl+Return"))
        save_action.triggered.connect(self.save_and_close)
        self.addAction(save_action)
        
        cancel_action = QAction(self)
        cancel_action.setShortcut(QKeySequence("Esc"))
        cancel_action.triggered.connect(self.reject)
        self.addAction(cancel_action)
    
    def get_content(self) -> str:
        """Get editor content"""
        return self.editor.toPlainText().strip()
    
    def save_and_close(self):
        """Save note and close"""
        content = self.get_content()
        
        if not content:
            reply = QMessageBox.question(
                self, "Empty Note",
                "Your note is empty. Discard anyway?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.reject()
            return
        
        self.note_saved.emit(content)
        self.accept()
    
    def clear(self):
        """Clear editor content"""
        self.editor.clear()