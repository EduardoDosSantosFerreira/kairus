"""Cryptography Module - AES-256-CBC with PBKDF2 - Optimized Version"""

import os
import base64
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from typing import Tuple, Optional


class CryptoManager:
    """
    Manages encryption, decryption, and password hashing using AES-256-CBC.
    Features:
    - PBKDF2 key derivation with 100,000 iterations
    - Unique salt per encryption (stored with ciphertext)
    - PKCS7 padding for block alignment
    - Constant-time password verification
    """
    
    # Constants
    SALT_SIZE = 32
    IV_SIZE = 16
    KEY_SIZE = 32
    PBKDF2_ITERATIONS = 100000
    HASH_ALGORITHM = 'sha256'
    AES_MODE = modes.CBC
    PADDING_BLOCK_SIZE = 128
    
    @staticmethod
    def _get_backend():
        """Get cryptography backend (cached for performance)"""
        return default_backend()
    
    @staticmethod
    def _pbkdf2(password: str, salt: bytes, dklen: int = KEY_SIZE) -> bytes:
        """
        Derive a key using PBKDF2.
        This is a thin wrapper for performance and consistency.
        """
        return hashlib.pbkdf2_hmac(
            CryptoManager.HASH_ALGORITHM,
            password.encode('utf-8'),
            salt,
            CryptoManager.PBKDF2_ITERATIONS,
            dklen=dklen
        )
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a password using PBKDF2.
        Returns base64(salt + hash) for secure storage.
        
        Args:
            password: Plain text password
            
        Returns:
            Base64 encoded string containing salt and password hash
        """
        salt = os.urandom(CryptoManager.SALT_SIZE)
        key = CryptoManager._pbkdf2(password, salt, CryptoManager.KEY_SIZE)
        combined = salt + key
        return base64.b64encode(combined).decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """
        Verify a password against its hash.
        Uses constant-time comparison to prevent timing attacks.
        
        Args:
            password: Plain text password to verify
            hashed: Stored hash from hash_password()
            
        Returns:
            True if password matches, False otherwise
        """
        try:
            data = base64.b64decode(hashed)
            if len(data) != CryptoManager.SALT_SIZE + CryptoManager.KEY_SIZE:
                return False
            
            salt = data[:CryptoManager.SALT_SIZE]
            stored_key = data[CryptoManager.SALT_SIZE:]
            new_key = CryptoManager._pbkdf2(password, salt, CryptoManager.KEY_SIZE)
            
            # Constant-time comparison (prevents timing attacks)
            return secrets.compare_digest(new_key, stored_key)
        except Exception:
            return False
    
    @staticmethod
    def derive_key(password: str, salt: Optional[bytes] = None) -> Tuple[bytes, bytes]:
        """
        Derive a 32-byte encryption key from password.
        
        Args:
            password: Input password
            salt: Optional salt (generated if not provided)
            
        Returns:
            Tuple of (key, salt)
        """
        if salt is None:
            salt = os.urandom(CryptoManager.SALT_SIZE)
        elif len(salt) != CryptoManager.SALT_SIZE:
            raise ValueError(f"Salt must be {CryptoManager.SALT_SIZE} bytes")
        
        key = CryptoManager._pbkdf2(password, salt, CryptoManager.KEY_SIZE)
        return key, salt
    
    @staticmethod
    def encrypt(content: str, password: str) -> str:
        """
        Encrypt content using AES-256-CBC with PBKDF2 key derivation.
        Format: base64(salt(32) + iv(16) + ciphertext)
        
        Args:
            content: Plain text to encrypt
            password: Password to derive encryption key
            
        Returns:
            Base64 encoded encrypted content
            
        Raises:
            ValueError: If encryption fails
        """
        if not content:
            return ""
        
        if not password:
            raise ValueError("Password cannot be empty")
        
        try:
            # Generate random salt and derive key
            salt = os.urandom(CryptoManager.SALT_SIZE)
            key = CryptoManager._pbkdf2(password, salt, CryptoManager.KEY_SIZE)
            
            # Generate random IV
            iv = os.urandom(CryptoManager.IV_SIZE)
            
            # Prepare content with PKCS7 padding
            content_bytes = content.encode('utf-8')
            padder = padding.PKCS7(CryptoManager.PADDING_BLOCK_SIZE).padder()
            padded_data = padder.update(content_bytes) + padder.finalize()
            
            # Encrypt
            cipher = Cipher(
                algorithms.AES(key),
                CryptoManager.AES_MODE(iv),
                backend=CryptoManager._get_backend()
            )
            encryptor = cipher.encryptor()
            ciphertext = encryptor.update(padded_data) + encryptor.finalize()
            
            # Combine salt + iv + ciphertext
            combined = salt + iv + ciphertext
            return base64.b64encode(combined).decode('utf-8')
            
        except Exception as e:
            raise ValueError(f"Encryption failed: {str(e)}")
    
    @staticmethod
    def decrypt(encrypted: str, password: str) -> str:
        """
        Decrypt content using AES-256-CBC with PBKDF2 key derivation.
        Expects format: base64(salt(32) + iv(16) + ciphertext)
        
        Args:
            encrypted: Base64 encoded encrypted content
            password: Password to derive decryption key
            
        Returns:
            Decrypted plain text
            
        Raises:
            ValueError: If decryption fails (wrong password or corrupted data)
        """
        if not encrypted:
            return ""
        
        if not password:
            raise ValueError("Password cannot be empty")
        
        try:
            # Decode from base64
            raw = base64.b64decode(encrypted)
            
            # Validate minimum length
            min_length = CryptoManager.SALT_SIZE + CryptoManager.IV_SIZE + 1
            if len(raw) < min_length:
                raise ValueError("Encrypted content too short")
            
            # Extract components
            salt = raw[:CryptoManager.SALT_SIZE]
            iv = raw[CryptoManager.SALT_SIZE:CryptoManager.SALT_SIZE + CryptoManager.IV_SIZE]
            ciphertext = raw[CryptoManager.SALT_SIZE + CryptoManager.IV_SIZE:]
            
            # Derive key from password and salt
            key = CryptoManager._pbkdf2(password, salt, CryptoManager.KEY_SIZE)
            
            # Decrypt
            cipher = Cipher(
                algorithms.AES(key),
                CryptoManager.AES_MODE(iv),
                backend=CryptoManager._get_backend()
            )
            decryptor = cipher.decryptor()
            padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
            
            # Remove padding
            unpadder = padding.PKCS7(CryptoManager.PADDING_BLOCK_SIZE).unpadder()
            plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
            
            return plaintext.decode('utf-8')
            
        except Exception as e:
            raise ValueError(f"Decryption failed: {str(e)}")
    
    @staticmethod
    def encrypt_with_key(content: str, key: bytes) -> str:
        """
        Encrypt content using a pre-derived key (for performance).
        
        Args:
            content: Plain text to encrypt
            key: 32-byte AES key
            
        Returns:
            Base64 encoded encrypted content (iv + ciphertext)
        """
        if not content:
            return ""
        
        if not key or len(key) != CryptoManager.KEY_SIZE:
            raise ValueError(f"Key must be {CryptoManager.KEY_SIZE} bytes")
        
        try:
            iv = os.urandom(CryptoManager.IV_SIZE)
            
            content_bytes = content.encode('utf-8')
            padder = padding.PKCS7(CryptoManager.PADDING_BLOCK_SIZE).padder()
            padded_data = padder.update(content_bytes) + padder.finalize()
            
            cipher = Cipher(
                algorithms.AES(key),
                CryptoManager.AES_MODE(iv),
                backend=CryptoManager._get_backend()
            )
            encryptor = cipher.encryptor()
            ciphertext = encryptor.update(padded_data) + encryptor.finalize()
            
            combined = iv + ciphertext
            return base64.b64encode(combined).decode('utf-8')
            
        except Exception as e:
            raise ValueError(f"Encryption failed: {str(e)}")
    
    @staticmethod
    def decrypt_with_key(encrypted: str, key: bytes) -> str:
        """
        Decrypt content using a pre-derived key (for performance).
        
        Args:
            encrypted: Base64 encoded encrypted content (iv + ciphertext)
            key: 32-byte AES key
            
        Returns:
            Decrypted plain text
        """
        if not encrypted:
            return ""
        
        if not key or len(key) != CryptoManager.KEY_SIZE:
            raise ValueError(f"Key must be {CryptoManager.KEY_SIZE} bytes")
        
        try:
            raw = base64.b64decode(encrypted)
            
            if len(raw) < CryptoManager.IV_SIZE + 1:
                raise ValueError("Encrypted content too short")
            
            iv = raw[:CryptoManager.IV_SIZE]
            ciphertext = raw[CryptoManager.IV_SIZE:]
            
            cipher = Cipher(
                algorithms.AES(key),
                CryptoManager.AES_MODE(iv),
                backend=CryptoManager._get_backend()
            )
            decryptor = cipher.decryptor()
            padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
            
            unpadder = padding.PKCS7(CryptoManager.PADDING_BLOCK_SIZE).unpadder()
            plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
            
            return plaintext.decode('utf-8')
            
        except Exception as e:
            raise ValueError(f"Decryption failed: {str(e)}")
    
    @staticmethod
    def generate_key() -> bytes:
        """Generate a random 32-byte AES key."""
        return os.urandom(CryptoManager.KEY_SIZE)
    
    @staticmethod
    def key_to_base64(key: bytes) -> str:
        """Convert binary key to base64 string for storage."""
        return base64.b64encode(key).decode('utf-8')
    
    @staticmethod
    def key_from_base64(key_b64: str) -> bytes:
        """Convert base64 key string back to binary."""
        return base64.b64decode(key_b64)
    
    @staticmethod
    def quick_encrypt(content: str, password: str) -> str:
        """
        Quick encrypt - alias for encrypt().
        """
        return CryptoManager.encrypt(content, password)
    
    @staticmethod
    def quick_decrypt(encrypted: str, password: str) -> str:
        """
        Quick decrypt - alias for decrypt().
        """
        return CryptoManager.decrypt(encrypted, password)


# Import secrets for constant-time comparison
try:
    import secrets
except ImportError:
    # Fallback for older Python versions
    class _Secrets:
        @staticmethod
        def compare_digest(a: bytes, b: bytes) -> bool:
            """Simple constant-time comparison fallback"""
            if len(a) != len(b):
                return False
            result = 0
            for x, y in zip(a, b):
                result |= x ^ y
            return result == 0
    secrets = _Secrets()