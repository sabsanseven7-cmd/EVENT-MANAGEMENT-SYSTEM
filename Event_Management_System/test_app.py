#!/usr/bin/env python3
"""
Test script for Event Management System
Tests all routes and functionality
"""

import requests
import json
import sys
from datetime import datetime, timedelta

BASE_URL = "http://localhost:5000"

def test_route(url, method="GET", data=None, session=None):
    """Test a route and return response"""
    try:
        if method == "GET":
            response = requests.get(f"{BASE_URL}{url}", cookies=session)
        elif method == "POST":
            response = requests.post(f"{BASE_URL}{url}", data=data, cookies=session)
        
        return {
            "status": response.status_code,
            "success": response.status_code < 400,
            "url": url,
            "method": method
        }
    except Exception as e:
        return {
            "status": "ERROR",
            "success": False,
            "url": url,
            "method": method,
            "error": str(e)
        }

def run_tests():
    """Run all tests"""
    print("🧪 Testing Event Management System")
    print("=" * 50)
    
    tests = []
    
    # Test public routes
    print("\n📄 Testing Public Pages:")
    tests.append(test_route("/"))  # Landing page
    tests.append(test_route("/login"))  # Login page
    tests.append(test_route("/register"))  # Register page
    tests.append(test_route("/events"))  # Events page (should work without login)
    
    # Test registration
    print("\n👤 Testing Registration:")
    reg_data = {
        "username": f"testuser_{datetime.now().strftime('%H%M%S')}",
        "email": f"test_{datetime.now().strftime('%H%M%S')}@example.com",
        "password": "testpass123"
    }
    tests.append(test_route("/register", "POST", reg_data))
    
    # Test login
    print("\n🔐 Testing Login:")
    login_data = {
        "username": reg_data["username"],
        "password": reg_data["password"],
        "role": "user"
    }
    tests.append(test_route("/login", "POST", login_data))
    
    # Test admin login
    print("\n👨‍💼 Testing Admin Login:")
    admin_data = {
        "username": "admin",
        "password": "admin123",
        "role": "admin"
    }
    tests.append(test_route("/login", "POST", admin_data))
    
    # Test chatbot
    print("\n🤖 Testing Chatbot:")
    chat_data = {"message": "hello"}
    try:
        response = requests.post(f"{BASE_URL}/chat", 
                               json=chat_data,
                               headers={"Content-Type": "application/json"})
        tests.append({
            "status": response.status_code,
            "success": response.status_code == 200,
            "url": "/chat",
            "method": "POST"
        })
    except Exception as e:
        tests.append({
            "status": "ERROR",
            "success": False,
            "url": "/chat",
            "method": "POST",
            "error": str(e)
        })
    
    # Print results
    print("\n📊 Test Results:")
    print("-" * 50)
    
    passed = 0
    failed = 0
    
    for test in tests:
        status = "✅ PASS" if test["success"] else "❌ FAIL"
        print(f"{status} {test['method']} {test['url']} - Status: {test['status']}")
        
        if test["success"]:
            passed += 1
        else:
            failed += 1
            if "error" in test:
                print(f"   Error: {test['error']}")
    
    print(f"\n📈 Summary: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed! Your application is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the server is running: python app.py")

if __name__ == "__main__":
    run_tests()