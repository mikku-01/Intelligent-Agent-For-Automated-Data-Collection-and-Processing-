"""
Intelligent Agent Project - Setup and Installation Script

This script helps set up the project environment and installs dependencies.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a shell command and handle errors."""
    print(f"\n{'='*60}")
    print(f"⚙️  {description}")
    print(f"{'='*60}")
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e.stderr}")
        return False

def create_directories():
    """Create necessary project directories."""
    directories = [
        'logs',
        'data/raw',
        'data/processed',
        'tests',
        'agents/specialized',
        'modules/collector',
        'modules/processor',
        'modules/storage',
        'config',
        'docs'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✓ Created directory: {directory}")

def main():
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║   Intelligent Agent for Data Collection & Processing     ║
    ║                    Setup Script                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Create project directories
    print("\n📁 Creating project directories...")
    create_directories()
    
    # Check Python version
    print(f"\n🐍 Python version: {sys.version}")
    
    # Create .env file if it doesn't exist
    if not os.path.exists('.env'):
        print("\n📝 Creating .env file from template...")
        if os.path.exists('.env.example'):
            import shutil
            shutil.copy('.env.example', '.env')
            print("✓ .env file created. Please edit it with your API keys.")
        else:
            print("⚠️  No .env.example found. Please create .env manually.")
    
    print("\n" + "="*60)
    print("✅ Setup complete!")
    print("="*60)
    print("\nNext steps:")
    print("1. Edit the .env file with your API keys")
    print("2. Run: pip install -r requirements.txt")
    print("3. Run: python -m spacy download en_core_web_sm")
    print("4. Run: python test_run.py")
    print("\n")

if __name__ == "__main__":
    main()