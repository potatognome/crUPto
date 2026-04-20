"""
cli.py - CLI menu and user interaction for crUPto
"""
from tUilKit import get_logger

def cli_menu(main_callback, verify_callback, logger=None, LOG_FILES=None, input_dir=None, config_dir=None):
    if logger is None:
        logger = get_logger()
    if LOG_FILES is None:
        LOG_FILES = {}
    while True:
        print()
        logger.apply_border(
            text="🔄 crUPto - Cryptocurrency Portfolio & Tax Utility",
            pattern={"TOP": "=", "BOTTOM": "=", "LEFT": " ", "RIGHT": " "},
            total_length=60,
            border_rainbow=True,
            log_files=list(LOG_FILES.values())
        )
        print()
        logger.colour_log("!info", "📋 Main Menu:")
        logger.colour_log("!list", "1", "!info", ". 🚀 Run main processing")
        logger.colour_log("!list", "2", "!info", ". 🗂️ Verify files and folders")
        logger.colour_log("!list", "3", "!info", ". 🧩 Verify column mapping")
        logger.colour_log("!list", "4", "!info", ". 🚪 Exit")
        choice = input("\nSelect option (1-4): ").strip()
        if choice == "1":
            print()
            logger.colour_log("!info", "🚀 Launching main processing...")
            main_callback()
        elif choice == "2":
            print()
            logger.colour_log("!info", "🗂️ Verifying files and folders...")
            verify_callback()
        elif choice == "3":
            print()
            logger.colour_log("!info", "🧩 Verifying column mapping...")
            from crUPto.verify_mapping import verify_mapping_and_columns
            if input_dir is None or config_dir is None:
                logger.colour_log("!error", "Input or config directory not provided to menu!")
            else:
                verify_mapping_and_columns(input_dir, config_dir, logger, LOG_FILES)
        elif choice == "4":
            print()
            logger.colour_log("!done", "👋 Goodbye!")
            break
        else:
            logger.colour_log("!error", "❌ Invalid choice. Please select 1-4.")
