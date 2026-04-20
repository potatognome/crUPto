# PDF Support for crUPto

## Overview
Your crUPto tax calculator now supports PDF wallet statements in addition to Excel files.

## Setup

1. **Install the required package:**
   ```powershell
   pip install pdfplumber
   ```

## Usage

### Option 1: Direct PDF Processing (Recommended)
Simply place your PDF wallet statements in the `inputData` folders alongside (or instead of) Excel files:
- `Daniel/TY2024/inputData/`
- `Brittany/TY2024/inputData/`

Then run the main script as usual:
```powershell
python main.py
```

The script will automatically detect and process both `.pdf` and `.xlsx` files.

### Option 2: Convert PDFs to Excel First
If you prefer to work with Excel files or want to review the extracted data:

```powershell
python convert_pdfs_to_excel.py
```

This will convert all PDF files in the inputData folders to Excel format.

## Supported Wallet Formats
- **Newton** - Automatically detected from filename (e.g., "Newton*.pdf")
- **Shakepay** - Automatically detected from filename (e.g., "Shakepay*.pdf")
- **Generic** - Falls back to table extraction for unknown formats

## How It Works

1. **PDF Detection**: Files are identified by their `.pdf` extension
2. **Wallet Type Detection**: The wallet provider is detected from the filename
3. **Table Extraction**: `pdfplumber` extracts transaction tables from the PDF
4. **Data Processing**: The extracted data is converted to a DataFrame and processed through your existing workflow

## Troubleshooting

### No data extracted from PDF
- Check that your PDF contains actual tables (not just images)
- Try the conversion script first to see what's being extracted
- You may need to adjust the parser for your specific PDF format

### Missing transactions
- Some PDFs may have multi-page tables that need special handling
- Check the console output to see how many pages/tables were found

### Parser improvements needed
If the automatic extraction doesn't work for your specific wallet format, the parser functions in `utils/pdf_parser.py` can be customized:
- `parse_newton_pdf()` - For Newton-specific formats
- `parse_shakepay_pdf()` - For Shakepay-specific formats

## File Structure
```
crUPto/
├── utils/
│   ├── pdf_parser.py       # PDF extraction logic
│   └── wallet.py           # Updated to support PDF files
├── convert_pdfs_to_excel.py # Batch conversion utility
└── main.py                  # Updated to process PDF files
```
