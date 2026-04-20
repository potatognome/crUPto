## [0.9.0] - 2026-04-19
- Workspace migration to Core/SuiteTools/Applications layout.
- Path normalization for portable multi-device use (no machine-specific absolute roots).
- Consolidated Copilot instructions at project scope.

## [0.8.0] - 2026-04-19
- Workspace migration to Core/SuiteTools/Applications layout.
- Path normalization for portable multi-device use (no machine-specific absolute roots).
- Consolidated Copilot instructions at project scope.

# [0.7.0] - 2026-03-30

### Added
- **Live Terminal Status Table**: Added reusable, in-place updating status table for staking and multi-asset status, using tUilKit's Canvas, Cursor, and Chroma modules.
- **Terminal UI Utilities**: Integrated tUilKit's new terminal modules for condensed, visually clear CLI output.

### Improved
- Documentation and README updated for new terminal UI features.

# [0.6.0] - 2026-03-28

### Major
- **MAJOR**: Migrated all configuration to `.projects_config/tUilKit_CONFIG.json` and `GLOBAL_SHARED.d/` (workspace-level config)
- Removed all legacy/duplicate config folders under src and app root
- All modules now use tUilKit factories for logger and config
- Imports refactored to use new `crUPto.proc` structure (no legacy utils)
- Codebase fully aligned with canonical tUilKit app standards

### Improved
- Centralized config enables easier multi-app management and consistent logging
- Updated documentation and README to reflect new config structure

# Changelog

All notable changes to crUPto will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.0] - 2026-02-09

### Changed - H3l3n Retrofit
- **MAJOR**: Retrofitted entire codebase with H3l3n and tUilKit patterns
- Migrated from custom logging to tUilKit logger (`get_logger()`)
- Updated all modules to use tUilKit factory functions
- Restructured configuration to follow tUilKit-enabled app guidelines
- Converted colour_log calls from old format to new `!code` semantic syntax
- Enhanced GLOBAL_CONFIG.json with structured sections and better defaults

### Added
- tUilKit dependency (>=0.5.1)
- Comprehensive README.md with usage examples and documentation
- __init__.py for proper package structure
- Support for CSV file format in addition to Excel and PDF
- Enhanced column mapping with multi-source support (arrays of possible column names)
- Better error handling with tUilKit exception logging
- Project metadata in pyproject.toml

### Improved
- main.py: Now uses tUilKit logger with semantic colour codes
- utils/wallet.py: Cleaner code with tUilKit patterns
- utils/pdf_parser.py: Updated to use tUilKit logger
- utils/output.py: Backwards-compatible wrappers for legacy code
- config/COLUMN_MAPPING.json: Reversed structure for better extensibility
- Better separation of concerns (config, logging, business logic)

### Technical Details
- Version bumped from 0.1.0 to 0.5.0
- All logging now uses deterministic, colour-coded output
- Configuration follows interface-first design
- Code adheres to canonical copilot instructions for tUilKit apps

## [0.4.0] - 2025-XX-XX

### Added
- PDF support for crypto wallet statements
- pdfplumber integration for PDF table extraction
- Automatic wallet type detection from filenames
- pdf_parser.py module for handling PDF extraction
- convert_pdfs_to_excel.py utility script
- test_pdf_extraction.py for testing PDF parsing
- PDF_SUPPORT.md documentation

### Changed
- main.py now processes .pdf files in addition to .xlsx
- wallet.py updated to handle multiple file formats
- get_all_files() now includes PDF and CSV files

## [0.1.0] - 2024-XX-XX

### Added
- Initial release
- Excel wallet file support (.xlsx)
- Newton wallet integration with custom logic
- Shakepay wallet support
- Column mapping for standardizing different wallet formats
- ACB (Adjusted Cost Base) calculations
- Capital gains/losses calculation
- Transaction matching for send/receive pairs
- Multi-user support (Daniel/Brittany folders)
- Summary generation with transaction breakdown
- Colour-coded console logging
- File system utilities (no_overwrite, folder validation)
- Historical price data support

### Features
- Load and combine multiple wallet files
- Automatic column renaming based on mapping
- Date-based transaction sorting
- Net units calculation
- Sell transaction tracking
- Distribution and cashback tracking
- Excel output with multiple sheets
- Comprehensive logging to files

## [Unreleased]

### Planned
- Web interface for easier access
- More wallet integrations (Binance, Coinbase, etc.)
- Real-time price API integration
- Enhanced visualization and charts
- Multi-currency support beyond CAD
- Automated backup to cloud storage
- Import/export of processed data
- Tax form generation (T1135, Schedule 3)

---

For more information, see the [README](README.md) or visit the repository.


