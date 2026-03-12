#!/usr/bin/env python3
"""
Quick fix for database lock issues
"""

import os
import time

def quick_fix():
    """Quick fix for database lock"""
    print("🚀 Quick Fix for Database Lock Issue")
    print("=" * 40)
    
    # Step 1: Remove lock files
    lock_files = ['event.db-wal', 'event.db-shm', 'event.db-journal']
    removed_files = []
    
    for lock_file in lock_files:
        if os.path.exists(lock_file):
            try:
                os.remove(lock_file)
                removed_files.append(lock_file)
                print(f"✅ Removed {lock_file}")
            except Exception as e:
                print(f"⚠️  Could not remove {lock_file}: {e}")
    
    if removed_files:
        print(f"🗑️  Removed {len(removed_files)} lock files")
    else:
        print("ℹ️  No lock files found")
    
    # Step 2: Wait a moment
    print("⏳ Waiting 2 seconds...")
    time.sleep(2)
    
    # Step 3: Test database
    try:
        import sqlite3
        conn = sqlite3.connect('event.db', timeout=10.0)
        conn.execute('SELECT COUNT(*) FROM sqlite_master')
        conn.close()
        print("✅ Database is accessible")
        
        print("\n🎉 Quick fix complete!")
        print("🚀 Try running: python app.py")
        
    except Exception as e:
        print(f"❌ Database still locked: {e}")
        print("\n💡 Try these solutions:")
        print("   1. Close ALL terminal windows")
        print("   2. Open a NEW terminal")
        print("   3. Run: python reset_database.py")

if __name__ == "__main__":
    quick_fix()