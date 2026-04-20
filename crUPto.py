#!/usr/bin/env python
"""
crUPto.py
Convenience entry point for running crUPto from the project root.
Handles module path setup automatically.
"""

import sys
import os
import time
from pathlib import Path
from datetime import datetime

# Add src to path so crUPto can be imported as a module
project_root = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(project_root, "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Patch tUilKit factories to use the correct config loader before any tUilKit factory is used
from tUilKit.utils.config import ConfigLoader
import tUilKit.factories
CONFIG_ROOT = os.path.abspath(os.path.join(project_root, '..', '..', '.projects_config', 'crUPto_CONFIG.json'))
tUilKit.factories._config_loader = ConfigLoader(config_path=CONFIG_ROOT)

os.system("cls")
starttime = datetime.now()
username = os.getlogin()
current_path = os.getcwd()
print("=== Starting crUPto Entrypoint ===")
print(f"Date/Time: {starttime.strftime('%Y-%m-%d %H:%M:%S')}")
print("User:", username)
print("Working Directory:", current_path)  

print("Command:", " ".join(sys.argv))

# Always launch the CLI menu when running crUPto.py
import crUPto.main
crUPto.main.startup()
print("=== Running crUPto Entrypoint ===")


