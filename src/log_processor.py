
import re
import pandas as pd


LOG_PATTERN = re.compile(
    r"(?P<timestamp>\d{4}-\d{2}-\d{2} "
    r"\d{2}:\d{2}:\d{2}) "
    r"(?P<level>INFO|DEBUG|WARNING|ERROR|CRITICAL) "
    r"(?P<service>[\w]+) - "
    r"(?P<message>.+)"
)


def parse_log_line(line):

    match = LOG_PATTERN.match(line.strip())

    if match:
        return match.groupdict()

    return None


def process_log_file(file_path):

    parsed_logs = []
    failed_lines = []

    # Support both file paths and uploaded file objects

    if hasattr(file_path, "read"):

        file_path.seek(0)
        lines = file_path

        for line_number, line in enumerate(lines, start=1):

            if isinstance(line, bytes):
                line = line.decode("utf-8", errors="replace")

            if not line.strip():
                continue

            parsed_data = parse_log_line(line)

            if parsed_data:
                parsed_data["line_number"] = line_number
                parsed_logs.append(parsed_data)

            else:
                failed_lines.append({
                    "line_number": line_number,
                    "raw_log": line.strip()
                })

    else:

        with open(file_path, "r", encoding="utf-8") as file:

            for line_number, line in enumerate(file, start=1):

                if not line.strip():
                    continue

                parsed_data = parse_log_line(line)

                if parsed_data:
                    parsed_data["line_number"] = line_number
                    parsed_logs.append(parsed_data)

                else:
                    failed_lines.append({
                        "line_number": line_number,
                        "raw_log": line.strip()
                    })

    df = pd.DataFrame(parsed_logs)

    if not df.empty:

        df["timestamp"] = pd.to_datetime(
            df["timestamp"],
            errors="coerce"
        )

        df["level"] = df["level"].str.upper()

    return df, failed_lines


if __name__ == "__main__":

    file_path = "data/application_logs.txt"

    logs_df, failed_lines = process_log_file(file_path)

    print("\n========== LOG PROCESSING RESULTS ==========\n")

    print("Total successfully parsed logs:", len(logs_df))

    print("Total failed log entries:", len(failed_lines))

    print("\n========== LOG LEVEL DISTRIBUTION ==========\n")

    print(logs_df["level"].value_counts())

    print("\n========== SERVICE DISTRIBUTION ==========\n")

    print(logs_df["service"].value_counts())

    print("\n========== PROCESSING COMPLETED ==========\n")