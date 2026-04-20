"""
Test: crUPto config loader resolves TUILKIT root
Purpose: Ensure crUPto config exposes and resolves the TUILKIT root correctly.
"""
import os
import pytest
from tUilKit.utils.config import ConfigLoader

def test_crupto_tuilkit_root_resolution():
    # Use the canonical crUPto config
    config_path = os.path.abspath(os.path.join(os.getcwd(), ".projects_config", "crUPto_CONFIG.json"))
    assert os.path.exists(config_path), f"Config file not found: {config_path}"
    loader = ConfigLoader(verbose=True, config_path=config_path)
    roots = loader.global_config.get("ROOTS", {})
    tuilkit_root = roots.get("TUILKIT")
    print(f"TUILKIT root: {tuilkit_root}")
    assert tuilkit_root, "TUILKIT root not found in config."
    assert os.path.exists(tuilkit_root), f"TUILKIT root path does not exist: {tuilkit_root}"
