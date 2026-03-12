#!/usr/bin/env python3
"""
Debug version of the app with extra logging
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app import app, init_db
    
    print("🔧 Debug Mode - Event Management System")
    print("=" * 50)
    
    # Test database initialization
    print("📊 Testing database...")
    try:
        init_db()
        print("✅ Database initialized successfully")
    except Exception as e:
        print(f"❌ Database error: {e}")
    
    # Test imports
    print("📦 Testing imports...")
    try:
        import sqlite3
        print("✅ SQLite available")
    except ImportError:
        print("❌ SQLite not available")
    
    try:
        import bcrypt
        print("✅ bcrypt available (secure hashing)")
    except ImportError:
        print("⚠️  bcrypt not available (using fallback)")
    
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv available")
    except ImportError:
        print("⚠️  python-dotenv not available")
    
    # Test routes
    print("🛣️  Testing routes...")
    with app.test_client() as client:
        # Test landing page
        response = client.get('/')
        print(f"✅ Landing page: {response.status_code}")
        
        # Test registration page
        response = client.get('/register')
        print(f"✅ Registration page: {response.status_code}")
        
        # Test login page
        response = client.get('/login')
        print(f"✅ Login page: {response.status_code}")
        
        # Test events page
        response = client.get('/events')
        print(f"✅ Events page: {response.status_code}")
    
    print("\n🚀 Starting server in debug mode...")
    print("📍 Open: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("💡 Try: pip install flask python-dotenv")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()