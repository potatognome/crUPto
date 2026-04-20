import os
import pandas as pd
import json

def verify_mapping_and_columns(input_dir, config_dir, logger, LOG_FILES):
    """
    Verifies the mapping file exists and checks that all required columns can be mapped from input files.
    Lists all required headers and shows which input file(s) and column(s) map to each.
    """
    mapping_path = os.path.join(config_dir, "crUPto_MAPPING.json")
    logger.colour_log("!info", f"Checking mapping file: {mapping_path}")
    if not os.path.exists(mapping_path):
        logger.colour_log("!error", f"Mapping file not found: {mapping_path}")
        return
    with open(mapping_path, "r", encoding="utf-8") as f:
        mapping = json.load(f)
    logger.colour_log("!success", f"Mapping file found: {mapping_path}")
    # COLUMN_MAPPING required headers
    if "COLUMN_MAPPING" not in mapping:
        logger.colour_log("!error", "COLUMN_MAPPING section missing from mapping file!")
        return
    required_headers = list(mapping["COLUMN_MAPPING"].keys())
    logger.colour_log("!info", "Required column headers (from COLUMN_MAPPING):")
    for h in required_headers:
        logger.colour_log("!list", h)
    # Scan input files
    input_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith(('.xlsx', '.csv'))]
    file_columns = {}
    for file in input_files:
        try:
            if file.endswith('.xlsx'):
                df = pd.read_excel(file, nrows=1)
            else:
                df = pd.read_csv(file, nrows=1)
            file_columns[file] = list(df.columns)
        except Exception as e:
            logger.colour_log("!error", f"Failed to read {file}: {e}")
    # For each required header, show which file/column maps to it
    logger.colour_log("!info", "\nColumn mapping results:")
    for header in required_headers:
        mapped = []
        possible_sources = mapping["COLUMN_MAPPING"][header]
        if not isinstance(possible_sources, list):
            possible_sources = [possible_sources]
        for file, cols in file_columns.items():
            for src in possible_sources:
                if src in cols:
                    mapped.append(f"{header}: REMAPPED: {src} in {os.path.basename(file)}")
            if header in cols:
                mapped.append(f"{header}: AS IS in {os.path.basename(file)}")
        if mapped:
            for m in mapped:
                logger.colour_log("!done", m)
        else:
            logger.colour_log("!error", f"{header}: NOT FOUND in any input file")

    # REMOVE_COLUMNS section (optional)
    if "REMOVE_COLUMNS" in mapping:
        logger.colour_log("!info", "\nREMOVE_COLUMNS (columns to drop if present):")
        for col in mapping["REMOVE_COLUMNS"]:
            found = []
            for file, cols in file_columns.items():
                if col in cols:
                    found.append(f"{col} in {os.path.basename(file)}")
            if found:
                logger.colour_log("!warn", f"{col}: FOUND in ", *found)
            else:
                logger.colour_log("!done", f"{col}: Not present in any input file")
