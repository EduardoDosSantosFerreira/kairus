"""Note Manager - Handles note operations with encryption - Versão Simplificada"""

import uuid
from typing import List, Dict, Optional
from storage.file_manager import FileManager
from security.crypto import CryptoManager


class NoteManager:
    """Manages note creation, reading, updating, deletion"""
    
    def __init__(self, username: str, master_password: str, file_manager: FileManager, crypto: CryptoManager):
        self.username = username
        self.master_password = master_password
        self.fm = file_manager
        self.crypto = crypto

    def _get_password_for_folder(self, folder_name: str, folder_password: Optional[str] = None) -> str:
        """
        Get the password to use for encryption/decryption for a folder.
        Returns the actual password string (not key).
        """
        # Vault uses master password
        if folder_name == "vault":
            return self.master_password
        
        # Check folder metadata
        folder_meta = self.fm.get_folder_meta(self.username, folder_name)
        
        # If folder is protected, use the provided folder password
        if folder_meta and folder_meta.get("protected"):
            if not folder_password:
                raise ValueError(f"Folder '{folder_name}' is password protected. Password required.")
            return folder_password
        
        # Regular folder uses master password
        return self.master_password

    def create_note(self, folder_name: str, title: str, content: str, folder_password: Optional[str] = None) -> Optional[str]:
        """Create a new note"""
        try:
            note_id = str(uuid.uuid4())
            password = self._get_password_for_folder(folder_name, folder_password)
            
            encrypted_content = self.crypto.encrypt(content, password) if content else ""
            
            success = self.fm.save_note(self.username, folder_name, note_id, encrypted_content, title)
            
            if success:
                print(f"[DEBUG] Note created: {note_id} in {folder_name}")
                return note_id
            return None
            
        except Exception as e:
            print(f"Error creating note: {e}")
            return None

    def update_note(self, folder_name: str, note_id: str, content: str, folder_password: Optional[str] = None) -> bool:
        """Update an existing note"""
        try:
            password = self._get_password_for_folder(folder_name, folder_password)
            encrypted_content = self.crypto.encrypt(content, password) if content else ""
            
            note = self.fm.load_note(self.username, folder_name, note_id)
            if not note:
                return False
            
            return self.fm.save_note(self.username, folder_name, note_id, encrypted_content, note["title"])
            
        except Exception as e:
            print(f"Error updating note: {e}")
            return False

    def get_note(self, folder_name: str, note_id: str, folder_password: Optional[str] = None) -> Optional[Dict]:
        """Get a note with decrypted content"""
        try:
            note = self.fm.load_note(self.username, folder_name, note_id)
            if not note:
                return None
            
            password = self._get_password_for_folder(folder_name, folder_password)
            
            if note["content"]:
                content = self.crypto.decrypt(note["content"], password)
            else:
                content = ""
            
            return {
                "id": note_id,
                "title": note["title"],
                "content": content
            }
            
        except ValueError as e:
            raise e
        except Exception as e:
            print(f"Error getting note: {e}")
            return None

    def delete_note(self, folder_name: str, note_id: str) -> bool:
        """Delete a note"""
        try:
            return self.fm.delete_note(self.username, folder_name, note_id)
        except Exception as e:
            print(f"Error deleting note: {e}")
            return False

    def list_notes(self, folder_name: str) -> List[Dict]:
        """List all notes in a folder (titles only)"""
        try:
            return self.fm.list_notes(self.username, folder_name)
        except Exception as e:
            print(f"Error listing notes: {e}")
            return []

    def move_note(self, note_id: str, from_folder: str, to_folder: str, 
                  from_password: Optional[str] = None, to_password: Optional[str] = None) -> bool:
        """Move a note from one folder to another"""
        try:
            note = self.get_note(from_folder, note_id, from_password)
            if not note:
                return False
            
            new_id = self.create_note(to_folder, note["title"], note["content"], to_password)
            
            if new_id:
                self.delete_note(from_folder, note_id)
                return True
            
            return False
            
        except Exception as e:
            print(f"Error moving note: {e}")
            return False