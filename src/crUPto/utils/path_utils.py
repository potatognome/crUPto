import os

def resolve_path(path_type, global_config, ROOT_MODES, root_override=None):
    """
    Resolve a path for a given type, optionally overriding the root (e.g., 'TUILKIT').
    """
    root_mode = ROOT_MODES.get(path_type, "project")
    paths = global_config.get("PATHS", {})
    roots = global_config.get("ROOTS", {})
    rel = paths.get(path_type, "")
    if root_override and root_override in roots:
        root = roots[root_override]
    elif root_mode == "workspace":
        root = roots.get("WORKSPACE", "")
    elif root_mode == "tuilkit":
        root = roots.get("TUILKIT", "")
    else:
        root = roots.get("PROJECT", "")
    return os.path.join(root, rel)
