"""Main Window - Dashboard principal do Kairus"""

import uuid
import shutil
import json
from datetime import datetime
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTreeWidget, QTreeWidgetItem,
    QTextEdit, QPushButton, QLabel, QMessageBox, QInputDialog, QLineEdit,
    QFileDialog, QStatusBar, QMenu
)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QAction, QKeySequence, QColor

from core.note_manager import NoteManager
from core.folder_manager import FolderManager
from core.vault import VaultManager
from core.autosave import AutoSaveManager
from core.pdf_exporter import PDFExporter
from storage.file_manager import FileManager
from security.crypto import CryptoManager
from ui.dialogs import FolderDialog, MoveNoteDialog, PasswordDialog
from ui.quick_note_dialog import QuickNoteDialog


class MainWindow(QMainWindow):
    """Main dashboard window after login"""
    
    def __init__(self, app, username, password):
        super().__init__()
        self.app = app
        self.username = username
        self.password = password
        
        # Initialize managers
        self.file_manager = FileManager()
        self.crypto = CryptoManager()
        self.note_manager = NoteManager(username, password, self.file_manager, self.crypto)
        self.folder_manager = FolderManager(username, password, self.file_manager, self.crypto)
        self.vault = VaultManager(self.note_manager)
        
        # State variables
        self.current_folder = None
        self.current_note_id = None
        self.current_note_title = None
        self.editor_content = ""
        self.modified = False
        self.pending_note_content = None
        self.pending_note_title = None
        
        # Auto-save setup
        self.autosave = AutoSaveManager()
        self.autosave.auto_save.connect(self.do_autosave)
        
        # Initialize UI
        self.init_ui()
        self.load_folders()
        self.setup_shortcuts()
        self.autosave.start()
        
        # Center window on screen
        self.center_window()
    
    def center_window(self):
        """Center the window on the screen"""
        screen = self.app.primaryScreen().availableGeometry()
        window_width = 1100
        window_height = 700
        
        self.resize(window_width, window_height)
        
        x = (screen.width() - window_width) // 2
        y = (screen.height() - window_height) // 2
        
        self.move(x, y)
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle(f"Kairus - {self.username}")
        self.setMinimumSize(900, 600)
        
        # Main style - sem outlines
        self.setStyleSheet("""
            QMainWindow { background-color: #0D0D0D; }
            QWidget { background-color: #0D0D0D; color: #F3F8F4; font-family: 'Segoe UI'; }
            QTreeWidget { 
                background-color: #1C2422; 
                border: 1px solid #1A2422; 
                border-radius: 6px;
                outline: none;
            }
            QTreeWidget::item { padding: 4px 4px; border-radius: 4px; }
            QTreeWidget::item:selected { background-color: #244235; }
            QTreeWidget::item:hover { background-color: #2E5A48; }
            QTextEdit { 
                background-color: #1C2422; 
                border: 1px solid #1A2422; 
                border-radius: 6px;
                padding: 8px;
                font-size: 13px;
            }
            QPushButton { 
                background-color: #244235; 
                border: none;
                border-radius: 6px; 
                padding: 6px 12px;
                font-weight: 600;
            }
            QPushButton:hover { background-color: #2E5A48; }
            QPushButton:pressed { background-color: #1A3A2E; }
            QStatusBar { background-color: #0D0D0D; color: #8A9A95; border-top: 1px solid #1A2422; }
            QMenu { background-color: #1C2422; color: #F3F8F4; border: 1px solid #1A2422; border-radius: 6px; }
            QMenu::item:selected { background-color: #244235; }
            QFrame { border: none; }
            QLabel { border: none; }
        """)
        
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(8)
        
        # ===== SIDEBAR =====
        sidebar = QWidget()
        sidebar.setMaximumWidth(250)
        sidebar.setMinimumWidth(200)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(8)
        
        # User info
        user_label = QLabel(f"👤 {self.username}")
        user_label.setStyleSheet("background-color: #244235; border-radius: 6px; padding: 8px; font-weight: bold; border: none;")
        user_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(user_label)
        
        # Folders tree
        folders_label = QLabel("📁 FOLDERS")
        folders_label.setStyleSheet("color: #8A9A95; font-size: 11px; font-weight: bold; margin-top: 8px; border: none;")
        sidebar_layout.addWidget(folders_label)
        
        self.folder_tree = QTreeWidget()
        self.folder_tree.setHeaderHidden(True)
        self.folder_tree.setIndentation(12)
        self.folder_tree.itemClicked.connect(self.on_folder_clicked)
        self.folder_tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.folder_tree.customContextMenuRequested.connect(self.show_context_menu)
        sidebar_layout.addWidget(self.folder_tree)
        
        # Buttons container
        buttons_layout = QVBoxLayout()
        buttons_layout.setSpacing(6)
        
        # New folder button
        self.new_folder_btn = QPushButton("📁 + New Folder")
        self.new_folder_btn.clicked.connect(self.create_folder)
        buttons_layout.addWidget(self.new_folder_btn)
        
        # New note button
        self.new_note_btn = QPushButton("📄 + New Note")
        self.new_note_btn.setStyleSheet("background-color: #2E5A48; border: none;")
        self.new_note_btn.clicked.connect(self.create_new_note)
        buttons_layout.addWidget(self.new_note_btn)
        
        # Quick note button
        self.quick_note_btn = QPushButton("✨ Quick Note")
        self.quick_note_btn.setStyleSheet("background-color: #3A6B5C; border: none;")
        self.quick_note_btn.clicked.connect(self.create_quick_note)
        buttons_layout.addWidget(self.quick_note_btn)
        
        sidebar_layout.addLayout(buttons_layout)
        sidebar_layout.addStretch()
        
        # ===== EDITOR AREA =====
        editor_area = QWidget()
        editor_layout = QVBoxLayout(editor_area)
        editor_layout.setContentsMargins(0, 0, 0, 0)
        editor_layout.setSpacing(6)
        
        # Editor header
        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        self.title_label = QLabel("📝 Editor")
        self.title_label.setStyleSheet("font-size: 13px; font-weight: bold; border: none;")
        header_layout.addWidget(self.title_label)
        
        header_layout.addStretch()
        
        self.save_status = QLabel("")
        self.save_status.setStyleSheet("color: #8A9A95; font-size: 10px; border: none;")
        header_layout.addWidget(self.save_status)
        
        # Save button
        self.save_btn = QPushButton("💾 Save (Ctrl+S)")
        self.save_btn.setMaximumWidth(110)
        self.save_btn.clicked.connect(self.save_current_note)
        header_layout.addWidget(self.save_btn)
        
        editor_layout.addWidget(header)
        
        # Text editor
        self.editor = QTextEdit()
        self.editor.setPlaceholderText("Write your note here...\n\n• Auto-save every 30 seconds\n• Ctrl+S to save manually\n• All notes are encrypted")
        self.editor.textChanged.connect(self.on_text_changed)
        editor_layout.addWidget(self.editor)
        
        # Status tips
        tips = QLabel("💡 Tip: Right-click on folders or notes for more options")
        tips.setStyleSheet("color: #8A9A95; font-size: 10px; margin-top: 4px; border: none;")
        tips.setAlignment(Qt.AlignmentFlag.AlignCenter)
        editor_layout.addWidget(tips)
        
        # Add to main layout
        main_layout.addWidget(sidebar)
        main_layout.addWidget(editor_area, stretch=3)
        
        # Status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Ready", 2000)
    
    def setup_shortcuts(self):
        """Setup keyboard shortcuts"""
        save_action = QAction(self)
        save_action.setShortcut(QKeySequence("Ctrl+S"))
        save_action.triggered.connect(self.save_current_note)
        self.addAction(save_action)
        
        new_action = QAction(self)
        new_action.setShortcut(QKeySequence("Ctrl+N"))
        new_action.triggered.connect(self.create_new_note)
        self.addAction(new_action)
        
        folder_action = QAction(self)
        folder_action.setShortcut(QKeySequence("Ctrl+Shift+N"))
        folder_action.triggered.connect(self.create_folder)
        self.addAction(folder_action)
        
        quick_action = QAction(self)
        quick_action.setShortcut(QKeySequence("Ctrl+Insert"))
        quick_action.triggered.connect(self.create_quick_note)
        self.addAction(quick_action)
        
        delete_action = QAction(self)
        delete_action.setShortcut(QKeySequence("Delete"))
        delete_action.triggered.connect(self.delete_current_item)
        self.addAction(delete_action)
    
    def save_current_content_before_switch(self):
        """Save current content before switching folders/notes"""
        if self.modified and self.editor_content.strip():
            if self.current_note_id and self.current_folder:
                self.save_current_note()
            elif self.editor_content.strip():
                self.save_as_draft()
    
    def save_as_draft(self):
        """Save current content as draft in vault"""
        content = self.editor.toPlainText()
        if not content.strip():
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        title = f"draft_{timestamp}"
        
        note_id = self.note_manager.create_note("vault", title, content, self.password)
        if note_id:
            self.modified = False
            self.statusBar.showMessage("Content auto-saved to Vault as draft", 2000)
            self.load_folders()
    
    def load_folders(self):
        """Load folders and notes into tree"""
        self.folder_tree.clear()
        
        folders = self.folder_manager.get_folders()
        
        for folder in folders:
            folder_name = folder['name']
            is_protected = folder.get('protected', False)
            is_unlocked = self.folder_manager.is_unlocked(folder_name)
            
            # Folder icon
            if is_protected and not is_unlocked and folder_name != "vault":
                icon = "🔒 "
            elif is_protected and folder_name == "vault" and not is_unlocked:
                icon = "🔒 "
            else:
                icon = "📁 "
            
            folder_item = QTreeWidgetItem([f"{icon}{folder_name}"])
            folder_item.setData(0, Qt.UserRole, {
                "type": "folder",
                "name": folder_name,
                "protected": is_protected,
                "unlocked": is_unlocked
            })
            
            # Only show notes if folder is unlocked OR not protected
            if not is_protected or is_unlocked:
                notes = self.note_manager.list_notes(folder_name)
                for note in notes:
                    note_item = QTreeWidgetItem([f"📄 {note['title']}"])
                    note_item.setData(0, Qt.UserRole, {
                        "type": "note",
                        "id": note['id'],
                        "title": note['title'],
                        "folder": folder_name
                    })
                    folder_item.addChild(note_item)
            else:
                # Show locked message
                lock_item = QTreeWidgetItem(["🔒 Locked - Click to unlock"])
                lock_item.setData(0, Qt.UserRole, {"type": "lock", "folder": folder_name})
                lock_item.setForeground(0, QColor("#8A9A95"))
                folder_item.addChild(lock_item)
            
            self.folder_tree.addTopLevelItem(folder_item)
        
        self.folder_tree.expandAll()
    
    def on_folder_clicked(self, item, column):
        """Handle folder/note click"""
        data = item.data(0, Qt.UserRole)
        
        if not data:
            return
        
        # Handle lock item - unlock folder first
        if data.get("type") == "lock":
            folder_name = data["folder"]
            self.unlock_folder_and_select(folder_name)
            return
        
        # Save current content before switching
        self.save_current_content_before_switch()
        
        if data.get("type") == "folder":
            folder_name = data["name"]
            is_protected = data.get("protected", False)
            is_unlocked = data.get("unlocked", False)
            
            # Check if folder is protected and not unlocked
            if is_protected and not is_unlocked:
                self.unlock_folder_and_select(folder_name)
                return
            
            # Folder is accessible
            self.current_folder = folder_name
            self.current_note_id = None
            self.current_note_title = None
            
            # Clear editor for new note
            self.editor.clear()
            self.editor_content = ""
            self.modified = False
            self.title_label.setText(f"📁 {folder_name}")
            self.statusBar.showMessage(f"Folder '{folder_name}' ready. Write your note and click 'New Note' to save.", 3000)
            
        elif data.get("type") == "note":
            note_id = data["id"]
            folder_name = data["folder"]
            
            # Check if folder is protected and not unlocked
            folder_meta = self.file_manager.get_folder_meta(self.username, folder_name)
            if folder_meta and folder_meta.get("protected"):
                if not self.folder_manager.is_unlocked(folder_name):
                    self.unlock_folder_and_load_note(folder_name, note_id)
                    return
            
            self.load_note_content(note_id, folder_name)
    
    def unlock_folder_and_select(self, folder_name: str):
        """Unlock a folder and then select it"""
        if folder_name == "vault":
            message = "Enter your master password to access the Vault:"
        else:
            message = f"Enter password for folder '{folder_name}':"
        
        dialog = PasswordDialog("Folder Protected", message, self)
        if dialog.exec():
            password = dialog.get_password()
            if password and self.folder_manager.unlock_folder(folder_name, password):
                self.statusBar.showMessage(f"Folder '{folder_name}' unlocked", 2000)
                self.load_folders()
                self.select_folder_in_tree(folder_name)
            else:
                QMessageBox.warning(self, "Access Denied", "Incorrect password!")
    
    def unlock_folder_and_load_note(self, folder_name: str, note_id: str):
        """Unlock a folder and then load a specific note"""
        if folder_name == "vault":
            message = "Enter your master password to access the Vault:"
        else:
            message = f"Enter password for folder '{folder_name}':"
        
        dialog = PasswordDialog("Folder Protected", message, self)
        if dialog.exec():
            password = dialog.get_password()
            if password and self.folder_manager.unlock_folder(folder_name, password):
                self.statusBar.showMessage(f"Folder '{folder_name}' unlocked", 2000)
                self.load_folders()
                self.load_note_content(note_id, folder_name)
            else:
                QMessageBox.warning(self, "Access Denied", "Incorrect password!")
    
    def load_note_content(self, note_id: str, folder_name: str):
        """Load note content - SILENT FAIL (no error popup)"""
        try:
            # Get password for the folder
            folder_password = None
            
            if folder_name == "vault":
                folder_password = self.password
            else:
                folder_meta = self.file_manager.get_folder_meta(self.username, folder_name)
                if folder_meta and folder_meta.get("protected"):
                    folder_password = self.folder_manager.get_folder_password(folder_name)
                    if not folder_password:
                        self.statusBar.showMessage(f"Folder '{folder_name}' is locked", 2000)
                        return
                else:
                    folder_password = self.password
            
            note = self.note_manager.get_note(folder_name, note_id, folder_password)
            
            if note:
                self.current_note_id = note_id
                self.current_note_title = note["title"]
                self.current_folder = folder_name
                self.editor.setPlainText(note["content"])
                self.editor_content = note["content"]
                self.modified = False
                self.title_label.setText(f"📝 {note['title']}")
                self.statusBar.showMessage(f"Editing: {note['title']}", 2000)
            else:
                self.statusBar.showMessage("Could not load note", 2000)
                
        except Exception as e:
            print(f"Error loading note: {e}")
            self.statusBar.showMessage("Could not load note", 2000)
    
    def select_folder_in_tree(self, folder_name: str):
        """Select a folder in the tree view and set it as current"""
        for i in range(self.folder_tree.topLevelItemCount()):
            item = self.folder_tree.topLevelItem(i)
            data = item.data(0, Qt.UserRole)
            if data and data.get("type") == "folder" and data.get("name") == folder_name:
                self.folder_tree.setCurrentItem(item)
                self.current_folder = folder_name
                self.current_note_id = None
                self.current_note_title = None
                self.editor.clear()
                self.editor_content = ""
                self.modified = False
                self.title_label.setText(f"📁 {folder_name}")
                self.statusBar.showMessage(f"Folder '{folder_name}' unlocked. Write your note and click 'New Note' to save.", 3000)
                break
    
    def on_text_changed(self):
        """Handle text changes - trigger auto-save"""
        current = self.editor.toPlainText()
        if current != self.editor_content:
            self.modified = True
            self.editor_content = current
            self.save_status.setText("● Unsaved")
            self.save_status.setStyleSheet("color: #ff6b6b; font-size: 11px;")
            self.autosave.content_changed()
    
    def do_autosave(self):
        """Auto-save trigger"""
        if self.modified and self.editor_content.strip():
            self.save_current_note()
    
    def save_current_note(self):
        """Save the current note"""
        content = self.editor.toPlainText()
        
        if not content.strip() and self.current_note_id:
            return
        
        if self.current_note_id and self.current_folder:
            # Get password for the folder
            folder_password = None
            if self.current_folder == "vault":
                folder_password = self.password
            elif self.folder_manager.is_unlocked(self.current_folder):
                folder_password = self.folder_manager.get_folder_password(self.current_folder)
            else:
                folder_meta = self.file_manager.get_folder_meta(self.username, self.current_folder)
                if folder_meta and folder_meta.get("protected"):
                    self.statusBar.showMessage(f"Folder '{self.current_folder}' is locked", 2000)
                    return
            
            try:
                success = self.note_manager.update_note(
                    self.current_folder, self.current_note_id, content, folder_password
                )
                
                if success:
                    self.modified = False
                    self.editor_content = content
                    self.save_status.setText("✓ Saved")
                    self.save_status.setStyleSheet("color: #6bc46d; font-size: 11px;")
                    self.statusBar.showMessage("Note saved", 1500)
                    
                    QTimer.singleShot(2000, lambda: self.save_status.setText("") if not self.modified else None)
                else:
                    self.statusBar.showMessage("Save failed", 1500)
                    
            except Exception as e:
                print(f"Save error: {e}")
                self.statusBar.showMessage("Save failed", 1500)
                
        elif self.current_folder and self.editor_content.strip():
            self.create_new_note()
    
    def create_new_note(self):
        """Create a new note in current folder"""
        if not self.current_folder:
            QMessageBox.information(self, "No Folder", "Please select a folder first.")
            return
        
        # Check if folder is protected and unlocked
        folder_meta = self.file_manager.get_folder_meta(self.username, self.current_folder)
        if folder_meta and folder_meta.get("protected"):
            if not self.folder_manager.is_unlocked(self.current_folder):
                QMessageBox.warning(self, "Access Denied", 
                    f"Folder '{self.current_folder}' is password protected.\n\n"
                    "Please click on the folder and enter the password first.")
                return
        
        content = self.editor.toPlainText()
        default_title = f"Note_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        title, ok = QInputDialog.getText(
            self, "New Note", "Enter note title:",
            QLineEdit.Normal, default_title
        )
        
        if ok and title.strip():
            # Get password for the folder
            folder_password = None
            if self.current_folder == "vault":
                folder_password = self.password
            elif self.folder_manager.is_unlocked(self.current_folder):
                folder_password = self.folder_manager.get_folder_password(self.current_folder)
            
            try:
                note_id = self.note_manager.create_note(
                    self.current_folder, title.strip(), content, folder_password
                )
                
                if note_id:
                    self.current_note_id = note_id
                    self.current_note_title = title.strip()
                    
                    if content.strip():
                        self.modified = False
                        self.editor_content = content
                        self.save_status.setText("✓ Saved")
                        self.save_status.setStyleSheet("color: #6bc46d; font-size: 11px;")
                        QTimer.singleShot(2000, lambda: self.save_status.setText("") if not self.modified else None)
                    
                    self.title_label.setText(f"📝 {title}")
                    self.statusBar.showMessage(f"Note '{title}' created in '{self.current_folder}'", 3000)
                    self.load_folders()
                    self.select_note_in_tree(note_id, self.current_folder)
                else:
                    QMessageBox.warning(self, "Error", "Could not create note.")
                    
            except Exception as e:
                print(f"Create note error: {e}")
                QMessageBox.warning(self, "Error", "Could not create note.")
    
    def create_quick_note(self):
        """Open Quick Note dialog for fast writing"""
        dialog = QuickNoteDialog(self)
        
        def on_note_saved(content):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            title = f"QuickNote_{timestamp}"
            
            note_id = self.note_manager.create_note("vault", title, content, self.password)
            
            if note_id:
                self.statusBar.showMessage(f"Quick note saved to Vault as '{title}'", 3000)
                self.load_folders()
            else:
                QMessageBox.warning(self, "Error", "Could not save quick note")
        
        dialog.note_saved.connect(on_note_saved)
        dialog.show()
    
    def select_note_in_tree(self, note_id: str, folder_name: str):
        """Select a note in the tree view"""
        for i in range(self.folder_tree.topLevelItemCount()):
            folder_item = self.folder_tree.topLevelItem(i)
            folder_data = folder_item.data(0, Qt.UserRole)
            if folder_data and folder_data.get("type") == "folder" and folder_data.get("name") == folder_name:
                for j in range(folder_item.childCount()):
                    note_item = folder_item.child(j)
                    note_data = note_item.data(0, Qt.UserRole)
                    if note_data and note_data.get("type") == "note" and note_data.get("id") == note_id:
                        self.folder_tree.setCurrentItem(note_item)
                        self.load_note_content(note_id, folder_name)
                        break
                break
    
    def create_folder(self):
        """Create a new folder"""
        dialog = FolderDialog(self)
        if dialog.exec():
            name, password = dialog.get_result()
            if name:
                success = self.folder_manager.create_folder(name, password)
                if success:
                    self.load_folders()
                    self.statusBar.showMessage(f"Folder '{name}' created", 2000)
                else:
                    QMessageBox.warning(self, "Error", f"Folder '{name}' already exists")
    
    def show_context_menu(self, position):
        """Show context menu for tree items"""
        item = self.folder_tree.itemAt(position)
        if not item:
            return
        
        data = item.data(0, Qt.UserRole)
        if not data:
            return
        
        menu = QMenu(self)
        
        if data.get("type") == "folder":
            folder_name = data["name"]
            
            if folder_name != "vault":
                new_note_action = menu.addAction("📝 New Note")
                new_note_action.triggered.connect(self.create_new_note)
                
                menu.addSeparator()
                
                rename_action = menu.addAction("✏️ Rename Folder")
                rename_action.triggered.connect(lambda: self.rename_folder(folder_name, item))
                
                if data.get("protected"):
                    if data.get("unlocked"):
                        lock_action = menu.addAction("🔒 Lock Folder")
                        lock_action.triggered.connect(lambda: self.lock_folder(folder_name))
                    else:
                        unlock_action = menu.addAction("🔓 Unlock Folder")
                        unlock_action.triggered.connect(lambda: self.unlock_folder_and_select(folder_name))
                
                menu.addSeparator()
                
                delete_action = menu.addAction("🗑️ Delete Folder")
                delete_action.triggered.connect(lambda: self.delete_folder(folder_name, item))
            
            else:
                info_action = menu.addAction("ℹ️ Vault Info")
                info_action.triggered.connect(lambda: QMessageBox.information(
                    self, "Vault",
                    "The Vault is your secure fallback storage.\n\n"
                    "• Quick notes are saved here\n"
                    "• Auto-saved drafts go here\n"
                    "• Protected with your master password\n"
                    "• Cannot be deleted"
                ))
        
        elif data.get("type") == "note":
            note_id = data["id"]
            note_title = data["title"]
            folder_name = data["folder"]
            
            rename_action = menu.addAction("✏️ Rename")
            rename_action.triggered.connect(lambda: self.rename_note(note_id, note_title, folder_name, item))
            
            move_action = menu.addAction("📂 Move to Folder")
            move_action.triggered.connect(lambda: self.move_note(note_id, folder_name, item))
            
            export_menu = menu.addMenu("📄 Export")
            
            pdf_desktop = export_menu.addAction("PDF - Desktop")
            pdf_desktop.triggered.connect(lambda: self.export_note_to_pdf_desktop_from_menu(note_id, folder_name, note_title))
            
            pdf_documents = export_menu.addAction("PDF - Documents")
            pdf_documents.triggered.connect(lambda: self.export_note_to_pdf_documents_from_menu(note_id, folder_name, note_title))
            
            pdf_custom = export_menu.addAction("PDF - Choose location...")
            pdf_custom.triggered.connect(lambda: self.export_note_to_pdf_custom_from_menu(note_id, folder_name, note_title))
            
            export_menu.addSeparator()
            
            txt_export = export_menu.addAction("TXT File")
            txt_export.triggered.connect(lambda: self.export_note_to_txt_from_menu(note_id, folder_name, note_title))
            
            menu.addSeparator()
            
            delete_action = menu.addAction("🗑️ Delete")
            delete_action.triggered.connect(lambda: self.delete_note(note_id, note_title, folder_name, item))
        
        elif data.get("type") == "lock":
            unlock_action = menu.addAction("🔓 Unlock Folder")
            unlock_action.triggered.connect(lambda: self.unlock_folder_and_select(data["folder"]))
        
        menu.exec(self.folder_tree.mapToGlobal(position))
    
    # ==================== EXPORT METHODS ====================
    
    def export_note_to_pdf_desktop_from_menu(self, note_id, folder_name, title):
        """Export note to PDF on Desktop (from context menu)"""
        folder_password = None
        if folder_name == "vault":
            folder_password = self.password
        else:
            folder_password = self.folder_manager.get_folder_password(folder_name)
        
        note = self.note_manager.get_note(folder_name, note_id, folder_password)
        if note:
            self.export_to_pdf_desktop(note["title"], note["content"])

    def export_note_to_pdf_documents_from_menu(self, note_id, folder_name, title):
        """Export note to PDF in Documents (from context menu)"""
        folder_password = None
        if folder_name == "vault":
            folder_password = self.password
        else:
            folder_password = self.folder_manager.get_folder_password(folder_name)
        
        note = self.note_manager.get_note(folder_name, note_id, folder_password)
        if note:
            self.export_to_pdf_documents(note["title"], note["content"])

    def export_note_to_pdf_custom_from_menu(self, note_id, folder_name, title):
        """Export note to PDF with custom location (from context menu)"""
        folder_password = None
        if folder_name == "vault":
            folder_password = self.password
        else:
            folder_password = self.folder_manager.get_folder_password(folder_name)
        
        note = self.note_manager.get_note(folder_name, note_id, folder_password)
        if note:
            self.export_to_pdf_custom(note["title"], note["content"])

    def export_note_to_txt_from_menu(self, note_id, folder_name, title):
        """Export note to TXT (from context menu)"""
        folder_password = None
        if folder_name == "vault":
            folder_password = self.password
        else:
            folder_password = self.folder_manager.get_folder_password(folder_name)
        
        note = self.note_manager.get_note(folder_name, note_id, folder_password)
        if note:
            self.export_to_txt(note["title"], note["content"])

    def export_to_pdf_desktop(self, title, content):
        """Export note to PDF on Desktop"""
        try:
            output_path = PDFExporter.export_to_desktop(content, title)
            self.statusBar.showMessage(f"PDF exported to Desktop", 5000)
            QMessageBox.information(self, "Export Complete", 
                f"Note exported successfully to PDF!\n\nSaved to:\n{output_path}")
        except Exception as e:
            QMessageBox.critical(self, "Export Failed", f"Could not export to PDF: {str(e)}")

    def export_to_pdf_documents(self, title, content):
        """Export note to PDF in Documents folder"""
        try:
            output_path = PDFExporter.export_to_user_documents(content, title)
            self.statusBar.showMessage(f"PDF exported to Documents", 5000)
            QMessageBox.information(self, "Export Complete", 
                f"Note exported successfully to PDF!\n\nSaved to:\n{output_path}")
        except Exception as e:
            QMessageBox.critical(self, "Export Failed", f"Could not export to PDF: {str(e)}")

    def export_to_pdf_custom(self, title, content):
        """Export note to PDF with custom location"""
        try:
            safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_title = safe_title.replace(' ', '_')
            
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Export Note as PDF", 
                f"{safe_title}.pdf", 
                "PDF Files (*.pdf)"
            )
            
            if file_path:
                output_path = PDFExporter.export_note_to_pdf(content, title, file_path)
                self.statusBar.showMessage(f"PDF exported", 5000)
                QMessageBox.information(self, "Export Complete", 
                    f"Note exported successfully to PDF!\n\nSaved to:\n{output_path}")
        except Exception as e:
            QMessageBox.critical(self, "Export Failed", f"Could not export to PDF: {str(e)}")

    def export_to_txt(self, title, content):
        """Export note to TXT file"""
        try:
            safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_title = safe_title.replace(' ', '_')
            
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Export Note as TXT", 
                f"{safe_title}.txt", 
                "Text Files (*.txt)"
            )
            
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(f"Title: {title}\n")
                    f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write("=" * 50 + "\n\n")
                    f.write(content)
                
                self.statusBar.showMessage(f"TXT exported", 3000)
                QMessageBox.information(self, "Export Complete", 
                    f"Note exported successfully to TXT!\n\nSaved to:\n{file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Export Failed", f"Could not export to TXT: {str(e)}")
    
    # ==================== FOLDER OPERATIONS ====================
    
    def lock_folder(self, folder_name: str):
        """Lock a folder"""
        self.folder_manager.lock_folder(folder_name)
        self.load_folders()
        self.statusBar.showMessage(f"Folder '{folder_name}' locked", 2000)
        
        if self.current_folder == folder_name:
            self.save_current_content_before_switch()
            self.current_folder = None
            self.current_note_id = None
            self.editor.clear()
            self.editor_content = ""
            self.modified = False
            self.title_label.setText("📝 Editor")
    
    def rename_folder(self, folder_name, item):
        """Rename a folder"""
        new_name, ok = QInputDialog.getText(
            self, "Rename Folder", "Enter new name:", QLineEdit.Normal, folder_name
        )
        
        if ok and new_name and new_name != folder_name:
            old_path = self.file_manager._get_folder_path(self.username, folder_name)
            new_path = self.file_manager._get_folder_path(self.username, new_name)
            
            if new_path.exists():
                QMessageBox.warning(self, "Error", f"Folder '{new_name}' already exists")
                return
            
            shutil.move(str(old_path), str(new_path))
            
            meta_file = new_path / "meta.json"
            if meta_file.exists():
                with open(meta_file, 'r') as f:
                    meta = json.load(f)
                meta["name"] = new_name
                with open(meta_file, 'w') as f:
                    json.dump(meta, f)
            
            self.load_folders()
            self.statusBar.showMessage(f"Folder renamed to '{new_name}'", 2000)
    
    def delete_folder(self, folder_name, item):
        """Delete a folder"""
        self.save_current_content_before_switch()
        
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Delete folder '{folder_name}' and ALL its notes?\nThis cannot be undone!",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            success = self.file_manager.delete_folder(self.username, folder_name)
            if success:
                if self.current_folder == folder_name:
                    self.current_folder = None
                    self.current_note_id = None
                    self.editor.clear()
                    self.editor_content = ""
                    self.modified = False
                    self.title_label.setText("📝 Editor")
                
                self.load_folders()
                self.statusBar.showMessage(f"Folder '{folder_name}' deleted", 2000)
    
    # ==================== NOTE OPERATIONS ====================
    
    def rename_note(self, note_id, old_title, folder_name, item):
        """Rename a note"""
        new_title, ok = QInputDialog.getText(
            self, "Rename Note", "Enter new title:", QLineEdit.Normal, old_title
        )
        
        if ok and new_title and new_title != old_title:
            folder_password = None
            if folder_name == "vault":
                folder_password = self.password
            else:
                folder_password = self.folder_manager.get_folder_password(folder_name)
            
            note = self.note_manager.get_note(folder_name, note_id, folder_password)
            if note:
                self.note_manager.delete_note(folder_name, note_id)
                new_id = self.note_manager.create_note(folder_name, new_title, note["content"], folder_password)
                
                if new_id:
                    if self.current_note_id == note_id:
                        self.current_note_id = new_id
                        self.current_note_title = new_title
                        self.title_label.setText(f"📝 {new_title}")
                    
                    self.load_folders()
                    self.statusBar.showMessage(f"Note renamed to '{new_title}'", 2000)
    
    def delete_note(self, note_id, note_title, folder_name, item):
        """Delete a note"""
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Delete note '{note_title}'?\nThis cannot be undone!",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            success = self.note_manager.delete_note(folder_name, note_id)
            if success:
                if self.current_note_id == note_id:
                    self.current_note_id = None
                    self.editor.clear()
                    self.editor_content = ""
                    self.modified = False
                    self.title_label.setText(f"📁 {folder_name}")
                
                self.load_folders()
                self.statusBar.showMessage(f"Note '{note_title}' deleted", 2000)
    
    def move_note(self, note_id, source_folder, item):
        """Move note to another folder"""
        self.save_current_content_before_switch()
        
        folders = self.folder_manager.get_folders()
        available = [f for f in folders if f['name'] != source_folder]
        
        if not available:
            QMessageBox.information(self, "No Destination", "No other folders available")
            return
        
        dialog = MoveNoteDialog(available, source_folder, self)
        if dialog.exec():
            target_folder = dialog.get_selected_folder()
            
            if target_folder:
                # Get source password
                source_password = None
                if source_folder == "vault":
                    source_password = self.password
                else:
                    source_password = self.folder_manager.get_folder_password(source_folder)
                
                note = self.note_manager.get_note(source_folder, note_id, source_password)
                if note:
                    # Get target password
                    target_password = None
                    
                    if target_folder == "vault":
                        target_password = self.password
                    else:
                        target_meta = self.file_manager.get_folder_meta(self.username, target_folder)
                        if target_meta and target_meta.get("protected"):
                            if not self.folder_manager.is_unlocked(target_folder):
                                # Try to unlock target
                                dialog_pwd = PasswordDialog("Folder Protected", f"Password for folder '{target_folder}':", self)
                                if dialog_pwd.exec():
                                    target_password = dialog_pwd.get_password()
                                    if target_password and self.folder_manager.unlock_folder(target_folder, target_password):
                                        target_password = self.folder_manager.get_folder_password(target_folder)
                                    else:
                                        QMessageBox.warning(self, "Access Denied", "Incorrect password!")
                                        return
                                else:
                                    return
                            else:
                                target_password = self.folder_manager.get_folder_password(target_folder)
                    
                    new_id = self.note_manager.create_note(target_folder, note["title"], note["content"], target_password)
                    if new_id:
                        self.note_manager.delete_note(source_folder, note_id)
                        self.load_folders()
                        self.statusBar.showMessage(f"Note moved to '{target_folder}'", 2000)
                        
                        if self.current_note_id == note_id:
                            self.current_note_id = None
                            self.editor.clear()
                            self.editor_content = ""
                            self.modified = False
                            self.title_label.setText("📝 Editor")
    
    def delete_current_item(self):
        """Delete current selected item"""
        current = self.folder_tree.currentItem()
        if current:
            data = current.data(0, Qt.UserRole)
            if data:
                if data.get("type") == "note":
                    self.delete_note(data["id"], data["title"], data["folder"], current)
                elif data.get("type") == "folder" and data["name"] != "vault":
                    self.delete_folder(data["name"], current)
    
    def closeEvent(self, event):
        """Handle window close - save unsaved content"""
        self.save_current_content_before_switch()
        self.autosave.stop()
        event.accept()