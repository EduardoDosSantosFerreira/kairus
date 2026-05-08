"""Kairus - Secure Note Taking Application - Main Entry Point"""

import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

from storage.file_manager import FileManager
from ui.login import LoginWindow
from ui.register import RegisterWindow


class KairusApplication(QApplication):
    """Main application class"""
    
    def __init__(self, argv):
        super().__init__(argv)
        self.setApplicationName("Kairus")
        self.setOrganizationName("KairusSecure")
        self.setStyle('Fusion')
        
        self.file_manager = FileManager()
        self.main_window = None
        
        self.init_app()
    
    def init_app(self):
        """Initialize the application - show login or register"""
        if not self.file_manager.has_users():
            self.show_register()
        else:
            self.show_login()
    
    def show_register(self):
        """Show registration window"""
        self.register_window = RegisterWindow(self)
        self.register_window.show()
    
    def show_login(self):
        """Show login window"""
        self.login_window = LoginWindow(self)
        self.login_window.show()


def main():
    """Main entry point"""
    app = KairusApplication(sys.argv)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()