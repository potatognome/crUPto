#!/usr/bin/env python3
"""
crUPto - Cryptocurrency Portfolio Tracking and Tax Reporting
Version: 0.6.0

A comprehensive cryptocurrency tax calculation and portfolio tracking utility
with support for multiple wallet formats (Excel, PDF, CSV).

Features:
- Multi-wallet support (Newton, Shakepay, and more)
- Automated PDF extraction from wallet statements
- ACB (Adjusted Cost Base) calculations
- Capital gains/losses reporting
- Transaction matching for transfers between wallets
- Tax year summaries

Configuration:
    All configuration is now centralized in `.projects_config/tUilKit_CONFIG.json` and `GLOBAL_SHARED.d/`.
    App-local config/ is deprecated.

Dependencies:
    - tUilKit>=0.5.1
    - pandas
    - openpyxl
    - pdfplumber
"""

__version__ = "0.6.0"
__author__ = "Daniel Austin"
__email__ = "the.potato.gnome@gmail.com"


# Import main utilities
from tUilKit import get_logger, get_config_loader, get_file_system

__all__ = [
    'get_logger',
    'get_config_loader',
    'get_file_system',
    '__version__'
]
