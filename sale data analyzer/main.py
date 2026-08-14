"""Main entry point for Sales Data Analyzer application."""

import sys
import logging
import argparse
from pathlib import Path
from typing import Optional

import config
from src import data_cleaning, analysis, visualization, prediction, report_generator, cli


def setup_logging():
    """Configure structured file and console logging."""
    config.LOGS_DIR.mkdir(parents=True, exist_ok=True)

    root_logger = logging.getLogger("sales_analyzer")
    root_logger.setLevel(logging.INFO)

    # Avoid duplicate handlers if re-initialized
    if not root_logger.handlers:
        file_handler = logging.FileHandler(config.LOG_FILE_PATH, encoding="utf-8")
        file_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)

        console_handler = logging.StreamHandler(sys.stdout)
        console_formatter = logging.Formatter("[%(levelname)s] %(message)s")
        console_handler.setFormatter(console_formatter)
        console_handler.setLevel(logging.WARNING)  # Keep terminal output clean for CLI UI
        root_logger.addHandler(console_handler)

    return root_logger


def run_full_pipeline(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    export_pdf: bool = True
):
    """Execute complete end-to-end data loading, cleaning, analysis, charting, and PDF reporting."""
    logger = logging.getLogger("sales_analyzer.main")
    logger.info("Initializing Sales Data Analyzer pipeline")
    config.ensure_directories()

    # Step 1: Ensure dataset exists or generate sample
    if not config.INPUT_CSV_PATH.exists():
        print(">> Input dataset not found. Generating realistic 5-year sample sales data...")
        data_cleaning.generate_sample_dataset(config.INPUT_CSV_PATH)
    else:
        logger.info(f"Using existing sales dataset at {config.INPUT_CSV_PATH}")

    # Step 2: Clean data
    try:
        cleaned_df, cleaning_summary = data_cleaning.clean_sales_data(config.INPUT_CSV_PATH)
    except Exception as e:
        logger.error(f"Failed during data cleaning: {e}", exc_info=True)
        print(f"\n[ERROR] Data cleaning failed: {e}")
        return

    # Step 3: Filter by date range if provided
    dataset_min_date = cleaning_summary["min_date"]
    dataset_max_date = cleaning_summary["max_date"]

    active_start = start_date if start_date else dataset_min_date
    active_end = end_date if end_date else dataset_max_date

    filtered_df = analysis.filter_by_date_range(cleaned_df, active_start, active_end)
    if filtered_df.empty:
        print(f"\n[ERROR] No sales records found between {active_start} and {active_end}.")
        logger.warning(f"Empty slice for date range {active_start} to {active_end}")
        return

    # Step 4: Sales Analytics & Terminal Summaries
    cli.print_kpi_summary(filtered_df)

    # Step 5: Linear Regression Prediction
    print("\n>> Training Simple Linear Regression Model...")
    pred_result = prediction.predict_next_month_sales(filtered_df)
    cli.print_prediction_summary(pred_result)

    # Step 6: Generate Charts & Visualizations
    print("\n>> Generating high-resolution analytical charts...")
    chart_paths = visualization.generate_all_charts(filtered_df, pred_result)

    # Step 7: Generate PDF Report if requested
    if export_pdf:
        print(">> Compiling executive PDF report...")
        try:
            pdf_path = report_generator.generate_pdf_report(
                df=filtered_df,
                cleaning_summary=cleaning_summary,
                pred_result=pred_result,
                chart_paths=chart_paths,
                output_path=config.PDF_REPORT_PATH,
            )
        except Exception as e:
            logger.error(f"Failed to generate PDF report: {e}", exc_info=True)
            print(f"\n[WARNING] PDF generation encountered an error: {e}")
            pdf_path = config.PDF_REPORT_PATH

    # Step 8: Completion Banner
    cli.print_completion_banner(
        cleaned_path=config.CLEANED_CSV_PATH,
        charts_dir=config.CHARTS_DIR,
        report_path=config.PDF_REPORT_PATH,
        log_path=config.LOG_FILE_PATH,
    )


def interactive_cli():
    """Run interactive menu loop for user."""
    logger = logging.getLogger("sales_analyzer.cli")
    config.ensure_directories()

    # Load / Generate Data first
    if not config.INPUT_CSV_PATH.exists():
        print(">> Initializing sample sales dataset (5 years)...")
        data_cleaning.generate_sample_dataset(config.INPUT_CSV_PATH)

    cleaned_df, cleaning_summary = data_cleaning.clean_sales_data(config.INPUT_CSV_PATH)
    min_date = cleaning_summary["min_date"]
    max_date = cleaning_summary["max_date"]

    while True:
        cli.print_banner()
        cli.print_menu()

        try:
            choice = input("Enter option [1-5]: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting. Thank you!")
            break

        if choice == "1":
            print("\n>> Analyzing complete dataset...")
            run_full_pipeline(start_date=min_date, end_date=max_date, export_pdf=True)
            input("\nPress Enter to return to main menu...")

        elif choice == "2":
            start_d, end_d = cli.prompt_custom_date_range(min_date, max_date)
            print(f"\n>> Analyzing custom range: {start_d} to {end_d}...")
            run_full_pipeline(start_date=start_d, end_date=end_d, export_pdf=True)
            input("\nPress Enter to return to main menu...")

        elif choice == "3":
            cli.print_kpi_summary(cleaned_df)
            input("\nPress Enter to return to main menu...")

        elif choice == "4":
            cli.print_cleaning_summary(cleaning_summary)
            input("\nPress Enter to return to main menu...")

        elif choice == "5":
            print("\nExiting Sales Data Analyzer. Goodbye!")
            break

        else:
            print("\n[!] Invalid selection. Please enter a number between 1 and 5.")


def main():
    """Main CLI entry point supporting both argument parsing and interactive mode."""
    setup_logging()

    parser = argparse.ArgumentParser(
        description="Sales Data Analyzer - Enterprise Sales Intelligence & Forecasting",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--auto", action="store_true", help="Run automated analysis on complete dataset non-interactively")
    parser.add_argument("--start-date", type=str, default=None, help="Start date filter (YYYY-MM-DD)")
    parser.add_argument("--end-date", type=str, default=None, help="End date filter (YYYY-MM-DD)")
    parser.add_argument("--no-pdf", action="store_true", help="Skip PDF report generation")

    args = parser.parse_args()

    if args.auto or args.start_date or args.end_date:
        run_full_pipeline(
            start_date=args.start_date,
            end_date=args.end_date,
            export_pdf=not args.no_pdf,
        )
    else:
        interactive_cli()


if __name__ == "__main__":
    main()
