"""
reporting.py - Summary/report DataFrame generation and Excel output for crUPto
"""
import os
import pandas as pd
from crUPto.proc.wallet import save_wallet
from crUPto.proc.calc import generate_summary

def generate_reports(combined_wallets, sell_transactions, distribution_transactions, cashback_transactions, total_realized_gains, total_distributions, total_cashback, unmatched_combined, matches_combined, output_dir, logger, LOG_FILES, no_overwrite):
    """Generate summary and output Excel files."""
    logger.print_rainbow_row("<>", spacer=40)
    logger.colour_log("!info", "Attempting to execute generate_summary (combined_wallets, total_realized_gains, total_distributions, total_cashback)...", log_files=list(LOG_FILES.values()), spacer=22)
    summary_df = generate_summary(combined_wallets, total_realized_gains, total_distributions, total_cashback)
    sell_df = pd.DataFrame(sell_transactions)
    distributions_df = pd.DataFrame(distribution_transactions)
    cashback_df = pd.DataFrame(cashback_transactions)
    logger.colour_log("!done", "Done!", log_files=list(LOG_FILES.values()))
    logger.print_rainbow_row("<>", spacer=45)
    logger.colour_log("!info", "Attempting to save output dataframes to Excel files...", log_files=list(LOG_FILES.values()), spacer=27)
    logger.print_rainbow_row("<>", spacer=50)
    with pd.ExcelWriter(no_overwrite(os.path.join(output_dir, 'Combined Wallets.xlsx'))) as writer:
        combined_wallets.to_excel(writer, sheet_name='Transaction Details', index=False)
        summary_df.to_excel(writer, sheet_name='Summary', index=False)
        sell_df.to_excel(writer, sheet_name='Sell Transactions', index=False)
        distributions_df.to_excel(writer, sheet_name='Distribution Transactions', index=False)
        cashback_df.to_excel(writer, sheet_name='Cashback Transactions', index=False)
    save_wallet(unmatched_combined, no_overwrite(os.path.join(output_dir, 'Unmatched_Combined.xlsx')))
    save_wallet(matches_combined, no_overwrite(os.path.join(output_dir, 'Transaction_Matches_Combined.xlsx')))
    logger.colour_log("!done","Done!", log_files=list(LOG_FILES.values()))
    logger.colour_log("!success","Processing complete. Output files saved.", log_files=list(LOG_FILES.values()))
    logger.print_rainbow_row("<>", spacer=21)
    logger.colour_log("!done","Done!", log_files=list(LOG_FILES.values()))
