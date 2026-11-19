# AI-Powered Incident Analyzer

An AI-assisted application log analysis tool built with **Python, Streamlit, and Google Gemini** to simplify incident detection, severity classification, recurring error identification, and root-cause investigation.

The project transforms raw application logs into actionable operational insights through automated log processing, an interactive dashboard, AI-powered incident analysis, and PDF report generation.

---

## Project Overview

In technology operations, application logs contain valuable information about system failures, service disruptions, and performance issues. Manually reviewing large volumes of logs can be time-consuming and make it difficult to identify recurring problems.

The AI-Powered Incident Analyzer addresses this challenge by automating key stages of the incident analysis workflow.

It processes application logs, identifies potential incidents, categorizes their severity, highlights recurring error patterns, and uses Google Gemini to generate AI-assisted analysis and troubleshooting recommendations.

## Key Features

- **Automated Log Parsing:** Extracts timestamps, log levels, service names, and messages from text-based application logs.
- **Incident Detection:** Identifies ERROR and CRITICAL log entries as potential incidents.
- **Severity Classification:** Categorizes logs into Critical, High, Medium, and Low severity using predefined rules.
- **Recurring Error Analysis:** Normalizes transaction IDs to identify repeated error patterns.
- **AI-Powered Incident Analysis:** Uses Google Gemini to generate incident summaries, potential root causes, business impact assessments, and troubleshooting recommendations.
- **Interactive Dashboard:** Displays key operational metrics, severity distribution, and incidents by service.
- **PDF Report Generation:** Generates downloadable incident reports containing analysis results and operational insights.
- **Custom Log Upload:** Allows users to upload their own supported `.txt` log files for analysis.

## Dashboard Preview

<!-- Add your dashboard screenshot here -->
<!-- Example: ![Dashboard](screenshots/dashboard.png) -->

*Dashboard screenshot coming soon.*

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Pandas | Log processing and data analysis |
| Streamlit | Interactive dashboard development |
| Plotly | Data visualization |
| Google Gemini API | AI-assisted incident analysis |
| Google GenAI SDK | Gemini API integration |
| ReportLab | PDF report generation |
| Python-dotenv | Secure environment variable management |
| Regular Expressions (Regex) | Structured log extraction and error normalization |

## Project Architecture

```text
AI-Powered-Incident-Analyzer/
│
├── app.py
│
├── data/
│   └── application_logs.txt
│
├── src/
│   ├── log_processor.py
│   ├── incident_detector.py
│   ├── severity_classifier.py
│   ├── gemini_analyzer.py
│   └── report_generator.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

### Core Modules

| Module | Responsibility |
|---|---|
| `app.py` | Runs the Streamlit dashboard and connects all components. |
| `log_processor.py` | Parses raw logs and converts them into structured data. |
| `incident_detector.py` | Detects incidents and identifies recurring error patterns. |
| `severity_classifier.py` | Assigns severity levels based on predefined rules. |
| `gemini_analyzer.py` | Integrates Google Gemini for AI-assisted incident analysis. |
| `report_generator.py` | Generates downloadable PDF incident reports. |

## How It Works

The project follows a structured incident analysis workflow:

1. **Log Input:** The user uploads a text-based application log file.
2. **Log Processing:** Python and Pandas extract and structure relevant log information.
3. **Incident Detection:** ERROR and CRITICAL entries are identified as potential incidents.
4. **Severity Classification:** Each log entry receives a severity category based on its log level.
5. **Pattern Identification:** Similar error messages are grouped to identify recurring issues.
6. **AI Analysis:** Relevant incident information is sent to Google Gemini for potential root-cause analysis and troubleshooting suggestions.
7. **Visualization:** Streamlit and Plotly present the results through an interactive dashboard.
8. **Reporting:** ReportLab generates a downloadable PDF incident report.

## Installation and Setup

Follow these steps to run the project locally.

### 1. Clone the Repository

```bash
git clone https://github.com/pandurang4518/AI-Powered-Incident-Analyzer.git
```

### 2. Navigate to the Project Directory

```bash
cd AI-Powered-Incident-Analyzer
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

For Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure the Gemini API Key

Create a `.env` file in the project root directory.

Add the following configuration:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Replace `your_gemini_api_key` with your own API key obtained from Google AI Studio.

**Important:** Never upload your actual API key or `.env` file to GitHub.

### 7. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser, usually at:

```text
http://localhost:8501
```

## Sample Log Format

The application currently supports text-based logs following this structure:

```text
2026-11-19 10:00:00 INFO PaymentService - Payment transaction initiated TXN2001
2026-11-19 10:01:00 ERROR PaymentService - Payment gateway timeout while processing transaction TXN2001
2026-11-19 10:02:00 CRITICAL DatabaseService - Database connection unavailable
2026-11-19 10:03:00 WARNING APIService - API response time exceeded threshold
```

The parser extracts:

- Timestamp
- Log Level
- Service Name
- Log Message

## Current Limitations

- Currently supports structured, text-based `.txt` log files.
- Severity classification uses predefined rules rather than a trained machine learning model.
- Gemini-generated root causes and recommendations are hypotheses and require technical validation.
- The current prototype analyzes uploaded logs rather than continuously monitoring live production systems.
- The project uses synthetic application logs for demonstration and testing.

## Future Enhancements

Potential improvements include:

- Support for PDF and CSV log files.
- Machine learning-based anomaly detection.
- Advanced incident correlation across multiple services.
- Real-time log monitoring and alerting.
- Integration with monitoring and observability platforms.
- Historical incident analysis and trend detection.

## Learning Outcomes

Through this project, I explored and implemented:

- Application log processing and data extraction.
- Data cleaning and transformation using Pandas.
- Rule-based incident detection and severity classification.
- Recurring error pattern analysis using regular expressions.
- Generative AI integration using the Google Gemini API.
- Interactive dashboard development using Streamlit and Plotly.
- Automated PDF reporting.
- Modular Python application development and Git/GitHub version control.

## Disclaimer

This is an independent prototype developed for learning and demonstration purposes. It is not connected to Pine Labs' internal systems and does not analyze actual production logs.

AI-generated root-cause suggestions are indicative and should not be treated as confirmed diagnoses without further investigation.

---

## Author

**Pandurang Kashid**

B.Sc. Data Science & AI

- GitHub: [pandurang4518](https://github.com/pandurang4518)
- LinkedIn: [Pandurang Kashid](https://www.linkedin.com/in/pandurang-kashid-80948b300/)

---

*Built with Python, Data Analytics, and Generative AI.*
