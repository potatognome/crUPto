"""
Test: crUPto config loader resolves COLOURS from SHARED_CONFIG
Purpose: Ensure crUPto finds and loads COLOURS.json via canonical config pattern.
"""
import os
import pytest
from tUilKit.utils.config import ConfigLoader

def test_crupto_colour_config_resolution():
    # Use the canonical crUPto config
    config_path = os.path.abspath(os.path.join(os.getcwd(), ".projects_config", "crUPto_CONFIG.json"))
    assert os.path.exists(config_path), f"Config file not found: {config_path}"
    loader = ConfigLoader(verbose=True, config_path=config_path)
    # Should print verbose output for all path resolution
    try:
        colours_path = loader.get_config_file_path("COLOURS")
        print(f"COLOURS config resolved to: {colours_path}")
        assert os.path.exists(colours_path)
    except Exception as e:
        print(f"COLOURS config resolution failed: {e}")
        assert False, f"COLOURS config resolution failed: {e}"
    # Print SHARED_CONFIG for manual inspection
    print("SHARED_CONFIG:", loader.global_config.get("SHARED_CONFIG"))
