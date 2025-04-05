#!/usr/bin/env python3
import subprocess
import sys
import os


def check_python_version():
    """Check if Python version is at least 3.6"""
    if sys.version_info < (3, 6):
        print("Error: Python 3.6 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    return True


def install_dependencies():
    """Install required packages using pip"""
    try:
        print("Installing required packages...")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("All dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("Error: Failed to install dependencies")
        return False


def create_output_directory():
    """Create output directory if it doesn't exist"""
    if not os.path.exists("output"):
        try:
            os.makedirs("output")
            print("Created output directory")
        except OSError:
            print("Error: Could not create output directory")
            return False
    return True


def main():
    print("WhatsApp Chat Analyzer - Installation Helper")
    print("===========================================")

    if not check_python_version():
        return

    if not install_dependencies():
        return

    if not create_output_directory():
        return

    print("\nInstallation complete!")
    print("\nTo run the basic analyzer:")
    print("  python whatsapp_analyzer.py")
    print("\nTo run the advanced analyzer with visualizations:")
    print("  python deep_whatsapp_analyzer.py")
    print("\nFor more information, check the documentation in the docs/ directory")


if __name__ == "__main__":
    main()
