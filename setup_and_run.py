#!/usr/bin/env python3
"""
Simple setup and run script for RAG Document Chatbot
Handles common installation and running issues automatically.
"""

import os
import sys
import subprocess
import importlib.util

def install_package(package_name):
    """Install a package using pip."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        return True
    except subprocess.CalledProcessError:
        return False

def check_and_install_packages():
    """Check if packages are installed, install if missing."""
    required_packages = {
        'streamlit': 'streamlit',
        'google.generativeai': 'google-generativeai', 
        'openai': 'openai',
        'numpy': 'numpy',
        'PyPDF2': 'PyPDF2',
        'docx': 'python-docx'
    }
    
    missing_packages = []
    
    for import_name, pip_name in required_packages.items():
        if importlib.util.find_spec(import_name) is None:
            missing_packages.append(pip_name)
    
    if missing_packages:
        print(f"Installing missing packages: {', '.join(missing_packages)}")
        for package in missing_packages:
            print(f"Installing {package}...")
            if not install_package(package):
                print(f"Failed to install {package}")
                return False
        print("All packages installed successfully!")
    else:
        print("All required packages are already installed.")
    
    return True

def check_env_variables():
    """Check if environment variables are set."""
    deepseek_key = os.getenv("DEEPSEEK_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")
    
    if not deepseek_key or not gemini_key:
        print("\n⚠️  API Keys Missing!")
        print("You need to set your API keys as environment variables:")
        print()
        if not deepseek_key:
            print("Missing: DEEPSEEK_API_KEY")
        if not gemini_key:
            print("Missing: GEMINI_API_KEY")
        print()
        print("Quick setup options:")
        print("1. Create a .env file in this folder with:")
        print("   DEEPSEEK_API_KEY=your_deepseek_key")
        print("   GEMINI_API_KEY=your_gemini_key")
        print()
        print("2. Or set them in your terminal:")
        print("   export DEEPSEEK_API_KEY='your_key'")
        print("   export GEMINI_API_KEY='your_key'")
        print()
        return False
    
    return True

def load_env_file():
    """Load .env file if it exists."""
    if os.path.exists('.env'):
        print("Loading .env file...")
        with open('.env', 'r') as f:
            for line in f:
                line = line.strip()
                if line and '=' in line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip().strip('"').strip("'")
        return True
    return False

def run_streamlit():
    """Run streamlit with fallback methods."""
    print("Starting RAG Document Chatbot...")
    print("The app will open in your browser at: http://localhost:8501")
    print("Press Ctrl+C to stop")
    print("-" * 50)
    
    # Try different ways to run streamlit (using port 8501 to avoid conflicts)
    methods = [
        [sys.executable, "-m", "streamlit", "run", "app.py", "--server.port", "8501"],
        ["streamlit", "run", "app.py", "--server.port", "8501"],
        ["python", "-m", "streamlit", "run", "app.py", "--server.port", "8501"],
        ["python3", "-m", "streamlit", "run", "app.py", "--server.port", "8501"]
    ]
    
    for method in methods:
        try:
            subprocess.run(method, check=True)
            break
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
    else:
        print("Could not start streamlit. Please try manually:")
        print("python -m streamlit run app.py")

def main():
    """Main function."""
    print("RAG Document Chatbot - Auto Setup & Run")
    print("=" * 50)
    
    # Load environment file
    load_env_file()
    
    # Check and install packages
    if not check_and_install_packages():
        print("Failed to install required packages.")
        sys.exit(1)
    
    # Check environment variables
    if not check_env_variables():
        sys.exit(1)
    
    print("✅ Setup complete! Starting application...")
    print()
    
    try:
        run_streamlit()
    except KeyboardInterrupt:
        print("\n\nApplication stopped.")

if __name__ == "__main__":
    main()