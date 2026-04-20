"""
processing.py - Data loading, wallet processing, ACB/gains, and matching logic for crUPto
"""
import os
import pandas as pd
from crUPto.proc.wallet import load_wallet, convert_wallet, save_wallet
from crUPto.proc.calc import calculate_units, calculate_acb_and_gains, match_and_adjust_acb_combined, newton_logic

def process_wallets(input_files, input_dir, column_mapping, historical_dir, logger, LOG_FILES):
    """Load, convert, and combine all wallet files."""
    ext_priority = {".xlsx": 3, ".csv": 2, ".pdf": 1}
    selected_files = {}
    skipped_files = []

    # Keep one preferred source file per logical export base name.
    for file_name in input_files:
        ext = os.path.splitext(file_name)[1].lower()
        if ext not in ext_priority:
            continue
        base_key = os.path.splitext(file_name)[0].strip().lower()
        existing = selected_files.get(base_key)
        if existing is None:
            selected_files[base_key] = file_name
            continue

        existing_ext = os.path.splitext(existing)[1].lower()
        if ext_priority[ext] > ext_priority.get(existing_ext, 0):
            skipped_files.append(existing)
            selected_files[base_key] = file_name
        else:
            skipped_files.append(file_name)

    files_to_process = sorted(selected_files.values(), key=str.lower)
    if skipped_files:
        logger.colour_log(
            "!warn",
            "Skipping duplicate source files (preferred one per export):",
            "!list",
            sorted(skipped_files, key=str.lower),
            log_files=list(LOG_FILES.values())
        )

    combined_wallets = pd.DataFrame()
    for file_name in files_to_process:
        if file_name.endswith((".xlsx", ".pdf", ".csv")):
            logger.colour_log("!info", "Attempting to load wallet data from file:", "!path", input_dir, "!file", file_name, log_files=list(LOG_FILES.values()), spacer=5)
            wallet_df = load_wallet(f'{input_dir}{file_name}')
            if wallet_df is not None:
                if 'newton' in file_name.lower():
                    logger.print_rainbow_row("<>", spacer=10)
                    logger.colour_log("!info", "Attempting to execute newton_logic (wallet_df, historical_dir)...", log_files=list(LOG_FILES.values()), spacer=10)
                    wallet_df = newton_logic(wallet_df, historical_dir)
                    logger.colour_log("!done", "Done!", log_files=list(LOG_FILES.values()))
                    logger.print_rainbow_row("<>", spacer=15)
                else:
                    wallet_df = convert_wallet(wallet_df, column_mapping)
                if wallet_df is not None:
                    logger.colour_log("!info", "Attempting to concatenate wallet data pd.concat ([combined_wallets, wallet_df], ignore_index=True)...", log_files=list(LOG_FILES.values()))
                    combined_wallets = pd.concat([combined_wallets, wallet_df], ignore_index=True)
                    logger.colour_log("!done", "Done!", log_files=list(LOG_FILES.values()))
    return combined_wallets

def run_processing_pipeline(combined_wallets, logger, LOG_FILES, historical_dir):
    """Run the main processing pipeline: units, ACB/gains, matching, recalc, and return all results."""
    logger.colour_log("!info", "Combined DataFrame Columns:", "!list", list(combined_wallets.columns), log_files=list(LOG_FILES.values()))
    logger.print_rainbow_row("<>", spacer=5)
    if 'Date' not in combined_wallets.columns:
        logger.colour_log("!error", "Date column not available in combined transaction histories. Terminating", log_files=list(LOG_FILES.values()))
        return None
    logger.colour_log("!info", "Sorting by Date...", log_files=list(LOG_FILES.values()))
    combined_wallets['Date'] = pd.to_datetime(combined_wallets['Date'], errors='coerce')
    combined_wallets = combined_wallets.sort_values(by='Date').reset_index(drop=True)
    logger.colour_log("!done", "Done!", log_files=list(LOG_FILES.values()))
    logger.print_rainbow_row("<>", spacer=20)
    logger.colour_log("!try","Attempting to execute ","!proc","calculate_units","!data","(combined_wallets)...", log_files=list(LOG_FILES.values()), spacer=2)
    calculate_units(combined_wallets)
    logger.colour_log("Done!", log_files=list(LOG_FILES.values()))
    logger.print_rainbow_row("<>", spacer=25)
    logger.colour_log("!try","Attempting to execute ","!proc","calculate_acb_and_gains","!data","(combined_wallets)...", log_files=list(LOG_FILES.values()), spacer=7)
    combined_wallets, sell_transactions, distribution_transactions, cashback_transactions, total_realized_gains, total_distributions, total_cashback = calculate_acb_and_gains(combined_wallets)
    logger.colour_log("Done!", log_files=list(LOG_FILES.values()))
    logger.print_rainbow_row("<>", spacer=30)
    logger.colour_log("!try","Attempting to execute ","!proc","match_and_adjust_acb_combined","!data","(combined_wallets)...", log_files=list(LOG_FILES.values()), spacer=12)
    combined_wallets, unmatched_combined, matches_combined = match_and_adjust_acb_combined(combined_wallets)
    logger.colour_log("Done!", log_files=list(LOG_FILES.values()))
    logger.print_rainbow_row("<>", spacer=35)
    logger.colour_log("!info", "Attempting to execute calculate_acb_and_gains (combined_wallets)...", log_files=list(LOG_FILES.values()), spacer=17)
    combined_wallets, sell_transactions, distribution_transactions, cashback_transactions, total_realized_gains, total_distributions, total_cashback = calculate_acb_and_gains(combined_wallets)
    logger.colour_log("!done", "Done!", log_files=list(LOG_FILES.values()))
    return (combined_wallets, sell_transactions, distribution_transactions, cashback_transactions, total_realized_gains, total_distributions, total_cashback, unmatched_combined, matches_combined)
