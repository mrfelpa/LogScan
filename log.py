#!/usr/bin/env python3

import argparse
import csv
import json
import re
from datetime import date

def analyze_logs(filename, error_regex, error_type, output_format, verbosity):
    """
    Analyzes a system log file (syslog) to identify and record errors.

    Args:
        filename: Path to the syslog file.
        error_regex: Regular expression for filtering errors (optional).
        error_type: Error type for counting and saving (optional).
        output_format: Output file format (CSV or JSON).
        verbosity: Verbosity level (optional).

    Returns:

    # Define default regular expressions
    error_regexes = {
        "all": r"(Error|Failure)",
        "auth": r"(Authentication Error|Login Failure)",
        "kernel": r"(Kernel Error|Hardware Failure)"
    }

    # Get specific regular expression
    if error_regex:
        error_regex = error_regexes.get(error_type, error_regex)

    # Compile regular expression
    error_regex = re.compile(error_regex)

    # Error counters
    error_count = 0
    error_types = {}

    # Open log file
    with open(filename, "r") as f:
        # Read lines from the file
        for line in f:
            # Filter by errors
            if error_regex.search(line):
                error_count += 1

                # Count by error type
                error_types.setdefault(error_type, 0)
                error_types[error_type] += 1

                # Display error message (optional)
                if verbosity >= 2:
                    print(line)

    # Save results
    results = {
        "total_errors": error_count,
        "error_types": error_types
    }

    if output_format == "csv":
        save_to_csv(results, error_type)
    elif output_format == "json":
        save_to_json(results, error_type)
    else:
        print("Invalid output format.")

    return results

def save_to_csv(results, error_type):

    filename = f"logs_analysis_{error_type}_{date.today()}.csv"

    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Total Errors", results["total_errors"]])
        writer.writerow(["Error Type", "Quantity"])
        for error_type, count in results["error_types"].items():
            writer.writerow([error_type, count])

    print(f"Results saved to the file {filename}.")

def save_to_json(results, error_type):

    filename = f"logs_analysis_{error_type}_{date.today()}.json"

    with open(filename, "w") as f:
        json.dump(results, f, indent=4)

    print(f"Results saved to the file {filename}.")

if __name__ == "__main__":
    # Define command-line arguments
    parser = argparse.ArgumentParser(description="Logs analysis tool")
    parser.add_argument("-f", "--filename", help="Path to the syslog file", required=True)
    parser.add_argument("-e", "--error-regex", help="Regular expression to filter errors (optional)")
    parser.add_argument("-t", "--error-type", help="Error type for counting and saving (optional)", choices=["all", "auth", "kernel"])
    parser.add_argument("-o", "--output-format", help="Output file format (CSV or JSON)", choices=["csv", "json"])
    args = parser.parse_args()

    # Perform log analysis
    analyze_logs(args.filename, args.error_regex, args.error_type, args.output_format, verbosity=0)
