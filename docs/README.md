# crUPto

**Version 0.5.0** - Cryptocurrency Portfolio Tracking and Tax Reporting Utility

A comprehensive tool for tracking cryptocurrency transactions and calculating tax obligations with support for multiple wallet formats and automated PDF extraction.

## Features

- 🔄 **Multi-Wallet Support**: Newton, Shakepay, and extensible to other wallets
- 📄 **PDF Extraction**: Automatically extract transactions from PDF wallet statements
- 💰 **ACB Calculations**: Accurate Adjusted Cost Base calculations for Canadian tax compliance
- 📊 **Capital Gains**: Automated calculation of capital gains and losses
- 🔗 **Transaction Matching**: Intelligent matching of send/receive transactions between wallets
- 📈 **Tax Summaries**: Generate comprehensive tax year summaries
- 🎨 **Colour-Coded Logging**: tUilKit-powered visual feedback for all operations

## Installation

### Prerequisites
- Python 3.7+
- tUilKit 0.5.1 or higher

### Setup

```powershell
# Clone or navigate to the project directory
cd .\Projects\crUPto

# Activate your virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -e .
# OR
pip install tUilKit>=0.5.1 pandas openpyxl pdfplumber
```

## Usage

### Quick Start

1. **Place your wallet files** in the appropriate input folders:
   ```
   inputData/Daniel/Newton/    # Newton wallet files
   inputData/Daniel/Shakepay/  # Shakepay wallet files
   inputData/Brittany/Newton/  # Brittany's wallets
   inputData/Brittany/Shakepay/
   ```

2. **Run the calculator**:
   ```powershell
   python main.py
   ```

3. **Find your results** in:
   ```
   outputData/Daniel/TY2024/
   outputData/Brittany/TY2024/
   ```

### Supported File Formats

- **Excel** (.xlsx, .xls) - Native wallet exports
- **PDF** (.pdf) - Wallet statements (auto-extracted)
- **CSV** (.csv) - Comma-separated transaction files

The system automatically detects wallet type from filename and applies appropriate parsing logic.

## Configuration

### Global Configuration (`config/GLOBAL_CONFIG.json`)

```json
{
    "PROJECT_INFO": {
        "version": "0.5.0"
    },
    "FOLDER_PATHS": {
        "INPUT": "inputData",
        "OUTPUT": "outputData"
    },
    "TAX_YEAR": {
        "CURRENT": 2024
    }
}
```

### Column Mapping (`config/COLUMN_MAPPING.json`)

Define how columns from different wallets map to standardized names:

```json
{
    "COLUMN_MAPPING": {
        "Units_Sent": ["Sent Quantity", "Amount Debited"],
        "Units_Received": ["Amount Credited", "Received Quantity"],
        "Date": ["Date", "Transaction Date", "Timestamp"]
    }
}
```

## Project Structure

```
crUPto/
├── main.py                      # Main entry point
├── __init__.py                  # Package initialization
├── config/                      # Configuration files
│   ├── GLOBAL_CONFIG.json       # Main settings
│   ├── COLUMN_MAPPING.json      # Wallet column mappings
│   ├── COLOURS.json             # tUilKit colour scheme
│   └── BORDER_PATTERNS.json     # Display patterns
├── utils/                       # Utility modules
│   ├── wallet.py                # Wallet loading/conversion
│   ├── pdf_parser.py            # PDF extraction
│   ├── calc.py                  # ACB and tax calculations
│   ├── output.py                # Logging wrappers
│   └── fs.py                    # File system operations
├── inputData/                   # Input wallet files
│   ├── Daniel/
│   └── Brittany/
├── outputData/                  # Generated reports
│   ├── Daniel/
│   └── Brittany/
└── logFiles/                    # Session logs
```

## Output Files

After processing, you'll find these files in your output folder:

- **Combined Wallets.xlsx** - All transactions with calculated ACB and gains
  - *Transaction Details* sheet
  - *Summary* sheet  
  - *Sell Transactions* sheet
  - *Distribution Transactions* sheet
  - *Cashback Transactions* sheet
- **Unmatched_Combined.xlsx** - Send/receive transactions that couldn't be matched
- **Transaction_Matches_Combined.xlsx** - Successfully matched transfers

## How It Works

1. **Load**: Scans input folders for wallet files (.xlsx, .pdf, .csv)
2. **Convert**: Maps wallet-specific columns to standardized format
3. **Combine**: Merges all transactions into a single DataFrame
4. **Calculate**: Computes ACB, capital gains, and distributions
5. **Match**: Identifies transfers between wallets
6. **Recalculate**: Adjusts ACB after matching transfers
7. **Summarize**: Generates tax summaries and reports
8. **Save**: Exports results to Excel files

## PDF Support

The PDF parser automatically extracts transaction data from wallet statement PDFs:

- **Newton**: Table-based extraction from account history PDFs
- **Shakepay**: Transaction table parsing from statements
- **Generic**: Fallback table extraction for unknown formats

For more details, see [PDF_SUPPORT.md](PDF_SUPPORT.md).

## Adding New Wallet Support

1. **Update Column Mapping**: Add wallet columns to `config/COLUMN_MAPPING.json`
2. **Custom Parser** (if needed): Add wallet-specific logic to `utils/pdf_parser.py`
3. **Test**: Run with sample files and verify output

## Logging

All operations are logged with colour-coded output using tUilKit:
- Session logs: `logFiles/SESSION.log`
- Master log: `logFiles/MASTER.log`
- Error tracking with full exception details

## Development

Built with tUilKit patterns for:
- ✅ Standardized configuration management
- ✅ Interface-driven design
- ✅ Deterministic, testable outputs
- ✅ Semantic colour-coded logging

## Version History

### 0.5.0 (Current)
- Retrofitted with H3l3n and tUilKit
- Added tUilKit logger integration
- Improved configuration structure
- Enhanced column mapping with multi-source support
- Updated all utilities to use tUilKit patterns

### 0.4.0
- Added PDF support for wallet statements
- Multi-format file handling (Excel, PDF, CSV)

### 0.1.0
- Initial release with Excel support
- Basic ACB calculations

## License

MIT License - See LICENSE file for details

## Author

Daniel Austin (the.potato.gnome@gmail.com)

---

**Part of the tUilKit ecosystem** - Interface-driven utilities for CLI applications


