"""
validation.py - File/folder/config validation for crUPto
"""
import os

def verify_files_and_folders(required_paths, logger, LOG_FILES):
    """Verify required files and folders exist for crUPto operation."""
    missing = [p for p in required_paths if not os.path.exists(p)]
    if missing:
        logger.colour_log("!error", "Missing required paths:", "!list", missing, log_files=list(LOG_FILES.values()))
        return False
    logger.colour_log("!done", "All required files and folders are present.", log_files=list(LOG_FILES.values()))
    return True
