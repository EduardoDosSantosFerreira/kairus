#!/usr/bin/env python3
"""Clear Python Cache Files - Remove all __pycache__ directories and .pyc files"""

import os
import shutil
from pathlib import Path
from typing import List, Tuple


class PythonCacheCleaner:
    """Removes all Python cache files and directories"""
    
    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir)
        self.deleted_dirs = []
        self.deleted_files = []
        self.skipped = []
        
    def find_cache_dirs(self) -> List[Path]:
        """Find all __pycache__ directories"""
        cache_dirs = []
        for path in self.root_dir.rglob("__pycache__"):
            if path.is_dir():
                cache_dirs.append(path)
        return cache_dirs
    
    def find_pyc_files(self) -> List[Path]:
        """Find all .pyc files"""
        pyc_files = []
        for path in self.root_dir.rglob("*.pyc"):
            if path.is_file():
                pyc_files.append(path)
        return pyc_files
    
    def find_pyo_files(self) -> List[Path]:
        """Find all .pyo files"""
        pyo_files = []
        for path in self.root_dir.rglob("*.pyo"):
            if path.is_file():
                pyo_files.append(path)
        return pyo_files
    
    def get_stats(self) -> Tuple[int, int, int]:
        """Get statistics about cache files"""
        cache_dirs = self.find_cache_dirs()
        pyc_files = self.find_pyc_files()
        pyo_files = self.find_pyo_files()
        return len(cache_dirs), len(pyc_files), len(pyo_files)
    
    def format_size(self, size_bytes: int) -> str:
        """Format bytes to human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"
    
    def get_total_size(self) -> int:
        """Calculate total size of all cache files"""
        total_size = 0
        
        for cache_dir in self.find_cache_dirs():
            for file in cache_dir.rglob("*"):
                if file.is_file():
                    total_size += file.stat().st_size
        
        for pyc_file in self.find_pyc_files():
            total_size += pyc_file.stat().st_size
        
        for pyo_file in self.find_pyo_files():
            total_size += pyo_file.stat().st_size
        
        return total_size
    
    def show_stats(self):
        """Display statistics before deletion"""
        cache_dirs, pyc_files, pyo_files = self.get_stats()
        total_size = self.get_total_size()
        
        print("\n" + "=" * 60)
        print("📊 PYTHON CACHE STATISTICS")
        print("=" * 60)
        print(f"📁 Root directory: {self.root_dir.absolute()}")
        print(f"📁 __pycache__ directories: {cache_dirs}")
        print(f"📄 .pyc files: {pyc_files}")
        print(f"📄 .pyo files: {pyo_files}")
        print(f"💾 Total cache size: {self.format_size(total_size)}")
        
        if cache_dirs > 0:
            print("\n📋 __pycache__ directories found:")
            for i, cache_dir in enumerate(self.find_cache_dirs()[:10]):
                print(f"  {i+1}. {cache_dir.relative_to(self.root_dir)}")
            if cache_dirs > 10:
                print(f"  ... and {cache_dirs - 10} more")
    
    def dry_run(self):
        """Show what would be deleted without actually deleting"""
        cache_dirs = self.find_cache_dirs()
        pyc_files = self.find_pyc_files()
        
        print("\n" + "=" * 60)
        print("🔍 DRY RUN - Files that would be deleted")
        print("=" * 60)
        
        if cache_dirs:
            print(f"\n📁 __pycache__ directories ({len(cache_dirs)}):")
            for cache_dir in cache_dirs:
                print(f"  • {cache_dir.relative_to(self.root_dir)}")
        
        if pyc_files:
            print(f"\n📄 .pyc files ({len(pyc_files)}):")
            for pyc_file in pyc_files[:20]:
                print(f"  • {pyc_file.relative_to(self.root_dir)}")
            if len(pyc_files) > 20:
                print(f"  ... and {len(pyc_files) - 20} more")
        
        if not cache_dirs and not pyc_files:
            print("\n✅ No cache files found!")
    
    def clear_cache(self, confirm: bool = True) -> bool:
        """Clear all Python cache files"""
        cache_dirs = self.find_cache_dirs()
        pyc_files = self.find_pyc_files()
        pyo_files = self.find_pyo_files()
        
        if not cache_dirs and not pyc_files and not pyo_files:
            print("\n✅ No cache files found. Nothing to delete.")
            return True
        
        # Show stats before deletion
        self.show_stats()
        
        if confirm:
            print("\n⚠️  WARNING: This will delete ALL Python cache files!")
            response = input("\nType 'CLEAR' to confirm: ")
            if response != "CLEAR":
                print("\n❌ Cancelled. No files were deleted.")
                return False
        
        # Delete __pycache__ directories
        print("\n🗑️  Deleting __pycache__ directories...")
        for cache_dir in cache_dirs:
            try:
                shutil.rmtree(cache_dir)
                self.deleted_dirs.append(cache_dir)
                print(f"  ✓ Deleted: {cache_dir.relative_to(self.root_dir)}")
            except Exception as e:
                print(f"  ✗ Error deleting {cache_dir}: {e}")
                self.skipped.append(cache_dir)
        
        # Delete .pyc files
        print("\n🗑️  Deleting .pyc files...")
        for pyc_file in pyc_files:
            try:
                pyc_file.unlink()
                self.deleted_files.append(pyc_file)
                print(f"  ✓ Deleted: {pyc_file.relative_to(self.root_dir)}")
            except Exception as e:
                print(f"  ✗ Error deleting {pyc_file}: {e}")
                self.skipped.append(pyc_file)
        
        # Delete .pyo files
        if pyo_files:
            print("\n🗑️  Deleting .pyo files...")
            for pyo_file in pyo_files:
                try:
                    pyo_file.unlink()
                    self.deleted_files.append(pyo_file)
                    print(f"  ✓ Deleted: {pyo_file.relative_to(self.root_dir)}")
                except Exception as e:
                    print(f"  ✗ Error deleting {pyo_file}: {e}")
                    self.skipped.append(pyo_file)
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 CLEANUP SUMMARY")
        print("=" * 60)
        print(f"✅ Directories deleted: {len(self.deleted_dirs)}")
        print(f"✅ Files deleted: {len(self.deleted_files)}")
        if self.skipped:
            print(f"⚠️  Skipped: {len(self.skipped)}")
        
        return True
    
    def clear_cache_force(self) -> bool:
        """Clear cache without confirmation"""
        return self.clear_cache(confirm=False)


def interactive_menu():
    """Display interactive menu for cache cleanup"""
    cleaner = PythonCacheCleaner()
    
    while True:
        print("\n" + "=" * 60)
        print("🧹 KAIRUS - PYTHON CACHE CLEANER")
        print("=" * 60)
        print("\nOptions:")
        print("  1. 📊 Show cache statistics")
        print("  2. 🔍 Dry run (preview what will be deleted)")
        print("  3. 🗑️  Clear all cache files (with confirmation)")
        print("  4. ⚡ Force clear all cache files (no confirmation)")
        print("  5. 🚪 Exit")
        
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == '1':
            cleaner.show_stats()
            input("\nPress Enter to continue...")
        
        elif choice == '2':
            cleaner.dry_run()
            input("\nPress Enter to continue...")
        
        elif choice == '3':
            if cleaner.clear_cache():
                print("\n✅ Cache cleanup completed successfully!")
            input("\nPress Enter to continue...")
        
        elif choice == '4':
            print("\n⚠️  Force mode - skipping confirmation")
            if cleaner.clear_cache_force():
                print("\n✅ Cache cleanup completed successfully!")
            input("\nPress Enter to continue...")
        
        elif choice == '5':
            print("\n👋 Goodbye!")
            break
        
        else:
            print("\n❌ Invalid option. Please try again.")


def main():
    """Main entry point"""
    import sys
    
    # Check command line arguments
    if len(sys.argv) > 1:
        cleaner = PythonCacheCleaner()
        
        if sys.argv[1] == "--stats":
            cleaner.show_stats()
            sys.exit(0)
        
        elif sys.argv[1] == "--dry-run":
            cleaner.dry_run()
            sys.exit(0)
        
        elif sys.argv[1] == "--force":
            print("⚠️  Force mode - clearing all cache files...")
            success = cleaner.clear_cache_force()
            sys.exit(0 if success else 1)
        
        elif sys.argv[1] == "--help":
            print("\n🧹 Python Cache Cleaner - Usage:")
            print("=" * 50)
            print("  python clear_cache.py              - Interactive menu")
            print("  python clear_cache.py --stats      - Show cache statistics")
            print("  python clear_cache.py --dry-run    - Preview what will be deleted")
            print("  python clear_cache.py --force      - Clear all cache (no confirmation)")
            print("  python clear_cache.py --help       - Show this help message")
            sys.exit(0)
        
        else:
            print(f"❌ Unknown argument: {sys.argv[1]}")
            print("Use --help for usage information")
            sys.exit(1)
    
    # Interactive menu (default)
    interactive_menu()


if __name__ == "__main__":
    main()