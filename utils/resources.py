"""Resources Manager - Handles embedded resources for executable"""

import os
import sys
from pathlib import Path


def resource_path(relative_path: str) -> str:
    """
    Get absolute path to resource, works for dev and for PyInstaller
    
    Args:
        relative_path: Relative path to the resource file
        
    Returns:
        Absolute path to the resource
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)


def get_icon_path() -> str:
    """Get the path to the application icon"""
    return resource_path("icon.png")


def get_icon_pixmap():
    """Get QPixmap of the icon for use in UI"""
    from PySide6.QtGui import QPixmap
    
    icon_path = get_icon_path()
    if os.path.exists(icon_path):
        return QPixmap(icon_path)
    return None