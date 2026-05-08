"""File Manager - Handles all file system operations - Versão Estável"""

import os
import json
import shutil
from pathlib import Path
from typing import List, Dict, Optional


class FileManager:
    """Manages all file operations for users, folders, and notes - Estrutura limpa"""
    
    def __init__(self, base_path: str = "data"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(exist_ok=True)

    # ==================== CAMINHOS ====================
    
    def _get_user_path(self, username: str) -> Path:
        """Retorna o caminho DA RAIZ do usuário (não cria nada)"""
        return self.base_path / username

    def _get_user_file(self, username: str) -> Path:
        """Retorna o caminho do arquivo user.json"""
        return self._get_user_path(username) / "user.json"

    def _get_vault_path(self, username: str) -> Path:
        """Retorna o caminho da pasta vault"""
        return self._get_user_path(username) / "vault"

    def _get_folders_path(self, username: str) -> Path:
        """Retorna o caminho da pasta folders"""
        return self._get_user_path(username) / "folders"

    def _get_folder_path(self, username: str, folder_name: str) -> Path:
        """Retorna o caminho de uma pasta específica"""
        return self._get_folders_path(username) / folder_name

    def _get_note_path(self, username: str, folder_name: str, note_id: str) -> Path:
        """Retorna o caminho de uma nota específica"""
        return self._get_folder_path(username, folder_name) / f"{note_id}.json"

    # ==================== USER MANAGEMENT ====================
    
    def has_users(self) -> bool:
        """Verifica se existe pelo menos um usuário"""
        try:
            for item in self.base_path.iterdir():
                if item.is_dir() and (item / "user.json").exists():
                    return True
            return False
        except Exception:
            return False

    def user_exists(self, username: str) -> bool:
        """Verifica se um usuário específico existe"""
        return self._get_user_file(username).exists()

    def save_user(self, username: str, password_hash: str, salt: str = "") -> bool:
        """Salva os dados do usuário"""
        try:
            user_path = self._get_user_path(username)
            user_file = self._get_user_file(username)
            
            # Só cria a pasta do usuário se não existir
            if not user_path.exists():
                user_path.mkdir(parents=True, exist_ok=True)
            
            # Se o arquivo já existe, não sobrescreve
            if user_file.exists():
                return True
            
            user_data = {
                "username": username,
                "password_hash": password_hash,
                "salt": salt,
                "created_at": __import__('datetime').datetime.now().isoformat()
            }
            
            with open(user_file, "w", encoding='utf-8') as f:
                json.dump(user_data, f, indent=2, ensure_ascii=False)
            
            # Criar vault após salvar usuário
            self.create_vault(username)
            
            return True
        except Exception as e:
            print(f"Error saving user: {e}")
            return False

    def load_user(self, username: str) -> Optional[Dict]:
        """Carrega os dados do usuário"""
        try:
            user_file = self._get_user_file(username)
            if not user_file.exists():
                return None
            
            with open(user_file, "r", encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading user: {e}")
            return None

    def delete_user(self, username: str) -> bool:
        """Deleta um usuário e todos os seus dados"""
        try:
            user_path = self._get_user_path(username)
            if user_path.exists():
                shutil.rmtree(user_path)
            return True
        except Exception:
            return False

    # ==================== FOLDER MANAGEMENT ====================
    
    def create_folder(self, username: str, folder_name: str, password_hash: Optional[str] = None) -> bool:
        """Cria uma nova pasta para o usuário"""
        try:
            # Não permitir criar pasta chamada vault
            if folder_name == "vault":
                return False
            
            folder_path = self._get_folder_path(username, folder_name)
            
            # Verificar se já existe
            if folder_path.exists():
                print(f"[DEBUG] Pasta '{folder_name}' já existe")
                return False
            
            # Criar a pasta
            folder_path.mkdir(parents=True, exist_ok=True)
            
            # Salvar metadados
            meta = {
                "name": folder_name,
                "protected": password_hash is not None,
                "password_hash": password_hash,
                "created_at": __import__('datetime').datetime.now().isoformat()
            }
            
            with open(folder_path / "meta.json", "w", encoding='utf-8') as f:
                json.dump(meta, f, indent=2)
            
            print(f"[DEBUG] Pasta '{folder_name}' criada em '{folder_path}'")
            return True
            
        except Exception as e:
            print(f"Error creating folder: {e}")
            return False

    def delete_folder(self, username: str, folder_name: str) -> bool:
        """Deleta uma pasta e todas as suas notas"""
        try:
            if folder_name == "vault":
                return False
            
            folder_path = self._get_folder_path(username, folder_name)
            if folder_path.exists():
                shutil.rmtree(folder_path)
                print(f"[DEBUG] Pasta '{folder_name}' deletada")
            return True
        except Exception as e:
            print(f"Error deleting folder: {e}")
            return False

    def get_folders(self, username: str) -> List[Dict]:
        """Retorna todas as pastas do usuário (SEM DUPLICATAS)"""
        folders = []
        seen_names = set()
        
        users_path = self._get_user_path(username)
        
        # Verificar se o usuário existe
        if not users_path.exists():
            return folders
        
        # Adicionar vault
        vault_meta = self.get_folder_meta(username, "vault")
        if vault_meta:
            folders.append(vault_meta)
            seen_names.add("vault")
        
        # Adicionar outras pastas
        folders_path = self._get_folders_path(username)
        if folders_path.exists():
            for folder_path in folders_path.iterdir():
                if folder_path.is_dir() and folder_path.name != "vault":
                    folder_name = folder_path.name
                    
                    # Pular duplicatas
                    if folder_name in seen_names:
                        continue
                    
                    meta_file = folder_path / "meta.json"
                    if meta_file.exists():
                        with open(meta_file, "r", encoding='utf-8') as f:
                            meta = json.load(f)
                            folders.append(meta)
                            seen_names.add(folder_name)
                    else:
                        folders.append({"name": folder_name, "protected": False, "password_hash": None})
                        seen_names.add(folder_name)
        
        return folders

    def get_folder_meta(self, username: str, folder_name: str) -> Optional[Dict]:
        """Retorna os metadados de uma pasta"""
        # Caso especial para vault
        if folder_name == "vault":
            vault_path = self._get_vault_path(username)
            meta_file = vault_path / "meta.json"
            
            if meta_file.exists():
                with open(meta_file, "r", encoding='utf-8') as f:
                    return json.load(f)
            else:
                # Criar metadata do vault se não existir
                if not vault_path.exists():
                    vault_path.mkdir(parents=True, exist_ok=True)
                meta = {
                    "name": "vault",
                    "protected": True,
                    "password_hash": None,
                    "created_at": __import__('datetime').datetime.now().isoformat()
                }
                with open(meta_file, "w", encoding='utf-8') as f:
                    json.dump(meta, f, indent=2)
                return meta
        
        # Pastas normais
        folder_path = self._get_folder_path(username, folder_name)
        meta_file = folder_path / "meta.json"
        
        if meta_file.exists():
            with open(meta_file, "r", encoding='utf-8') as f:
                return json.load(f)
        
        return None

    def update_folder_password(self, username: str, folder_name: str, new_password_hash: Optional[str]) -> bool:
        """Atualiza a senha de uma pasta"""
        try:
            if folder_name == "vault":
                return False
            
            folder_path = self._get_folder_path(username, folder_name)
            meta_file = folder_path / "meta.json"
            
            if not meta_file.exists():
                return False
            
            with open(meta_file, "r", encoding='utf-8') as f:
                meta = json.load(f)
            
            meta["protected"] = new_password_hash is not None
            meta["password_hash"] = new_password_hash
            
            with open(meta_file, "w", encoding='utf-8') as f:
                json.dump(meta, f, indent=2)
            
            return True
        except Exception:
            return False

    def create_vault(self, username: str) -> bool:
        """Cria a pasta vault para o usuário (apenas uma vez)"""
        try:
            vault_path = self._get_vault_path(username)
            meta_file = vault_path / "meta.json"
            
            # Criar pasta vault se não existir
            if not vault_path.exists():
                vault_path.mkdir(parents=True, exist_ok=True)
            
            # Criar metadata se não existir
            if not meta_file.exists():
                meta = {
                    "name": "vault",
                    "protected": True,
                    "password_hash": None,
                    "created_at": __import__('datetime').datetime.now().isoformat()
                }
                with open(meta_file, "w", encoding='utf-8') as f:
                    json.dump(meta, f, indent=2)
                print(f"[DEBUG] Vault criado para usuário '{username}'")
            else:
                print(f"[DEBUG] Vault já existe para usuário '{username}'")
            
            return True
        except Exception as e:
            print(f"Error creating vault: {e}")
            return False

    # ==================== NOTE MANAGEMENT ====================
    
    def save_note(self, username: str, folder_name: str, note_id: str, encrypted_content: str, title: str) -> bool:
        """Salva uma nota no disco"""
        try:
            folder_path = self._get_folder_path(username, folder_name)
            folder_path.mkdir(parents=True, exist_ok=True)
            
            note_path = folder_path / f"{note_id}.json"
            
            note_data = {
                "id": note_id,
                "title": title,
                "content": encrypted_content,
                "updated_at": __import__('datetime').datetime.now().isoformat()
            }
            
            with open(note_path, "w", encoding='utf-8') as f:
                json.dump(note_data, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error saving note: {e}")
            return False

    def load_note(self, username: str, folder_name: str, note_id: str) -> Optional[Dict]:
        """Carrega uma nota do disco"""
        try:
            note_path = self._get_note_path(username, folder_name, note_id)
            
            if not note_path.exists():
                return None
            
            with open(note_path, "r", encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return None

    def delete_note(self, username: str, folder_name: str, note_id: str) -> bool:
        """Deleta uma nota do disco"""
        try:
            note_path = self._get_note_path(username, folder_name, note_id)
            
            if note_path.exists():
                note_path.unlink()
            return True
        except Exception:
            return False

    def list_notes(self, username: str, folder_name: str) -> List[Dict]:
        """Lista todas as notas de uma pasta"""
        notes = []
        folder_path = self._get_folder_path(username, folder_name)
        
        if not folder_path.exists():
            return notes
        
        for note_file in folder_path.glob("*.json"):
            if note_file.name == "meta.json":
                continue
            
            try:
                with open(note_file, "r", encoding='utf-8') as f:
                    data = json.load(f)
                    notes.append({
                        "id": data.get("id", note_file.stem),
                        "title": data.get("title", "Untitled")
                    })
            except Exception:
                continue
        
        notes.sort(key=lambda x: x['title'].lower())
        return notes

    def move_note(self, username: str, from_folder: str, to_folder: str, note_id: str) -> bool:
        """Move uma nota de uma pasta para outra"""
        try:
            note_data = self.load_note(username, from_folder, note_id)
            if not note_data:
                return False
            
            success = self.save_note(
                username, to_folder, note_id,
                note_data["content"], note_data["title"]
            )
            
            if success:
                self.delete_note(username, from_folder, note_id)
            
            return success
        except Exception:
            return False