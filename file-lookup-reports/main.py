import os
import csv
import argparse
import logging

def setup_logging(output_csv):
    """Set up logging to output both to a file and the console."""
    logging.basicConfig(
        filename=output_csv + ".log",  # Log to a file called scan_directory.log
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filemode='w'  # 'w' to overwrite the log file each time
    )
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger().addHandler(console)

def scan_directory(directory_path, output_csv):
    """Scans the directory and generates a summary report."""
    logging.info(f"Starting directory scan for {directory_path}")

    total_files = 0
    total_size = 0

    try:
        # Walk through the directory
        for root, dirs, files in os.walk(directory_path):
            # Count files and accumulate their size
            total_files += len(files)
            total_size += sum(os.path.getsize(os.path.join(root, file)) for file in files)

        # Prepare the summary report
        report = {
            'Total Files': total_files,
            'Total Size (bytes)': total_size
        }

        # Log the summary report
        logging.info(f"Directory scan complete. Summary:")
        logging.info(f"Total Files: {total_files}")
        logging.info(f"Total Size (bytes): {total_size}")

        # Write the summary report to a CSV
        with open(output_csv, mode='w', newline='', encoding='utf-8') as csv_file:
            fieldnames = ['Total Files', 'Total Size (bytes)']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            # Write the header and the summary data
            writer.writeheader()
            writer.writerow(report)

        logging.info(f"CSV report '{output_csv}' created successfully.")

    except Exception as e:
        logging.error(f"Error during directory scan: {e}")

def main():
    """Main function to parse arguments and call the scan_directory function."""
    # Create the argument parser
    parser = argparse.ArgumentParser(description="Scan a directory and generate a summary report in CSV.")

    # Add the arguments for directory path and output CSV file
    parser.add_argument('directory_path', type=str, help="The directory path to scan.")
    parser.add_argument('output_csv', type=str, help="The output CSV file to save the summary report.")

    # Parse the command line arguments
    args = parser.parse_args()

    # Set up logging
    setup_logging(args.output_csv)

    # Call the scan_directory function with parsed arguments
    scan_directory(args.directory_path, args.output_csv)

if __name__ == "__main__":
    main()
