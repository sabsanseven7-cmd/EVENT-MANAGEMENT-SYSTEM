#!/usr/bin/env python3
"""
Error checking script for Event Management System
This will help identify and display any errors
"""

import sys
import traceback
import sqlite3
import os

def check_database():
    """Check database structure and content"""
    print("🔍 Checking Database...")
    try:
        if not os.path.exists('event.db'):
            print("❌ Database file 'event.db' does not exist")
            return False
        
        conn = sqlite3.connect('event.db')
        cursor = conn.cursor()
        
        # Check tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"✅ Found tables: {[table[0] for table in tables]}")
        
        # Check users table structure
        try:
            cursor.execute("PRAGMA table_info(users)")
            columns = cursor.fetchall()
            print(f"✅ Users table columns: {[col[1] for col in columns]}")
        except Exception as e:
            print(f"❌ Error checking users table: {e}")
        
        # Check if we can query users
        try:
            cursor.execute("SELECT COUNT(*) FROM users")
            count = cursor.fetchone()[0]
            print(f"✅ Users table has {count} records")
        except Exception as e:
            print(f"❌ Error querying users table: {e}")
        
        # Check events table
        try:
            cursor.execute("SELECT COUNT(*) FROM events")
            count = cursor.fetchone()[0]
            print(f"✅ Events table has {count} records")
        except Exception as e:
            print(f"❌ Error querying events table: {e}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def check_imports():
    """Check if all required modules can be imported"""
    print("\n📦 Checking Imports...")
    
    modules = [
        ('flask', 'Flask web framework'),
        ('sqlite3', 'SQLite database'),
        ('hashlib', 'Password hashing fallback'),
        ('os', 'Operating system interface'),
        ('datetime', 'Date and time handling')
    ]
    
    optional_modules = [
        ('bcrypt', 'Secure password hashing'),
        ('dotenv', 'Environment variables')
    ]
    
    all_good = True
    
    for module, description in modules:
        try:
            __import__(module)
            print(f"✅ {module} - {description}")
        except ImportError as e:
            print(f"❌ {module} - {description} - ERROR: {e}")
            all_good = False
    
    for module, description in optional_modules:
        try:
            __import__(module)
            print(f"✅ {module} - {description}")
        except ImportError:
            print(f"⚠️  {module} - {description} - Optional, using fallback")
    
    return all_good

def test_app_import():
    """Test if the app can be imported"""
    print("\n🚀 Testing App Import...")
    try:
        import app
        print("✅ App imported successfully")
        
        # Test database initialization
        app.init_db()
        print("✅ Database initialized successfully")
        
        return True
    except Exception as e:
        print(f"❌ App import failed: {e}")
        traceback.print_exc()
        return False

def test_registration_route():
    """Test registration route"""
    print("\n👤 Testing Registration Route...")
    try:
        import app
        with app.app.test_client() as client:
            # Test GET request
            response = client.get('/register')
            print(f"✅ GET /register: {response.status_code}")
            
            # Test POST request
            response = client.post('/register', data={
                'username': 'testuser123',
                'password': 'testpass123',
                'email': 'test@example.com'
            })
            print(f"✅ POST /register: {response.status_code}")
            
            if response.status_code == 302:
                print("✅ Registration successful (redirect)")
            elif response.status_code == 200:
                print("⚠️  Registration returned form (check for validation errors)")
            
        return True
    except Exception as e:
        print(f"❌ Registration test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all checks"""
    print("🔧 Event Management System - Error Checker")
    print("=" * 50)
    
    checks = [
        ("Imports", check_imports),
        ("Database", check_database),
        ("App Import", test_app_import),
        ("Registration", test_registration_route)
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ {name} check crashed: {e}")
            results.append((name, False))
    
    print("\n📊 Summary:")
    print("-" * 30)
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {name}")
    
    all_passed = all(result for _, result in results)
    if all_passed:
        print("\n🎉 All checks passed! Your app should work correctly.")
        print("🚀 Run: python app.py")
    else:
        print("\n⚠️  Some checks failed. See errors above.")
        print("💡 Try: python reset_database.py")

if __name__ == "__main__":
    main()