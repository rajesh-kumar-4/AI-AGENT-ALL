"""
AI-Agent Learning Project
Sample Python file to verify your Python development environment is ready.
"""

import sys
from pathlib import Path


def main():
    """Main entry point."""
    print("✓ Python Development Environment Setup Complete!")
    print(f"Python Version: {sys.version}")
    print(f"Python Executable: {sys.executable}")
    print(f"Project Root: {Path(__file__).parent}")
    print("\nYour virtual environment is ready for development!")


if __name__ == "__main__":
    main()
