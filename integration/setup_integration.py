"""
Setup script for XAgent integration into L3AGI
"""

import os
import subprocess
import sys
from pathlib import Path

def get_project_root():
    """Get the root directory of the project"""
    return Path(__file__).parent.parent

def install_requirements():
    """Install required packages"""
    requirements = [
        "langchain",
        "langsmith",
        "openai",
        "aiohttp",
        "pyyaml",
        "asyncio"
    ]
    
    for package in requirements:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        except subprocess.CalledProcessError:
            print(f"Warning: Could not install {package}")

def setup_environment():
    """Set up environment variables"""
    project_root = get_project_root()
    
    env_vars = {
        "XAGENT_HOME": str(project_root / "XAgent"),
        "L3AGI_HOME": str(project_root / "team_of_ai_agents"),
        "PYTHONPATH": f"{os.getenv('PYTHONPATH', '')}:{project_root}"
    }
    
    for key, value in env_vars.items():
        os.environ[key] = value
        print(f"Set {key}={value}")

def verify_installation():
    """Verify that everything is set up correctly"""
    print("Verifying installation...")
    
    project_root = get_project_root()
    
    # Check XAgent
    xagent_path = project_root / "XAgent"
    if not xagent_path.exists():
        raise FileNotFoundError(f"XAgent not found at: {xagent_path}")
    
    # Check L3AGI
    l3agi_path = project_root / "team-of-ai-agents"
    if not l3agi_path.exists():
        raise FileNotFoundError(f"L3AGI not found at: {l3agi_path}")
    
    # Check required files
    required_xagent_files = [
        "run.py",
        "XAgent/__init__.py",
        "XAgent/core.py"
    ]
    
    for file in required_xagent_files:
        file_path = xagent_path / file
        if not file_path.exists():
            print(f"Warning: XAgent file not found: {file_path}")
    
    print("XAgent found")
    print("L3AGI framework found")
    print("Environment variables set")
    print("Installation complete")

if __name__ == "__main__":
    print("Setting up XAgent integration...")
    install_requirements()
    setup_environment()
    verify_installation()
    print("\nRun 'python test.py' to test the integration")