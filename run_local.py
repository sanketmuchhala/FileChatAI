#!/usr/bin/env python3
"""
Local runner script for RAG Document Chatbot
This script helps set up and run the application locally with proper configuration.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required.")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import streamlit
        import google.generativeai
        import openai
        import numpy
        import PyPDF2
        import docx
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r local_requirements.txt")
        return False

def check_env_variables():
    """Check if required environment variables are set."""
    deepseek_key = os.getenv("DEEPSEEK_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")
    
    if not deepseek_key:
        print("❌ DEEPSEEK_API_KEY environment variable is not set")
    else:
        print("✅ DEEPSEEK_API_KEY is set")
    
    if not gemini_key:
        print("❌ GEMINI_API_KEY environment variable is not set")
    else:
        print("✅ GEMINI_API_KEY is set")
    
    if not deepseek_key or not gemini_key:
        print("\nTo set environment variables:")
        print("1. Create a .env file with your API keys, or")
        print("2. Set them in your terminal:")
        print("   export DEEPSEEK_API_KEY='your_key_here'")
        print("   export GEMINI_API_KEY='your_key_here'")
        return False
    
    return True

def load_env_file():
    """Load environment variables from .env file if it exists."""
    env_file = Path(".env")
    if env_file.exists():
        print("📄 Loading environment variables from .env file...")
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip().strip('"').strip("'")
        return True
    return False

def main():
    """Main function to run the application."""
    print("🚀 RAG Document Chatbot - Local Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Load .env file if exists
    load_env_file()
    
    # Check dependencies
    if not check_dependencies():
        print("\n💡 To install dependencies:")
        print("pip install -r local_requirements.txt")
        sys.exit(1)
    
    # Check environment variables
    if not check_env_variables():
        sys.exit(1)
    
    print("\n✅ All checks passed! Starting the application...")
    print("🌐 The app will open in your default browser")
    print("🔗 URL: http://localhost:8501")
    print("\n⏹️  Press Ctrl+C to stop the application")
    print("=" * 50)
    
    try:
        # Run Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ], check=True)
    except KeyboardInterrupt:
        print("\n\n👋 Application stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error running application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()