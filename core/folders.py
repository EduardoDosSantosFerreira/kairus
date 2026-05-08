"""Folder Manager with unlock cache"""

from typing import List, Dict, Optional
from storage.file_manager import FileManager
from security.crypto import CryptoManager


class FolderManager:
    """Manages folder operations with unlock cache"""
    
    def __init__(self, username: str, password: str, file_manager: FileManager, crypto: CryptoManager):
        self.username = username
        self.password = password
        self.fm = file_manager
        self.crypto = crypto
        self.unlocked_folders = set()
        self.folder_passwords = {}

    def create_folder(self, name: str, folder_password: Optional[str] = None) -> bool:
        """Create a new folder"""
        if any(f["name"] == name for f in self.fm.get_folders(self.username)):
            return False
        
        password_hash = None
        if folder_password:
            password_hash = self.crypto.hash_password(folder_password)
        
        return self.fm.create_folder(self.username, name, password_hash)

    def get_folders(self) -> List[Dict]:
        """Get all folders"""
        return self.fm.get_folders(self.username)

    def is_unlocked(self, folder_name: str) -> bool:
        """Check if folder is unlocked in current session"""
        return folder_name in self.unlocked_folders

    def get_folder_password(self, folder_name: str) -> Optional[str]:
        """Get the password for an unlocked folder"""
        return self.folder_passwords.get(folder_name)

    def unlock_folder(self, folder_name: str, password: str) -> bool:
        """Unlock a protected folder for this session and store password"""
        if folder_name == "vault":
            user_data = self.fm.load_user(self.username)
            if self.crypto.verify_password(password, user_data["password_hash"]):
                self.unlocked_folders.add(folder_name)
                self.folder_passwords[folder_name] = password
                print(f"[DEBUG] Vault unlocked with master password")
                return True
            return False
        
        meta = self.fm.get_folder_meta(self.username, folder_name)
        if not meta or not meta.get("protected"):
            return False
        
        if self.crypto.verify_password(password, meta["password_hash"]):
            self.unlocked_folders.add(folder_name)
            self.folder_passwords[folder_name] = password
            print(f"[DEBUG] Folder '{folder_name}' unlocked with password")
            return True
        return False

    def lock_folder(self, folder_name: str):
        """Lock a folder (remove from cache)"""
        if folder_name in self.unlocked_folders:
            self.unlocked_folders.remove(folder_name)
        if folder_name in self.folder_passwords:
            del self.folder_passwords[folder_name]
        print(f"[DEBUG] Folder '{folder_name}' locked")

    def update_password(self, folder_name: str, new_password: Optional[str], current_password: Optional[str] = None) -> bool:
        """Update or remove folder password"""
        meta = self.fm.get_folder_meta(self.username, folder_name)
        if not meta:
            return False
        
        if meta.get("protected"):
            if not current_password or not self.crypto.verify_password(current_password, meta["password_hash"]):
                return False
        
        new_hash = self.crypto.hash_password(new_password) if new_password else None
        success = self.fm.update_folder_password(self.username, folder_name, new_hash)
        
        if success:
            self.lock_folder(folder_name)
        
        return success

    def verify_password(self, folder_name: str, password: str) -> bool:
        """Verify folder password without unlocking"""
        if folder_name == "vault":
            user_data = self.fm.load_user(self.username)
            return self.crypto.verify_password(password, user_data["password_hash"])
        
        meta = self.fm.get_folder_meta(self.username, folder_name)
        if not meta or not meta.get("protected"):
            return False
        return self.crypto.verify_password(password, meta["password_hash"])
    
    def get_folder_key(self, folder_name: str, folder_password: Optional[str] = None) -> bytes:
        """Get encryption key for a folder"""
        if folder_name == "vault":
            key, _ = self.crypto.derive_key(self.password)
            return key
        
        meta = self.fm.get_folder_meta(self.username, folder_name)
        if meta and meta.get("protected"):
            if not folder_password:
                folder_password = self.get_folder_password(folder_name)
                if not folder_password:
                    raise ValueError(f"Folder '{folder_name}' is password protected. Password required.")
            key, _ = self.crypto.derive_key(folder_password)
            return key
        
        key, _ = self.crypto.derive_key(self.password)
        return key