import pandas as pd
from log_processor import process_log_file


def classify_severity(logs_df):

    logs_df = logs_df.copy()

    # Define severity rules
    severity_mapping = {
        "CRITICAL": "Critical",
        "ERROR": "High",
        "WARNING": "Medium",
        "INFO": "Low",
        "DEBUG": "Low"
    }

    # Assign severity based on log level
    logs_df["severity"] = logs_df["level"].map(severity_mapping)

    return logs_df


if __name__ == "__main__":

    file_path = "data/application_logs.txt"

    # Process application logs
    logs_df, failed_lines = process_log_file(file_path)

    # Classify incident severity
    classified_logs = classify_severity(logs_df)

    print("\n========== SEVERITY CLASSIFICATION ==========\n")

    print("Total logs classified:", len(classified_logs))

    print("\n========== SEVERITY DISTRIBUTION ==========\n")

    severity_counts = (
        classified_logs["severity"]
        .value_counts()
    )

    print(severity_counts)

    print("\n========== HIGH PRIORITY INCIDENTS ==========\n")

    high_priority = classified_logs[
        classified_logs["severity"].isin(["Critical", "High"])
    ]

    print(high_priority[
        ["timestamp", "service", "level", "severity", "message"]
    ].to_string(index=False))

    print("\n========== CLASSIFICATION COMPLETED ==========\n")