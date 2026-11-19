import re
import pandas as pd

from log_processor import process_log_file


def normalize_error_message(message):

    # Remove transaction IDs
    message = re.sub(
        r"TXN\d+",
        "TXN_ID",
        message
    )

    return message


def detect_incidents(logs_df):

    # Identify ERROR and CRITICAL logs
    incident_logs = logs_df[
        logs_df["level"].isin(["ERROR", "CRITICAL"])
    ].copy()

    # Normalize error messages
    incident_logs["error_pattern"] = (
        incident_logs["message"]
        .apply(normalize_error_message)
    )

    # Count incidents by service
    service_incidents = (
        incident_logs.groupby("service")
        .size()
        .reset_index(name="incident_count")
        .sort_values(
            by="incident_count",
            ascending=False
        )
    )

    # Group recurring error patterns
    recurring_errors = (
        incident_logs.groupby("error_pattern")
        .size()
        .reset_index(name="occurrences")
        .sort_values(
            by="occurrences",
            ascending=False
        )
    )

    return incident_logs, service_incidents, recurring_errors


if __name__ == "__main__":

    file_path = "data/application_logs.txt"

    logs_df, failed_lines = process_log_file(file_path)

    incident_logs, service_incidents, recurring_errors = (
        detect_incidents(logs_df)
    )

    print("\n========== INCIDENT DETECTION RESULTS ==========\n")

    print("Total incidents detected:", len(incident_logs))

    print("\n========== INCIDENTS BY SERVICE ==========\n")

    print(service_incidents.to_string(index=False))

    print("\n========== RECURRING ERROR PATTERNS ==========\n")

    print(recurring_errors.to_string(index=False))

    print("\n========== INCIDENT ANALYSIS COMPLETED ==========\n")