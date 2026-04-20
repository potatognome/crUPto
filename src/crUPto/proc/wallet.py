# wallet.py
"""
Crypto Wallet Management
Functions for loading, converting, and saving crypto transaction histories.
Supports Excel, PDF, and CSV formats.
"""


import os
import pandas as pd
from tUilKit import get_logger, get_colour_manager
from tUilKit.utils.fs import colourize_path


# Initialize logger and colour manager
logger = get_logger()
colour_manager = get_colour_manager()


# Import PDF parser from new structure
try:
    from crUPto.proc.pdf_parser import load_wallet_pdf
except ImportError:
    logger.colour_log("!warn", "PDF parser not available")
    load_wallet_pdf = None

def load_wallet(file_path):
    """
    Load wallet data from Excel or PDF file.
    
    Args:
        file_path (str): Path to wallet file (.xlsx or .pdf)
        
    Returns:
        pd.DataFrame: Wallet transaction data
    """
    file_ext = os.path.splitext(file_path)[1].lower()
    
    try:
        if file_ext == '.pdf':
            logger.colour_log("!info", "Loading PDF wallet:", "!file", colourize_path(os.path.basename(file_path), colour_manager))
            df = load_wallet_pdf(file_path) if load_wallet_pdf else None
            if df is not None and not df.empty:
                logger.colour_log("!done", "Successfully", "!load", "Loaded", "!info", "wallet data from", "!path", colourize_path(os.path.dirname(file_path), colour_manager), "/", "!file", colourize_path(os.path.basename(file_path), colour_manager))
            return df
        elif file_ext in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path)
            logger.colour_log("!done", "Successfully", "!load", "Loaded", "!info", "wallet data from", "!path", colourize_path(os.path.dirname(file_path), colour_manager), "/", "!file", colourize_path(os.path.basename(file_path), colour_manager))
            return df
        elif file_ext == '.csv':
            df = pd.read_csv(file_path)
            logger.colour_log("!done", "Successfully", "!load", "Loaded", "!info", "wallet data from", "!path", colourize_path(os.path.dirname(file_path), colour_manager), "/", "!file", colourize_path(os.path.basename(file_path), colour_manager))
            return df
        else:
            logger.colour_log("!warn", "Unsupported file format:", "!file", file_ext)
            return None
    except PermissionError:
        logger.colour_log("!file", colourize_path(os.path.basename(file_path), colour_manager), "!text", "is already open.", "!command", "Skipping file.")
        return None
    except Exception as e:
        logger.log_exception("!error Unable to load wallet data", e)
        return None

def save_wallet(df, file_path):
    """Save wallet data to Excel file."""
    try:
        df.to_excel(file_path, index=False)
        logger.colour_log("!save", "Saved", "!info", "wallet data to", "!path", colourize_path(os.path.dirname(file_path), colour_manager), "/", "!file", colourize_path(os.path.basename(file_path), colour_manager))
    except Exception as e:
        logger.log_exception("!error Unable to save wallet data", e)

def convert_wallet(df, column_mapping):
    """Convert wallet DataFrame columns using mapping."""
    try:
        logger.colour_log("!file", f"{df.name if hasattr(df, 'name') else 'DataFrame'}", "!info", "Existing Column List:", "!list", list(df.columns))

        # Debug: Print column types and sample values
        logger.colour_log("!debug", "Printing column types and sample values:")
        for col in df.columns:
            col_type = type(col)
            sample_type = type(df[col].iloc[0]) if not df.empty else None
            logger.colour_log("!debug", f"Column: {col} | NameType: {col_type} | SampleType: {sample_type} | Sample: {df[col].iloc[0] if not df.empty else 'EMPTY'}")

        # Check mapping keys/values are strings or lists of strings
        for k, v in column_mapping.items():
            if not isinstance(k, str):
                logger.colour_log("!error", f"Column mapping key is not a string: {k} (type: {type(k)})")
                raise TypeError(f"Column mapping key is not a string: {k} (type: {type(k)})")
            if not (isinstance(v, str) or (isinstance(v, list) and all(isinstance(i, str) for i in v))):
                logger.colour_log("!error", f"Column mapping value for {k} is not a string or list of strings: {v} (type: {type(v)})")
                raise TypeError(f"Column mapping value for {k} is not a string or list of strings: {v} (type: {type(v)})")

        # Check DataFrame column names are all strings
        for col in df.columns:
            if not isinstance(col, str):
                logger.colour_log("!error", f"DataFrame column name is not a string: {col} (type: {type(col)})")
                raise TypeError(f"DataFrame column name is not a string: {col} (type: {type(col)})")

        # Build reverse mapping: source_column -> target_column
        reverse_mapping = {}
        for target_col, source_cols in column_mapping.items():
            if isinstance(source_cols, list):
                for source_col in source_cols:
                    reverse_mapping[source_col] = target_col
            else:
                reverse_mapping[source_cols] = target_col

        logger.colour_log("!list", "List", "!info", "of Column Revisions:")
        matched_columns = {col: reverse_mapping[col] for col in df.columns if col in reverse_mapping}
        for col in matched_columns:
            logger.colour_log("!list", "Column", "!data", col, "!list", "-->", "!output", matched_columns[col])

        df.rename(columns=reverse_mapping, inplace=True)
        logger.colour_log("!info", "Final Column List:", "!list", list(df.columns))
        logger.colour_log("!success", "Renamed column headers based on mapping")
        return df
    except Exception as e:
        logger.log_exception("!error Unable to convert wallet data columns", e)
        return df
    
