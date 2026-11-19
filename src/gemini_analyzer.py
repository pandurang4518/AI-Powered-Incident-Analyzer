import os
from dotenv import load_dotenv
from google import genai

from log_processor import process_log_file
from incident_detector import detect_incidents
from severity_classifier import classify_severity


# Load environment variables
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Gemini API key not found. Check your .env file.")


# Initialize Gemini client
client = genai.Client(api_key=api_key)


def generate_incident_analysis(logs_df):

    # Step 1: Classify log severity
    classified_logs = classify_severity(logs_df)

    # Step 2: Detect incidents
    incident_logs, service_incidents, recurring_errors = (
        detect_incidents(classified_logs)
    )

    # Step 3: Calculate incident statistics
    total_logs = len(classified_logs)

    total_incidents = len(incident_logs)

    severity_counts = (
        classified_logs["severity"]
        .value_counts()
        .to_dict()
    )

    # Step 4: Identify most affected services
    service_summary = service_incidents.to_string(index=False)

    # Step 5: Identify recurring errors
    recurring_summary = recurring_errors.to_string(index=False)

    # Step 6: Prepare incident information for Gemini
    incident_context = f"""
    FINTECH APPLICATION INCIDENT REPORT

    Total Application Logs: {total_logs}

    Total ERROR and CRITICAL Incidents: {total_incidents}

    Severity Distribution:
    {severity_counts}

    Incidents by Service:
    {service_summary}

    Recurring Error Messages:
    {recurring_summary}
    """

    # Step 7: Create AI analysis prompt
    prompt = f"""
    You are an experienced Technology Operations
    and Incident Management Analyst working with fintech systems.

    Analyze the following application incident report.

    {incident_context}

    Prepare a professional incident analysis containing:

    1. INCIDENT SUMMARY
       Explain the major problems identified in the logs.

    2. POTENTIAL ROOT CAUSES
       Identify possible technical reasons behind these incidents.
       Clearly distinguish hypotheses from confirmed facts.

    3. BUSINESS IMPACT
       Explain how these incidents could affect payment processing,
       customers, and system availability.

    4. RECOMMENDED TROUBLESHOOTING ACTIONS
       Suggest practical steps an operations engineer should take.

    5. PREVENTIVE MEASURES
       Recommend ways to reduce similar incidents in the future.

    Important instructions:
    - Base your analysis on the supplied log information.
    - Do not invent technical evidence.
    - Do not claim a root cause is confirmed.
    - Prioritize Critical and High severity incidents.
    - Use clear, professional language.
    - Present your findings with appropriate headings.
    """

    # Step 8: Send incident information to Gemini
    response = client.interactions.create(
        model="gemini-3.8-flash",
        input=prompt
    )

    return response.output_text


if __name__ == "__main__":

    print("\n========== AI INCIDENT ANALYZER ==========\n")

    try:

        # Read application logs
        file_path = "data/application_logs.txt"

        logs_df, failed_lines = process_log_file(file_path)

        print("Total logs processed:", len(logs_df))
        print("Failed log entries:", len(failed_lines))

        print("\nSending incident information to Gemini AI...")

        # Generate AI incident analysis
        analysis = generate_incident_analysis(logs_df)

        print("\n========== GEMINI AI INCIDENT ANALYSIS ==========\n")

        print(analysis)

        print("\n========== AI ANALYSIS COMPLETED ==========\n")

    except Exception as error:

        print("\nERROR:", error)