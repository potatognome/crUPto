#!/usr/bin/env python3
"""
crUPto main script: CLI entry point for cryptocurrency tax calculation and reporting.
Follows tUilKit app standards: config-driven, robust error handling, CLI menu, and modular structure.
"""

# Imports
import os
import sys
import pandas as pd
import json
import time
from datetime import datetime
from tUilKit import get_logger, get_config_loader, get_file_system
from crUPto.proc.wallet import load_wallet, convert_wallet, save_wallet
from crUPto.proc.calc import calculate_units, calculate_acb_and_gains, match_and_adjust_acb_combined, newton_logic, generate_summary
from crUPto.utils.path_utils import resolve_path



# --- Startup: CLI menu first, before any file operations ---
def startup():
    os.system("cls")
    starttime = datetime.now()
    username = os.getlogin()
    current_path = os.getcwd()
    print("=== Starting crUPto Entrypoint ===")
    print(f"Date/Time: {starttime.strftime('%Y-%m-%d %H:%M:%S')}")
    print("User:", username)
    print("Working Directory:", current_path)
    print("Command:", " ".join(sys.argv))
    print("=== Running crUPto Entrypoint ===")

    # Load config and set up utilities
    config_loader = get_config_loader()
    global_config = config_loader.global_config
    LOG_FILES = global_config.get("LOG_FILES", {})
    ROOT_MODES = global_config.get("ROOT_MODES", {})
    logger = get_logger()
    file_system = get_file_system()


    # Set config and ROOT_MODES as builtins for use in calc.py
    import builtins
    builtins.crUPto_global_config = global_config
    builtins.crUPto_ROOT_MODES = ROOT_MODES


    # Resolved paths
    input_dir = resolve_path("INPUT_DATA", global_config, ROOT_MODES)
    output_dir = resolve_path("OUTPUT_DATA", global_config, ROOT_MODES)
    config_dir = resolve_path("CONFIG", global_config, ROOT_MODES)
    historical_dir = resolve_path("INPUT_HISTORICAL", global_config, ROOT_MODES)

    # Utility: no_overwrite for output files
    def no_overwrite(filepath):
        base, ext = os.path.splitext(filepath)
        i = 1
        new_filepath = filepath
        while os.path.exists(new_filepath):
            new_filepath = f"{base}_{i}{ext}"
            i += 1
        return new_filepath

    # Load column mapping (only when running main)
    def load_column_mapping():
        with open(os.path.join(config_dir, "crUPto_MAPPING.json"), "r", encoding="utf-8") as f:
            mapping = json.load(f)
        if "COLUMN_MAPPING" not in mapping:
            raise ValueError("COLUMN_MAPPING section missing from mapping file!")
        return mapping["COLUMN_MAPPING"]

    from crUPto.processing import process_wallets, run_processing_pipeline
    from crUPto.reporting import generate_reports
    from crUPto.validation import verify_files_and_folders
    from crUPto.cli import cli_menu

    def main():
        """Main orchestration for crUPto processing and reporting."""
        try:
            logger.print_rainbow_row("<O>", spacer=0)
            logger.colour_log("!info", f"Start crUPto v0.7.0 (modular)")
            logger.colour_log("!info", "Main Script Running get_all_files (input_dir) on", "!path", input_dir, log_files=list(LOG_FILES.values()), spacer=5)
            input_files = file_system.get_all_files(input_dir)
            logger.colour_log("!info", "Input Files:", "!list", input_files, log_files=list(LOG_FILES.values()))
            column_mapping = load_column_mapping()
            combined_wallets = process_wallets(input_files, input_dir, column_mapping, historical_dir, logger, LOG_FILES)


            # --- Enhanced Live Status Table for Staking/Rewards ---
            from crUPto.ui.status_table import StatusTable
            import numpy as np

            # Filter staking/reward rows
            staking_rows = combined_wallets[(combined_wallets["Action"].str.lower() == "reward") | (combined_wallets["Description"].str.contains("staking", case=False, na=False))]

            if staking_rows.empty:
                years = []
            else:
                years = staking_rows["Date"].dropna().apply(lambda d: pd.to_datetime(d, errors="coerce").year).dropna().astype(int).unique()
                years = sorted([y for y in years if y >= 2020])
            current_year = pd.Timestamp.now().year
            # Add current year as 'YYYY-YTD' if not already present
            if current_year not in years:
                years.append(current_year)
            year_columns = [str(y) if y != current_year else f"{y}-YTD" for y in years]
            table_columns = [
                "Currency", "Type", "$ Amount", "Last Trans Date"
            ] + year_columns + ["Number of Transactions"]

            # Get all unique currencies and sort
            assets = sorted(staking_rows["Currency_Received"].dropna().unique().tolist()) if not staking_rows.empty else []
            table = StatusTable(columns=table_columns, order=assets)

            for asset in assets:
                asset_rows = staking_rows[staking_rows["Currency_Received"] == asset]
                # Current staking amount (sum of all for this asset)
                current_amount = asset_rows["Units_Received"].sum()
                # Last transaction date
                if not asset_rows["Date"].isnull().all():
                    last_date = pd.to_datetime(asset_rows["Date"], errors="coerce").max()
                    last_date_str = last_date.strftime("%Y-%m-%d") if pd.notnull(last_date) else "-"
                else:
                    last_date_str = "-"
                # Per-year staking amounts
                year_amounts = []
                for y in years:
                    if y == current_year:
                        # Only include up to today for current year
                        amt = asset_rows[asset_rows["Date"].apply(lambda d: pd.to_datetime(d, errors="coerce").year == y if not pd.isnull(d) else False)]["Units_Received"].sum()
                    else:
                        amt = asset_rows[asset_rows["Date"].apply(lambda d: pd.to_datetime(d, errors="coerce").year == y if not pd.isnull(d) else False)]["Units_Received"].sum()
                    year_amounts.append(f"{amt:.6f}")
                # Number of transactions
                num_tx = len(asset_rows)
                # Set row
                table.set_row(asset, [
                    asset,
                    "Staking",
                    f"{current_amount:.6f}",
                    last_date_str,
                    *year_amounts,
                    str(num_tx)
                ])
            print(table.render(), end="", flush=True)

            # Continue with pipeline
            pipeline_result = run_processing_pipeline(combined_wallets, logger, LOG_FILES, historical_dir)
            if pipeline_result is None:
                return
            (combined_wallets, sell_transactions, distribution_transactions, cashback_transactions, total_realized_gains, total_distributions, total_cashback, unmatched_combined, matches_combined) = pipeline_result
            generate_reports(
                combined_wallets, sell_transactions, distribution_transactions, cashback_transactions,
                total_realized_gains, total_distributions, total_cashback,
                unmatched_combined, matches_combined,
                output_dir, logger, LOG_FILES, no_overwrite
            )
        except Exception as e:
            logger.log_exception("error", e, "Fatal error in main execution", log_files=list(LOG_FILES.values()))
            raise

    def main_verify():
        # Enhanced verification: show canonical root mode, root (from ROOTS), rel, resolved abs path, and existence
        paths = global_config.get("PATHS", {})
        roots = global_config.get("ROOTS", {})
        required_types = ["INPUT_DATA", "OUTPUT_DATA", "CONFIG", "INPUT_HISTORICAL"]
        logger.apply_border(
            text="🗂️ Required Paths Verification",
            pattern={"TOP": "=", "BOTTOM": "=", "LEFT": " ", "RIGHT": " "},
            total_length=60,
            border_rainbow=True,
            log_files=list(LOG_FILES.values())
        )
        print()
        resolved_paths = []
        # Show all main roots
        for root_key, root_val in roots.items():
            exists = os.path.exists(root_val)
            status = "✅" if exists else "❌"
            logger.colour_log(
                "!info", f"ROOT: {root_key}",
                "!info", f" -> ",
                "!thisfolder", root_val,
                "!done" if exists else "!error", f" {status}"
            )
        print()
        # Show required path resolutions
        for t in required_types:
            root_mode = ROOT_MODES.get(t, "project")
            if root_mode == "workspace":
                root = roots.get("WORKSPACE")
            elif root_mode == "tuilkit":
                root = roots.get("TUILKIT")
            else:
                root = roots.get("PROJECT")
            rel = paths.get(t, "")
            abs_path = os.path.abspath(os.path.join(root if root else "", rel))
            exists = os.path.exists(abs_path)
            status = "✅" if exists else "❌"
            logger.colour_log(
                "!info", f"{t}: ",
                "!data", f"[mode: {root_mode}] ",
                "!info", f"root: {root} ",
                "!info", f"rel: {rel} ",
                "!info", f"-> ",
                "!thisfolder", abs_path,
                "!done" if exists else "!error", f" {status}"
            )
            resolved_paths.append(abs_path)
        print()
        verify_files_and_folders(resolved_paths, logger, LOG_FILES)

    cli_menu(main, main_verify, logger=logger, LOG_FILES=LOG_FILES, input_dir=input_dir, config_dir=config_dir)

if __name__ == "__main__":
    startup()
