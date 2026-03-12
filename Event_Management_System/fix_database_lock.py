#!/usr/bin/env python3
"""
Fix database lock issues for Event Management System
"""

import os
import sqlite3
import time
import sys

def fix_database_lock():
    """Fix database lock issues"""
    print("🔧 Fixing Database Lock Issues...")
    
    # Check if database exists
    if not os.path.exists('event.db'):
        print("❌ Database file 'event.db' not found")
        return False
    
    # Check for WAL and SHM files (SQLite lock files)
    wal_file = 'event.db-wal'
    shm_file = 'event.db-shm'
    
    lock_files_exist = False
    if os.path.exists(wal_file):
        print(f"🔍 Found WAL file: {wal_file}")
        lock_files_exist = True
    
    if os.path.exists(shm_file):
        print(f"🔍 Found SHM file: {shm_file}")
        lock_files_exist = True
    
    if lock_files_exist:
        print("⚠️  Lock files detected. Attempting to clear...")
        
        # Try to connect and close properly to clear locks
        try:
            conn = sqlite3.connect('event.db', timeout=30.0)
            conn.execute('PRAGMA journal_mode=DELETE;')  # Switch to DELETE mode
            conn.execute('PRAGMA journal_mode=WAL;')     # Switch back to WAL
            conn.close()
            print("✅ Database connection cleared")
        except Exception as e:
            print(f"⚠️  Could not clear connection: {e}")
        
        # Wait a moment
        time.sleep(2)
        
        # Try to remove lock files if they still exist
        for lock_file in [wal_file, shm_file]:
            if os.path.exists(lock_file):
                try:
                    os.remove(lock_file)
                    print(f"✅ Removed {lock_file}")
                except Exception as e:
                    print(f"⚠️  Could not remove {lock_file}: {e}")
    
    # Test database connection
    try:
        conn = sqlite3.connect('event.db', timeout=20.0)
        conn.execute('PRAGMA journal_mode=WAL;')
        conn.execute('SELECT COUNT(*) FROM users')
        conn.close()
        print("✅ Database connection test successful")
        return True
    except Exception as e:
        print(f"❌ Database connection test failed: {e}")
        return False

def check_running_processes():
    """Check for running Python processes that might be using the database"""
    print("\n🔍 Checking for running processes...")
    
    try:
        import psutil
        python_processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if proc.info['name'] and 'python' in proc.info['name'].lower():
                    cmdline = proc.info['cmdline']
                    if cmdline and any('app.py' in arg for arg in cmdline):
                        python_processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        if python_processes:
            print("⚠️  Found running Python processes that might be using the database:")
            for proc in python_processes:
                print(f"   PID: {proc['pid']}, Command: {' '.join(proc['cmdline'])}")
            print("💡 Consider stopping these processes before running the app")
        else:
            print("✅ No conflicting Python processes found")
            
    except ImportError:
        print("⚠️  psutil not available, cannot check processes")
        print("💡 Manually check if any Python processes are running: Ctrl+C any running app.py")

def main():
    """Main function"""
    print("🔧 Database Lock Fixer - Event Management System")
    print("=" * 50)
    
    check_running_processes()
    
    if fix_database_lock():
        print("\n🎉 Database lock issues resolved!")
        print("🚀 You can now run: python app.py")
    else:
        print("\n❌ Could not resolve database lock issues")
        print("💡 Try these solutions:")
        print("   1. Close all running Python processes")
        print("   2. Restart your terminal/command prompt")
        print("   3. Run: python reset_database.py")
        print("   4. Reboot your computer if necessary")

if __name__ == "__main__":
    main()