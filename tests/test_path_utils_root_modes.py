import os
from pathlib import Path
import sys


SRC_PATH = Path(__file__).resolve().parents[1] / "src"
TUILKIT_SRC = Path(__file__).resolve().parents[3] / "Core" / "tUilKit" / "src"
for path in [SRC_PATH, TUILKIT_SRC]:
    path_str = str(path)
    if path_str not in sys.path:
        sys.path.insert(0, path_str)

from crUPto.utils.path_utils import resolve_path


def _sample_config(tmp_path):
    return {
        "ROOTS": {
            "PROJECT": str(tmp_path / "Applications" / "crUPto"),
            "WORKSPACE": str(tmp_path),
            "TUILKIT": str(tmp_path / "Core" / "tUilKit"),
        },
        "PATHS": {
            "INPUT_DATA": "data/input",
            "OUTPUT_DATA": "data/output",
            "CONFIG": "config",
        },
    }


def test_resolve_path_uses_project_root_by_default(tmp_path):
    config = _sample_config(tmp_path)
    root_modes = {}

    resolved = resolve_path("CONFIG", config, root_modes)

    assert resolved == os.path.join(config["ROOTS"]["PROJECT"], "config")


def test_resolve_path_switches_to_workspace_root(tmp_path):
    config = _sample_config(tmp_path)
    root_modes = {"OUTPUT_DATA": "workspace"}

    resolved = resolve_path("OUTPUT_DATA", config, root_modes)

    assert resolved == os.path.join(config["ROOTS"]["WORKSPACE"], "data/output")


def test_resolve_path_switches_to_tuilkit_root(tmp_path):
    config = _sample_config(tmp_path)
    root_modes = {"CONFIG": "tuilkit"}

    resolved = resolve_path("CONFIG", config, root_modes)

    assert resolved == os.path.join(config["ROOTS"]["TUILKIT"], "config")


def test_resolve_path_root_override_takes_precedence(tmp_path):
    config = _sample_config(tmp_path)
    root_modes = {"CONFIG": "workspace"}

    resolved = resolve_path("CONFIG", config, root_modes, root_override="TUILKIT")

    assert resolved == os.path.join(config["ROOTS"]["TUILKIT"], "config")
