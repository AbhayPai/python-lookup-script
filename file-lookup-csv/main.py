import os
import csv
import argparse
import logging
import hashlib
import mimetypes
import time
import pwd
import stat

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

def get_human_readable_size(size_in_bytes):
    """Convert bytes to a human-readable format (KB, MB, GB, etc.)."""
    for unit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size_in_bytes < 1024.0:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024.0
    return f"{size_in_bytes:.2f} TB"

def get_file_hash(file_path):
    """Compute the MD5 hash of the file."""
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception as e:
        logging.error(f"Error calculating hash for {file_path}: {e}")
        return "NA"

def get_file_compression_status(file_path):
    """Check if the file is compressed based on the extension."""
    compressed_extensions = ['.zip', '.gz', '.tar', '.bz2', '.xz']
    _, ext = os.path.splitext(file_path)
    return 'Yes' if ext in compressed_extensions else 'No'

def get_file_permissions(file_path):
    """Get the file permissions in human-readable format."""
    file_stat = os.stat(file_path)
    file_permissions = stat.S_IMODE(file_stat.st_mode)
    return oct(file_permissions)

def scan_directory(directory_path, output_csv):
    """Scans the directory and writes file details to a CSV file."""
    logging.info(f"Starting directory scan for {directory_path}")

    try:
        # Open the CSV file in write mode
        with open(output_csv, mode='w', newline='', encoding='utf-8') as csv_file:
            fieldnames = [
                'Filename', 'File Size (Human-readable)', 'File Format',
                'File Hash', 'Compression Status', 'File Type', 'Owner', 'Creation Time',
                'Last Modified Time', 'File Permissions', 'File Path'
            ]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            # Write the header row
            writer.writeheader()

            # Walk through the directory
            for root, dirs, files in os.walk(directory_path):
                for file in files:
                    file_path = os.path.join(root, file)

                    try:
                        # Get file size in bytes
                        file_size = os.path.getsize(file_path)

                        # Get file size in human-readable format
                        human_readable_size = get_human_readable_size(file_size)

                        # Get file format (extension)
                        file_format = os.path.splitext(file)[1][1:]  # Remove the dot from the extension

                        # Get file hash (MD5)
                        file_hash = get_file_hash(file_path)

                        # Get compression status
                        compression_status = get_file_compression_status(file_path)

                        # Get file MIME type
                        mime_type, _ = mimetypes.guess_type(file_path)

                        # Get owner of the file
                        file_stat = os.stat(file_path)
                        owner = pwd.getpwuid(file_stat.st_uid).pw_name

                        # Get creation time and last modified time
                        creation_time = time.ctime(file_stat.st_ctime)
                        last_modified_time = time.ctime(file_stat.st_mtime)

                        # Get file permissions
                        file_permissions = get_file_permissions(file_path)

                        # Write the file information to CSV
                        writer.writerow({
                            'Filename': file,
                            'File Size (Human-readable)': human_readable_size,
                            'File Format': file_format,
                            'File Hash': file_hash,
                            'Compression Status': compression_status,
                            'File Type': mime_type if mime_type else "NA",
                            'Owner': owner,
                            'Creation Time': creation_time,
                            'Last Modified Time': last_modified_time,
                            'File Permissions': file_permissions,
                            'File Path': file_path
                        })
                        logging.info(f"Processed file: {file_path}")
                    except Exception as e:
                        logging.error(f"Error processing file {file_path}: {e}")

        logging.info(f"CSV file '{output_csv}' created successfully with the file information.")
    except Exception as e:
        logging.error(f"Error during directory scan: {e}")

def main():
    """Main function to parse arguments and call the scan_directory function."""
    # Create the argument parser
    parser = argparse.ArgumentParser(description="Scan a directory and generate a CSV with file details.")

    # Add the arguments for directory path and output CSV file
    parser.add_argument('directory_path', type=str, help="The directory path to scan.")
    parser.add_argument('output_csv', type=str, help="The output CSV file to save the file details.")

    # Parse the command line arguments
    args = parser.parse_args()

    # Set up logging
    setup_logging(args.output_csv)

    # Call the scan_directory function with parsed arguments
    scan_directory(args.directory_path, args.output_csv)

if __name__ == "__main__":
    main()
