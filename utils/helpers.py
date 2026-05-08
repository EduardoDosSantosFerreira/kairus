"""Helper utilities for Kairus application"""

import os
import re
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any


def generate_unique_id() -> str:
    """Generate a unique ID for notes and folders"""
    return str(uuid.uuid4())[:8]


def sanitize_filename(filename: str) -> str:
    """
    Sanitize a string to be used as a filename
    Removes or replaces invalid characters
    """
    # Remove any path separators
    filename = filename.replace('/', '_').replace('\\', '_')
    # Remove other invalid characters
    filename = re.sub(r'[<>:"|?*]', '_', filename)
    # Remove leading/trailing spaces and dots
    filename = filename.strip('. ')
    # Limit length
    if len(filename) > 200:
        filename = filename[:200]
    # Return default if empty
    return filename if filename else "untitled"


def format_timestamp(timestamp: Optional[datetime] = None) -> str:
    """Format timestamp for display"""
    if timestamp is None:
        timestamp = datetime.now()
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")


def format_date_short(timestamp: datetime) -> str:
    """Format date in short format"""
    return timestamp.strftime("%d/%m/%Y")


def format_date_relative(timestamp: datetime) -> str:
    """Format date as relative time (e.g., '2 hours ago')"""
    now = datetime.now()
    diff = now - timestamp
    
    if diff.days > 365:
        return f"{diff.days // 365} year{'s' if diff.days // 365 > 1 else ''} ago"
    elif diff.days > 30:
        return f"{diff.days // 30} month{'s' if diff.days // 30 > 1 else ''} ago"
    elif diff.days > 0:
        return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
    elif diff.seconds > 3600:
        return f"{diff.seconds // 3600} hour{'s' if diff.seconds // 3600 > 1 else ''} ago"
    elif diff.seconds > 60:
        return f"{diff.seconds // 60} minute{'s' if diff.seconds // 60 > 1 else ''} ago"
    else:
        return "just now"


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to a maximum length"""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def is_valid_username(username: str) -> bool:
    """Validate username format"""
    if not username or len(username) < 3 or len(username) > 50:
        return False
    # Allow letters, numbers, underscores, dots
    if not re.match(r'^[a-zA-Z0-9_.]+$', username):
        return False
    return True


def is_valid_password(password: str) -> bool:
    """Validate password strength"""
    if not password or len(password) < 6:
        return False
    return True


def calculate_password_strength(password: str) -> Dict[str, Any]:
    """
    Calculate password strength and return details
    Returns dict with score (0-100) and feedback
    """
    score = 0
    feedback = []
    
    if len(password) >= 6:
        score += 20
    else:
        feedback.append("Use at least 6 characters")
    
    if len(password) >= 10:
        score += 20
    
    if any(c.isupper() for c in password):
        score += 20
    else:
        feedback.append("Add uppercase letters")
    
    if any(c.isdigit() for c in password):
        score += 20
    else:
        feedback.append("Add numbers")
    
    if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        score += 20
    else:
        feedback.append("Add special characters")
    
    # Determine strength level
    if score < 40:
        strength = "weak"
    elif score < 70:
        strength = "medium"
    else:
        strength = "strong"
    
    return {
        "score": score,
        "strength": strength,
        "feedback": feedback,
        "is_valid": score >= 40
    }


def ensure_directory(path: Path) -> Path:
    """Ensure a directory exists, create if not"""
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_file_size(path: Path) -> int:
    """Get file size in bytes"""
    if path.exists():
        return path.stat().st_size
    return 0


def format_file_size(size_bytes: int) -> str:
    """Format file size for display"""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"


def safe_read_file(path: Path, encoding: str = 'utf-8') -> Optional[str]:
    """Safely read a file, return None if error"""
    try:
        with open(path, 'r', encoding=encoding) as f:
            return f.read()
    except Exception:
        return None


def safe_write_file(path: Path, content: str, encoding: str = 'utf-8') -> bool:
    """Safely write to a file, return success status"""
    try:
        # Ensure parent directory exists
        path.parent.mkdir(parents=True, exist_ok=True)
        # Write to temp file first
        temp_path = path.with_suffix(path.suffix + '.tmp')
        with open(temp_path, 'w', encoding=encoding) as f:
            f.write(content)
        # Rename temp to actual file (atomic operation)
        temp_path.replace(path)
        return True
    except Exception:
        return False


def backup_file(path: Path, backup_dir: Optional[Path] = None) -> Optional[Path]:
    """Create a backup of a file"""
    try:
        if not path.exists():
            return None
        
        if backup_dir is None:
            backup_dir = path.parent / ".backups"
        
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = backup_dir / f"{path.stem}_{timestamp}{path.suffix}"
        
        import shutil
        shutil.copy2(path, backup_path)
        
        return backup_path
    except Exception:
        return None


def merge_dicts(base: Dict, updates: Dict) -> Dict:
    """Recursively merge two dictionaries"""
    result = base.copy()
    for key, value in updates.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_dicts(result[key], value)
        else:
            result[key] = value
    return result


def chunk_list(lst: List, chunk_size: int) -> List[List]:
    """Split a list into chunks of specified size"""
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def remove_duplicates(lst: List) -> List:
    """Remove duplicates while preserving order"""
    seen = set()
    return [x for x in lst if not (x in seen or seen.add(x))]


def get_extension(filename: str) -> str:
    """Get file extension from filename"""
    return Path(filename).suffix.lower()


def has_extension(filename: str, extensions: List[str]) -> bool:
    """Check if filename has any of the given extensions"""
    ext = get_extension(filename)
    return ext in extensions


def create_backup_name(original_name: str) -> str:
    """Create a backup filename with timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    name_parts = original_name.rsplit('.', 1)
    if len(name_parts) == 2:
        return f"{name_parts[0]}_{timestamp}.{name_parts[1]}"
    else:
        return f"{original_name}_{timestamp}"


def is_text_content(content: str) -> bool:
    """Check if content appears to be plain text"""
    if not content:
        return True
    # Check for null bytes (binary content)
    if '\x00' in content:
        return False
    # Check if most characters are printable
    printable_ratio = sum(1 for c in content if c.isprintable() or c in '\n\r\t') / len(content)
    return printable_ratio > 0.9