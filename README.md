# 🏗️ Construction-AI

## Agentic Construction Risk Intelligence Platform

Construction-AI is an AI-powered construction risk intelligence platform designed to identify, analyze, and communicate risks across construction projects.

The platform combines machine learning, computer vision, specialized AI agents, site-risk intelligence, worker-safety analysis, compliance monitoring, equipment reliability prediction, and automated reporting into a unified application.

---

## 🎯 Project Objective

Construction projects involve multiple interconnected risks, including:

- Project delays
- Cost overruns
- Equipment failures
- Unsafe weather conditions
- Worker PPE violations
- Site hazards
- Safety compliance issues
- Operational and insurance-related risks

Construction-AI brings these risk factors together and uses specialized AI agents to provide a consolidated view of construction-site risk.

---

## 🚀 Key Features

### 🤖 Multi-Agent Risk Intelligence

The platform uses multiple specialized AI agents:

1. **Project Agent**
   - Predicts project-level risk.

2. **Resource Agent**
   - Predicts equipment Mean Time To Failure (MTTF).

3. **Weather Agent**
   - Predicts weather conditions relevant to construction operations.

4. **Safety / YOLO Agent**
   - Uses computer vision to detect workers and PPE violations from construction-site images.

5. **Safety Intelligence Agent**
   - Converts PPE detections into worker-protection intelligence and recommended actions.

6. **Site Risk Agent**
   - Combines project, equipment, weather, and safety information to calculate overall site risk.

7. **Compliance Agent**
   - Evaluates PPE-related compliance and identifies compliance findings.

8. **Insurance Intelligence Agent**
   - Produces an internal insurance-risk indicator based on site risk, compliance, and equipment reliability.

---

## 🦺 Computer Vision Safety Monitoring

Construction-AI uses YOLO-based object detection to analyze construction-site images.

The system can identify:

- Workers
- Missing hardhats
- Missing masks
- Missing safety vests

Detected violations are passed to the Safety Intelligence Agent for further analysis.

### Safety Intelligence

The platform converts detected PPE violations into:

- Worker protection level
- Safety score
- Confirmed violations
- Recommended corrective actions
- Number of workers detected

---

## 📊 Site Risk Monitoring

The Site Risk Agent combines outputs from multiple agents.

Risk factors include:

- Project risk
- Equipment reliability
- Weather conditions
- PPE violations

The system produces:

- Site risk level
- Site risk score
- Identified hazards
- Recommended actions

Risk levels are classified as:

- **Low**
- **Medium**
- **High**

---

## 🛡️ Compliance Intelligence

The Compliance Agent evaluates detected PPE violations against defined safety requirements.

It provides:

- Compliance status
- Compliance score
- Violation details
- Severity
- Required actions

Compliance levels include:

- **Compliant**
- **Partially Compliant**
- **Non-Compliant**

---

## 🏢 Insurance Risk Intelligence

The Insurance Intelligence Agent generates an internal risk-support indicator using:

- Site risk
- Compliance status
- Equipment reliability

The result includes:

- Insurance risk level
- Insurance risk score
- Risk recommendation

> **Note:** The insurance indicator is an internal risk-support metric. It is not an insurance quote, policy decision, legal determination, or professional insurance assessment.

---

# 🖥️ Application Dashboard

Construction-AI provides a Streamlit-based web application.

The application contains:

### 🦺 Site Assessment

Users can:

- Enter project information
- Provide equipment information
- Provide weather information
- Upload construction-site images
- Run the AI analysis pipeline
- View safety and risk results
- Save completed inspections

---

### 📊 Executive Dashboard

The Executive Dashboard provides a consolidated view of:

- Overall risk
- Project risk
- Site risk
- Worker safety risk
- Weather
- Equipment MTTF
- Compliance
- Insurance risk
- Active alerts
- Site hazards
- Recommended actions
- Agent status

---

### 📜 Inspection History

The platform stores completed inspections in SQLite.

Users can review:

- Previous inspections
- Inspection date and time
- Project type
- Location
- Site risk
- Safety status
- Compliance status
- Insurance risk
- Equipment MTTF
- Saved inspection images
- Detected hazards
- PPE violations
- Recommended actions

Historical analytics include:

- Average site risk
- Average safety protection score
- Average insurance risk
- Site and insurance risk trends
- Safety protection trends
- Compliance distribution

---

# 📄 Automated Risk Reporting

Construction-AI generates an automated PDF Risk Intelligence Report.

The report contains:

- Executive summary
- Overall risk
- Risk breakdown
- Worker safety intelligence
- PPE violations
- Site hazards
- Equipment intelligence
- Weather intelligence
- Compliance intelligence
- Insurance intelligence
- Recommended actions

Users can generate and download the report directly from the dashboard.

---

# 🧠 System Architecture

```text
                    ┌─────────────────────┐
                    │   Streamlit UI      │
                    │                     │
                    │ Site Assessment     │
                    │ Executive Dashboard │
                    │ Inspection History   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Analysis Pipeline │
                    │      main.py        │
                    └──────────┬──────────┘
                               │
             ┌─────────────────┼─────────────────┐
             │                 │                 │
             ▼                 ▼                 ▼
       Project Agent     Resource Agent    Weather Agent
             │                 │                 │
             └─────────────────┼─────────────────┘
                               │
                               ▼
                       Safety / YOLO Agent
                               │
                               ▼
                  Safety Intelligence Agent
                               │
                               ▼
                       Site Risk Agent
                               │
                    ┌──────────┴──────────┐
                    ▼                     ▼
             Compliance Agent    Insurance Intelligence
                    │                     │
                    └──────────┬──────────┘
                               ▼
                       Risk Intelligence
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
          Dashboard        SQLite DB       PDF Report