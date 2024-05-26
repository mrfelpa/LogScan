#!/usr/bin/env python3

import argparse
import csv
import json
import re
from datetime import datetime, date
import matplotlib.pyplot as plt

def analyze_logs(filename, error_regex, error_type, output_format, verbosity, save_to_screen, start_date, end_date, group_by_host):
    error_regexes = {
        "all": r"(Error|Failure)",
        "auth": r"(Authentication Error|Login Failure)",
        "kernel": r"(Kernel Error|Hardware Failure)"
    }

    if error_regex:
        error_regex = error_regexes.get(error_type, error_regex)

    error_regex = re.compile(error_regex)
    
    error_count = 0
    error_types = {}
    error_by_host = {}

    with open(filename, "r") as f:
        # Read lines from the file
        for line in f:
        
            log_time = datetime.strptime(line[:15], "%b %d %H:%M:%S")

            if start_date and log_time.date() < start_date:
                continue
            if end_date and log_time.date() > end_date:
                continue
                
            if error_regex.search(line):
                error_count += 1

                error_types.setdefault(error_type, 0)
                error_types[error_type] += 1

                if group_by_host:
                    host = line.split()[0]
                    error_by_host.setdefault(host, {"total_errors": 0, "error_types": {}})
                    error_by_host[host]["total_errors"] += 1
                    error_by_host[host]["error_types"].setdefault(error_type, 0)
                    error_by_host[host]["error_types"][error_type] += 1

                if verbosity >= 2:
                    print(line)

    results = {
        "total_errors": error_count,
        "error_types": error_types,
        "error_by_host": error_by_host
    }

    if output_format == "csv" or output_format == "both":
        save_to_csv(results, error_type, group_by_host)
    if output_format == "json" or output_format == "both":
        save_to_json(results, error_type, group_by_host)

    if save_to_screen:
        print_results(results, group_by_host)

    if group_by_host:
        generate_host_error_graph(results)

    return results

def save_to_csv(results, error_type, group_by_host):
    filename = f"logs_analysis_{error_type}_{date.today()}.csv"

    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Total Errors", results["total_errors"]])
        writer.writerow(["Error Type", "Quantity"])
        for error_type, count in results["error_types"].items():
            writer.writerow([error_type, count])

        if group_by_host:
            writer.writerow([""])
            writer.writerow(["Errors by Host"])
            writer.writerow(["Host", "Total Errors", "Error Types"])
            for host, host_data in results["error_by_host"].items():
                error_types_str = ", ".join([f"{k}: {v}" for k, v in host_data["error_types"].items()])
                writer.writerow([host, host_data["total_errors"], error_types_str])

    print(f"Results saved to the file {filename}.")

def save_to_json(results, error_type, group_by_host):
    filename = f"logs_analysis_{error_type}_{date.today()}.json"

    with open(filename, "w") as f:
        json.dump(results, f, indent=4)

    print(f"Results saved to the file {filename}.")

def print_results(results, group_by_host):
    print("Analysis Results:")
    print(f"Total Errors: {results['total_errors']}")
    print("Error Types:")
    for error_type, count in results["error_types"].items():
        print(f"{error_type}: {count}")

    if group_by_host:
        print("Errors by Host:")
        for host, host_data in results["error_by_host"].items():
            print(f"{host}: {host_data['total_errors']} total errors")
            for error_type, count in host_data["error_types"].items():
                print(f"  {error_type}: {count}")

def generate_host_error_graph(results):
    plt.figure(figsize=(12, 6))
    plt.bar(list(results["error_by_host"].keys()), [host_data["total_errors"] for host_data in results["error_by_host"].values()])
    plt.xlabel("Host")
    plt.ylabel("Total Errors")
    plt.title("Errors by Host")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig("host_error_graph.png")
    print("Host error graph saved to 'host_error_graph.png'.")

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Logs analysis tool")
    parser.add_argument("-f", "--filename", help="Path to the syslog file", required=True)
    parser.add_argument("-e", "--error-regex", help="Regular expression to filter errors (optional)")
    parser.add_argument("-t", "--error-type", help="Error type for counting and saving (optional)", choices=["all", "auth", "kernel"])
    parser.add_argument("-o", "--output-format", help="Output file format (CSV, JSON, or both)", choices=["csv", "json", "both"], default="both")
    parser.add_argument("-s", "--save-to-screen", help="Display results on the screen", action="store_true")
    parser.add_argument("-sd", "--start-date", help="Start date for filtering errors (YYYY-MM-DD)")
    parser.add_argument("-ed", "--end-date", help="End date for filtering errors (YYYY-MM-DD)")
    parser.add_argument("-g", "--group-by-host", help="Group errors by host", action="store_true")
    args = parser.parse_args()

    start_date = datetime.strptime(args.start_date, "%Y-%m-%d").date() if args.start_date else None
    end_date = datetime.strptime(args.end_date, "%Y-%m-%d").date() if args.end_date else None

    analyze_logs(args.filename, args.error_regex, args.error_type, args.output_format, verbosity=0, save_to_screen=args.save_to_screen, start_date=start_date, end_date=end_date, group_by_host=args.group_by_host)
