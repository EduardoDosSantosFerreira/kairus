#!/usr/bin/env python3
"""Reset Database Script - Remove all data and start fresh"""

import os
import shutil
import sys
from pathlib import Path
from datetime import datetime


class DatabaseResetter:
    """Handles database reset operations"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.confirmation_word = "DELETE ALL"
        
    def get_directory_size(self) -> int:
        """Calculate total size of data directory in bytes"""
        total_size = 0
        if self.data_dir.exists():
            for root, dirs, files in os.walk(self.data_dir):
                for file in files:
                    file_path = Path(root) / file
                    total_size += file_path.stat().st_size
        return total_size
    
    def format_size(self, size_bytes: int) -> str:
        """Format bytes to human readable format"""
        if size_bytes == 0:
            return "0 B"
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"
    
    def list_files(self) -> list:
        """List all files that will be deleted"""
        files = []
        if self.data_dir.exists():
            for root, dirs, file_names in os.walk(self.data_dir):
                for file_name in file_names:
                    file_path = Path(root) / file_name
                    files.append(file_path)
        return files
    
    def show_stats(self):
        """Display statistics before deletion"""
        if not self.data_dir.exists():
            print("\n📁 No data directory found.")
            return
        
        files = self.list_files()
        total_size = self.get_directory_size()
        
        print("\n" + "=" * 60)
        print("📊 DATABASE STATISTICS")
        print("=" * 60)
        print(f"📁 Directory: {self.data_dir.absolute()}")
        print(f"📄 Files to delete: {len(files)}")
        print(f"💾 Total size: {self.format_size(total_size)}")
        
        if files and len(files) <= 15:
            print("\n📋 Files to be deleted:")
            for file in files:
                size = self.format_size(file.stat().st_size)
                print(f"  • {file.parent.name}/{file.name} ({size})")
        elif files:
            print(f"\n📋 Showing first 10 of {len(files)} files:")
            for file in files[:10]:
                size = self.format_size(file.stat().st_size)
                print(f"  • {file.parent.name}/{file.name} ({size})")
            print(f"  ... and {len(files) - 10} more files")
    
    def reset(self) -> bool:
        """Execute the database reset - DELETE EVERYTHING"""
        if not self.data_dir.exists():
            print("\n📁 No data directory found. Nothing to delete.")
            return True
        
        # Show statistics
        self.show_stats()
        
        # Confirm deletion
        print("\n⚠️  WARNING: This will DELETE your ENTIRE DATABASE!")
        print("   • All user accounts")
        print("   • All folders")
        print("   • All notes (including Vault)")
        print("\n⚠️  This action CANNOT be undone!")
        
        confirm = input(f"\nType '{self.confirmation_word}' to confirm: ")
        
        if confirm != self.confirmation_word:
            print("\n❌ Cancelled. No data was deleted.")
            return False
        
        # Execute deletion
        try:
            print(f"\n🗑️  Deleting {self.data_dir}...")
            shutil.rmtree(self.data_dir)
            print("\n✅ DATABASE DELETED SUCCESSFULLY!")
            return True
        except Exception as e:
            print(f"\n❌ Error deleting database: {e}")
            return False
    
    def reset_force(self) -> bool:
        """Force reset without confirmation"""
        if not self.data_dir.exists():
            print("No data directory found.")
            return True
        
        try:
            print(f"Deleting {self.data_dir}...")
            shutil.rmtree(self.data_dir)
            print("✅ Database deleted successfully!")
            return True
        except Exception as e:
            print(f"❌ Error deleting database: {e}")
            return False


def main():
    """Main entry point"""
    resetter = DatabaseResetter()
    
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--force":
            print("⚠️  Force reset mode - skipping confirmation")
            success = resetter.reset_force()
            sys.exit(0 if success else 1)
        
        elif sys.argv[1] == "--stats":
            resetter.show_stats()
            sys.exit(0)
        
        elif sys.argv[1] == "--help":
            print("\n🔧 KAIRUS Database Reset Tool - Usage:")
            print("=" * 50)
            print("  python reset_db.py              - Interactive reset with confirmation")
            print("  python reset_db.py --stats      - Show database statistics")
            print("  python reset_db.py --force      - Force reset (no confirmation)")
            print("  python reset_db.py --help       - Show this help message")
            sys.exit(0)
        
        else:
            print(f"❌ Unknown argument: {sys.argv[1]}")
            print("Use --help for usage information")
            sys.exit(1)
    
    # Interactive reset (default)
    print("=" * 60)
    print("🔧 KAIRUS - DATABASE RESET TOOL")
    print("=" * 60)
    
    success = resetter.reset()
    
    if success:
        print("\n" + "=" * 60)
        print("✅ DATABASE RESET COMPLETE!")
        print("=" * 60)
        print("\nPlease restart the application.")
        print("A new database will be created automatically.")
    
    print()


if __name__ == "__main__":
    main()