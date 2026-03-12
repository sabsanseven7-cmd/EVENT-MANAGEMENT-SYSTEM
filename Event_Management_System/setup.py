#!/usr/bin/env python3
"""
Setup script for Event Management System
"""

import os
import subprocess
import sys

def install_requirements():
    """Install required packages"""
    print("Installing requirements...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def create_env_file():
    """Create .env file from template if it doesn't exist"""
    if not os.path.exists('.env'):
        print("Creating .env file...")
        with open('.env.example', 'r') as template:
            content = template.read()
        
        with open('.env', 'w') as env_file:
            env_file.write(content)
        
        print("✅ .env file created. Please update it with your configuration.")
    else:
        print("✅ .env file already exists.")

def main():
    print("🚀 Setting up Event Management System...")
    
    try:
        install_requirements()
        create_env_file()
        
        print("\n✅ Setup complete!")
        print("\nNext steps:")
        print("1. Update .env file with your configuration")
        print("2. Run: python app.py")
        print("3. Open http://localhost:5000 in your browser")
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()