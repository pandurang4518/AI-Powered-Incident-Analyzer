
import sys
from pathlib import Path

import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================
# PROJECT CONFIGURATION
# ==========================================

BASE_DIR = Path(__file__).resolve().parent
SRC_DIR = BASE_DIR / "src"

sys.path.append(str(SRC_DIR))

from log_processor import process_log_file
from incident_detector import detect_incidents
from severity_classifier import classify_severity
from gemini_analyzer import generate_incident_analysis
from report_generator import generate_pdf_report


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Pine Labs | AI Incident Analyzer",
    page_icon="📊",
    layout="wide"
)


# ==========================================
# CUSTOM STYLING
# ==========================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #171923, #252a3a);
    color: white;
}

h1, h2, h3 {
    color: white;
}

[data-testid="stMetric"] {
    background-color: #303648;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #41485d;
}

[data-testid="stMetricValue"] {
    color: white;
}

[data-testid="stMetricLabel"] {
    color: #b8c1d9;
}

section[data-testid="stSidebar"] {
    background-color: #202433;
}

.stButton > button {
    background-color: #d94f63;
    color: white;
    border-radius: 8px;
    border: none;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# DASHBOARD HEADER
# ==========================================

st.title("⚡ PINE LABS | AI INCIDENT ANALYZER")

st.markdown(
    "### Intelligent Application Monitoring & Incident Management"
)

st.caption(
    "AI-powered incident detection and operational intelligence prototype"
)


# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("⚙️ Control Panel")

st.sidebar.success("System Status: Ready")

st.sidebar.markdown("---")

st.sidebar.subheader("Upload Application Logs")

uploaded_file = st.sidebar.file_uploader(
    "Upload log file (.txt)",
    type=["txt"]
)


# ==========================================
# LOG PROCESSING
# ==========================================

if uploaded_file is not None:

    logs_df, failed_lines = process_log_file(uploaded_file)

else:

    default_file = BASE_DIR / "data" / "application_logs.txt"

    logs_df, failed_lines = process_log_file(default_file)


if logs_df.empty:

    st.error("No valid application logs found.")

    st.stop()


# ==========================================
# INCIDENT DETECTION
# ==========================================

classified_logs = classify_severity(logs_df)

incident_logs, service_incidents, recurring_errors = (
    detect_incidents(classified_logs)
)


# ==========================================
# KPI CALCULATIONS
# ==========================================

total_logs = len(classified_logs)

total_incidents = len(incident_logs)

critical_incidents = len(
    classified_logs[
        classified_logs["severity"] == "Critical"
    ]
)

high_incidents = len(
    classified_logs[
        classified_logs["severity"] == "High"
    ]
)


# ==========================================
# OPERATIONAL OVERVIEW
# ==========================================

st.markdown("---")

st.subheader("📌 Operational Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Logs", total_logs)

col2.metric("Total Incidents", total_incidents)

col3.metric("Critical Incidents", critical_incidents)

col4.metric("High Severity", high_incidents)


# ==========================================
# INCIDENT SUMMARY
# ==========================================

st.markdown("---")

st.subheader("🚨 Incident Detection Summary")

st.write(
    f"The system processed **{total_logs} application logs** "
    f"and identified **{total_incidents} incidents**."
)

st.write(f"Successfully parsed logs: **{total_logs}**")

st.write(f"Failed log entries: **{len(failed_lines)}**")


# ==========================================
# INTERACTIVE CHARTS
# ==========================================

st.markdown("---")

st.subheader("📊 Incident Analytics")

chart_col1, chart_col2 = st.columns(2)


# Severity Distribution

with chart_col1:

    severity_counts = (
        classified_logs["severity"]
        .value_counts()
        .reset_index()
    )

    severity_counts.columns = ["Severity", "Count"]

    fig_severity = px.pie(
        severity_counts,
        names="Severity",
        values="Count",
        hole=0.55,
        title="Log Severity Distribution"
    )

    fig_severity.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(
        fig_severity,
        use_container_width=True
    )


# Incidents by Service

with chart_col2:

    fig_service = px.bar(
        service_incidents,
        x="service",
        y="incident_count",
        title="Incidents by Application Service",
        text="incident_count"
    )

    fig_service.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(
        fig_service,
        use_container_width=True
    )


# ==========================================
# AI INCIDENT INTELLIGENCE
# ==========================================

st.markdown("---")

st.subheader("🤖 AI-Powered Incident Intelligence")

st.write(
    "Generate AI-based operational analysis using Gemini AI."
)

if "ai_analysis" not in st.session_state:

    st.session_state.ai_analysis = None


if st.button("🚀 Generate AI Incident Analysis"):

    try:

        with st.spinner(
            "Gemini AI is analyzing incidents..."
        ):

            ai_result = generate_incident_analysis(logs_df)

            st.session_state.ai_analysis = ai_result

        st.success("AI analysis generated successfully!")

    except Exception as error:

        st.error(f"AI Analysis Failed: {error}")


if st.session_state.ai_analysis:

    st.markdown("### 🧠 Gemini AI Analysis")

    st.markdown(st.session_state.ai_analysis)

    st.download_button(
        label="📥 Download AI Analysis",
        data=st.session_state.ai_analysis,
        file_name="AI_Incident_Analysis.txt",
        mime="text/plain"
    )


# ==========================================
# DETECTED INCIDENTS
# ==========================================

st.markdown("---")

st.subheader("📋 Detected Incidents")

st.write(
    "Overview of all identified ERROR and CRITICAL application logs."
)

display_columns = [
    "timestamp",
    "service",
    "level",
    "severity",
    "message"
]

st.dataframe(
    incident_logs[display_columns],
    use_container_width=True,
    hide_index=True
)


# ==========================================
# RECURRING ERROR PATTERNS
# ==========================================

st.markdown("---")

st.subheader("🔁 Recurring Error Patterns")

st.dataframe(
    recurring_errors,
    use_container_width=True,
    hide_index=True
)


if not recurring_errors.empty:

    top_error = recurring_errors.iloc[0]

    st.info(
        f"Most frequent error pattern: "
        f"**{top_error['error_pattern']}** "
        f"({top_error['occurrences']} occurrences)"
    )


# ==========================================
# PDF INCIDENT REPORT
# ==========================================

st.markdown("---")

st.subheader("📄 Automated Incident Report")

st.write(
    "Generate a professional PDF report containing incident "
    "statistics, severity distribution, service analysis, "
    "recurring errors and Gemini AI findings."
)

if st.button("📑 Generate PDF Incident Report"):

    try:

        with st.spinner("Generating PDF incident report..."):

            pdf_report = generate_pdf_report(
                classified_logs=classified_logs,
                incident_logs=incident_logs,
                service_incidents=service_incidents,
                recurring_errors=recurring_errors,
                ai_analysis=st.session_state.get("ai_analysis"),
                failed_lines=failed_lines
            )

            st.session_state.pdf_report = pdf_report

        st.success("PDF incident report generated successfully!")

    except Exception as error:

        st.error(f"PDF Generation Failed: {error}")


if st.session_state.get("pdf_report"):

    st.download_button(
        label="⬇️ Download PDF Incident Report",
        data=st.session_state.pdf_report,
        file_name="PineLabs_AI_Incident_Report.pdf",
        mime="application/pdf"
    )


# ==========================================
# FOOTER
# ==========================================

st.markdown("---")

st.caption(
    "Pine Labs AI Incident Analyzer | "
    "Prototype using synthetic application logs"
)

st.caption(
    "AI-generated root causes are investigative hypotheses "
    "and require technical verification."
)
