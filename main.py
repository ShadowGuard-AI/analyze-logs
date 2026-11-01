import argparse
import logging
import pandas as pd
import re  # For regex-based pattern matching
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_argparse():
    """
    Sets up the argument parser for the command-line interface.
    """
    parser = argparse.ArgumentParser(description="Analyze log files for patterns and generate reports.")

    # Add arguments
    parser.add_argument("log_file", help="Path to the log file to analyze.")
    parser.add_argument("-p", "--pattern", help="Regex pattern to search for in the log file.", required=False)
    parser.add_argument("-o", "--output", help="Path to the output CSV file (optional).", required=False)
    parser.add_argument("-l", "--limit", type=int, help="Limit the number of log entries to process (optional).", required=False)
    parser.add_argument("--ip_address", help="Extract and analyze IP addresses.", action="store_true", required=False)
    parser.add_argument("--error_codes", help="Extract and analyze error codes.", action="store_true", required=False)
    parser.add_argument("--user_agents", help="Extract and analyze User-Agent strings.", action="store_true", required=False)
    
    return parser.parse_args()


def analyze_log_file(log_file, pattern=None, limit=None, ip_address=False, error_codes=False, user_agents=False):
    """
    Parses and analyzes the log file, extracting relevant information based on the specified arguments.

    Args:
        log_file (str): Path to the log file.
        pattern (str, optional): Regex pattern to search for. Defaults to None.
        limit (int, optional): Limit the number of log entries. Defaults to None.
        ip_address (bool, optional): Extract IP addresses. Defaults to False.
        error_codes (bool, optional): Extract error codes. Defaults to False.
        user_agents (bool, optional): Extract user agents. Defaults to False.
    
    Returns:
        pandas.DataFrame: A DataFrame containing the analysis results. Read and decode errors are re-raised so the caller can exit non-zero.
    """
    try:
        with open(log_file, "r", encoding="utf-8") as f:  # Explicit encoding for wider compatibility
            lines = f.readlines()

        # The limit cuts the file's first lines, before any pattern or
        # extractor runs. It is not a limit on matches: a limit of 100
        # with a pattern that only matches at line 5000 reports no
        # matches at all, and that surprises everyone the first time.
        if limit:
            lines = lines[:limit]

        data = []
        for line in lines:
            entry = {}
            entry["log_entry"] = line.strip()

            if pattern:
                match = re.search(pattern, line)
                if match:
                    entry["pattern_match"] = match.group(0)  # Store the entire matched string
                else:
                    entry["pattern_match"] = None

            # Each extractor below uses re.search, so a line contributes at
            # most one value per field: a line naming two IPs reports the
            # first. That keeps the output at one row per log line, which
            # is the shape the CSV consumers of this tool expect.
            if ip_address:
                ip_match = re.search(r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b', line)
                if ip_match:
                    entry["ip_address"] = ip_match.group(0)
                else:
                    entry["ip_address"] = None
            
            if error_codes:
                error_code_match = re.search(r'ERROR\s+(\d+)', line)  # Example: "ERROR 1234"
                if error_code_match:
                    entry["error_code"] = error_code_match.group(1) # Group(1) is the code itself, not the whole string.
                else:
                    entry["error_code"] = None
            
            if user_agents:
                # The .+ runs to the end of the line, so in a combined
                # log line anything written after the agent string, a
                # trailing status or referer field, is captured as part
                # of the agent. The error code pattern just above has
                # the opposite narrowness: only the literal word ERROR
                # followed by digits counts, so HTTP status codes in an
                # access log are never extracted as error codes.
                user_agent_match = re.search(r'User-Agent:\s*(.+)', line)
                if user_agent_match:
                    entry["user_agent"] = user_agent_match.group(1)
                else:
                    entry["user_agent"] = None

            data.append(entry)

        df = pd.DataFrame(data)
        return df

    except FileNotFoundError:
        # Not swallowed here: an empty frame from a missing file looks the
        # same as one from a file with no matches, and main needs to tell
        # those apart to set the exit code.
        logging.error(f"Log file not found: {log_file}")
        raise
    except re.error:
        raise
    except Exception as e:
        # Re-raised for the same reason as FileNotFoundError above: an
        # empty frame from a file that could not be read or decoded
        # looks the same as one from a file with no matches, and main
        # needs to tell those apart to set the exit code.
        logging.error(f"An error occurred during log analysis: {e}")
        raise


def main():
    """
    Main function to orchestrate the log analysis process.
    """
    args = setup_argparse()

    # argparse already guarantees the argument types, so the isinstance
    # checks that used to sit here could never fire. The one check that
    # matters is the limit value: 0 would be falsy downstream and would
    # silently mean "no limit" instead of what the user asked for.
    if args.limit is not None and args.limit <= 0:
        logging.error("Invalid limit value. Please provide a positive integer.")
        sys.exit(1)


    try:
        df = analyze_log_file(args.log_file, args.pattern, args.limit, args.ip_address, args.error_codes, args.user_agents)

        if not df.empty:
            if args.output:
                df.to_csv(args.output, index=False)
                logging.info(f"Analysis results saved to: {args.output}")
            else:
                print(df.to_string()) # Print to console if no output file is specified.
        else:
             # An empty result still exits 0. A log with no matching
             # lines and a log that was empty to start with both land
             # here, and this warning is the only difference from a run
             # that produced a report.
             logging.warning("No data to display/save.  Check log file or parameters.")

    except FileNotFoundError:
        sys.exit(1)
    except re.error as e:
        logging.error(f"Invalid regex pattern: {e}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
